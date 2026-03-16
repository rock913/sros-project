from __future__ import annotations

import json
from pathlib import Path

import pytest

from sros.gateway.main import SROSGateway


def _rpc_call(gateway: SROSGateway, tool: str, args: dict, request_id: int = 1) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {"name": tool, "arguments": args},
    }
    return gateway.dispatch_jsonrpc(payload)


def test_gateway_reflects_skill_insert_section(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    (tmp_path / ".sros").mkdir(parents=True, exist_ok=True)
    (tmp_path / "draft.md").write_text("# T\n\n## Intro\n\nExisting.\n", encoding="utf-8")

    gw = SROSGateway()

    resp = _rpc_call(
        gw,
        "manuscript.insert_section",
        {
            "target": "heading:Intro",
            "content": "Inserted via gateway reflector.",
            "citations": ["doe2021"],
            "file_path": "draft.md",
        },
    )

    assert resp.get("error") is None, resp
    result = resp["result"]["content"][0]["text"]
    data = json.loads(result)
    assert data["ok"] is True

    updated = (tmp_path / "draft.md").read_text(encoding="utf-8")
    assert "Inserted via gateway reflector." in updated


def test_gateway_reflects_skill_scholar_search(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SROS_WORKSPACE_DIR", str(tmp_path))

    gw = SROSGateway()
    resp = _rpc_call(gw, "scholar.federated_search", {"query": "transformer attention", "max_results": 2, "filters": {}})

    assert resp.get("error") is None, resp
    result = resp["result"]["content"][0]["text"]
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) >= 1
