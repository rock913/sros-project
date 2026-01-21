"""
Implementation of the McpServer protocol using the 'fastmcp' library.
"""

from typing import List

from fastmcp import FastMCP  # Assuming this is the FastMCP library

from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool


class FastMcpServer(McpServer):
    """Adapter implementation of McpServer using the 'fastmcp' library."""

    def __init__(self, fastmcp_instance: FastMCP):
        """Initialize the FastMcpServer with a FastMCP instance.
        
        Args:
            fastmcp_instance: An instance of the FastMCP server.
        """
        self.fastmcp = fastmcp_instance
        self.tools = {}

    def register_tool(self, tool: McpTool) -> None:
        """Register a tool with the FastMCP server.
        
        Args:
            tool: The tool to be registered.
            
        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if tool.name in self.tools:
            raise ValueError(f"Tool with name {tool.name} already registered.")
        self.tools[tool.name] = tool
        self.fastmcp.add_tool(tool.name, tool.handler)

    def list_tools(self) -> List[McpTool]:
        """List all registered tools.
        
        Returns:
            A list of all registered tools.
        """
        return list(self.tools.values())

    async def start(self) -> None:
        """Start the FastMCP server."""
        await self.fastmcp.start()
