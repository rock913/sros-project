"""
Unit tests for the Unpaywall MCP tool factory.
"""

import json
import unittest
from unittest.mock import patch

from agent.domain.schemas.mcp import McpTool  # Import McpTool
from agent.domain.schemas.paper import Paper, OpenAccessInfo
from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool


class TestUnpaywallMcpAdapter(unittest.TestCase):

    @patch('agent.infrastructure.mcp.tools.unpaywall.UnpaywallAdapter')
    def test_factory_returns_valid_mcp_tool(self, MockUnpaywallAdapter):
        mcp_tool = get_unpaywall_mcp_tool()
        self.assertIsNotNone(mcp_tool)
        self.assertIsInstance(mcp_tool, McpTool)  # Fix: Expect object, not dict
        self.assertEqual(mcp_tool.name, "unpaywall-fetch-paper")
        self.assertTrue(hasattr(mcp_tool, 'description'))
        self.assertTrue(hasattr(mcp_tool, 'input_schema'))
        self.assertTrue(hasattr(mcp_tool, 'handler'))

    @patch('agent.infrastructure.mcp.tools.unpaywall.UnpaywallAdapter')
    def test_handler_calls_unpaywall_adapter(self, MockUnpaywallAdapter):
        mock_adapter = MockUnpaywallAdapter.return_value
        mock_adapter.fetch_by_doi.return_value = Paper(
            doi="10.1234/5678", 
            title="Test Paper", 
            authors=[], 
            publication_date=None, 
            publisher=None, 
            oa_info=None
        )

        mcp_tool = get_unpaywall_mcp_tool()
        result = mcp_tool.handler({"doi": "10.1234/5678"})  # Pass dict argument

        mock_adapter.fetch_by_doi.assert_called_once_with(doi="10.1234/5678")
        # result is a string message, not JSON; check that it's a string
        self.assertIsInstance(result, str)
        # Since the mock returns a Paper with no OA info, the handler returns "No open access version found"
        self.assertEqual(result, "No open access version found")

    @patch('agent.infrastructure.mcp.tools.unpaywall.UnpaywallAdapter')
    def test_handler_with_open_access_info(self, MockUnpaywallAdapter):
        mock_adapter = MockUnpaywallAdapter.return_value
        mock_adapter.fetch_by_doi.return_value = Paper(
            doi="10.1234/5678", 
            title="Test Paper", 
            authors=[], 
            publication_date=None, 
            publisher=None, 
            oa_info=OpenAccessInfo(is_oa=True, oa_status="gold", oa_url="http://example.com/paper.pdf")
        )

        mcp_tool = get_unpaywall_mcp_tool()
        result = mcp_tool.handler({"doi": "10.1234/5678"})  # Pass dict argument

        mock_adapter.fetch_by_doi.assert_called_once_with(doi="10.1234/5678")
        # result is a string message, not JSON; check that it's a string
        self.assertIsInstance(result, str)
        # Since the mock returns a Paper with OA info, the handler returns the OA status and URL
        self.assertEqual(result, "Open access version found! Status: gold. URL: http://example.com/paper.pdf")


if __name__ == '__main__':
    unittest.main()
