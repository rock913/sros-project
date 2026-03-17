from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_manuscript_outline_alias_get_outline_tree(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "draft.md").write_text("# My Paper\n\n## Intro\n\nText\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "manuscript", "get-outline-tree", "--file", "draft.md"])
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["id"] == "root"
    assert payload["title"] in {"Document", "Environment Error", "Path Security Error"}


def test_manuscript_sha256_alias_get_file_sha256(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "draft.md").write_text("# My Paper\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "manuscript", "get-file-sha256", "--file", "draft.md"])
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["file_path"] == "draft.md"
    assert isinstance(payload["sha256"], str)
    assert len(payload["sha256"]) == 64


def test_manuscript_insert_accepts_section_end_target(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text("# My Paper\n\nIntro.\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "manuscript",
            "insert",
            "--target",
            "section:end",
            "--content",
            "# Results\n\nHello.\n",
            "--file",
            "draft.md",
        ],
    )
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["ok"] is True

    updated = draft.read_text(encoding="utf-8")
    assert "# Results" in updated


def test_manuscript_insert_accepts_deprecated_position_option(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text("# My Paper\n\nIntro.\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "manuscript",
            "insert",
            "--target",
            "end",
            "--position",
            "after",
            "--content",
            "Appended.",
            "--file",
            "draft.md",
        ],
    )
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["ok"] is True

    updated = draft.read_text(encoding="utf-8")
    assert "Appended." in updated
