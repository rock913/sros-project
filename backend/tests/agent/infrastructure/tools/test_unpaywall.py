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

@patch('requests.get')
def test_unpaywall_handler_success(mock_get):
    """
    Test that the unpaywall_handler function returns the correct message when the API call is successful.
    """
    with patch.dict(os.environ, {'UNPAYWALL_EMAIL': 'test@example.com'}):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "best_oa_location": {
                "url_for_pdf": "http://example.com/paper.pdf",
                "url": "http://example.com/paper",
                "oa_status": "gold"
            }
        }
        mock_get.return_value = mock_response
    
        tool = get_unpaywall_tool()
        result = tool.handler(doi="10.1234/example.doi")
        assert "Open access version found! Status: gold. URL: http://example.com/paper" in result

@patch('requests.get')
def test_unpaywall_handler_no_email_set(mock_get):
    """
    Test that the unpaywall_handler function returns an error message when no email is set for the Unpaywall API.
    """
    # Use patch.dict to safely remove the environment variable for this test only
    with patch.dict(os.environ, {}, clear=True):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "best_oa_location": {
                "url_for_pdf": "http://example.com/paper.pdf",
                "url": "http://example.com/paper",
                "oa_status": "gold"
            }
        }
        mock_get.return_value = mock_response
    
        tool = get_unpaywall_tool()
        result = tool.handler(doi="10.1234/example.doi")
        assert "No email set for Unpaywall API" in result

@patch('requests.get')
def test_unpaywall_handler_api_failure(mock_get):
    """
    Test that the unpaywall_handler function returns an error message when the API call fails.
    """
    with patch.dict(os.environ, {'UNPAYWALL_EMAIL': 'test@example.com'}):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
    
        tool = get_unpaywall_tool()
        result = tool.handler(doi="10.1234/example.doi")
        assert "An error occurred: API Error" in result
