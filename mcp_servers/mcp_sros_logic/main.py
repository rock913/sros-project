#!/usr/bin/env python3
"""
Main entry point for the SROS Logic MCP Server.
This server implements custom SROS logic and workflow management.
Supports both stdio and SSE modes
"""
import sys
import json
import asyncio
import argparse
from .mcp_handler import handle_mcp_request, get_handler
from ..common.sse_server import MCPSSEServer
import logging

# Ensure logging is configured
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main_stdio(port=None):
    """Main async function to handle MCP communication via stdio.
    
    Args:
        port (int, optional): Port number for the server. Defaults to None.
    """
    # For stdio MCP communication
    print("SROS Logic MCP Server started", file=sys.stderr)
    sys.stderr.flush()
    
    # Example of handling a request
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        await demo_requests()
        return
    
    # Handle MCP requests via stdin/stdout
    try:
        while True:
            # Read JSON-RPC request from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            try:
                request = json.loads(line.strip())
                method = request.get("method", "")
                params = request.get("params", {})
                
                # Handle the request
                response = handle_mcp_request(method, params)
                
                # Extract result/error from response
                if "result" in response:
                    result = response["result"]
                    response_obj = {
                        "jsonrpc": "2.0",
                        "result": result,
                        "id": request.get("id")
                    }
                elif "error" in response:
                    response_obj = {
                        "jsonrpc": "2.0",
                        "error": response["error"],
                        "id": request.get("id")
                    }
                else:
                    response_obj = {
                        "jsonrpc": "2.0",
                        "result": response,
                        "id": request.get("id")
                    }
                
                print(json.dumps(response_obj), flush=True)
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    },
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    },
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.stderr.flush()

def main_sse(host="127.0.0.1", port=8006):
    """Main function to handle MCP communication via SSE.
    
    Args:
        host (str): Host to bind to
        port (int): Port to listen on
    """
    def sse_handler(method, params):
        """Handle MCP requests via SSE"""
        try:
            # Call the existing MCP handler
            response = handle_mcp_request(method, params)
            return response
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    # Create the SSE server
    server = MCPSSEServer(host=host, port=port, endpoint="/sse")
    server.register_handler(sse_handler)
    
    # Pre-initialize handler to avoid first-request timeout
    logger.info("Pre-initializing SROS Logic handler...")
    get_handler()
    logger.info("SROS Logic handler initialized")

    # Start the server
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server shutdown requested by user")

async def demo_requests():
    """Demonstrate handling of various requests."""
    print("Running demo requests...", file=sys.stderr)
    sys.stderr.flush()
    
    # Initialize request
    init_result = handle_mcp_request("initialize", {})
    if "result" in init_result:
        result = init_result["result"]
    else:
        result = init_result
        
    response_obj = {
        "jsonrpc": "2.0",
        "result": result,
        "id": 1
    }
    print(json.dumps(response_obj), flush=True)

def main():
    """Main entry point with mode selection."""
    parser = argparse.ArgumentParser(description="SROS Logic MCP Server")
    parser.add_argument("--mode", choices=["stdio", "sse"], default="stdio",
                       help="Communication mode (stdio or sse)")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                       help="Host for SSE mode (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8006,
                       help="Port for SSE mode (default: 8006)")
    
    args = parser.parse_args()
    
    if args.mode == "sse":
        main_sse(host=args.host, port=args.port)
    else:
        # Python 3.6 compatibility for stdio mode
        if hasattr(asyncio, 'run'):
            asyncio.run(main_stdio())
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main_stdio())

if __name__ == "__main__":
    main()