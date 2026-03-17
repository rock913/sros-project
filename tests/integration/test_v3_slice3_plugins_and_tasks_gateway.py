from __future__ import annotations

import json
import os
import socket
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_health(port: int, timeout_s: float = 10.0) -> None:
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            resp = requests.get(f"http://localhost:{port}/health", timeout=1)
            if resp.status_code == 200:
                return
        except Exception as e:  # noqa: BLE001
            last_error = e
        time.sleep(0.2)
    raise AssertionError(f"Gateway did not become healthy on port {port}: {last_error}")


def _init_workspace(temp_dir: str, name: str, env: dict) -> str:
    subprocess.run(
        [sys.executable, "-m", "sros.cli", "init", name],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return str(Path(temp_dir) / name)


@pytest.mark.integration
def test_slice3_dynamic_plugin_tools_and_task_notification():
    port = _find_free_port()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(_repo_root())

    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = _init_workspace(temp_dir, "test_slice3_plugins", env)

        plugins_dir = Path(workspace) / ".sros" / "plugins"
        plugins_dir.mkdir(parents=True, exist_ok=True)

        (plugins_dir / "hello.py").write_text(
            "\n".join(
                [
                    'SKILL_NAME = "Hello"',
                    'SKILL_DESCRIPTION = "Hello plugin"',
                    'SKILL_INPUT_SCHEMA = {"type": "object", "properties": {"x": {"type": "integer"}}, "additionalProperties": False}',
                    "",
                    "def run(args: dict):",
                    "    return {\"echo\": args, \"answer\": 42}",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        (plugins_dir / "slow.py").write_text(
            "\n".join(
                [
                    'SKILL_NAME = "Slow"',
                    'SKILL_DESCRIPTION = "Sleep and return"',
                    "",
                    "import time",
                    "",
                    "def run(args: dict):",
                    "    time.sleep(float(args.get('sleep_s', 0.2)))",
                    "    return {'ok': True, 'slept': float(args.get('sleep_s', 0.2))}",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        process = subprocess.Popen(
            [sys.executable, "-m", "sros.cli", "start", "-w", workspace, "-p", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        try:
            _wait_for_health(port, timeout_s=10)

            # tools/list should include plugin.hello
            tools_list_payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
            resp = requests.post(f"http://localhost:{port}/sse", json=tools_list_payload, timeout=5)
            assert resp.status_code == 200
            result = resp.json()
            tools = result["result"]["tools"]
            names = [t["name"] for t in tools]
            assert "plugin.hello" in names

            # tools/call plugin.hello
            call_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "plugin.hello", "arguments": {"x": 7}},
            }
            resp = requests.post(f"http://localhost:{port}/sse", json=call_payload, timeout=5)
            assert resp.status_code == 200
            out = resp.json()
            content_text = out["result"]["content"][0]["text"]
            plugin_res = json.loads(content_text)
            assert plugin_res["ok"] is True
            assert plugin_res["plugin"] == "hello"
            assert plugin_res["result"]["answer"] == 42
            assert plugin_res["result"]["echo"]["x"] == 7

            # SSE session: start async task and wait for notification
            stream = requests.get(f"http://localhost:{port}/sse", stream=True, timeout=5)
            session_url = None
            try:
                it = stream.iter_lines(decode_unicode=True)

                for line in it:
                    if not line:
                        continue
                    if line.startswith("data:"):
                        data = line.split(":", 1)[1].strip()
                        if data.startswith("/messages?"):
                            session_url = f"http://localhost:{port}{data}"
                            break
                assert session_url is not None

                start_payload = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "tasks.run_plugin_async",
                        "arguments": {"plugin": "slow", "args": {"sleep_s": 0.2}},
                    },
                }
                post = requests.post(session_url, json=start_payload, timeout=5)
                assert post.status_code == 200

                # Consume SSE messages until we see the completion notification.
                saw_notification = False
                deadline = time.time() + 10
                for line in it:
                    if time.time() > deadline:
                        break
                    if not line or not line.startswith("data:"):
                        continue
                    data = line.split(":", 1)[1].strip()
                    if not data:
                        continue
                    msg = json.loads(data)
                    if isinstance(msg, dict) and msg.get("method") == "sros.task.completed":
                        params = msg.get("params") or {}
                        task = params.get("task") or {}
                        if task.get("kind") == "plugin" and task.get("name") == "slow":
                            saw_notification = True
                            break
                assert saw_notification is True
            finally:
                stream.close()

        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
