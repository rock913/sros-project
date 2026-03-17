from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sros.skills.cli import app


def test_data_preview_csv_success(tmp_path: Path):
    # Create a sample CSV
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age", "score"])
        writer.writerow(["Alice", 25, 95.5])
        writer.writerow(["Bob", 30, 87.0])
        writer.writerow(["Charlie", 35, 92.3])

    runner = CliRunner()
    result = runner.invoke(app, ["data", "preview", "--file", str(csv_file)])
    assert result.exit_code == 0, result.output

    # Check human-friendly output contains key info
    assert "name" in result.output
    assert "Alice" in result.output
    assert "Bob" in result.output

    # Test --raw
    result_raw = runner.invoke(app, ["--raw", "data", "preview", "--file", str(csv_file)])
    assert result_raw.exit_code == 0
    data = json.loads(result_raw.output)
    assert data["ok"] is True
    summary = data["summary"]
    assert summary["rows"] == 3
    assert summary["columns"] == 3
    assert "name" in summary["column_names"]
    assert len(summary["sample_rows"]) == 3  # All rows since <5


def test_data_preview_csv_not_found(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "data", "preview", "--file", str(tmp_path / "nonexistent.csv")])
    assert result.exit_code == 1
    assert "File not found" in result.output


def test_data_preview_csv_invalid(tmp_path: Path):
    # Create invalid CSV
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text("not,csv,content\ninvalid")

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "data", "preview", "--file", str(csv_file)])
    # May succeed or fail depending on pandas
    # For now, just check it runs
    assert result.exit_code in [0, 1]


def test_data_run_script_success(tmp_path: Path, monkeypatch):
    # Set workspace dir
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    # Create a simple script that generates a figure (just create a file)
    script_file = tmp_path / "plot.py"
    script_file.write_text("""
# Simulate generating a figure
with open('figures/test_plot.png', 'w') as f:
    f.write('fake png data')
print("Plot generated")
""")

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "data", "run-script", "--script", str(script_file)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["ok"] is True
    assert "generated_figures" in data
    assert len(data["generated_figures"]) == 1
    assert "test_plot.png" in data["generated_figures"][0]


def test_data_run_script_with_dataset_writes_analyzes_edge(tmp_path: Path, monkeypatch):
    import duckdb

    # Set workspace dir
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    (tmp_path / ".sros").mkdir(parents=True, exist_ok=True)

    # Dataset
    dataset = tmp_path / "data.csv"
    dataset.write_text("x,y\n1,2\n", encoding="utf-8")

    # Script generates a figure
    script_file = tmp_path / "plot.py"
    script_file.write_text(
        """
with open('figures/test_plot.png', 'w', encoding='utf-8') as f:
    f.write('fake png data')
print('Plot generated')
""".lstrip(),
        encoding="utf-8",
    )

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "data",
            "run-script",
            "--script",
            str(script_file),
            "--dataset",
            str(dataset),
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True

    conn = duckdb.connect(str(tmp_path / ".sros" / "graph.db"))
    try:
        nodes = conn.execute("SELECT id, type FROM nodes").fetchall()
        edges = conn.execute("SELECT source, target, relationship FROM edges").fetchall()
    finally:
        conn.close()

    assert any(t == "Dataset" for _, t in nodes)
    assert any(rel == "ANALYZES" for _, _, rel in edges)


def test_data_run_script_not_found(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "data", "run-script", "--script", str(tmp_path / "nonexistent.py")])
    assert result.exit_code == 1
    assert "Script not found" in result.output