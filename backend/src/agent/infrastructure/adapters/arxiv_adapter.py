"""
Module for the ArxivAdapter, which is used to search for academic papers on Arxiv.
"""

from typing import List

from agent.domain.ports.paper_searcher import PaperSearcher
from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.paper import Paper


class ArxivAdapter(PaperSearcher):
    """Adapter for searching academic papers on Arxiv."""

    def search(self, query: str, max_results: int = 5) -> List[Paper]:
        """Search for academic papers on Arxiv.

        Args:
            query: The search string.
            max_results: Maximum number of papers to return.

        Returns:
            List[Paper]: List of domain model Paper objects.
        """
        # Implementation will go here
        pass

def get_tool() -> McpTool:
    """Get the MCP tool for Arxiv search.

    Returns:
        McpTool: The MCP tool for Arxiv search.
    """
    return McpTool(
        name="arxiv_search",
        description="Search for academic papers on Arxiv",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        },
        handler=ArxivAdapter().search
    )
