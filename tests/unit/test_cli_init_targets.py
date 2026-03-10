from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.cli import app


def test_init_target_claude_code(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, [
        "init",
        "proj-claude",
        "--target",
        "claude-code",
        "--gateway-url",
        "http://127.0.0.1:8000/sse",
    ])
    assert result.exit_code == 0, result.output

    project = tmp_path / "proj-claude"
    assert (project / "draft.md").exists()
    assert (project / ".sros" / "graph.db").exists()

    # Claude artifacts
    rc = project / ".clauderc"
    assert rc.exists()
    assert (project / "CLAUDE.md").exists()

    data = json.loads(rc.read_text(encoding="utf-8"))
    assert "custom_instructions" in data
    assert "mcp_servers" in data
    assert data["mcp_servers"]["sros-gateway"]["url"] == "http://127.0.0.1:8000/sse"

    # Roo artifacts should NOT be created in claude-only mode
    assert not (project / ".roo" / "mcp.json").exists()


def test_init_target_both(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, [
        "init",
        "proj-both",
        "--target",
        "both",
    ])
    assert result.exit_code == 0, result.output

    project = tmp_path / "proj-both"
    assert (project / ".roo" / "mcp.json").exists()
    assert (project / ".clauderc").exists()
    assert (project / "CLAUDE.md").exists()


def test_init_default_target_roo_only(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "proj-default"]) 
    assert result.exit_code == 0, result.output

    project = tmp_path / "proj-default"
    assert (project / ".roo" / "mcp.json").exists()
    assert not (project / ".clauderc").exists()
    assert not (project / "CLAUDE.md").exists()
