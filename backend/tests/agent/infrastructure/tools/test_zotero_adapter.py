import unittest
from unittest.mock import MagicMock, patch

from agent.domain.schemas.paper import Paper
from agent.infrastructure.tools.zotero_adapter import ZoteroAdapter


class TestZoteroAdapter(unittest.TestCase):
    @patch('pyzotero.zotero.Zotero')
    def test_save_paper_success(self, mock_zotero):
        # Mock Zotero instance
        mock_zotero_instance = MagicMock()
        mock_zotero.return_value = mock_zotero_instance
        mock_zotero_instance.create_items.return_value = {'successful': {'key': {'key': '123'}}}

        # Create ZoteroAdapter instance
        adapter = ZoteroAdapter(library_id='test_library_id', api_key='test_api_key')

        # Create a sample paper
        paper = Paper(
            title="Test Paper",
            authors=["John Doe"],
            abstract="This is a test abstract.",
            publication_date="2023-01-01",
            doi="10.1234/5678",
            oa_info={'is_oa': True, 'oa_status': 'gold', 'oa_url': 'http://example.com/paper.pdf'},
            publisher="Test Publisher"
        )

        # Save the paper
        result = adapter.save_paper(paper)

        # Check the result
        self.assertIn("Saved to Zotero. Item Key: 123", result)

    @patch('pyzotero.zotero.Zotero')
    def test_save_paper_failure(self, mock_zotero):
        # Mock Zotero instance
        mock_zotero_instance = MagicMock()
        mock_zotero.return_value = mock_zotero_instance
        mock_zotero_instance.create_items.return_value = {'failed': {'key': {'error': 'Some error'}}}

        # Create ZoteroAdapter instance
        adapter = ZoteroAdapter(library_id='test_library_id', api_key='test_api_key')

        # Create a sample paper
        paper = Paper(
            title="Test Paper",
            authors=["John Doe"],
            abstract="This is a test abstract.",
            publication_date="2023-01-01",
            doi="10.1234/5678",
            oa_info={'is_oa': True, 'oa_status': 'gold', 'oa_url': 'http://example.com/paper.pdf'},
            publisher="Test Publisher"
        )

        # Save the paper
        with self.assertRaises(RuntimeError):
            adapter.save_paper(paper)
