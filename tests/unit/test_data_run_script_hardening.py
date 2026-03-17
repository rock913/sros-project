from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from sros.servers.data.handler import DataHandler


class _Completed:
    def __init__(self, returncode: int = 0, stdout: str = "ok", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_run_script_injects_mplbackend_agg(tmp_path: Path, monkeypatch):
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "figures").mkdir()
    (ws / "scripts").mkdir()

    script = ws / "scripts" / "plot.py"
    script.write_text("print('hi')\n", encoding="utf-8")

    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(ws))

    seen = {}

    def _fake_run(argv, cwd, capture_output, text, env, timeout):
        seen["env"] = env
        seen["argv"] = argv
        assert cwd == ws
        return _Completed(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", _fake_run)

    res = DataHandler().run_script("scripts/plot.py", dataset_paths=[])
    assert res["ok"] is True
    assert seen["env"]["MPLBACKEND"] == "Agg"


def test_run_script_respects_user_mplbackend_override(tmp_path: Path, monkeypatch):
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "figures").mkdir()
    (ws / "scripts").mkdir()

    (ws / "scripts" / "plot.py").write_text("print('hi')\n", encoding="utf-8")

    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(ws))
    monkeypatch.setenv("MPLBACKEND", "TkAgg")

    def _fake_run(argv, cwd, capture_output, text, env, timeout):
        assert env["MPLBACKEND"] == "TkAgg"
        return _Completed(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", _fake_run)

    res = DataHandler().run_script("scripts/plot.py", dataset_paths=[])
    assert res["ok"] is True


def test_run_script_detects_modified_figure(tmp_path: Path, monkeypatch):
    ws = tmp_path / "ws"
    ws.mkdir()
    (ws / "figures").mkdir()
    (ws / "scripts").mkdir()

    (ws / "scripts" / "plot.py").write_text("print('hi')\n", encoding="utf-8")

    fig = ws / "figures" / "scores.png"
    fig.write_bytes(b"old")

    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(ws))

    # Avoid touching real DuckDB: capture what would be stored.
    captured = {"nodes": None, "edges": None}

    from sros.servers import memory as _mem_pkg  # noqa: F401
    from sros.servers.memory import handler as memory_handler

    def _store(nodes, edges):
        captured["nodes"] = nodes
        captured["edges"] = edges
        return True

    monkeypatch.setattr(memory_handler.MemoryHandler, "store_knowledge", staticmethod(_store), raising=True)

    def _fake_run(argv, cwd, capture_output, text, env, timeout):
        # Modify the existing figure (overwrite scenario)
        fig.write_bytes(b"new")
        return _Completed(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", _fake_run)

    res = DataHandler().run_script("scripts/plot.py", dataset_paths=[])
    assert res["ok"] is True
    assert any("scores.png" in p for p in res.get("generated_figures", []))

    # Ensure a GENERATES edge would be written.
    assert captured["edges"] is not None
    assert any(getattr(e, "relationship", None) == "GENERATES" for e in captured["edges"])
