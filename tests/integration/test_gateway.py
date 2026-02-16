"""Integration test for gateway functionality."""
import os
import socket
import tempfile
from pathlib import Path

import pytest
import subprocess
import sys
import time
import requests


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


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

@pytest.mark.integration
def test_gateway_startup():
    """Test that gateway starts up correctly."""
    port = _find_free_port()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(_repo_root())

    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = _init_workspace(temp_dir, "test_gateway_startup", env)

        # Start sros in background
        process = subprocess.Popen(
            [sys.executable, "-m", "sros.cli", "start", "-w", workspace, "-p", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        try:
            _wait_for_health(port, timeout_s=10)

            if process.poll() is not None:
                stdout, stderr = process.communicate()
                pytest.fail(f"Process failed to start. Stdout: {stdout.decode()}, Stderr: {stderr.decode()}")

            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            assert response.status_code == 200

        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

if __name__ == "__main__":
    test_gateway_startup()