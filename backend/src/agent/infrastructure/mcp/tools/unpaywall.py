"""Module for creating an MCP tool for fetching papers using Unpaywall."""

from pydantic import BaseModel, Field

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.tools.unpaywall_adapter import UnpaywallAdapter


class UnpaywallArgs(BaseModel):
    """Arguments for the Unpaywall MCP tool."""

    doi: str = Field(..., description="The Digital Object Identifier of the paper")


def get_unpaywall_mcp_tool() -> McpTool:
    """Create an MCP tool for fetching papers from Unpaywall.

    Returns:
        McpTool: The MCP tool for fetching papers.
    """

    def handler(args: dict) -> str:
        try:
            unpaywall_args = UnpaywallArgs(**args)
        except Exception as e:
            return f"Error: {e}"

        adapter = UnpaywallAdapter()
        try:
            paper = adapter.fetch_by_doi(doi=unpaywall_args.doi)
            if paper is None:
                return "Paper not found"
            
            # Extract the relevant information for the old format
            if paper.oa_info and paper.oa_info.oa_url:
                return f"Open access version found! Status: {paper.oa_info.oa_status}. URL: {paper.oa_info.oa_url}"
            else:
                return "No open access version found"
        except ValueError as e:
            if "Invalid DOI format" in str(e):
                return "An error occurred: Invalid DOI format"
            raise
        except Exception as e:
            return f"An error occurred: {e}"

    unpaywall_tool = McpTool(
        name="unpaywall-fetch-paper",
        description="Fetches a paper from Unpaywall using its DOI",
        input_schema=UnpaywallArgs.model_json_schema(),
        handler=handler
    )
    return unpaywall_tool
