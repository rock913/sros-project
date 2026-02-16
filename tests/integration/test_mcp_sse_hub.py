"""Integration test for MCP SSE Hub functionality."""
import os
import pytest
import subprocess
import sys
import time
import requests
import json
import socket
import tempfile
from pathlib import Path
from typing import Dict, Any


def _find_free_port() -> int:
    """Find a free port for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_health(port: int, timeout_s: float = 10.0) -> None:
    """Wait for the gateway to become healthy."""
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


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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
def test_mcp_sse_hub_functionality():
    """Test that the gateway acts as an MCP SSE Hub with required functionality."""
    port = _find_free_port()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(_repo_root())

    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = _init_workspace(temp_dir, "test_mcp_sse_hub", env)

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

            # Test 1: GET /sse returns text/event-stream
            response = requests.get(f"http://localhost:{port}/sse", stream=True, timeout=5)
            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "").lower()

            # Read first few lines to verify SSE format
            lines = []
            for line in response.iter_lines(decode_unicode=True):
                lines.append(line)
                if len(lines) >= 3:
                    break
            response.close()

            has_data_events = any(line.startswith("data:") for line in lines)
            assert has_data_events, f"Expected SSE data events, got: {lines}"

            # Test 2: POST /sse initialize returns valid JSON-RPC response
            initialize_payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
            response = requests.post(f"http://localhost:{port}/sse", json=initialize_payload, timeout=5)
            assert response.status_code == 200
            result = response.json()
            assert result["jsonrpc"] == "2.0"
            assert result["id"] == 1
            assert "result" in result
            assert "capabilities" in result["result"]

            # Test 3: POST /sse tools/list returns tools including manuscript.find_gaps
            tools_list_payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
            response = requests.post(f"http://localhost:{port}/sse", json=tools_list_payload, timeout=5)
            assert response.status_code == 200
            result = response.json()
            assert result["jsonrpc"] == "2.0"
            assert result["id"] == 2
            assert "result" in result
            assert "tools" in result["result"]

            tools = result["result"]["tools"]
            tool_names = [tool["name"] for tool in tools]
            assert "manuscript.find_gaps" in tool_names, f"Expected manuscript.find_gaps in tools, got: {tool_names}"

            # Test 4: POST /sse tools/call manuscript.find_gaps returns structured content
            # Create test file in workspace
            test_file_path = Path(workspace) / "test_document.md"
            test_file_path.write_text("# Test Document\n\nThis is a test document.\n\n[TODO: Add more content here]", encoding="utf-8")

            try:
                call_payload = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "manuscript.find_gaps", "arguments": {"file_path": "test_document.md"}},
                }
                response = requests.post(f"http://localhost:{port}/sse", json=call_payload, timeout=5)
                assert response.status_code == 200
                result = response.json()
                assert result["jsonrpc"] == "2.0"
                assert result["id"] == 3
                assert "result" in result
                assert "content" in result["result"]
                assert isinstance(result["result"]["content"], list)
            finally:
                # Cleanup test file from workspace
                if test_file_path.exists():
                    test_file_path.unlink()

        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def test_duckdb_file_creation():
    """
    Test that sros init creates a real DuckDB file that can be connected to
    """
    import tempfile
    import subprocess
    import sys
    import os
    from pathlib import Path
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(_repo_root())
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize the project
        init_process = subprocess.run([
            sys.executable, "-m", "sros.cli", "init", "test_project"
        ], cwd=temp_dir, capture_output=True, text=True, env=env)
        
        assert init_process.returncode == 0, "sros init should succeed"
        
        # Check if .sros/graph.db exists
        db_path = Path(temp_dir) / "test_project" / ".sros" / "graph.db"
        assert db_path.exists(), ".sros/graph.db should exist after sros init"
        
        # Test that duckdb.connect() can connect to it without error
        import duckdb
        try:
            conn = duckdb.connect(str(db_path))
            conn.close()
        except Exception as e:
            pytest.fail(f"duckdb.connect() failed on .sros/graph.db: {e}")

if __name__ == "__main__":
    # Run tests manually if executed directly
    test_mcp_sse_hub_functionality()
    print("✓ MCP SSE Hub test passed")
    
    test_duckdb_file_creation()
    print("✓ DuckDB file creation test passed")
    
    print("All tests passed!")
