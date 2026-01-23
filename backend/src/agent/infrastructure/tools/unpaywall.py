"""Compatibility layer for Unpaywall tool. This module provides backward compatibility
while migrating to the new MCP architecture.

DEPRECATED: Use `agent.infrastructure.mcp.tools.unpaywall.get_unpaywall_mcp_tool()` instead.
"""

import warnings
from typing import Any, Dict

from agent.domain.schemas.mcp import McpTool


def unpaywall_handler(doi: str) -> str:
    """Handle the Unpaywall tool. This function calls the Unpaywall API and returns a message indicating whether an open-access version of the paper was found.

    Args:
        doi (str): The DOI of the paper to search for.

    Returns:
        str: A message indicating the result of the search.
    """
    warnings.warn(
        "unpaywall_handler is deprecated. Use the new MCP tool from agent.infrastructure.mcp.tools.unpaywall",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Import the new MCP tool handler
    from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool
    
    try:
        # Get the new MCP tool and call its handler
        mcp_tool = get_unpaywall_mcp_tool()
        # The new handler expects a dict with 'doi' key
        result = mcp_tool.handler({"doi": doi})
        return result
    except Exception as e:
        return f"An error occurred: {e}"

def get_unpaywall_tool() -> McpTool:
    """Create an McpTool for the Unpaywall tool.
    
    DEPRECATED: Use `get_unpaywall_mcp_tool()` from `agent.infrastructure.mcp.tools.unpaywall` instead.

    Returns:
        McpTool: An instance of McpTool configured for the Unpaywall tool.
    """
    warnings.warn(
        "get_unpaywall_tool is deprecated. Use get_unpaywall_mcp_tool() from agent.infrastructure.mcp.tools.unpaywall instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    return McpTool(
        name="unpaywall",
        description="Searches Unpywall for a given DOI to find open-access versions of a research paper.",
        input_schema={"doi": {"type": "string", "description": "The DOI of the paper to search for."}},
        handler=unpaywall_handler
    )
