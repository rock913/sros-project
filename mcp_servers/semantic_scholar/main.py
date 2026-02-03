"""
Main entry point for Semantic Scholar MCP Server
"""
import asyncio
import sys
import os

# Add the parent directory to the path so we can import from mcp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .server import SemanticScholarServer

async def main():
    """Main entry point."""
    server = SemanticScholarServer()
    await server.run(sys.stdin, sys.stdout)

if __name__ == "__main__":
    asyncio.run(main())