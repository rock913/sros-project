"""
Module for creating an MCP tool to search for academic papers on arXiv.
"""

from agent.infrastructure.mcp.base import McpTool
from pydantic import BaseModel

from agent.infrastructure.tools.arxiv_adapter import ArxivAdapter

class ArxivSearchInput(BaseModel):
    """
    Input schema for the arXiv search MCP tool.
    """
    query: str
    max_results: int = 5

def get_arxiv_search_mcp_tool() -> McpTool:
    """
    Create and return an MCP tool for searching academic papers on arXiv.
    """
    adapter = ArxivAdapter()
    
    async def handler(input_data: ArxivSearchInput) -> list:
        results = adapter.search(input_data.query, input_data.max_results)
        return [result.dict() for result in results]
    
    return McpTool(
        name="arxiv-search",
        description="Search for academic papers on arXiv",
        input_schema=ArxivSearchInput,
        handler=handler
    )
