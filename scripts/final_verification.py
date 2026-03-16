#!/usr/bin/env python3
"""
Final verification script to ensure all requirements are met
"""
import subprocess
import sys
import time
import requests
import json
import tempfile
import os
from pathlib import Path


def _wait_for_health(port: int, timeout_s: float = 10.0) -> bool:
    """Wait until /health returns 200 or timeout."""
    deadline = time.time() + timeout_s
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            resp = requests.get(f"http://localhost:{port}/health", timeout=1)
            if resp.status_code == 200:
                return True
        except Exception as e:  # noqa: BLE001
            last_error = e
        time.sleep(0.2)
    print(f"   ✗ /health did not become ready on port {port}: {last_error}")
    return False

def test_cli_port_option():
    """Test that sros start -p <port> actually binds to the specified port"""
    print("1. Testing CLI port option...")
    
    test_port = 8082
    
    # Start sros in background
    process = subprocess.Popen([
        sys.executable, "-m", "sros.cli", "start", "-p", str(test_port)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not _wait_for_health(test_port, timeout_s=12):
        stdout, stderr = process.communicate(timeout=2) if process.poll() is not None else (b"", b"")
        if stdout or stderr:
            print(f"   Process output:\n{stdout.decode(errors='replace')}{stderr.decode(errors='replace')}")
        return False
    
    try:
        # Check if the process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"   Process failed to start: {stderr.decode()}")
            return False
            
        # Test that the custom port responds with 200
        response = requests.get(f"http://localhost:{test_port}/health", timeout=5)
        if response.status_code != 200:
            print(f"   Expected 200, got {response.status_code}")
            return False
            
        print(f"   ✓ Port {test_port} correctly bound and responding")
        return True
        
    except Exception as e:
        print(f"   ✗ Failed to test port binding: {e}")
        return False
        
    finally:
        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def test_sse_content_type():
    """Test that /sse?once=1 returns text/event-stream"""
    print("2. Testing SSE content type...")
    
    test_port = 8083
    
    # Start sros in background
    process = subprocess.Popen([
        sys.executable, "-m", "sros.cli", "start", "-p", str(test_port)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not _wait_for_health(test_port, timeout_s=12):
        stdout, stderr = process.communicate(timeout=2) if process.poll() is not None else (b"", b"")
        if stdout or stderr:
            print(f"   Process output:\n{stdout.decode(errors='replace')}{stderr.decode(errors='replace')}")
        return False
    
    try:
        # Test SSE endpoint
        response = requests.get(f"http://localhost:{test_port}/sse?once=1", timeout=5)
        if response.status_code != 200:
            print(f"   Expected 200, got {response.status_code}")
            return False
            
        content_type = response.headers.get('content-type', '')
        if 'text/event-stream' not in content_type:
            print(f"   Expected text/event-stream, got {content_type}")
            return False
            
        print("   ✓ SSE endpoint returns correct content-type")
        return True
        
    except Exception as e:
        print(f"   ✗ Failed to test SSE content type: {e}")
        return False
        
    finally:
        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def test_mcp_json_schema():
    """Test that .roo/mcp.json schema is correct"""
    print("3. Testing .roo/mcp.json schema...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Initialize a project
            init_process = subprocess.run([
                sys.executable, "-m", "sros.cli", "init", "test_project"
            ], capture_output=True, text=True)
            
            if init_process.returncode != 0:
                print(f"   Failed to initialize project: {init_process.stderr}")
                return False
                
            # Check if .roo/mcp.json exists
            mcp_json_path = Path("test_project/.roo/mcp.json")
            if not mcp_json_path.exists():
                print("   .roo/mcp.json not found")
                return False
                
            # Read and validate the JSON
            with open(mcp_json_path, 'r') as f:
                mcp_config = json.load(f)
            
            # Validate schema
            if "mcpServers" not in mcp_config:
                print("   Missing mcpServers key")
                return False
                
            if "sros-gateway" not in mcp_config["mcpServers"]:
                print("   Missing sros-gateway server")
                return False
                
            gateway_config = mcp_config["mcpServers"]["sros-gateway"]
            required_fields = ["name", "url", "type", "description", "disabled", "alwaysAllow"]
            
            for field in required_fields:
                if field not in gateway_config:
                    print(f"   Missing required field: {field}")
                    return False
                    
            # Validate URL format
            if gateway_config["url"] != "http://localhost:8000/sse":
                print(f"   Unexpected URL: {gateway_config['url']}")
                return False
                
            print("   ✓ .roo/mcp.json schema is correct")
            return True
            
        finally:
            os.chdir(original_cwd)


def test_v3_golden_thread():
    """V3 MVP: gap -> search (mock) -> insert, via gateway JSON-RPC."""
    print("4. Testing V3 golden thread (gap->search->insert)...")

    test_port = 8084

    with tempfile.TemporaryDirectory() as temp_dir:
        ws = Path(temp_dir) / "ws"

        init_process = subprocess.run(
            [sys.executable, "-m", "sros.cli", "init", str(ws)],
            capture_output=True,
            text=True,
        )
        if init_process.returncode != 0:
            print(f"   Failed to init workspace: {init_process.stderr}")
            return False

        (ws / "draft.md").write_text("# T\n\n## Intro\n\n[TODO: add citation]\n", encoding="utf-8")

        process = subprocess.Popen(
            [sys.executable, "-m", "sros.cli", "start", "-w", str(ws), "-p", str(test_port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            if not _wait_for_health(test_port, timeout_s=12):
                stdout, stderr = process.communicate(timeout=2) if process.poll() is not None else (b"", b"")
                if stdout or stderr:
                    print(f"   Process output:\n{stdout.decode(errors='replace')}{stderr.decode(errors='replace')}")
                return False

            # gap
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "manuscript.find_gaps", "arguments": {"file_path": "draft.md"}},
            }
            r = requests.post(f"http://localhost:{test_port}/sse", json=payload, timeout=10)
            if r.status_code != 200:
                print(f"   gap call failed: {r.status_code} {r.text[:200]}")
                return False

            # search
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "scholar.federated_search",
                    "arguments": {"query": "transformer attention", "max_results": 2, "filters": {}},
                },
            }
            r = requests.post(f"http://localhost:{test_port}/sse", json=payload, timeout=10)
            if r.status_code != 200:
                print(f"   search call failed: {r.status_code} {r.text[:200]}")
                return False

            # insert
            payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "manuscript.insert_section",
                    "arguments": {
                        "target": "heading:Intro",
                        "content": "Inserted by final verification.",
                        "citations": ["doe2021"],
                        "file_path": "draft.md",
                    },
                },
            }
            r = requests.post(f"http://localhost:{test_port}/sse", json=payload, timeout=10)
            if r.status_code != 200:
                print(f"   insert call failed: {r.status_code} {r.text[:200]}")
                return False

            updated = (ws / "draft.md").read_text(encoding="utf-8")
            if "Inserted by final verification." not in updated:
                print("   draft.md was not updated")
                return False

            print("   ✓ V3 golden thread ok")
            return True
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def main():
    """Run all verification tests"""
    print("Running final verification tests...\n")
    
    tests = [
        test_cli_port_option,
        test_sse_content_type,
        test_mcp_json_schema,
        test_v3_golden_thread,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All verification tests passed! The fix is working correctly.")
        return 0
    else:
        print("❌ Some verification tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())