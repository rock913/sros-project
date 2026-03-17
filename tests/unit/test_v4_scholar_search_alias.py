from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_scholar_search_alias_outputs_citekeys(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))
    monkeypatch.setenv("SROS_SCHOLAR_BACKEND", "mock")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--raw",
            "scholar",
            "search",
            "--query",
            "transformer astronomy light curve",
            "--max-results",
            "3",
        ],
    )
    assert result.exit_code == 0, result.output

    items = json.loads(result.stdout)
    assert isinstance(items, list)
    assert items
    assert all("citekey" in it and it["citekey"] for it in items)
