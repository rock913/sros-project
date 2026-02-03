#!/usr/bin/env python3
"""
Main entry point for the Zotero Expert MCP Server
"""
import sys
import os
import json
import asyncio
import logging

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .mcp_handler import ZoteroExpertMCPHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(port=None):
    """Main async function to handle MCP communication.
    
    Args:
        port (int, optional): Port number for the server. Defaults to None.
    """
    # For stdio MCP communication
    print("Zotero Expert MCP Server started", file=sys.stderr)
    sys.stderr.flush()
    
    # Example of handling a request
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        await demo_requests()
        return
    
    # Create handler instance
    handler = ZoteroExpertMCPHandler()
    
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
                response = handler.handle_request(method, params)
                
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

async def demo_requests():
    """Demonstrate handling of various requests."""
    print("Running demo requests...", file=sys.stderr)
    sys.stderr.flush()
    
    handler = ZoteroExpertMCPHandler()
    
    # Initialize request
    init_result = handler.handle_request("initialize", {})
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

if __name__ == "__main__":
    # Python 3.6 compatibility
    if hasattr(asyncio, 'run'):
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())