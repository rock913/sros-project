from fastapi import FastAPI
from typing import List, Dict, Any
from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool

class FastAPIMcpServer(McpServer):
    """MCP server implementation using FastAPI."""

    def __init__(self, app: FastAPI, mcp_schema: str):
        self.app = app
        self.mcp_schema = mcp_schema
        self.tools: Dict[str, McpTool] = {}

    def register_tool(self, tool: McpTool) -> None:
        if tool.name in self.tools:
            raise ValueError(f"Tool with name {tool.name} already registered.")
        self.tools[tool.name] = tool

    def list_tools(self) -> List[McpTool]:
        return list(self.tools.values())

    async def start(self) -> None:
        @self.app.post("/execute/{tool_name}")
        async def execute_tool(tool_name: str, input_data: Dict[str, Any]):
            tool = self.tools.get(tool_name)
            if not tool:
                return {"error": "Tool not found"}
            return tool.handler(**input_data)

        # Start the FastAPI application
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8001)
