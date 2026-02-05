#!/usr/bin/env python3
"""
SROS Gateway - MCP Aggregation Server (Production Mode)
"""
import asyncio
import json
import os
import sys
import logging
import uvicorn
from typing import Dict, Any

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [Gateway] %(message)s')
logger = logging.getLogger("SROS-Gateway")

# --- Production Imports (No Mocks) ---
# This will Fail Fast if dependencies are missing, as requested.
try:
    from mcp.server import Server
    from mcp.server.sse import SseServerTransport
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError as e:
    logger.critical(f"❌ CRITICAL DEPS MISSING: {e}")
    logger.critical("Please install 'mcp' library: pip install mcp")
    sys.exit(1)

try:
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount
    from starlette.requests import Request
    from starlette.responses import Response, JSONResponse
except ImportError as e:
    logger.critical(f"❌ CRITICAL DEPS MISSING: {e}")
    logger.critical("Please install 'starlette': pip install starlette")
    sys.exit(1)

# --- Global State ---
clients: Dict[str, Any] = {} # Connected sub-server sessions
tools_registry: Dict[str, Any] = {} # Local registry of tool wrappers
GATEWAY_READY = False

# --- MCP Server Instance ---
app_server = Server("SROS Gateway")

# --- Tools Aggregation ---
@app_server.list_tools()
async def list_tools() -> list[Tool]:
    """List tools from all connected sub-servers."""
    return list(tools_registry.values())

@app_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch tool calls to appropriate sub-server."""
    # Find which server owns this tool (naming convention: server_tool)
    parts = name.split("_", 1)
    if len(parts) < 2:
        raise ValueError(f"Invalid tool name format: {name}")
    
    server_name = parts[0]
    original_tool_name = parts[1]
    
    session = clients.get(server_name)
    if not session:
        # Try to reconnect or fail
        raise RuntimeError(f"Server {server_name} is not connected")
        
    logger.info(f"🔄 Dispatching {name} -> {server_name}:{original_tool_name}")
    try:
        result = await session.call_tool(original_tool_name, arguments=arguments)
        # Normalize result to list of TextContent
        return result.content
    except Exception as e:
        logger.error(f"❌ Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

# --- Connection Logic ---
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def register_tool_wrapper_real(server_name: str, tool_schema: Any):
    """Register a tool definition in our local registry."""
    new_name = f"{server_name}_{tool_schema.name}"
    try:
        # Create a new Tool object with the prefixed name
        new_tool = Tool(
            name=new_name,
            description=f"[{server_name}] {tool_schema.description or ''}",
            inputSchema=tool_schema.inputSchema
        )
        tools_registry[new_name] = new_tool
    except Exception as e:
        logger.error(f"⚠️ Failed to register tool {new_name}: {e}")

async def connect_to_server(name: str, config: Dict[str, Any]):
    """Connect to a sub-server via stdio."""
    cmd = config["command"]
    args = config["args"]
    if "--mode" not in args:
        args.extend(["--mode", "stdio"])

    # Ensure environment variables are strings
    env_config = config.get("env", {})
    env = os.environ.copy()
    for k, v in env_config.items():
        env[str(k)] = str(v)

    server_params = StdioServerParameters(
        command=cmd,
        args=args,
        env=env
    )

    logger.info(f"🔌 Connecting to {name}...")
    try:
        # Properly handle async context managers manually to keep connection alive
        # 1. Start stdio client
        stdio_cm = stdio_client(server_params)
        read, write = await stdio_cm.__aenter__()
        
        # 2. Start ClientSession
        session_cm = ClientSession(read, write)
        session = await session_cm.__aenter__()
        
        # Setting timeout for initialization
        await asyncio.wait_for(session.initialize(), timeout=10.0)
        
        # Store session and context managers to prevent them from closing
        # We attach them to the session object or a separate registry to keep references
        session._flask_stdio_cm = stdio_cm
        session._flask_session_cm = session_cm
        
        clients[name] = session
        
        # Ingest tools with timeout protection
        try:
             # Just getting tool list, should be fast if server is initialized
             tools = await asyncio.wait_for(session.list_tools(), timeout=5.0)
             for tool in tools.tools:
                 register_tool_wrapper_real(name, tool)
        except asyncio.TimeoutError:
             logger.warning(f"⚠️ Timeout fetching tools from {name}, but session initialized.")
            
        logger.info(f"✅ {name} ready.")
        return True
    except asyncio.TimeoutError:
         logger.error(f"❌ Timeout connecting to {name}")
         return False
    except Exception as e:
        logger.error(f"❌ Failed to connect to {name}: {e}")
        return False

# --- HTTP Routes ---

sse = SseServerTransport("/messages")

class McpConnectionResponse:
    """
    Custom ASGI Response that wraps the MCP Connection loop.
    Mimics Starlette Response interface but handles raw ASGI.
    """
    def __init__(self, transport: SseServerTransport, server: Server):
        self.transport = transport
        self.server = server
        self.status_code = 200  

    async def __call__(self, scope, receive, send):
        try:
             async with self.transport.connect_sse(scope, receive, send) as streams:
                # create_initialization_options is synchronous in mcp>=1.0.0
                init_opts = self.server.create_initialization_options()
                await self.server.run(streams[0], streams[1], init_opts)
        except Exception as e:
            logger.error(f"❌ Connection Error: {e}", exc_info=True)

class McpMessageResponse:
    """Wraps MCP's handle_post_message"""
    def __init__(self, transport: SseServerTransport):
        self.transport = transport
        self.status_code = 200
    
    async def __call__(self, scope, receive, send):
        await self.transport.handle_post_message(scope, receive, send)

