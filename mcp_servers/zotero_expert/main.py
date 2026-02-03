#!/usr/bin/env python3
"""
Main entry point for the Zotero Expert MCP Server
"""
import sys
import os
import logging

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_handler import ZoteroExpertMCPHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    handler = ZoteroExpertMCPHandler()
    
    # For now, just print capabilities
    result = handler.handle_request("initialize", {})
    print("Zotero Expert MCP Server")
    print("Capabilities:", result.get("result", {}).get("capabilities", {}))

if __name__ == "__main__":
    main()