from typing import Any, Dict, List

from fastapi import FastAPI

from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool


class FastAPIMcpServerAdapter(McpServer):
    """Adapter for integrating MCP server functionality with a FastAPI application.
    """

    def __init__(self, app: FastAPI):
        """Initialize the FastAPIMcpServerAdapter.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.app = app
        self.tools: Dict[str, McpTool] = {}

    def register_tool(self, tool: McpTool) -> None:
        """Register a tool with the MCP server.

        Args:
            tool (McpTool): The tool to register.

        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if tool.name in self.tools:
            raise ValueError(f"Tool with name {tool.name} already registered.")
        self.tools[tool.name] = tool

    def list_tools(self) -> List[McpTool]:
        """List all registered tools.

        Returns:
            List[McpTool]: A list of all registered tools.
        """
        return list(self.tools.values())

    async def start(self) -> None:
        """Start the MCP server and register the execute_tool endpoint.
        """
        @self.app.post("/execute/{tool_name}")
        async def execute_tool(tool_name: str, input_data: Dict[str, Any]):
            tool = self.tools.get(tool_name)
            if not tool:
                return {"error": "Tool not found"}
            return tool.handler(**input_data)

        # Start the FastAPI application
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
