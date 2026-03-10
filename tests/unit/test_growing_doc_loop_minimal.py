from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from sros.servers.manuscript.handler import ManuscriptHandler
from sros.servers.memory.handler import MemoryHandler


def test_growing_doc_loop_minimal_persists_citation_map(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Isolated workspace
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text(
        "# Paper Title\n\n## Introduction\n\nExisting paragraph.\n\n[TODO: Add evidence]\n",
        encoding="utf-8",
    )

    manuscript = ManuscriptHandler()

    gaps = manuscript.find_gaps("draft.md")
    assert any(g.type == "Task Pending" for g in gaps)

    ok = manuscript.insert_section(
        target="heading:Introduction",
        content="New evidence-backed sentence.",
        citations=["smith2020"],
        file_path="draft.md",
    )
    assert isinstance(ok, dict)
    assert ok["ok"] is True

    updated = draft.read_text(encoding="utf-8")
    intro_idx = updated.find("## Introduction")
    assert intro_idx != -1
    # Inserted content should appear after the heading and before the existing paragraph.
    assert updated.find("New evidence-backed sentence.") > intro_idx
    assert updated.find("New evidence-backed sentence.") < updated.find("Existing paragraph.")

    # Section id rule: heading line number is deterministic for this file.
    section_id = "draft_section:draft.md#heading-3"

    db_path = tmp_path / ".sros" / "graph.db"
    assert db_path.exists()

    conn = duckdb.connect(str(db_path))
    try:
        edges = conn.execute(
            "SELECT source, target, relationship FROM edges WHERE source = ? ORDER BY target",
            [section_id],
        ).fetchall()
    finally:
        conn.close()

    assert (section_id, "paper:smith2020", "CITES") in edges

    memory = MemoryHandler()
    citation_map = memory.get_citation_map(section_id)
    assert any(e.relationship == "CITES" and e.target == "paper:smith2020" for e in citation_map)
