from __future__ import annotations

import json
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def test_rag_build_and_query(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "materials").mkdir(parents=True, exist_ok=True)
    (tmp_path / "materials" / "note.md").write_text("Transformer works well.\n\nLight curves.", encoding="utf-8")

    runner = CliRunner()
    build = runner.invoke(app, ["--raw", "rag", "build", "--source", "materials/"])
    assert build.exit_code == 0, build.output

    con = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        cnt = con.execute("SELECT count(*) FROM document_chunks").fetchone()[0]
        assert cnt > 0
    finally:
        con.close()

    q = runner.invoke(app, ["--raw", "rag", "query", "--query", "transformer light curves", "--top-k", "3"])
    assert q.exit_code == 0, q.output

    payload = json.loads(q.stdout)
    assert payload["ok"] is True
    assert payload["chunks"]
    assert any("Transformer" in c["text"] for c in payload["chunks"])
