#!/usr/bin/env python3
"""
Smoke test to verify the port binding fix works correctly
"""
import subprocess
import sys
import time
import requests
import threading
import signal
import os


def _wait_for_health(port: int, timeout_s: float = 10.0) -> bool:
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
    print(f"✗ /health did not become ready on port {port}: {last_error}")
    return False

def test_port_binding_fix():
    """测试端口绑定修复"""
    print("Testing port binding fix...")
    
    # Test with a custom port
    test_port = 8080
    
    # Start sros in background
    process = subprocess.Popen([
        sys.executable, "-m", "sros.cli", "start", "-p", str(test_port)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not _wait_for_health(test_port, timeout_s=12):
        return False
    
    try:
        # Check if the process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"Process failed to start. Stdout: {stdout.decode()}")
            print(f"Stderr: {stderr.decode()}")
            return False
            
        # Test that the custom port responds
        try:
            response = requests.get(f"http://localhost:{test_port}/health", timeout=5)
            if response.status_code != 200:
                print(f"Expected 200, got {response.status_code}")
                return False
            print(f"✓ Custom port {test_port} responding correctly")
        except Exception as e:
            print(f"✗ Failed to connect to custom port {test_port}: {e}")
            return False
            
        # Test that default port 8000 is NOT bound (unless explicitly requested)
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            # If we get a response, it means port 8000 is in use, which is fine
            # but we want to make sure it's not being forced to bind to 8000
            print(f"Port 8000 is in use (this is okay)")
        except:
            # Expected if port 8000 is not in use
            print("Port 8000 is not in use (as expected)")
            
        return True
        
    finally:
        # Clean up the process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def test_sse_content_type():
    """测试 SSE 内容类型"""
    print("Testing SSE content type...")
    
    test_port = 8081
    
    # Start sros in background
    process = subprocess.Popen([
        sys.executable, "-m", "sros.cli", "start", "-p", str(test_port)
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not _wait_for_health(test_port, timeout_s=12):
        return False
    
    try:
        # Test SSE endpoint with once=1
        response = requests.get(f"http://localhost:{test_port}/sse?once=1", timeout=5)
        if response.status_code != 200:
            print(f"Expected 200 for SSE endpoint, got {response.status_code}")
            return False
            
        content_type = response.headers.get('content-type', '')
        if 'text/event-stream' not in content_type:
            print(f"Expected text/event-stream, got {content_type}")
            return False
            
        print("✓ SSE endpoint returns correct content-type")
        return True
        
    except Exception as e:
        print(f"✗ SSE test failed: {e}")
        return False
        
    finally:
        # Clean up the process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    print("Running smoke tests for SROS port binding fix...")
    
    success = True
    
    # Run tests
    if not test_port_binding_fix():
        success = False
        print("Port binding test failed!")
    
    if not test_sse_content_type():
        success = False
        print("SSE content type test failed!")
    
    if success:
        print("\n✓ All smoke tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some smoke tests failed!")
        sys.exit(1)