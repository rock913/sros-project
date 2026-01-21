"""Module for interacting with Google Scholar to search for papers.
"""


import requests
from bs4 import BeautifulSoup
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
    url = f"https://scholar.google.com/scholar?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('.gs_ri'):
        title = item.select_one('.gs_rt').text
        authors = item.select_one('.gs_a').text
        results.append(f"{title} by {authors}")

    return "\n".join(results)


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
