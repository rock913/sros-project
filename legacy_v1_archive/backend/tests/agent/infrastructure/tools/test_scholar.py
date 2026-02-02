"""
Unit tests for the Google Scholar search tool.
"""

import unittest
from unittest.mock import MagicMock, patch

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.tools.scholar import get_scholar_tool


class TestScholarTool(unittest.TestCase):

    @patch('agent.infrastructure.tools.scholar.requests.get')
    def test_get_scholar_tool(self, mock_requests_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
                <div class="gs_ri">
                  <h3 class="gs_rt">Test Paper 1</h3>
                  <div class="gs_a">Author 1</div>
                </div>
                <div class="gs_ri">
                  <h3 class="gs_rt">Test Paper 2</h3>
                  <div class="gs_a">Author 2</div>
                </div>
            </body>
        </html>
        """
        mock_requests_get.return_value = mock_response

        # Get the scholar tool
        tool = get_scholar_tool()

        # Check if the tool is an instance of McpTool
        self.assertIsInstance(tool, McpTool)

        # Check if the tool has the correct name and description
        self.assertEqual(tool.name, 'search_google_scholar')
        self.assertEqual(tool.description, 'Search Google Scholar for papers based on a query.')

        # Check if the tool has the correct input schema
        self.assertEqual(tool.input_schema, {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'The search query for Google Scholar.'}
            },
            'required': ['query']
        })

        # Call the handler with a sample query
        result = tool.handler(query='test query')

        # Check if the handler returns the expected result
        self.assertIn('Test Paper 1 by Author 1', result)
        self.assertIn('Test Paper 2 by Author 2', result)

if __name__ == '__main__':
    unittest.main()
