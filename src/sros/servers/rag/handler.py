from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import duckdb


def _workspace_root() -> Path:
    ws = os.getenv("SROS_WORKSPACE_DIR")
    if not ws:
        raise ValueError("SROS_WORKSPACE_DIR is not set. Please export SROS_WORKSPACE_DIR to your workspace root.")
    return Path(ws)


def _resolve_ws_path(p: str) -> Path:
    root = _workspace_root().resolve()
    rel = Path(p)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("path must be workspace-relative (no absolute paths or '..')")
    resolved = (root / rel).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"path resolves outside workspace: {resolved}")
    return resolved


def _db_path() -> Path:
    root = _workspace_root()
    db = root / ".sros" / "graph.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    return db


@dataclass(frozen=True)
class RagChunk:
    chunk_id: str
    source_path: str
    text: str
    score: float


class RagHandler:
    """Phase-1 MVP RAG: lexical chunking + scoring stored in DuckDB.

    This intentionally avoids heavy embedding dependencies; vss/embeddings can be
    introduced as Phase 1+ or Phase 2.
    """

    def _ensure_schema(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                chunk_id VARCHAR PRIMARY KEY,
                source_path VARCHAR,
                chunk_text TEXT,
                metadata_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_document_chunks_source_path ON document_chunks(source_path)")

    def _iter_files(self, sources: List[str]) -> Iterable[Tuple[str, Path]]:
        root = _workspace_root().resolve()
        for src in sources:
            src = (src or "").strip()
            if not src:
                continue
            p = _resolve_ws_path(src)
            if p.is_dir():
                for fp in p.rglob("*"):
                    if not fp.is_file():
                        continue
                    if fp.suffix.lower() not in {".md", ".txt", ".bib"}:
                        continue
                    rel = str(fp.resolve().relative_to(root))
                    yield rel, fp
            else:
                if p.suffix.lower() not in {".md", ".txt", ".bib"}:
                    continue
                rel = str(p.resolve().relative_to(root))
                yield rel, p

    def _chunk_text(self, text: str) -> List[str]:
        # Paragraph chunking is good enough for Phase-1.
        blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
        out: List[str] = []
        for b in blocks:
            # Prevent enormous chunks (simple split)
            if len(b) <= 1200:
                out.append(b)
            else:
                step = 900
                for i in range(0, len(b), step):
                    seg = b[i : i + step].strip()
                    if seg:
                        out.append(seg)
        return out

    def build(self, *, sources: List[str]) -> Dict[str, Any]:
        if not sources:
            return {"ok": False, "error": "Missing required arg: sources"}

        # Lazy import to avoid circular deps at import time.
        from sros.servers.ext.handler import ExtHandler

        db_path = _db_path()
        conn = duckdb.connect(str(db_path))
        try:
            self._ensure_schema(conn)

            inserted = 0
            scanned_files = 0
            for rel_path, fp in self._iter_files(sources):
                scanned_files += 1
                try:
                    raw = fp.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                # Phase-1 MVP: follow URLs embedded in notes and index the scraped text.
                # This keeps the loop offline-testable because requests.get can be monkeypatched.
                urls = sorted(set(re.findall(r"https?://[^\s\)\]\>\"\']+", raw)))
                for url in urls:
                    scraped = ExtHandler.web_scrape(url)
                    if not isinstance(scraped, dict) or not scraped.get("ok"):
                        continue
                    scraped_text = str(scraped.get("text") or "").strip()
                    if not scraped_text:
                        continue
                    source = f"url:{url}"
                    for block in self._chunk_text(scraped_text):
                        key = f"{source}\n{block}".encode("utf-8")
                        chunk_id = "chunk_" + hashlib.sha1(key).hexdigest()[:16]
                        metadata = {"source_path": source, "url": url, "title": scraped.get("title")}
                        conn.execute(
                            """
                            INSERT OR REPLACE INTO document_chunks (chunk_id, source_path, chunk_text, metadata_json, created_at)
                            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                            """,
                            [chunk_id, source, block, json.dumps(metadata, ensure_ascii=False)],
                        )
                        inserted += 1

                for block in self._chunk_text(raw):
                    key = f"{rel_path}\n{block}".encode("utf-8")
                    chunk_id = "chunk_" + hashlib.sha1(key).hexdigest()[:16]
                    metadata = {"source_path": rel_path}
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO document_chunks (chunk_id, source_path, chunk_text, metadata_json, created_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """,
                        [chunk_id, rel_path, block, json.dumps(metadata, ensure_ascii=False)],
                    )
                    inserted += 1

            count = conn.execute("SELECT count(*) FROM document_chunks").fetchone()[0]
            return {
                "ok": True,
                "db_path": str(db_path),
                "scanned_files": scanned_files,
                "inserted": inserted,
                "chunk_count": int(count),
            }
        finally:
            conn.close()

    def query(self, *, query: str, top_k: int = 5) -> Dict[str, Any]:
        q = (query or "").strip()
        if not q:
            return {"ok": False, "error": "Missing required arg: query"}

        top_k = int(top_k) if top_k is not None else 5
        if top_k <= 0:
            top_k = 5

        db_path = _db_path()
        conn = duckdb.connect(str(db_path))
        try:
            self._ensure_schema(conn)
            rows = conn.execute("SELECT chunk_id, source_path, chunk_text FROM document_chunks").fetchall()
        finally:
            conn.close()

        tokens = [t for t in re.findall(r"[a-zA-Z0-9_]+", q.lower()) if len(t) >= 2]
        token_set = set(tokens)

        scored: List[RagChunk] = []
        for chunk_id, source_path, chunk_text in rows:
            text = str(chunk_text or "")
            hay = text.lower()
            score = float(sum(1 for t in token_set if t in hay))
            if score <= 0:
                continue
            scored.append(
                RagChunk(
                    chunk_id=str(chunk_id),
                    source_path=str(source_path),
                    text=text,
                    score=score,
                )
            )

        scored.sort(key=lambda c: c.score, reverse=True)
        out = scored[:top_k]
        return {
            "ok": True,
            "query": q,
            "top_k": top_k,
            "chunks": [
                {"chunk_id": c.chunk_id, "source_path": c.source_path, "text": c.text, "score": c.score}
                for c in out
            ],
        }
