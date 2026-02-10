#!/usr/bin/env python3
"""
Test script to verify SSE communication with all MCP servers
"""

import asyncio
import aiohttp
import time
from typing import Dict, Any

SERVERS = {
    "federal-academic-search": {
        "url": "http://localhost:8001/sse",
        "name": "Federal Academic Search",
    },
    "zotero-expert": {
        "url": "http://localhost:8003/sse",
        "name": "Zotero Expert",
    },
    "manuscript-manager": {
        "url": "http://localhost:8004/sse",
        "name": "Manuscript Manager",
    },
    "duckdb-memory": {
        "url": "http://localhost:8005/sse",
        "name": "DuckDB Memory",
    },
    "sros-logic": {
        "url": "http://localhost:8006/sse",
        "name": "SROS Logic",
    },
}


async def test_server_connection(server_name: str, server_url: str) -> Dict[str, Any]:
    """Test connection to a single server with initialization request"""
    print(f"\nTesting {server_name} at {server_url}...")

    try:
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"capabilities": {}, "processId": None, "rootUri": None},
            "id": 1,
        }

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            start_time = time.time()

            async with session.post(
                server_url, json=init_request, headers={"Content-Type": "application/json"}
            ) as response:
                response_time = time.time() - start_time

                if response.status == 200:
                    result = await response.json()
                    print(f"✅ {server_name}: SUCCESS (Response time: {response_time:.2f}s)")
                    print(f"   Response: {result}")

                    return {
                        "status": "success",
                        "response_time": response_time,
                        "response": result,
                        "error": None,
                    }

                error_text = await response.text()
                print(f"❌ {server_name}: HTTP {response.status} - {error_text}")

                return {
                    "status": "http_error",
                    "response_time": response_time,
                    "response": None,
                    "error": f"HTTP {response.status}: {error_text}",
                }

    except asyncio.TimeoutError:
        print(f"❌ {server_name}: TIMEOUT - Server did not respond within 10 seconds")
        return {
            "status": "timeout",
            "response_time": 10.0,
            "response": None,
            "error": "Timeout - Server did not respond",
        }
    except aiohttp.ClientConnectorError as e:
        print(f"❌ {server_name}: CONNECTION ERROR - {str(e)}")
        return {
            "status": "connection_error",
            "response_time": 0,
            "response": None,
            "error": f"Connection error: {str(e)}",
        }
    except Exception as e:
        print(f"❌ {server_name}: ERROR - {str(e)}")
        return {
            "status": "error",
            "response_time": 0,
            "response": None,
            "error": f"Exception: {str(e)}",
        }


async def test_sse_streaming(server_name: str, server_url: str) -> Dict[str, Any]:
    """Test SSE streaming capability"""
    print(f"\nTesting SSE streaming for {server_name}...")

    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(server_url) as response:
                if response.status == 200:
                    print(f"✅ {server_name}: SSE endpoint accessible")
                    return {"status": "success", "error": None}

                print(f"⚠️ {server_name}: SSE endpoint returned {response.status}")
                return {"status": "http_error", "error": f"HTTP {response.status}"}
    except Exception as e:
        print(f"⚠️ {server_name}: SSE test failed - {str(e)}")
        return {"status": "error", "error": str(e)}


async def run_comprehensive_tests():
    """Run comprehensive tests on all servers"""
    print("=" * 60)
    print("SSE COMMUNICATION TEST SUITE")
    print("=" * 60)

    results = {}

    for server_name, server_info in SERVERS.items():
        server_results = {}

        conn_result = await test_server_connection(server_info["name"], server_info["url"])
        server_results["connection"] = conn_result

        if conn_result["status"] == "success":
            sse_result = await test_sse_streaming(server_info["name"], server_info["url"])
            server_results["sse"] = sse_result

        results[server_name] = server_results

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for server_name, server_results in results.items():
        server_info = SERVERS[server_name]
        print(f"\n{server_info['name']} ({server_name}):")

        conn_result = server_results.get("connection", {})
        if conn_result.get("status") == "success":
            print(f"  ✅ Connection: PASSED ({conn_result.get('response_time', 0):.2f}s)")
        else:
            print(f"  ❌ Connection: FAILED - {conn_result.get('error', 'Unknown error')}")
            all_passed = False

        sse_result = server_results.get("sse", {})
        if sse_result.get("status") == "success":
            print("  ✅ SSE: PASSED")
        elif sse_result:
            print(f"  ⚠️  SSE: ISSUE - {sse_result.get('error', 'Unknown error')}")
        else:
            print("  ⚠️  SSE: NOT TESTED (connection failed)")

    print(f"\n{'=' * 60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! All servers are accessible via SSE.")
    else:
        print("❌ SOME TESTS FAILED. Please check server configurations.")
    print(f"{'=' * 60}")

    return results


async def send_test_requests():
    """Send various test requests to verify server functionality"""
    print("\n" + "=" * 60)
    print("FUNCTIONALITY TESTS")
    print("=" * 60)

    test_requests = [
        {
            "name": "Initialize",
            "request": {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {"capabilities": {}},
                "id": 1,
            },
        },
        {
            "name": "Shutdown",
            "request": {"jsonrpc": "2.0", "method": "shutdown", "id": 2},
        },
        {
            "name": "Invalid Method",
            "request": {"jsonrpc": "2.0", "method": "nonexistent_method", "params": {}, "id": 3},
        },
    ]

    for server_name, server_info in SERVERS.items():
        print(f"\nTesting {server_info['name']} with various requests:")

        for test_req in test_requests:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                    async with session.post(
                        server_info["url"],
                        json=test_req["request"],
                        headers={"Content-Type": "application/json"},
                    ) as response:
                        result = await response.json()
                        print(f"  {test_req['name']}: {response.status} -> {result}")
            except Exception as e:
                print(f"  {test_req['name']}: ERROR - {str(e)}")


if __name__ == "__main__":
    print("Starting SSE Communication Tests...")
    print("Make sure all MCP servers are running before executing this test!")

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_comprehensive_tests())
        loop.run_until_complete(send_test_requests())
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
