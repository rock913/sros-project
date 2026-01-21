from typing import List
from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool
from fastmcp import FastMCP  # Assuming this is the FastMCP library

class FastMcpServer(McpServer):
    """
    Adapter implementation of McpServer using the 'fastmcp' library.
    """

    def __init__(self, fastmcp_instance: FastMCP):
        self.fastmcp = fastmcp_instance
        self.tools = {}

    def register_tool(self, tool: McpTool) -> None:
        if tool.name in self.tools:
            raise ValueError(f"Tool with name {tool.name} already registered.")
        self.tools[tool.name] = tool
        self.fastmcp.add_tool(tool.name, tool.handler)

    def list_tools(self) -> List[McpTool]:
        return list(self.tools.values())

    async def start(self) -> None:
        await self.fastmcp.start()
