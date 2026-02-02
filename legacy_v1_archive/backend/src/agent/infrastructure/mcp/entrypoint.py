"""Entry point for the MCP Server."""

import asyncio
import sys

from agent.infrastructure.mcp.simple_mcp_server import SimpleMcpServer
# Temporarily disabled due to Phase 4.2 migration issues
# from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool
# from agent.infrastructure.mcp.tools.orchestrator import get_orchestrator_mcp_tool
# from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool
# from agent.infrastructure.mcp.tools.zotero import get_zotero_save_mcp_tool


async def main():
    """Initialize and start the MCP Server."""
    print("MCP server starting...") # Print immediately to satisfy extension

    # 1. Initialize Server
    try:
        server = SimpleMcpServer(name="gemini-research-agent")
        print("✓ MCP server initialized successfully")  # Signal extension we're ready
    except Exception as e:
        print(f"MCP server initialization error: {e}")
        return  # Exit gracefully

    # 2. Register Tools (disabled during Phase 4.2 migration)
    print("✓ MCP server ready - no tools available during Phase 4.2 migration")

    # Tools disabled due to import errors in hexagonal architecture
    # print("Registering MCP tools...")
    # tools_to_register = [
    #     ("unpaywall", get_unpaywall_mcp_tool),
    #     ("arxiv", get_arxiv_search_mcp_tool),
    #     ("zotero", get_zotero_save_mcp_tool),
    #     ("orchestrator", get_orchestrator_mcp_tool),
    # ]

    # for tool_name, get_tool_func in tools_to_register:
    #     try:
    #         tool = get_tool_func()
    #         server.register_tool(tool)
    #         print(f"✓ Registered {tool_name} tool")
    #     except Exception as e:
    #         print(f"✗ Failed to register {tool_name} tool: {e}")
    #         # Continue with other tools rather than crashing

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
