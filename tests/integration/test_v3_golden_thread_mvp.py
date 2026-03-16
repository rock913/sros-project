from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest
import requests


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = int(s.getsockname()[1])
    s.close()
    return port


def _wait_for_health(port: int, timeout_s: float = 12.0) -> None:
    deadline = time.time() + timeout_s
    last: Exception | None = None
    while time.time() < deadline:
        try:
            r = requests.get(f"http://127.0.0.1:{port}/health", timeout=1)
            if r.status_code == 200:
                return
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(0.2)
    raise AssertionError(f"Gateway not healthy in time: {last}")


@pytest.mark.integration
def test_v3_golden_thread_gap_search_insert():
    port = _find_free_port()

    env = os.environ.copy()
    # Ensure the subprocess can import the editable package in CI-like contexts.
    env["PYTHONPATH"] = str(_repo_root())

    with tempfile.TemporaryDirectory() as temp_dir:
        ws = Path(temp_dir) / "ws"
        subprocess.check_call([sys.executable, "-m", "sros.cli", "init", str(ws)], env=env)

        # Seed a TODO to make gaps non-empty
        (ws / "draft.md").write_text("# T\n\n## Intro\n\n[TODO: add citation]\n", encoding="utf-8")

        proc = subprocess.Popen(
            [sys.executable, "-m", "sros.cli", "start", "-w", str(ws), "-p", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        try:
            _wait_for_health(port)

            # 1) gaps
            payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "manuscript.find_gaps", "arguments": {"file_path": "draft.md"}}}
            r = requests.post(f"http://127.0.0.1:{port}/sse", json=payload, timeout=10)
            assert r.status_code == 200

            # 2) search (mock)
            payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "scholar.federated_search", "arguments": {"query": "transformer attention", "max_results": 2, "filters": {}}}}
            r = requests.post(f"http://127.0.0.1:{port}/sse", json=payload, timeout=10)
            assert r.status_code == 200

            # 3) insert
            payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "manuscript.insert_section",
                    "arguments": {
                        "target": "heading:Intro",
                        "content": "Inserted by V3 golden thread.",
                        "citations": ["doe2021"],
                        "file_path": "draft.md",
                    },
                },
            }
            r = requests.post(f"http://127.0.0.1:{port}/sse", json=payload, timeout=10)
            assert r.status_code == 200

            updated = (ws / "draft.md").read_text(encoding="utf-8")
            assert "Inserted by V3 golden thread." in updated

        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
