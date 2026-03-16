from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_skills_find_gaps_raw_json(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / "draft.md").write_text(
        "# Title\n\n[TODO: add citations]\n\nShort.\n",
        encoding="utf-8",
    )

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "manuscript", "find-gaps", "--file", "draft.md"])
    assert result.exit_code == 0, result.output

    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert any(item.get("type") == "Task Pending" for item in data)


def test_skills_insert_raw_json_and_updates_file(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    draft = tmp_path / "draft.md"
    draft.write_text("# Title\n\n## Intro\n\nExisting.\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "manuscript",
            "insert",
            "--target",
            "heading:Intro",
            "--content",
            "Inserted from skill.",
            "--cite",
            "doe2021",
            "--file",
            "draft.md",
        ],
    )
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["ok"] is True

    updated = draft.read_text(encoding="utf-8")
    assert "Inserted from skill." in updated
