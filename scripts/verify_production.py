import argparse
import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from time import perf_counter

from mcp import ClientSession
from mcp.client.sse import sse_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ProdVerifier")


async def verify_gateway(port: int, query: str):
    """Verify the production gateway by connecting via SSE and running tools.

    This verifier targets the current SROS Gateway tool names:
    - manuscript.find_gaps
    - scholar.federated_search
    - memory.store_knowledge
    """
    logger.info("🔍 Connecting to SROS Gateway (SSE Mode)...")

    report = {
        "started_at": datetime.now().isoformat(),
        "port": port,
        "query": query,
        "ok": False,
        "tools": {
            "listed": [],
            "required": [
                "manuscript.find_gaps",
                "scholar.federated_search",
                "memory.store_knowledge",
            ],
            "missing": [],
        },
        "checks": [],
        "errors": [],
    }

    sse_url = f"http://localhost:{port}/sse"

    try:
        async with sse_client(sse_url) as (read, write):
            async with ClientSession(read, write) as session:
                t0 = perf_counter()
                await session.initialize()
                report["checks"].append({"name": "initialize", "ok": True, "duration_s": perf_counter() - t0})
                logger.info("✅ Connection Established & Initialized")

                logger.info("📋 Listing Tools...")
                t0 = perf_counter()
                tools_response = await session.list_tools()
                report["checks"].append({"name": "tools/list", "ok": True, "duration_s": perf_counter() - t0})

                tool_names = [t.name for t in tools_response.tools]
                report["tools"]["listed"] = tool_names
                logger.info(f"🛠️  Found {len(tool_names)} tools: {', '.join(tool_names)}")

                missing = [t for t in report["tools"]["required"] if t not in tool_names]
                report["tools"]["missing"] = missing
                if missing:
                    logger.error(f"❌ Missing critical tools: {missing}")
                    report["errors"].append({"stage": "tools/list", "message": f"Missing tools: {missing}"})
                    return False

                logger.info("✅ All core service tools detected.")

                logger.info("🧪 Testing Manuscript (manuscript.find_gaps)...")
                try:
                    t0 = perf_counter()
                    result = await session.call_tool("manuscript.find_gaps", {"file_path": "draft.md"})
                    content = result.content[0].text
                    gaps = json.loads(content)
                    if isinstance(gaps, list):
                        logger.info(f"✅ Gap analysis executed. Found {len(gaps)} gaps.")
                        report["checks"].append(
                            {
                                "name": "tool:manuscript.find_gaps",
                                "ok": True,
                                "duration_s": perf_counter() - t0,
                                "observations": {"gaps_count": len(gaps)},
                            }
                        )
                    else:
                        logger.warning(f"⚠️ Unexpected gaps format: {content[:120]}...")
                        report["checks"].append(
                            {
                                "name": "tool:manuscript.find_gaps",
                                "ok": True,
                                "duration_s": perf_counter() - t0,
                                "observations": {"unexpected_format": True},
                            }
                        )
                except Exception as e:
                    logger.error(f"❌ Manuscript test failed: {e}")
                    report["checks"].append({"name": "tool:manuscript.find_gaps", "ok": False, "error": str(e)})

                logger.info("🧪 Testing Scholar Federated Search (scholar.federated_search)...")
                try:
                    t0 = perf_counter()
                    search_res = await session.call_tool(
                        "scholar.federated_search",
                        {"query": query, "max_results": 3, "filters": {}},
                    )
                    content = search_res.content[0].text
                    results = json.loads(content)
                    if isinstance(results, list) and results:
                        logger.info(
                            f"✅ Search executed. Got {len(results)} results. First source={results[0].get('source')} title={results[0].get('title')}"
                        )
                        report["checks"].append(
                            {
                                "name": "tool:scholar.federated_search",
                                "ok": True,
                                "duration_s": perf_counter() - t0,
                                "observations": {
                                    "results_count": len(results),
                                    "first_source": results[0].get("source"),
                                    "first_title": results[0].get("title"),
                                },
                            }
                        )
                    else:
                        logger.warning(f"⚠️ Search returned no results or unexpected format: {content[:200]}")
                        report["checks"].append(
                            {
                                "name": "tool:scholar.federated_search",
                                "ok": True,
                                "duration_s": perf_counter() - t0,
                                "observations": {"empty_or_unexpected": True},
                            }
                        )
                except Exception as e:
                    logger.error(f"❌ Federal search failed: {e}")
                    report["checks"].append({"name": "tool:scholar.federated_search", "ok": False, "error": str(e)})

                logger.info("🧪 Testing Memory (memory.store_knowledge)...")
                try:
                    unique_title = f"Test Paper {datetime.now().isoformat()}"
                    t0 = perf_counter()
                    mem_res = await session.call_tool(
                        "memory.store_knowledge",
                        {
                            "nodes": [
                                {"id": "paper:verify", "type": "paper", "title": unique_title, "year": 2026},
                                {"id": "note:verify", "type": "note", "title": "prod-verify"},
                            ],
                            "edges": [
                                {
                                    "source": "note:verify",
                                    "target": "paper:verify",
                                    "relationship": "MENTIONS",
                                    "confidence": 0.5,
                                }
                            ],
                        },
                    )
                    logger.info(f"✅ Memory write executed. Result: {mem_res.content[0].text}")
                    report["checks"].append(
                        {
                            "name": "tool:memory.store_knowledge",
                            "ok": True,
                            "duration_s": perf_counter() - t0,
                        }
                    )
                except Exception as e:
                    logger.error(f"❌ Memory write failed: {e}")
                    report["checks"].append({"name": "tool:memory.store_knowledge", "ok": False, "error": str(e)})

                logger.info("🎉 Verification Complete!")
                report["ok"] = all(c.get("ok") for c in report["checks"])
                return report["ok"]

    except Exception as e:
        logger.error(f"🔥 Fatal Connection Error: {e}")
        report["errors"].append({"stage": "connect", "message": str(e)})
        return False
    finally:
        report["finished_at"] = datetime.now().isoformat()
        try:
            out_dir = Path("logs")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "production_verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
        except Exception as e:
            logger.warning(f"Failed to write JSON report: {e}")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", type=int, default=8000)
        parser.add_argument("--query", type=str, default="neuro ai")
        args = parser.parse_args()
        asyncio.run(verify_gateway(port=args.port, query=args.query))
    except KeyboardInterrupt:
        logger.info("Stopped by user")
