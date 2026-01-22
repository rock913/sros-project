"""
Unit tests for the arXiv MCP tool.
"""

import unittest
from unittest.mock import MagicMock, patch

import pytest

from agent.domain.schemas.mcp import McpTool  # Updated import statement
from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool


@pytest.mark.asyncio
async def test_arxiv_search_mcp_tool():
    # Mock the search method
    mock_paper = MagicMock()
    mock_paper.dict.return_value = {'title': 'Test Title'}
    with patch('agent.infrastructure.tools.arxiv_adapter.ArxivAdapter.search', return_value=[mock_paper]) as mock_search:
        # Get the MCP tool
        tool = get_arxiv_search_mcp_tool()

        # Verify the tool properties
        assert isinstance(tool, McpTool)
        assert tool.name == "arxiv-search"
        assert tool.description == "Search for academic papers on arXiv"

        # Test the handler
        input_data = {'query': 'test query', 'max_results': 1}
        result = await tool.handler(input_data)
        
        # Verify the result
        assert result == [{'title': 'Test Title'}]
        mock_search.assert_called_once_with('test query', 1)

if __name__ == '__main__':
    unittest.main()
