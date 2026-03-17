from __future__ import annotations

import json
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def test_manuscript_index_figures_writes_referenced_in_edges(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text(
        """
# Intro

Some text.

![plot](figures/out.png)

## Methods

![plot2](figures/out.png "same")
![other](figures/other.png)
![ignore](images/not_indexed.png)
""".lstrip(),
        encoding="utf-8",
    )

    runner = CliRunner()
    res = runner.invoke(app, ["--raw", "manuscript", "index-figures", "--file", "draft.md"])
    assert res.exit_code == 0, res.output

    payload = json.loads(res.output)
    assert payload["ok"] is True
    assert payload["counts"]["references"] == 3
    assert payload["counts"]["sections"] >= 2
    assert payload["counts"]["edges"] >= 2

    conn = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        nodes = conn.execute("SELECT id, type FROM nodes").fetchall()
        edges = conn.execute(
            "SELECT source, target, relationship FROM edges WHERE relationship='REFERENCED_IN'"
        ).fetchall()
    finally:
        conn.close()

    assert any(t == "draft_section" for _, t in nodes)
    assert any(i == "figure_out.png" for i, _ in nodes)
    assert any(i == "figure_other.png" for i, _ in nodes)
    assert len(edges) >= 2
    assert all(rel == "REFERENCED_IN" for _, _, rel in edges)
