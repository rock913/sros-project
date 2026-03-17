from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from sros.cli import app


def _write_pid_file(workspace: Path, pid: int, port: int = 8000) -> Path:
    pid_path = workspace / ".sros" / "gateway.pid"
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(
        json.dumps(
            {
                "pid": int(pid),
                "port": int(port),
                "started_at": "2026-03-17T16:59:00Z",
            }
        ),
        encoding="utf-8",
    )
    return pid_path


def test_start_refuses_when_workspace_pid_alive(tmp_path: Path, monkeypatch):
    runner = CliRunner()

    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / ".sros").mkdir()

    _write_pid_file(workspace, os.getpid(), port=8123)

    # If start incorrectly tries to run the gateway, fail the test.
    import sros.gateway.main as gateway_main

    async def _boom(_config=None):  # pragma: no cover
        raise AssertionError("gateway main() should not be called when PID is already alive")

    monkeypatch.setattr(gateway_main, "main", _boom, raising=True)

    result = runner.invoke(
        app,
        [
            "start",
            "--workspace",
            str(workspace),
            "--port",
            "8123",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "already" in result.output.lower() or "running" in result.output.lower()


def test_stop_cleans_zombie_pid_file(tmp_path: Path):
    runner = CliRunner()

    workspace = tmp_path / "ws"
    workspace.mkdir()

    pid_path = _write_pid_file(workspace, 999999, port=8123)
    assert pid_path.exists()

    result = runner.invoke(app, ["stop", "--workspace", str(workspace)])
    assert result.exit_code == 0, result.output
    assert not pid_path.exists()


def test_stop_terminates_spawned_process(tmp_path: Path):
    runner = CliRunner()

    workspace = tmp_path / "ws"
    workspace.mkdir()

    proc = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        pid_path = _write_pid_file(workspace, proc.pid, port=8123)
        assert pid_path.exists()

        result = runner.invoke(app, ["stop", "--workspace", str(workspace)])
        assert result.exit_code == 0, result.output

        proc.wait(timeout=5)
        assert proc.poll() is not None
        assert not pid_path.exists()
    finally:
        # Cleanup in case stop failed
        try:
            proc.kill()
        except Exception:
            pass


def test_status_cleans_zombie_pid_file(tmp_path: Path, monkeypatch):
    runner = CliRunner()

    workspace = tmp_path / "ws"
    workspace.mkdir()

    pid_path = _write_pid_file(workspace, 999999, port=8123)
    assert pid_path.exists()

    # Ensure status inspects this workspace
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(workspace))

    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0, result.output
    assert not pid_path.exists()


def test_stop_kills_port_owner_when_no_pid_file(tmp_path: Path, monkeypatch):
    runner = CliRunner()

    workspace = tmp_path / "ws"
    workspace.mkdir()

    # No gateway.pid
    (workspace / ".sros").mkdir(exist_ok=True)

    import sros.cli as cli

    class _Owner:
        pid = 424242
        name = "sros"

    monkeypatch.setattr(cli, "find_port_owner", lambda _port: _Owner(), raising=True)
    monkeypatch.setattr(cli, "terminate_process", lambda _pid, timeout_s=3.0: (True, "Terminated"), raising=True)

    result = runner.invoke(
        app,
        [
            "stop",
            "--workspace",
            str(workspace),
            "--kill-port-owner",
            "--port",
            "8000",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Stopped port owner" in result.output
