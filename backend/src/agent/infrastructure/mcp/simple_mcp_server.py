import asyncio
from typing import List, Any
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

from agent.domain.schemas.mcp import McpTool
from agent.domain.ports.mcp_server import McpServer

class SimpleMcpServer:
    """
    Adapter implementation of McpServer using the official 'mcp' Python SDK.
    """
    
    def __init__(self, name: str = "agent-mcp-server"):
        self.name = name
        # Initialize the underlying MCP SDK Server
        self._server = Server(name)
        self._registered_tools: dict[str, McpTool] = {}
        
        # Set up the internal handlers for the SDK
        self._setup_handlers()

    def _setup_handlers(self):
        """Configure the underlying MCP server handlers."""
        
        @self._server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.input_schema
                )
                for tool in self._registered_tools.values()
            ]

        @self._server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            if name not in self._registered_tools:
                raise ValueError(f"Tool {name} not found")
            
            tool = self._registered_tools[name]
            args = arguments or {}
            
            try:
                # Execute the tool's handler
                # Support both sync and async handlers
                if asyncio.iscoroutinefunction(tool.handler):
                    result = await tool.handler(**args)
                else:
                    result = tool.handler(**args)
                
                # Convert result to MCP content format (assuming text for now)
                return [types.TextContent(type="text", text=str(result))]
                
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]

    def register_tool(self, tool: McpTool) -> None:
        """
        Register a tool capability with the server.
        """
        if tool.name in self._registered_tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        
        self._registered_tools[tool.name] = tool

    def list_tools(self) -> List[McpTool]:
        """
        Return a list of currently registered tools.
        """
        return list(self._registered_tools.values())

    async def start(self) -> None:
        """
        Start the MCP server over Stdio.
        """
        # Read from stdin and write to stdout
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self._server.run(
                read_stream,
                write_stream,
                self._server.create_initialization_options()
            )