async def handle_sse_request(request: Request):
    """
    GET /sse -> Establishes SSE Connection
    POST /sse -> Fallback for clients sending messages to the wrong endpoint
    """
    if request.method == "POST":
        logger.info("🔀 Redirecting POST /sse to /messages (Response Layer)")
        return McpMessageResponse(sse)
    
    # GET: Return the streaming response
    return McpConnectionResponse(sse, app_server)

async def handle_messages(request: Request):
    """POST /messages: Handle JSON-RPC messages."""
    return McpMessageResponse(sse)

async def health_check_endpoint(request: Request):
    """GET /health: System status."""
    status = {
        "status": "healthy" if GATEWAY_READY else "starting",
        "ready": GATEWAY_READY,
        "connected_servers": list(clients.keys()),
        "tool_count": len(tools_registry)
    }
    return JSONResponse(status)

# --- Main App Construction ---

routes = [
    Route("/messages", endpoint=handle_messages, methods=["POST"]),
    Route("/health", endpoint=health_check_endpoint, methods=["GET"]),
    Route("/sse", endpoint=handle_sse_request, methods=["GET", "POST"]), 
]

starlette_app = Starlette(routes=routes)

async def main():
    global GATEWAY_READY
    config = load_config()
    
    # Boot sub-processes
    logger.info("🚀 Gateway booting up (PRODUCTION MODE)...")
    results = await asyncio.gather(*[
        connect_to_server(name, cfg) 
        for name, cfg in config["servers"].items()
    ])
    
    GATEWAY_READY = True
    success_count = sum(1 for r in results if r)
    logger.info(f"🌟 Gateway ready. Connected to {success_count} servers.")
    logger.info(f"🌍 Starting Gateway at http://0.0.0.0:8000")
    
    # Start Uvicorn
    config = uvicorn.Config(
        starlette_app, 
        host="0.0.0.0", 
        port=8000, 
        log_level="info",
        timeout_keep_alive=600
    )
    server = uvicorn.Server(config)
    await server.serve()

def run_main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Gateway stopping...")

if __name__ == "__main__":
    run_main()
