from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import duckdb
import pytest
from typer.testing import CliRunner

from sros.skills.cli import app


@pytest.mark.integration
def test_v4_phase1_lit_pack_mvp(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    monkeypatch.setenv("SROS_SCHOLAR_BACKEND", "mock")

    # Workspace assets
    (tmp_path / "materials" / "raw_notes").mkdir(parents=True, exist_ok=True)
    (tmp_path / "references").mkdir(parents=True, exist_ok=True)

    (tmp_path / "materials" / "raw_notes" / "idea_brainstorm.md").write_text(
        "# Idea\n\nSee https://example.com/mock-astro-blog-post\n\n[TODO] Research.\n",
        encoding="utf-8",
    )

    (tmp_path / "draft.md").write_text(
        "# My Paper\n\n## Related Work\n\nPlaceholder.\n",
        encoding="utf-8",
    )

    # Fake web scrape
    import requests

    def _fake_get(url: str, timeout: float = 15.0, headers=None):
        assert "example.com" in url
        return SimpleNamespace(
            status_code=200,
            text="<html><head><title>Blog</title></head><body>PINN and Transformers in astronomy.</body></html>",
            headers={"content-type": "text/html"},
        )

    monkeypatch.setattr(requests, "get", _fake_get)

    runner = CliRunner()

    # 1) ext web-scrape
    r = runner.invoke(app, ["--raw", "ext", "web-scrape", "--url", "https://example.com/mock-astro-blog-post"])
    assert r.exit_code == 0, r.output
    scrape = json.loads(r.stdout)
    assert scrape["ok"] is True
    assert "PINN" in scrape["text"]

    # 2) scholar search
    r = runner.invoke(app, ["--raw", "scholar", "search", "--query", "Transformer astronomy light curve", "--max-results", "3"])
    assert r.exit_code == 0, r.output
    items = json.loads(r.stdout)
    assert items
    citekeys = [it["citekey"] for it in items[:2]]

    # 3) zotero-sync
    args = ["--raw", "scholar", "zotero-sync"]
    for ck in citekeys:
        args += ["--citekeys", ck]
    r = runner.invoke(app, args)
    assert r.exit_code == 0, r.output
    payload = json.loads(r.stdout)
    assert payload["ok"] is True

    bib = tmp_path / "references" / "zotero_library.bib"
    assert bib.exists()

    # 4) rag build/query
    r = runner.invoke(app, ["--raw", "rag", "build", "--source", "materials/", "--source", "references/"])
    assert r.exit_code == 0, r.output

    r = runner.invoke(app, ["--raw", "rag", "query", "--query", "Transformer PINN astronomy", "--top-k", "5"])
    assert r.exit_code == 0, r.output
    q = json.loads(r.stdout)
    assert q["ok"] is True
    assert q["chunks"]

    # 5) manuscript refactor
    content = "## Related Work\n\nSynthesized: [@%s]." % citekeys[0]
    args = [
        "--raw",
        "manuscript",
        "refactor",
        "--target",
        "heading:Related Work",
        "--content",
        content,
        "--file",
        "draft.md",
    ]
    for ck in citekeys:
        args += ["--cite", ck]

    r = runner.invoke(app, args)
    assert r.exit_code == 0, r.output
    ref = json.loads(r.stdout)
    assert ref["ok"] is True

    updated = (tmp_path / "draft.md").read_text(encoding="utf-8")
    assert "Synthesized" in updated

    # Verify DuckDB artifacts
    con = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        chunk_count = con.execute("SELECT count(*) FROM document_chunks").fetchone()[0]
        assert chunk_count > 0

        cite_edges = con.execute("SELECT count(*) FROM edges WHERE relationship='CITES'").fetchone()[0]
        assert cite_edges > 0
    finally:
        con.close()
