import os
from unittest.mock import patch, MagicMock
from typing import Any, Dict

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.tools.unpaywall import get_unpaywall_tool

def test_get_unpaywall_tool_returns_valid_mcp_tool():
    tool = get_unpaywall_tool()
    assert isinstance(tool, McpTool)
    assert tool.name == "unpaywall"
    assert tool.description.startswith("Searches Unpywall for a given DOI to find open-access versions of a research paper.")
    assert tool.input_schema == {"doi": {"type": "string", "description": "The DOI of the paper to search for."}}
    assert callable(tool.handler)

@patch('requests.get')
def test_unpaywall_handler_success(mock_get):
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
    os.environ.pop('UNPAYWALL_EMAIL', None)
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
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_response

    tool = get_unpaywall_tool()
    result = tool.handler(doi="10.1234/example.doi")
    assert "An error occurred: API Error" in result
