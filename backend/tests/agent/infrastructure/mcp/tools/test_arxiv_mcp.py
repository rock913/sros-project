"""
Unit tests for the arXiv MCP tool.
"""

import unittest
from unittest.mock import MagicMock, patch

from agent.infrastructure.mcp.base import McpTool

from agent.infrastructure.mcp.tools.arxiv import get_arxiv_search_mcp_tool


class TestArxivMcpTool(unittest.TestCase):

    @patch('agent.infrastructure.tools.arxiv_adapter.ArxivAdapter.search')
    def test_arxiv_search_mcp_tool(self, mock_search):
        # Mock the search method
        mock_paper = MagicMock()
        mock_paper.dict.return_value = {'title': 'Test Title'}
        mock_search.return_value = [mock_paper]

        # Get the MCP tool
        tool = get_arxiv_search_mcp_tool()

        # Verify the tool properties
        self.assertIsInstance(tool, McpTool)
        self.assertEqual(tool.name, "arxiv-search")
        self.assertEqual(tool.description, "Search for academic papers on arXiv")

        # Test the handler
        input_data = {'query': 'test query', 'max_results': 1}
        result = tool.handler(input_data)
        
        # Verify the result
        self.assertEqual(result, [{'title': 'Test Title'}])
        mock_search.assert_called_once_with('test query', 1)

if __name__ == '__main__':
    unittest.main()
