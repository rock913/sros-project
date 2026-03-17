from __future__ import annotations

import json
import os
from pathlib import Path

import duckdb
from typer.testing import CliRunner

from sros.skills.cli import app


def test_slice2_data_loop_end_to_end(tmp_path: Path, monkeypatch):
    # Arrange: workspace
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    (tmp_path / ".sros").mkdir(parents=True, exist_ok=True)
    duckdb.connect(str(tmp_path / ".sros" / "graph.db")).close()

    (tmp_path / "data" / "raw").mkdir(parents=True, exist_ok=True)
    (tmp_path / "figures").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)

    csv_path = tmp_path / "data" / "raw" / "sample.csv"
    csv_path.write_text("name,score\nAlice,1\nBob,2\n", encoding="utf-8")

    # Script writes a new file into figures/
    script_path = tmp_path / "scripts" / "plot.py"
    script_path.write_text(
        """
with open('figures/out.png', 'w', encoding='utf-8') as f:
    f.write('fake image')
print('ok')
""".lstrip(),
        encoding="utf-8",
    )

    runner = CliRunner()

    # Act 1: preview data
    preview = runner.invoke(app, ["--raw", "data", "preview", "--file", str(csv_path)])
    assert preview.exit_code == 0, preview.output
    preview_json = json.loads(preview.output)
    assert preview_json["ok"] is True
    assert preview_json["summary"]["rows"] == 2

    # Act 2: run script
    run = runner.invoke(
        app,
        [
            "--raw",
            "data",
            "run-script",
            "--script",
            str(script_path),
            "--dataset",
            str(csv_path),
        ],
    )
    assert run.exit_code == 0, run.output
    run_json = json.loads(run.output)
    assert run_json["ok"] is True
    assert any(p.endswith("out.png") for p in run_json["generated_figures"])

    # Assert: figure file exists
    assert (tmp_path / "figures" / "out.png").exists()

    # Assert: graph contains Script/Figure + GENERATES edge
    conn = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        nodes = conn.execute("SELECT id, type FROM nodes").fetchall()
        edges = conn.execute("SELECT source, target, relationship FROM edges").fetchall()
    finally:
        conn.close()

    assert any(t == "Script" for _, t in nodes)
    assert any(t == "Figure" for _, t in nodes)
    assert any(t == "Dataset" for _, t in nodes)
    assert any(rel == "GENERATES" for _, _, rel in edges)
    assert any(rel == "ANALYZES" for _, _, rel in edges)
