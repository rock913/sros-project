#!/usr/bin/env python3
"""Live verification for Scholar OpenAlex backend.

This script is intentionally not part of pytest because it requires network.

Usage (recommended):
  1) Put OPENALEX_* and SROS_SCHOLAR_BACKEND=openalex in your workspace .env
  2) Start gateway: sros start --auto-port
  3) Run: python scripts/verify_openalex_live.py --port 8000 --query "..."

It will call tools/list + tools/call (scholar.federated_search) via the Gateway.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists() or not dotenv_path.is_file():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def rpc(port: int, payload: Dict[str, Any], timeout_s: float) -> Dict[str, Any]:
    resp = requests.post(f"http://localhost:{port}/sse", json=payload, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.getenv("SROS_PORT", "8000")))
    parser.add_argument("--query", type=str, default="transformer attention")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--dotenv", type=str, default=".env")
    parser.add_argument("--out", type=str, default="logs/openalex_live_verification.json")
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))

    # 1) tools/list
    tools_list = rpc(
        args.port,
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        timeout_s=args.timeout,
    )

    tool_names = {t.get("name") for t in (tools_list.get("result", {}).get("tools") or [])}
    if "scholar.federated_search" not in tool_names:
        raise SystemExit("scholar.federated_search not exposed by gateway (tools/list)")

    # 2) tools/call scholar.federated_search
    call = rpc(
        args.port,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "scholar.federated_search",
                "arguments": {"query": args.query, "max_results": args.max_results, "filters": {}},
            },
        },
        timeout_s=args.timeout,
    )

    content = call.get("result", {}).get("content")
    # Gateway returns MCP-ish content; accept list/dict and keep raw.
    results: Optional[List[Dict[str, Any]]] = None
    if isinstance(content, list) and content and isinstance(content[0], dict):
        # heuristic: many implementations return [{'type':'text','text':'...'}]
        # but our Scholar mock/openalex returns a JSONable list of dicts.
        # If it's not that, we still dump raw.
        if all(isinstance(x, dict) and "title" in x for x in content):
            results = content  # type: ignore[assignment]

    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "port": args.port,
        "query": args.query,
        "max_results": args.max_results,
        "env": {
            "SROS_SCHOLAR_BACKEND": os.getenv("SROS_SCHOLAR_BACKEND"),
            "OPENALEX_BASE_URL": os.getenv("OPENALEX_BASE_URL"),
            "OPENALEX_EMAIL": os.getenv("OPENALEX_EMAIL"),
            "SROS_OPENALEX_BASE_URL": os.getenv("SROS_OPENALEX_BASE_URL"),
            "SROS_OPENALEX_MAILTO": os.getenv("SROS_OPENALEX_MAILTO"),
        },
        "tools_list_ok": True,
        "tools_call_raw": call,
        "parsed_results": results,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    # Minimal human output
    if results is not None:
        print(f"OK: got {len(results)} results")
        if results:
            print("First title:", results[0].get("title"))
            print("First source:", results[0].get("source"))
    else:
        print("OK: call succeeded; see output file for raw response")

    print("Wrote:", str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
