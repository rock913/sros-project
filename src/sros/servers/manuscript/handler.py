from typing import List, Dict, Any, Optional, Tuple
import re
import os
from pathlib import Path
import json
import hashlib
import difflib

import duckdb
from sros.domain.ports import ManuscriptProtocol
from sros.domain.schemas import GapAnalysisResult, OutlineNode

def resolve_workspace_path(file_path: str) -> Path:
    """
    Resolve a workspace-relative file path.
    Enforces that file_path is relative to SROS_WORKSPACE_DIR and prevents path traversal.
    """
    workspace = Path(os.environ["SROS_WORKSPACE_DIR"])
    
    rel = Path(file_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("file_path must be workspace-relative (no absolute paths or '..')")
    
    resolved_path = (workspace / rel).resolve()
    
    # Verify the resolved path is still within the workspace
    try:
        resolved_path.relative_to(workspace.resolve())
    except ValueError:
        raise ValueError(f"file_path resolves outside workspace: {resolved_path}")
    
    return resolved_path

class ManuscriptHandler(ManuscriptProtocol):
    """稿件管理器实现"""

    def get_file_sha256(self, file_path: str = "draft.md") -> str:
        """Return sha256 of the current file contents (empty file if missing)."""
        path = resolve_workspace_path(file_path)
        data = path.read_bytes() if path.exists() else b""
        return hashlib.sha256(data).hexdigest()

    def _ensure_graph_schema(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                id VARCHAR PRIMARY KEY,
                type VARCHAR,
                title VARCHAR,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS edges (
                id VARCHAR PRIMARY KEY,
                source VARCHAR,
                target VARCHAR,
                relationship VARCHAR,
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_relationship ON edges(relationship)")

    def _collect_headings(self, content_lines: List[str]) -> List[Dict[str, Any]]:
        headings: List[Dict[str, Any]] = []
        occurrence: Dict[Tuple[int, str], int] = {}
        for i, line in enumerate(content_lines, 1):
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            m = re.match(r"^(#+)\s+(.*)$", stripped)
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2).strip()
            title_norm = title.lower()
            key = (level, title_norm)
            occurrence[key] = occurrence.get(key, 0) + 1
            occ = occurrence[key]
            anchor_hash = hashlib.sha1(f"{level}:{title_norm}:{occ}".encode("utf-8")).hexdigest()[:8]
            headings.append({"line": i, "level": level, "title": title, "title_norm": title_norm, "anchor": anchor_hash})
        return headings

    def _derive_anchor(self, target: str, content_lines: List[str]) -> Tuple[str, Optional[int], Optional[str], str]:
        """Return (anchor_id, line_no_1_based_if_known, anchor_hash_if_any, match_mode)."""
        t = (target or "").strip()
        if not t or t.lower() in {"append", "end"}:
            return "append", None, None, "append"

        headings = self._collect_headings(content_lines)

        if t.lower().startswith("anchor:"):
            requested = t.split(":", 1)[1].strip()
            if requested.startswith("h:"):
                requested = requested[2:]
            matches = [h for h in headings if h["anchor"].startswith(requested)]
            if len(matches) == 1:
                h = matches[0]
                return f"heading-{h['line']}", int(h["line"]), str(h["anchor"]), "anchor"
            if len(matches) > 1:
                raise ValueError(
                    f"Anchor hash '{requested}' is ambiguous. Matches: {[(m['title'], m['anchor'], m['line']) for m in matches]}. "
                    "Please use a longer anchor prefix from get_outline_tree()."
                )
            raise ValueError(
                f"Anchor hash '{requested}' not found. Please call get_outline_tree() and use target='anchor:<hash>'."
            )

        m = re.fullmatch(r"heading-(\d+)", t)
        if m:
            line_no = int(m.group(1))
            return f"heading-{line_no}", line_no, None, "heading_line"

        m = re.fullmatch(r"line:(\d+)", t, flags=re.IGNORECASE)
        if m:
            line_no = int(m.group(1))
            return f"line-{line_no}", line_no, None, "line"

        m = re.fullmatch(r"Line\s+(\d+)", t)
        if m:
            line_no = int(m.group(1))
            return f"line-{line_no}", line_no, None, "line"

        title = t
        if t.lower().startswith("heading:"):
            title = t.split(":", 1)[1].strip()

        # Exact match
        by_title = [h for h in headings if h["title"] == title]
        if by_title:
            h = by_title[0]
            return f"heading-{h['line']}", int(h["line"]), str(h["anchor"]), "heading_exact"

        # Case-insensitive match
        title_norm = title.strip().lower()
        by_title_ci = [h for h in headings if h["title_norm"] == title_norm]
        if by_title_ci:
            h = by_title_ci[0]
            return f"heading-{h['line']}", int(h["line"]), str(h["anchor"]), "heading_case_insensitive"

        # Fuzzy match within strict cutoff
        candidates = [h["title"] for h in headings]
        if candidates:
            matches = difflib.get_close_matches(title, candidates, n=1, cutoff=0.86)
            if matches:
                best = matches[0]
                h = next(x for x in headings if x["title"] == best)
                return f"heading-{h['line']}", int(h["line"]), str(h["anchor"]), "heading_fuzzy"

        available = [h["title"] for h in headings]
        raise ValueError(
            f"Target heading '{title}' not found. Current headings: {available}. "
            "Next: call get_outline_tree() and use target='anchor:<hash>' for reliable insertion."
        )

    def _find_insertion_index(self, anchor: str, line_no: Optional[int], content_lines: List[str]) -> int:
        """Return insertion index into content_lines (0..len), inserting *after* the anchor line."""
        if anchor == "append":
            return len(content_lines)

        if line_no is None:
            return len(content_lines)

        # Clamp into valid range.
        if line_no <= 0:
            return 0
        if line_no >= len(content_lines):
            return len(content_lines)
        return line_no  # after line_no (1-based) => index line_no

    def _format_insert_block(self, content: str, citations: List[str]) -> str:
        body = (content or "").rstrip()
        block = "\n" + body + "\n"
        if citations:
            citation_text = " ".join([f"[@{c}]" for c in citations])
            block += "\n" + citation_text + "\n"
        block += "\n"
        return block

    def _persist_citation_mapping(self, *, file_path: str, anchor: str, citations: List[str]) -> None:
        if not citations:
            return

        workspace = Path(os.environ["SROS_WORKSPACE_DIR"])
        db_path = (workspace / ".sros" / "graph.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)

        section_id = f"draft_section:{file_path}#{anchor}"
        conn = duckdb.connect(str(db_path))
        try:
            self._ensure_graph_schema(conn)

            conn.execute(
                """
                INSERT OR REPLACE INTO nodes (id, type, title, content, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                [
                    section_id,
                    "draft_section",
                    anchor,
                    json.dumps({"file_path": file_path, "anchor": anchor}, ensure_ascii=False),
                ],
            )

            for citekey in citations:
                paper_id = f"paper:{citekey}"
                conn.execute(
                    """
                    INSERT OR REPLACE INTO nodes (id, type, title, content, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    [paper_id, "paper", citekey, json.dumps({"citekey": citekey}, ensure_ascii=False)],
                )

                edge_key = f"{section_id}|{paper_id}|CITES".encode("utf-8")
                edge_id = "edge_" + hashlib.sha1(edge_key).hexdigest()[:16]
                conn.execute(
                    """
                    INSERT OR REPLACE INTO edges (id, source, target, relationship, confidence, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    [edge_id, section_id, paper_id, "CITES", 0.9],
                )
        finally:
            conn.close()
    
    def find_gaps(self, file_path: str = "draft.md") -> List[GapAnalysisResult]:
        """
        基于规则识别待办项
        """
        gaps = []
        
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找 TODO 标记
            todo_pattern = r'\[TODO:\s*(.*?)\]'
            for match in re.finditer(todo_pattern, content):
                gaps.append(GapAnalysisResult(
                    section=f"Line {content[:match.start()].count(chr(10))+1}",
                    type="Task Pending",
                    confidence=0.9,
                    suggestions=[match.group(1)]
                ))
            
            # 查找短段落（可能需要扩展）
            paragraphs = content.split('\n\n')
            for i, para in enumerate(paragraphs):
                if len(para.strip()) > 0 and len(para.strip()) < 50:  # 少于50字符的段落
                    gaps.append(GapAnalysisResult(
                        section=f"Paragraph {i+1}",
                        type="Elaboration Needed",
                        confidence=0.7,
                        suggestions=["Expand this section with more details"]
                    ))
            
            # 查找缺少引用的部分
            if content.count('[@') == 0 and content.count('()]') == 0:  # 没有引用标记
                gaps.append(GapAnalysisResult(
                    section="Entire Document",
                    type="Citation Needed",
                    confidence=0.8,
                    suggestions=["Add relevant citations to support claims"]
                ))
                
        except FileNotFoundError:
            gaps.append(GapAnalysisResult(
                section="File Error",
                type="File Not Found",
                confidence=1.0,
                suggestions=[f"File {file_path} does not exist in workspace"]
            ))
        except KeyError:
            gaps.append(GapAnalysisResult(
                section="Environment Error",
                type="SROS_WORKSPACE_DIR not set",
                confidence=1.0,
                suggestions=["Please set SROS_WORKSPACE_DIR environment variable"]
            ))
        except ValueError as e:
            gaps.append(GapAnalysisResult(
                section="Path Security Error",
                type="Invalid path",
                confidence=1.0,
                suggestions=[str(e)]
            ))
        except Exception as e:
            gaps.append(GapAnalysisResult(
                section="Processing Error",
                type="Error",
                confidence=1.0,
                suggestions=[f"Error processing file: {str(e)}"]
            ))
            
        return gaps
    
    def get_outline_tree(self, file_path: str = "draft.md") -> OutlineNode:
        """
        返回 Markdown/AST 的树状结构
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 Markdown 标题来构建大纲（并为每个 heading 生成稳定 anchor hash）
            lines = content.split('\n')
            root = OutlineNode(id="root", title="Document", level=0, content="", children=[])
            stack = [(root, -1)]  # (node, level)

            occurrence: Dict[Tuple[int, str], int] = {}
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith('#'):
                    # 计算标题级别
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        elif char == ' ':
                            break
                        else:
                            break
                    
                    if level > 0:  # 有效标题
                        title = line[level:].strip()  # 移除 # 和空格
                        node_id = f"heading-{line_num}"

                        title_norm = title.strip().lower()
                        key = (level, title_norm)
                        occurrence[key] = occurrence.get(key, 0) + 1
                        occ = occurrence[key]
                        anchor_hash = hashlib.sha1(f"{level}:{title_norm}:{occ}".encode("utf-8")).hexdigest()[:8]
                        node_content = json.dumps(
                            {"anchor": anchor_hash, "line": line_num, "level": level, "title": title},
                            ensure_ascii=False,
                        )
                        
                        # 找到合适的父节点
                        while stack and stack[-1][1] >= level:
                            stack.pop()
                        
                        new_node = OutlineNode(
                            id=node_id,
                            title=title,
                            level=level,
                            content=node_content,
                            children=[]
                        )
                        
                        if stack:
                            parent, parent_level = stack[-1]
                            parent.children.append(new_node)
                        
                        stack.append((new_node, level))
            
            return root
        except KeyError:
            return OutlineNode(
                id="root",
                title="Environment Error",
                level=0,
                content="SROS_WORKSPACE_DIR not set",
                children=[]
            )
        except ValueError as e:
            return OutlineNode(
                id="root",
                title="Path Security Error",
                level=0,
                content=str(e),
                children=[]
            )
        except Exception:
            return OutlineNode(
                id="root",
                title="Document",
                level=0,
                content="Error reading document",
                children=[]
            )
    
    def insert_section(
        self,
        target: str,
        content: str,
        citations: List[str],
        file_path: str = "draft.md",
        expected_sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        带引用的增量写入（支持定位插入）

        target 语义（最小可用，确定性）：
        - "append"/"end"/""：追加到文末
        - "heading:<Title>"：插入到匹配标题行之后
        - "heading-<line_no>"：插入到指定行号（标题行）之后（与 get_outline_tree 的节点 id 对齐）
        - "line:<n>" 或 "Line <n>"：插入到第 n 行之后
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            # 读取当前文件
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    current_content = f.read()
            else:
                current_content = ""

            current_sha256 = hashlib.sha256(current_content.encode("utf-8")).hexdigest()
            if expected_sha256 and expected_sha256 != current_sha256:
                return {
                    "ok": False,
                    "error": (
                        "Version mismatch: file changed since last read. "
                        f"expected_sha256={expected_sha256} current_sha256={current_sha256}. "
                        "Next: re-read outline/file and retry with the new expected_sha256."
                    ),
                    "expected_sha256": expected_sha256,
                    "current_sha256": current_sha256,
                }
            
            content_lines = current_content.splitlines(keepends=True)
            anchor, line_no, anchor_hash, match_mode = self._derive_anchor(target, content_lines)
            insert_at = self._find_insertion_index(anchor, line_no, content_lines)
            block = self._format_insert_block(content, citations)

            if insert_at == len(content_lines):
                # Append
                new_content = current_content.rstrip("\n") + block
            else:
                # Insert after the anchor line
                prefix = "".join(content_lines[:insert_at])
                suffix = "".join(content_lines[insert_at:])
                new_content = prefix.rstrip("\n") + block + suffix.lstrip("\n")

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Persist mapping into graph.db (aligned with memory nodes/edges tables)
            self._persist_citation_mapping(file_path=file_path, anchor=anchor, citations=citations)

            new_sha256 = hashlib.sha256(new_content.encode("utf-8")).hexdigest()
            section_id = f"draft_section:{file_path}#{anchor}" if citations else None

            return {
                "ok": True,
                "match": match_mode,
                "anchor": anchor,
                "anchor_hash": anchor_hash,
                "insert_at": insert_at,
                "section_id": section_id,
                "current_sha256": new_sha256,
            }
        except ValueError as e:
            current_sha256 = hashlib.sha256(current_content.encode("utf-8")).hexdigest() if "current_content" in locals() else None
            return {"ok": False, "error": str(e), "current_sha256": current_sha256}
        except Exception as e:
            current_sha256 = hashlib.sha256(current_content.encode("utf-8")).hexdigest() if "current_content" in locals() else None
            return {"ok": False, "error": f"Unexpected error in insert_section: {e}", "current_sha256": current_sha256}
    
    def patch_draft(
        self,
        patches: List[Dict[str, Any]],
        file_path: str = "draft.md",
        expected_sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        批量更新稿件内容
        """
        try:
            # Resolve workspace-relative path
            path = resolve_workspace_path(file_path)
            
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = ""

            current_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if expected_sha256 and expected_sha256 != current_sha256:
                return {
                    "ok": False,
                    "error": (
                        "Version mismatch: file changed since last read. "
                        f"expected_sha256={expected_sha256} current_sha256={current_sha256}."
                    ),
                    "expected_sha256": expected_sha256,
                    "current_sha256": current_sha256,
                }
            
            # 应用补丁（简化实现：追加内容）
            for patch in patches:
                if patch.get('action') == 'append':
                    content += f"\n\n{patch.get('content', '')}"
                elif patch.get('action') == 'prepend':
                    content = f"{patch.get('content', '')}\n\n{content}"
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            new_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
            return {"ok": True, "patches_count": len(patches), "current_sha256": new_sha256}
        except ValueError as e:
            return {"ok": False, "error": str(e)}
        except Exception as e:
            return {"ok": False, "error": f"Unexpected error in patch_draft: {e}"}
