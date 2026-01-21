"""Entry point for the MCP Server."""

import asyncio
import sys

from agent.infrastructure.mcp.simple_mcp_server import SimpleMcpServer
from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool
from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool
from agent.infrastructure.mcp.tools.zotero import ZoteroMCPTool


async def main():
    """Initialize and start the MCP Server."""
    # 1. Initialize Server
    server = SimpleMcpServer(name="gemini-research-agent")

    # 2. Register Tools
    try:
        unpaywall_tool = get_unpaywall_mcp_tool()
        server.register_tool(unpaywall_tool)
        
        arxiv_search_tool = get_arxiv_search_mcp_tool()
        server.register_tool(arxiv_search_tool)
        
        zotero_tool = ZoteroMCPTool()
        server.register_tool(zotero_tool)
    except Exception as e:
        sys.exit(f"Failed to register tool: {e}")

    # 3. Start Server
    try:
        await server.start()
    except Exception as e:
        sys.exit(f"Server crashed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit("Server stopped by user")
