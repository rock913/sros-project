"""Module for interacting with Google Scholar to search for papers.
"""

from pydantic import BaseModel, Field

from agent.domain.schemas.mcp import McpTool


class ScholarQuery(BaseModel):
    """Represents a query for Google Scholar.
    """
    query: str = Field(..., description="The search query for Google Scholar.")


def search_google_scholar(query: str) -> str:
    """Search Google Scholar for papers based on a query.

    Args:
        query (str): The search query for Google Scholar.

    Returns:
        str: A string containing the results of the search.
    """
    # Mocked URL for demonstration purposes
    url = f"https://scholar.google.com/scholar?q={query}"

    # For demonstration, we will return a fixed response
    # In a real scenario, you would parse the response and extract the relevant information
    return f"Results for query '{query}':\n- Test Paper 1 by Author 1\n- Test Paper 2 by Author 2"


def get_scholar_tool() -> McpTool:
    """Create an McpTool for searching Google Scholar.

    Returns:
        McpTool: An McpTool object for the Google Scholar search tool.
    """
    return McpTool(
        name="search_google_scholar",
        description="Search Google Scholar for papers based on a query.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query for Google Scholar."}
            },
            "required": ["query"]
        },
        handler=search_google_scholar
    )
