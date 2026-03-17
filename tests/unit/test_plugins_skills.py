from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_plugins_list_and_run(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    plugins_dir = tmp_path / ".sros" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    plugin_code = (
        "\n".join(
            [
                '"""A minimal SROS plugin."""',
                "",
                'SKILL_NAME = "hello"',
                'SKILL_DESCRIPTION = "Hello plugin"',
                "",
                "def run(args: dict):",
                "    return {\"echo\": args, \"answer\": 42}",
                "",
            ]
        )
        + "\n"
    )
    (plugins_dir / "hello.py").write_text(plugin_code, encoding="utf-8")

    runner = CliRunner()

    listed = runner.invoke(app, ["--raw", "plugins", "list"])
    assert listed.exit_code == 0, listed.output
    payload = json.loads(listed.output)
    assert payload["ok"] is True
    assert payload["count"] == 1
    assert payload["plugins"][0]["name"] == "hello"

    ran = runner.invoke(app, ["--raw", "plugins", "run", "--name", "hello", "--args-json", "{\"x\": 1}"])
    assert ran.exit_code == 0, ran.output
    out = json.loads(ran.output)
    assert out["ok"] is True
    assert out["plugin"] == "hello"
    assert out["result"]["echo"]["x"] == 1
    assert out["result"]["answer"] == 42
