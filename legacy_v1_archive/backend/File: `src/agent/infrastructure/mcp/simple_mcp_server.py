"""This module provides an implementation of the McpServer protocol using the MCP SDK."""

from typing import List

from mcp.server import Server

from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool


class SimpleMcpServer(McpServer):
    """A simple implementation of the McpServer protocol using the MCP SDK."""

    def __init__(self):
        """Initialize the SimpleMcpServer instance."""
        self._tools = {}
        self._server = Server()

    def register_tool(self, tool: McpTool) -> None:
        """Register a tool capability with the server.

        Args:
            tool: The defined McpTool containing metadata and handler.

        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        self._tools[tool.name] = tool
        self._server.register_tool(tool.name, tool.handler, tool.input_schema)

    def list_tools(self) -> List[McpTool]:
        """Return a list of currently registered tools.

        Returns:
            List[McpTool]: A list of registered McpTool instances.
        """
        return list(self._tools.values())

    async def start(self) -> None:
        """Start the MCP server (e.g., over Stdio or SSE)."""
        await self._server.start()
