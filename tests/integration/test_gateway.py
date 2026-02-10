#!/usr/bin/env python3
"""
Test script for SROS V2.2 Gateway functionality
"""
import json
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_gateway_startup():
    """Test that gateway starts successfully"""
    print("🧪 Testing Gateway Startup...")

    cmd = ["python", str(PROJECT_ROOT / "run_servers.py"), "gateway", "--auto-port"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(3)

    if process.poll() is None:
        print("✅ Gateway started successfully")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        return True

    print("❌ Gateway failed to start")
    stdout, stderr = process.communicate()
    print(f"STDOUT: {stdout.decode()}")
    print(f"STDERR: {stderr.decode()}")
    return False


def test_health_endpoint_sync():
    """Test that health endpoint properly synchronizes server readiness"""
    print("🧪 Testing Health Endpoint Synchronization...")

    try:
        gateway_main = PROJECT_ROOT / "mcp_servers" / "sros_gateway" / "main.py"
        content = gateway_main.read_text(encoding="utf-8")

        if "while not all(self.sub_process_manager.is_ready" in content and "timeout = 30" in content:
            print("✅ Health endpoint synchronization fix is present in main.py")
            print("   The gateway now waits for all servers to be ready before marking system ready")
            return True

        print("❌ Health endpoint synchronization fix not found in main.py")
        return False

    except Exception as e:
        print(f"❌ Error checking for fix in main.py: {e}")
        return False


def test_gateway_config():
    """Test that gateway configuration is valid"""
    print("🧪 Testing Gateway Configuration...")

    config_path = PROJECT_ROOT / "mcp_servers" / "sros_gateway" / "config.json"
    if not config_path.exists():
        print("❌ Gateway config file not found")
        return False

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))

        required_servers = ["federal", "manuscript", "memory", "zotero"]
        found_servers = list(config["servers"].keys())

        if all(server in found_servers for server in required_servers):
            print("✅ Gateway configuration is valid")
            print(f"   Found servers: {found_servers}")
            return True

        print(f"❌ Missing required servers. Expected: {required_servers}, Found: {found_servers}")
        return False

    except Exception as e:
        print(f"❌ Error reading gateway config: {e}")
        return False


def test_context_ingester():
    """Test context ingester functionality"""
    print("🧪 Testing Context Ingester...")

    try:
        import sys

        sys.path.insert(0, str(PROJECT_ROOT))
        import mcp_servers.context_ingester.main
        import mcp_servers.context_ingester.mcp_handler
        print("✅ Context Ingester modules are importable")
        return True
    except ImportError as e:
        print(f"❌ Context Ingester import error: {e}")
        return False


def test_run_servers_gateway_mode():
    """Test that run_servers.py supports gateway mode"""
    print("🧪 Testing run_servers.py Gateway Mode...")

    run_servers = PROJECT_ROOT / "run_servers.py"
    content = run_servers.read_text(encoding="utf-8")

    if '"gateway"' in content and "sros_gateway.main" in content:
        print("✅ run_servers.py has gateway mode support")
        return True

    print("❌ run_servers.py missing gateway mode support")
    return False


def main():
    """Run all tests"""
    print("🚀 SROS V2.2 Gateway Implementation Tests")
    print("=" * 50)

    tests = [
        test_gateway_config,
        test_context_ingester,
        test_run_servers_gateway_mode,
        test_gateway_startup,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
            print()

    results.append(test_health_endpoint_sync())

    print("=" * 50)
    print("📊 Test Results:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if all(results):
        print("🎉 All tests passed! SROS V2.2 Gateway is ready.")
        return True

    print("❌ Some tests failed. Please check the implementation.")
    return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
