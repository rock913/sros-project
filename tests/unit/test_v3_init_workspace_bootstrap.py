from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from sros.cli import app


def test_v3_init_creates_workspace_dirs_and_openclaw(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "proj-v3", "--target", "both"])
    assert result.exit_code == 0, result.output

    project = tmp_path / "proj-v3"

    # Core workspace
    assert (project / "draft.md").exists()
    assert (project / "ideas.md").exists()
    assert (project / ".sros" / "graph.db").exists()
    assert (project / ".sros" / "plugins").is_dir()

    # V3 workspace expansion
    assert (project / "data" / "raw").is_dir()
    assert (project / "data" / "processed").is_dir()
    assert (project / "figures").is_dir()
    assert (project / "scripts").is_dir()

    # Agent bootstrap artifacts
    assert (project / "openclaw.yaml").exists()
    assert (project / ".roo" / "mcp.json").exists()
    assert (project / ".clauderc").exists()
    assert (project / "CLAUDE.md").exists()
