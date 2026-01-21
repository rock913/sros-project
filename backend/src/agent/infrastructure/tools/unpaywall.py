import os
from typing import Any, Dict

import requests

from agent.domain.schemas.mcp import McpTool

"""
This module provides an adapter for interacting with the Unpaywall API.
"""

class UnpaywallAdapter:
    """
    Adapter for fetching open-access information from Unpaywall.
    """

    def fetch_by_doi(self, doi: str) -> Dict[str, Any]:
        """
        Fetches the open-access information for a given DOI from Unpaywall.

        Args:
            doi (str): The DOI of the paper to search for.

        Returns:
            Dict[str, Any]: The JSON response from the Unpaywall API.

        Raises:
            ValueError: If no email is set for the Unpaywall API.
        """
        unpaywall_email = os.getenv('UNPAYWALL_EMAIL')
        if not unpaywall_email:
            raise ValueError("No email set for Unpaywall API")

        url = f"https://api.unpaywall.org/v2/{doi}?email={unpaywall_email}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

def unpaywall_handler(doi: str) -> str:
    """
    Handler function for the Unpaywall tool. This function calls the Unpaywall API
    and returns a message indicating whether an open-access version of the paper was found.

    Args:
        doi (str): The DOI of the paper to search for.

    Returns:
        str: A message indicating the result of the search.
    """
    try:
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi(doi)
        
        if paper and paper.get("best_oa_location"):
            oa_info = paper["best_oa_location"]
            return f"Open access version found! Status: {oa_info['oa_status']}. URL: {oa_info['url']}"
        else:
            return "No open access version found for this DOI."
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_unpaywall_tool() -> McpTool:
    """
    Factory function to create an McpTool for the Unpaywall tool.

    Returns:
        McpTool: An instance of McpTool configured for the Unpaywall tool.
    """
    return McpTool(
        name="unpaywall",
        description="Searches Unpywall for a given DOI to find open-access versions of a research paper.",
        input_schema={"doi": {"type": "string", "description": "The DOI of the paper to search for."}},
        handler=unpaywall_handler
    )
