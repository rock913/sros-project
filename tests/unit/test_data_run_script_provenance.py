from __future__ import annotations

import os
from pathlib import Path

import duckdb

from sros.servers.data.handler import DataHandler


def test_data_run_script_passes_dataset_args_and_writes_provenance(tmp_path: Path, monkeypatch):
    ws = tmp_path / "ws"
    (ws / ".sros").mkdir(parents=True)
    (ws / "figures").mkdir(parents=True)
    (ws / "scripts").mkdir(parents=True)
    (ws / "data" / "raw").mkdir(parents=True)

    dataset = ws / "data" / "raw" / "d.csv"
    dataset.write_text("a,b\n1,2\n", encoding="utf-8")

    # Script expects argv[1] dataset path and writes a new figure file.
    script = ws / "scripts" / "make_fig.py"
    script.write_text(
        """
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print('Usage: make_fig.py <dataset>')
    raise SystemExit(1)

# Prove dataset arg was passed
Path('figures').mkdir(exist_ok=True)
(Path('figures') / 'dummy.png').write_bytes(b'not-a-real-png')
print('dataset_arg:', sys.argv[1])
""".lstrip(),
        encoding="utf-8",
    )

    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(ws))

    res = DataHandler().run_script("scripts/make_fig.py", dataset_paths=["data/raw/d.csv"])
    assert res.get("ok") is True, res
    assert any("dummy.png" in p for p in res.get("generated_figures", []))

    con = duckdb.connect(str(ws / ".sros" / "graph.db"))
    relationships = {r[0] for r in con.execute("SELECT DISTINCT relationship FROM edges").fetchall()}
    assert "ANALYZES" in relationships
    assert "GENERATES" in relationships


def test_data_run_script_counts_overwritten_figure_as_generated(tmp_path: Path, monkeypatch):
    ws = tmp_path / "ws"
    (ws / ".sros").mkdir(parents=True)
    (ws / "figures").mkdir(parents=True)
    (ws / "scripts").mkdir(parents=True)
    (ws / "data" / "raw").mkdir(parents=True)

    dataset = ws / "data" / "raw" / "d.csv"
    dataset.write_text("a,b\n1,2\n", encoding="utf-8")

    # Pre-existing figure file (will be overwritten)
    fig = ws / "figures" / "dummy.png"
    fig.write_bytes(b"old")

    script = ws / "scripts" / "overwrite_fig.py"
    script.write_text(
        """
import sys
from pathlib import Path

Path('figures').mkdir(exist_ok=True)
(Path('figures') / 'dummy.png').write_bytes(b'new')
print('ok')
""".lstrip(),
        encoding="utf-8",
    )

    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(ws))

    res = DataHandler().run_script("scripts/overwrite_fig.py", dataset_paths=["data/raw/d.csv"])
    assert res.get("ok") is True, res

    con = duckdb.connect(str(ws / ".sros" / "graph.db"))
    relationships = {r[0] for r in con.execute("SELECT DISTINCT relationship FROM edges").fetchall()}
    assert "GENERATES" in relationships
