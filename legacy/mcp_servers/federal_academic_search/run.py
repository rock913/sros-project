#!/usr/bin/env python3
"""
Runner script for Federal Academic Search MCP Server
"""
import sys
import os
import argparse
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.federal_academic_search.main import main as server_main

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Federal Academic Search MCP Server')
    parser.add_argument('--port', type=int, default=8001, help='Port to run server on')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Run server
    return server_main()

if __name__ == '__main__':
    sys.exit(main())