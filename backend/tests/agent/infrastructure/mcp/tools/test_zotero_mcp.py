import unittest
from unittest.mock import MagicMock, patch

from agent.infrastructure.mcp.tools.zotero import ZoteroMCPTool


class TestZoteroMCPTool(unittest.TestCase):
    @patch('agent.infrastructure.tools.zotero_adapter.ZoteroAdapter')
    def test_execute_success(self, mock_zotero_adapter):
        # Mock ZoteroAdapter instance
        mock_zotero_adapter_instance = MagicMock()
        mock_zotero_adapter.return_value = mock_zotero_adapter_instance
        mock_zotero_adapter_instance.save_paper.return_value = "Saved to Zotero. Item Key: 123"

        # Create ZoteroMCPTool instance
        tool = ZoteroMCPTool()

        # Create a sample paper
        paper_data = {
            "title": "Test Paper",
            "authors": ["John Doe"],
            "abstract": "This is a test abstract.",
            "publication_date": "2023-01-01",
            "doi": "10.1234/5678",
            "oa_info": {'is_oa': True, 'oa_status': 'gold', 'oa_url': 'http://example.com/paper.pdf'},
            "publisher": "Test Publisher"
        }

        # Execute the tool
        result = tool.execute(paper_data)

        # Check the result
        self.assertTrue(result.success)
        self.assertIn("Saved to Zotero. Item Key: 123", result.message)

    @patch('agent.infrastructure.tools.zotero_adapter.ZoteroAdapter')
    def test_execute_failure(self, mock_zotero_adapter):
        # Mock ZoteroAdapter instance
        mock_zotero_adapter_instance = MagicMock()
        mock_zotero_adapter.return_value = mock_zotero_adapter_instance
        mock_zotero_adapter_instance.save_paper.side_effect = RuntimeError("Some error")

        # Create ZoteroMCPTool instance
        tool = ZoteroMCPTool()

        # Create a sample paper
        paper_data = {
            "title": "Test Paper",
            "authors": ["John Doe"],
            "abstract": "This is a test abstract.",
            "publication_date": "2023-01-01",
            "doi": "10.1234/5678",
            "oa_info": {'is_oa': True, 'oa_status': 'gold', 'oa_url': 'http://example.com/paper.pdf'},
            "publisher": "Test Publisher"
        }

        # Execute the tool
        result = tool.execute(paper_data)

        # Check the result
        self.assertFalse(result.success)
        self.assertIn("Some error", result.message)
