#!/usr/bin/env python3
"""
Base SSE Server for MCP communication
Provides HTTP-based Server-Sent Events communication for MCP servers
"""

import asyncio
import json
import logging
from typing import Dict, Any, Callable, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import uvicorn
import time

logger = logging.getLogger(__name__)

class MCPSSEServer:
    """Base class for MCP servers using Server-Sent Events"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, endpoint: str = "/sse"):
        """
        Initialize the SSE server
        
        Args:
            host: Host to bind to
            port: Port to listen on
            endpoint: HTTP endpoint for SSE events (default: /sse)
        """
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.app = FastAPI()
        self.request_handler: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None
        self.running = False
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP routes for the server"""
        
        @self.app.post(self.endpoint)
        async def handle_mcp_request(request: Request):
            """Handle MCP JSON-RPC requests via HTTP POST"""
            try:
                logger.info(f"POST request received on {self.endpoint} endpoint")
                body = await request.json()
                
                method = body.get("method", "")
                params = body.get("params", {})
                request_id = body.get("id")
                
                # Handle the request using the registered handler
                if self.request_handler:
                    logger.info(f"Processing MCP request: {method} from {request.client.host if hasattr(request, 'client') else 'unknown'}")
                    # Run the synchronous handler in an executor to avoid blocking the async event loop
                    # This is crucial for initialization tasks or long-running operations
                    response = await asyncio.get_event_loop().run_in_executor(
                        None,
                        self.request_handler,
                        method,
                        params
                    )
                    logger.info(f"Completed MCP request: {method}")
                    
                    # Format response according to JSON-RPC spec
                    if "result" in response:
                        result = response["result"]
                        response_obj = {
                            "jsonrpc": "2.0",
                            "result": result,
                            "id": request_id
                        }
                    elif "error" in response:
                        response_obj = {
                            "jsonrpc": "2.0",
                            "error": response["error"],
                            "id": request_id
                        }
                    else:
                        response_obj = {
                            "jsonrpc": "2.0",
                            "result": response,
                            "id": request_id
                        }
                    
                    logger.info(f"Sending response for {method}: {response_obj}")
                    return response_obj
                else:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": "Method not found - no handler registered"
                        },
                        "id": request_id
                    }
                    logger.warning(f"No handler registered for request: {method}")
                    return error_response
                    
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    },
                    "id": None
                }
                logger.error(f"JSON decode error in POST request: {e}")
                return error_response
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    },
                    "id": None
                }
                logger.error(f"MCP request error: {e}")
                return error_response
        
        @self.app.get(self.endpoint)
        async def handle_sse_stream(request: Request):
            """Handle SSE streaming for real-time events"""
            
            async def event_generator():
                """Generate SSE events"""
                try:
                    # Send immediate endpoint discovery event to help clients like Roo Code
                    # This ensures that even if Roo Code connects late or misses the initial event,
                    # it gets the endpoint information right away
                    endpoint_info = {
                        "type": "endpoint_discovery",
                        "endpoints": {
                            "messages": self.endpoint,  # This is where JSON-RPC should go (same endpoint)
                            "sse": self.endpoint,
                            "health": "/health"
                        },
                        "capabilities": ["json-rpc", "sse", "streaming"],
                        "version": "2.0"
                    }
                    yield f"data: {json.dumps(endpoint_info)}\n\n"
                    
                    # Send initial connection event
                    yield f"data: {json.dumps({'type': 'connected', 'timestamp': time.time()})}\n\n"
                    
                    # Send endpoint discovery event immediately to help clients like Roo Code
                    endpoint_info = {
                        "type": "endpoint_discovery",
                        "endpoints": {
                            "messages": self.endpoint,  # This is where JSON-RPC should go (same endpoint)
                            "sse": self.endpoint,
                            "health": "/health"
                        },
                        "capabilities": ["json-rpc", "sse", "streaming"],
                        "version": "2.0"
                    }
                    yield f"data: {json.dumps(endpoint_info)}\n\n"
                    
                    # Keep connection alive and send periodic heartbeat
                    while self.running:
                        await asyncio.sleep(30)  # Heartbeat every 30 seconds
                        yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': time.time()})}\n\n"
                        
                except asyncio.CancelledError:
                    logger.info("SSE connection cancelled")
                    yield f"data: {json.dumps({'type': 'disconnected', 'timestamp': time.time()})}\n\n"
                except Exception as e:
                    logger.error(f"SSE stream error: {e}")
                    yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'timestamp': time.time()})}\n\n"
            
            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                }
            )
    
    def register_handler(self, handler: Callable[[str, Dict[str, Any]], Dict[str, Any]]):
        """Register the request handler function
        
        Args:
            handler: Function that takes (method, params) and returns response dict
        """
        self.request_handler = handler
    
    def start(self, host: str = None, port: int = None):
        """Start the HTTP server
        
        Args:
            host: Override host (uses default if None)
            port: Override port (uses default if None)
        """
        start_host = host or self.host
        start_port = port or self.port
        
        logger.info(f"Starting MCP SSE Server on {start_host}:{start_port}{self.endpoint}")
        
        self.running = True
        uvicorn.run(
            self.app,
            host=start_host,
            port=start_port,
            log_level="info",
            timeout_keep_alive=300
        )
    
    async def start_async(self, host: str = None, port: int = None):
        """Start the HTTP server asynchronously
        
        Args:
            host: Override host (uses default if None)
            port: Override port (uses default if None)
        """
        start_host = host or self.host
        start_port = port or self.port
        
        logger.info(f"Starting MCP SSE Server on {start_host}:{start_port}{self.endpoint}")
        
        self.running = True
        config = uvicorn.Config(
            self.app,
            host=start_host,
            port=start_port,
            log_level="info",
            timeout_keep_alive=300
        )
        server = uvicorn.Server(config)
        await server.serve()

# Example usage and testing
if __name__ == "__main__":
    # Example handler function
    def example_handler(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Example request handler"""
        if method == "initialize":
            return {
                "result": {
                    "capabilities": {
                        "methods": ["initialize", "shutdown", "example_method"],
                        "version": "1.0.0"
                    }
                }
            }
        elif method == "example_method":
            return {"result": {"message": "Hello from SSE server!", "params": params}}
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
    
    # Create and configure server
    server = MCPSSEServer(host="127.0.0.1", port=8004, endpoint="/sse")
    server.register_handler(example_handler)
    
    # Start server
    server.start()