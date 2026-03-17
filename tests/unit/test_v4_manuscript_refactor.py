from __future__ import annotations

import json
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def test_manuscript_refactor_validates_citations_and_writes_edges(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    # Seed citations via zotero-sync
    runner = CliRunner()
    seed = runner.invoke(app, ["--raw", "scholar", "zotero-sync", "--citekeys", "smith2024transformer"])
    assert seed.exit_code == 0, seed.output

    (tmp_path / "draft.md").write_text("# My Paper\n\n## Related Work\n\nOld\n", encoding="utf-8")

    res = runner.invoke(
        app,
        [
            "--raw",
            "manuscript",
            "refactor",
            "--target",
            "heading:Related Work",
            "--content",
            "New section with cite [@smith2024transformer].",
            "--cite",
            "smith2024transformer",
            "--file",
            "draft.md",
        ],
    )
    assert res.exit_code == 0, res.output

    payload = json.loads(res.stdout)
    assert payload["ok"] is True

    updated = (tmp_path / "draft.md").read_text(encoding="utf-8")
    assert "New section" in updated

    con = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        cites = con.execute("SELECT source, target FROM edges WHERE relationship='CITES'").fetchall()
        assert cites
    finally:
        con.close()


def test_manuscript_refactor_rejects_missing_citation(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "draft.md").write_text("# My Paper\n\n## Related Work\n\nOld\n", encoding="utf-8")

    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "--raw",
            "manuscript",
            "refactor",
            "--target",
            "heading:Related Work",
            "--content",
            "Cite [@missing2020].",
            "--cite",
            "missing2020",
            "--file",
            "draft.md",
        ],
    )
    assert res.exit_code != 0
    payload = json.loads(res.stdout)
    assert payload["ok"] is False
    assert "missing" in payload["error"].lower()
