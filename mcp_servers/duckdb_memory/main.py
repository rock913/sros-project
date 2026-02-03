#!/usr/bin/env python3
"""
Main entry point for DuckDB Memory MCP Server
"""

import sys
import json
import asyncio
from .mcp_handler import handle_mcp_request

async def main():
    """Main async function to handle MCP communication."""
    # In a real implementation, this would handle stdin/stdout communication
    # For now, we'll just demonstrate the handler
    
    print("DuckDB Memory MCP Server started", file=sys.stderr)
    
    # Example of handling a request
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_requests()
    
    # In a real MCP server, you would read from stdin and write to stdout
    # This is a simplified example
    
async def demo_requests():
    """Demonstrate handling of various requests."""
    print("Running demo requests...", file=sys.stderr)
    
    # Initialize request
    init_result = handle_mcp_request("initialize", {})
    print(f"Initialize result: {json.dumps(init_result, indent=2)}")
    
    # Create a paper
    paper_params = {
        "title": "Example Paper",
        "authors": "John Doe, Jane Smith",
        "year": 2023,
        "venue": "Example Conference",
        "doi": "10.1234/example.2023",
        "abstract": "This is an example paper abstract.",
        "citation_key": "doe2023example"
    }
    paper_result = handle_mcp_request("create_paper", paper_params)
    print(f"Create paper result: {json.dumps(paper_result, indent=2)}")
    
    if "result" in paper_result and "id" in paper_result["result"]:
        paper_id = paper_result["result"]["id"]
        
        # Get the paper
        get_params = {"id": paper_id}
        get_result = handle_mcp_request("get_paper", get_params)
        print(f"Get paper result: {json.dumps(get_result, indent=2)}")
        
        # Update the paper
        update_params = {
            "id": paper_id,
            "abstract": "This is an updated example paper abstract."
        }
        update_result = handle_mcp_request("update_paper", update_params)
        print(f"Update paper result: {json.dumps(update_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())