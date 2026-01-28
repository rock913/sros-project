"""Module for creating an MCP tool to search for academic papers on arXiv."""

from pydantic import BaseModel

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.tools.arxiv_adapter import ArxivAdapter
from typing import List
from agent.domain.ports.paper_searcher import PaperSearcherPort
from agent.domain.schemas.paper import Paper



class ArxivSearchInput(BaseModel):
    """Input schema for the arXiv search MCP tool."""
    query: str
    max_results: int = 5

def get_arxiv_search_mcp_tool() -> McpTool:
    """Create and return an MCP tool for searching academic papers on arXiv."""
    adapter = ArxivAdapter()
    
    async def handler(input_data: dict | ArxivSearchInput) -> list:
        # Ensure input_data is an instance of ArxivSearchInput
        if isinstance(input_data, dict):
            input_data = ArxivSearchInput(**input_data)
        
        results = adapter.search(input_data.query, input_data.max_results)
        return [result.dict() for result in results]
    
    return McpTool(
        name="arxiv-search",
        description="Search for academic papers on arXiv",
        input_schema=ArxivSearchInput.model_json_schema(),
        handler=handler
    )

class ArxivSearcher(PaperSearcherPort):
    """Implementation of the PaperSearcherPort for arXiv search."""

    def __init__(self):
        self.adapter = ArxivAdapter()

    async def search_papers(self, keywords: List[str]) -> List[Paper]:
        """Search for papers using the provided keywords.

        Args:
            keywords: Search keywords (e.g., ["quantum", "computing", "algorithms"])

        Returns:
            List of Paper domain models with populated metadata
        """
        if not keywords:
            return []

        query = ' '.join(keywords)
        # Always search for a reasonable number of papers, not dependent on keyword count
        results = self.adapter.search(query, max_results=5)
        return [Paper(**result.dict()) for result in results]

