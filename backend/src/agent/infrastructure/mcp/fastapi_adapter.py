from typing import Any, Dict, List
import uvicorn  # 导入 uvicorn 模块
from contextlib import asynccontextmanager

from fastapi import FastAPI
from agent.infrastructure.mcp.fastapi_mcp_server import FastAPIMcpServer

from agent.domain.ports.mcp_server import McpServer
from agent.domain.schemas.mcp import McpTool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mcp_server.start()
    yield
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)  # 创建 FastAPI 应用实例

# 定义 MCP Schema
mcp_schema = """
{
  "name": "auto-researcher-mcp",
  "description": "MCP server for Auto-Researcher",
  "version": "1.0.0",
  "tools": []
}
"""

mcp_server = FastAPIMcpServer(app, mcp_schema)  # 初始化 MCP 服务器

# 注册示例工具
def example_tool(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return {"result": "Example tool executed successfully"}

# 手动创建 McpTool 对象并注册
example_tool_mcp = McpTool(
    name="example_tool",
    description="An example tool for demonstration purposes",
    input_schema={
        "type": "object",
        "properties": {
            "input_data": {
                "type": "object",
                "description": "The input data for the tool"
            }
        },
        "required": ["input_data"]
    },
    handler=example_tool
)

mcp_server.register_tool(example_tool_mcp)

@app.get("/")
async def root():
    return {"message": "Hello, MCP!"}

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
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
