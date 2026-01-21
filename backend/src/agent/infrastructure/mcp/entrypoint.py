import asyncio
import sys

from agent.infrastructure.mcp.simple_mcp_server import SimpleMcpServer
from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool
from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool


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
    except Exception as e:
        print(f"Failed to register tool: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Start Server
    print("MCP Server starting on Stdio...", file=sys.stderr)
    try:
        await server.start()
    except Exception as e:
        print(f"Server crashed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
