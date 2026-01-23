"""
Unit tests for the ArxivAdapter class.
"""

import unittest
from unittest.mock import MagicMock, patch

from agent.domain.schemas.paper import OpenAccessInfo, Paper
from agent.infrastructure.tools.arxiv_adapter import ArxivAdapter


class TestArxivAdapter(unittest.TestCase):

    @patch('arxiv.Client')
    @patch('arxiv.Search')
    def test_search(self, MockSearch, MockClient):
        # Mock the arxiv.Client and arxiv.Search
        mock_client = MockClient.return_value
        mock_result = MagicMock()
        mock_result.doi = '1234.5678'
        mock_result.title = 'Test Title'
        # Create mock authors with actual string names
        author1 = MagicMock()
        author1.name = 'Author 1'
        author2 = MagicMock()
        author2.name = 'Author 2'
        mock_result.authors = [author1, author2]
        mock_result.published = MagicMock(date=lambda: '2023-01-01')
        mock_result.summary = 'Test Abstract'
        mock_result.pdf_url = 'http://example.com/pdf'
        mock_client.results.return_value = [mock_result]

        # Create the adapter
        adapter = ArxivAdapter()

        # Call the search method
        results = adapter.search(query="test query", max_results=1)

        # Verify the results
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Paper)
        self.assertEqual(results[0].doi, '1234.5678')
        self.assertEqual(results[0].title, 'Test Title')
        self.assertEqual(results[0].authors, ['Author 1', 'Author 2'])
        self.assertEqual(str(results[0].publication_date), '2023-01-01')
        self.assertEqual(results[0].publisher, 'arXiv')
        self.assertEqual(results[0].abstract, 'Test Abstract')
        self.assertEqual(results[0].oa_info, OpenAccessInfo(is_oa=True, oa_status="green", oa_url='http://example.com/pdf'))

if __name__ == '__main__':
    unittest.main()
