from __future__ import annotations

import json
from types import SimpleNamespace
from pathlib import Path

from typer.testing import CliRunner

from sros.skills.cli import app


def test_ext_web_scrape_returns_text(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    # Import path used by the handler (requests.get)
    import requests

    def _fake_get(url: str, timeout: float = 15.0, headers=None):
        assert url == "https://example.com/x"
        return SimpleNamespace(
            status_code=200,
            text="<html><head><title>T</title></head><body><h1>Hello</h1> world</body></html>",
            headers={"content-type": "text/html"},
        )

    monkeypatch.setattr(requests, "get", _fake_get)

    runner = CliRunner()
    result = runner.invoke(app, ["--raw", "ext", "web-scrape", "--url", "https://example.com/x"])
    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["url"] == "https://example.com/x"
    assert "Hello" in payload["text"]
    assert payload.get("title") == "T"
