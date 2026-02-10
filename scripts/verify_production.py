import asyncio
import json
import logging
from datetime import datetime

from mcp import ClientSession
from mcp.client.sse import sse_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ProdVerifier")


async def verify_gateway():
    """Verify the production gateway by connecting via SSE and running tools."""
    logger.info("🔍 Connecting to SROS Gateway (SSE Mode)...")

    sse_url = "http://localhost:8000/sse"

    try:
        async with sse_client(sse_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                logger.info("✅ Connection Established & Initialized")

                logger.info("📋 Listing Tools...")
                tools_response = await session.list_tools()

                tool_names = [t.name for t in tools_response.tools]
                logger.info(f"🛠️  Found {len(tool_names)} tools: {', '.join(tool_names)}")

                required_tools = [
                    "federal_search_papers",
                    "manuscript_get_structure",
                    "memory_create_paper",
                ]

                missing = [t for t in required_tools if t not in tool_names]
                if missing:
                    logger.error(f"❌ Missing critical tools: {missing}")
                    return False

                logger.info("✅ All core service tools detected.")

                logger.info("🧪 Testing Manuscript Manager (manuscript_get_structure)...")
                try:
                    result = await session.call_tool("manuscript_get_structure", {})
                    content = result.content[0].text
                    structure = json.loads(content)
                    if "headers" in structure:
                        logger.info(
                            f"✅ Manuscript structure retrieved. Found {len(structure['headers'])} headers."
                        )
                    else:
                        logger.warning(f"⚠️ Unexpected structure format: {content[:100]}...")
                except Exception as e:
                    logger.error(f"❌ Manuscript test failed: {e}")

                logger.info("🧪 Testing Federal Search (federal_search_papers)...")
                try:
                    search_res = await session.call_tool(
                        "federal_search_papers",
                        {"query": "SROS: Scholarly Research Operating System", "limit": 1},
                    )
                    content = search_res.content[0].text
                    logger.info(f"✅ Search executed. Response length: {len(content)} chars.")
                    logger.debug(f"Response snippet: {content[:200]}")
                except Exception as e:
                    logger.error(f"❌ Federal search failed: {e}")

                logger.info("🧪 Testing Memory (memory_create_paper)...")
                try:
                    unique_title = f"Test Paper {datetime.now().isoformat()}"
                    mem_res = await session.call_tool(
                        "memory_create_paper",
                        {
                            "title": unique_title,
                            "abstract": "Test abstract for production verification.",
                            "year": 2026,
                        },
                    )
                    logger.info(f"✅ Memory write executed. Result: {mem_res.content[0].text}")
                except Exception as e:
                    logger.error(f"❌ Memory write failed: {e}")

                logger.info("🎉 Verification Complete!")
                return True

    except Exception as e:
        logger.error(f"🔥 Fatal Connection Error: {e}")
        return False


if __name__ == "__main__":
    try:
        asyncio.run(verify_gateway())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
