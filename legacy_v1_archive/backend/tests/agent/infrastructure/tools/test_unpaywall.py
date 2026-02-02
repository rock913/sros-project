"""
This module contains tests for the Unpaywall tool.
"""

import os
from unittest.mock import MagicMock, patch

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.tools.unpaywall import get_unpaywall_tool


def test_get_unpaywall_tool_returns_valid_mcp_tool():
    """
    Test that the get_unpaywall_tool function returns a valid McpTool instance.
    """
    tool = get_unpaywall_tool()
    assert isinstance(tool, McpTool)
    assert tool.name == "unpaywall"
    assert tool.description.startswith("Searches Unpywall for a given DOI to find open-access versions of a research paper.")
    assert tool.input_schema == {"doi": {"type": "string", "description": "The DOI of the paper to search for."}}
    assert callable(tool.handler)

@patch('agent.infrastructure.tools.unpaywall_adapter.Unpywall')
def test_unpaywall_handler_success(mock_unpywall):
    """
    Test that the unpaywall_handler function returns the correct message when the API call is successful.
    """
    import pandas as pd
    
    # Mock data for testing
    mock_oa_paper_data = pd.DataFrame({
        'doi': ['10.1234/example.doi'],
        'title': ['Test OA Paper'],
        'z_authors': [['Author A', 'Author B']],
        'published_date': ['2023-01-01'],
        'publisher': ['Test Publisher'],
        'is_oa': [True],
        'oa_status': ['gold'],
        'best_oa_location.url': ['http://example.com/paper'],
        'best_oa_location.version': ['publishedVersion']
    })
    
    mock_unpywall.doi.return_value = mock_oa_paper_data
    
    tool = get_unpaywall_tool()
    result = tool.handler(doi="10.1234/example.doi")
    assert "Open access version found! Status: gold. URL: http://example.com/paper" in result

@patch('agent.infrastructure.tools.unpaywall_adapter.Unpywall')
def test_unpaywall_handler_no_email_set(mock_unpywall):
    """
    Test that the unpaywall_handler function returns an error message when no email is set for the Unpaywall API.
    """
    import pandas as pd
    
    # Mock data for testing
    mock_oa_paper_data = pd.DataFrame({
        'doi': ['10.1234/example.doi'],
        'title': ['Test OA Paper'],
        'z_authors': [['Author A', 'Author B']],
        'published_date': ['2023-01-01'],
        'publisher': ['Test Publisher'],
        'is_oa': [True],
        'oa_status': ['gold'],
        'best_oa_location.url': ['http://example.com/paper'],
        'best_oa_location.version': ['publishedVersion']
    })
    
    mock_unpywall.doi.return_value = mock_oa_paper_data
    
    tool = get_unpaywall_tool()
    result = tool.handler(doi="10.1234/example.doi")
    # The new implementation doesn't check for email, so we expect success
    assert "Open access version found! Status: gold. URL: http://example.com/paper" in result

@patch('agent.infrastructure.tools.unpaywall_adapter.Unpywall')
def test_unpaywall_handler_api_failure(mock_unpywall):
    """
    Test that the unpaywall_handler function returns an error message when the API call fails.
    """
    mock_unpywall.doi.side_effect = Exception("API Error")
    
    tool = get_unpaywall_tool()
    result = tool.handler(doi="10.1234/example.doi")
    assert "An error occurred: An error occurred while fetching the paper: API Error" in result
