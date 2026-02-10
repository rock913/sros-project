import asyncio
import httpx

# 配置你要测试的端口
TARGET_PORTS = [8001, 8002, 8003, 8004, 8005, 8006]


async def check_server_health(port):
    base_url = f"http://127.0.0.1:{port}"
    print(f"\n--- Diagnosing Server at {base_url} ---")

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            print("[1] Pinging SSE endpoint...")
            async with client.stream(
                "GET", f"{base_url}/sse", headers={"Accept": "text/event-stream"}
            ) as resp:
                if resp.status_code == 200:
                    print("    ✅ SSE Endpoint is UP (Status 200)")
                else:
                    print(f"    ❌ SSE Endpoint returned {resp.status_code}")
                    return

            print("[2] Sending JSON-RPC initialize...")
            payload = {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "debug-script", "version": "1.0"},
                },
                "id": 1,
            }

            rpc_resp = await client.post(f"{base_url}/sse", json=payload)

            if rpc_resp.status_code == 200:
                print(f"    ✅ JSON-RPC Response: {rpc_resp.text[:100]}...")
            else:
                print(f"    ❌ JSON-RPC Failed: {rpc_resp.status_code} - {rpc_resp.text}")

        except httpx.ConnectError:
            print("    ❌ Connection Refused (Server not running?)")
        except httpx.ReadTimeout:
            print("    ❌ Read Timeout (Server hung?)")
        except Exception as e:
            print(f"    ❌ Error: {e}")


async def main():
    print("Starting Diagnosis... ensuring servers are running first.")
    tasks = [check_server_health(p) for p in TARGET_PORTS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
