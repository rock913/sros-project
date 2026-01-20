"""Module for creating an MCP tool for fetching papers using Unpaywall.
"""

from pydantic import BaseModel, Field

from agent.domain.ports.paper_fetcher import UnpaywallAdapter
from agent.domain.schemas.mcp import McpTool


class UnpaywallArgs(BaseModel):
    """Arguments for the Unpaywall MCP tool.
    """

    doi: str = Field(..., description="The Digital Object Identifier of the paper")


def get_unpaywall_mcp_tool() -> McpTool:
    """Creates an MCP tool for fetching papers from Unpaywall.

    Returns:
        McpTool: The MCP tool for fetching papers.
    """

    def handler(doi: str) -> str:
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi(doi)
        if paper is None:
            return "Paper not found"
        return paper.json()

    unpaywall_tool = McpTool(
        name="unpaywall-fetch-paper",
        description="Fetches a paper from Unpaywall using its DOI",
        input_schema=UnpaywallArgs.schema(),
        handler=handler
    )
    return unpaywall_tool
