#!/usr/bin/env python3
"""
SSE Main entry point for Manuscript Manager MCP Server
"""

import sys
import json
import logging
from typing import Dict, Any
import argparse

from .mcp_handler import handle_mcp_request
from ..common.sse_server import MCPSSEServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_sse_handler():
    """Create the SSE request handler for manuscript manager"""
    def sse_handler(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests via SSE"""
        try:
            # Call the existing MCP handler
            response = handle_mcp_request(method, params)
            return response
        except Exception as e:
            logger.error(f"Error handling request {method}: {e}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    return sse_handler

def main(host: str = "127.0.0.1", port: int = 8004):
    """Main function to start the SSE server"""
    logger.info("Starting Manuscript Manager MCP Server in SSE mode...")
    
    # Create the SSE server
    server = MCPSSEServer(host=host, port=port, endpoint="/sse")
    
    # Register the request handler
    handler = create_sse_handler()
    server.register_handler(handler)
    
    logger.info(f"Manuscript Manager MCP Server listening on {host}:{port}/sse")
    
    # Start the server
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manuscript Manager MCP Server (SSE)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8004, help="Port to listen on")
    
    args = parser.parse_args()
    
    sys.exit(main(host=args.host, port=args.port))