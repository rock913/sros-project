#!/usr/bin/env python3
"""
Context Ingester - Parses unstructured materials and injects into knowledge graph
"""
import json
import sys
import logging
import os
from pathlib import Path
from typing import Dict, Any, List
import asyncio
import re
from datetime import datetime

from .mcp_handler import ContextIngesterMCPHandler

logger = logging.getLogger(__name__)

def main_stdio():
    """Main entry point for stdio mode"""
    try:
        logger.info("Starting Context Ingester in stdio mode...")
        
        handler = ContextIngesterMCPHandler()
        
        # Initialize server
        init_result = handler.handle_request("initialize", {})
        if "error" in init_result:
            logger.error(f"Failed to initialize: {init_result['error']}")
            return 1
            
        logger.info("Context Ingester initialized successfully")
        
        # Handle MCP requests via stdin/stdout
        while True:
            line = sys.stdin.readline()
            if not line:
                break
                
            try:
                request = json.loads(line.strip())
                method = request.get("method", "")
                params = request.get("params", {})
                request_id = request.get("id")
                
                response = handler.handle_request(method, params)
                
                # Format response
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
                
                print(json.dumps(response_obj), flush=True)
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
                
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        return 1

def main():
    """Main entry point with mode selection"""
    import argparse
    parser = argparse.ArgumentParser(description="Context Ingester MCP Server")
    parser.add_argument("--mode", choices=["stdio", "sse"], default="stdio",
                       help="Communication mode")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8007)
    
    args = parser.parse_args()
    
    if args.mode == "sse":
        from ..common.sse_server import MCPSSEServer
        
        def sse_handler(method, params):
            handler = ContextIngesterMCPHandler()
            return handler.handle_request(method, params)
            
        server = MCPSSEServer(host=args.host, port=args.port, endpoint="/sse")
        server.register_handler(sse_handler)
        server.start()
    else:
        return main_stdio()

if __name__ == "__main__":
    sys.exit(main())