import unittest
from unittest.mock import patch

from agent.domain.schemas.paper import Paper
from agent.infrastructure.mcp.tools.unpaywall import get_unpaywall_mcp_tool


class TestUnpaywallMcpAdapter(unittest.TestCase):

    @patch('agent.infrastructure.mcp.tools.unpaywall.UnpaywallAdapter')
    def test_factory_returns_valid_mcp_tool(self, MockUnpaywallAdapter):
        mcp_tool = get_unpaywall_mcp_tool()
        self.assertIsNotNone(mcp_tool)
        self.assertIsInstance(mcp_tool, dict)
        self.assertIn('name', mcp_tool)
        self.assertIn('description', mcp_tool)
        self.assertIn('input_schema', mcp_tool)
        self.assertIn('handler', mcp_tool)

    @patch('agent.infrastructure.mcp.tools.unpaywall.UnpaywallAdapter')
    def test_handler_calls_unpaywall_adapter(self, MockUnpaywallAdapter):
        mock_adapter = MockUnpaywallAdapter.return_value
        mock_adapter.fetch_by_doi.return_value = Paper(doi="10.1234/5678", title="Test Paper", authors=[], publication_date=None, publisher=None, oa_info=None)

        mcp_tool = get_unpaywall_mcp_tool()
        result = mcp_tool['handler'](doi="10.1234/5678")

        mock_adapter.fetch_by_doi.assert_called_once_with(doi="10.1234/5678")
        self.assertEqual(result, '{"doi": "10.1234/5678", "title": "Test Paper", "authors": [], "publication_date": null, "publisher": null, "oa_info": null}')

if __name__ == '__main__':
    unittest.main()
