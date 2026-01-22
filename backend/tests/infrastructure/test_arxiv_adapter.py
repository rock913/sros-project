import unittest
from unittest.mock import MagicMock, patch

from agent.domain.schemas.paper import Paper
from agent.infrastructure.adapters.arxiv_adapter import ArxivAdapter


class TestArxivAdapter(unittest.TestCase):
    """
    Test cases for the ArxivAdapter class.
    """

    @patch('arxiv.Search')
    def test_basic_search(self, mock_search):
        # Mock the search results
        mock_result = MagicMock()
        mock_result.results.return_value = [
            {
                'entry_id': '1234.5678',
                'title': 'Test Title',
                'authors': [{'name': 'Author One'}, {'name': 'Author Two'}],
                'published': '2023-01-01',
                'summary': 'Test Abstract',
                'pdf_url': 'http://example.com/paper.pdf'
            }
        ]
        mock_search.return_value = mock_result

        adapter = ArxivAdapter()
        results = adapter.search(query="machine learning", max_results=2)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Paper)
        self.assertEqual(results[0].doi, '1234.5678')
        self.assertEqual(results[0].title, 'Test Title')
        self.assertEqual(results[0].authors, ['Author One', 'Author Two'])
        self.assertEqual(results[0].publication_date, '2023-01-01')
        self.assertEqual(results[0].abstract, 'Test Abstract')
        self.assertEqual(results[0].oa_info.oa_url, 'http://example.com/paper.pdf')

    @patch('arxiv.Search')
    def test_empty_results(self, mock_search):
        # Mock the search results
        mock_result = MagicMock()
        mock_result.results.return_value = []
        mock_search.return_value = mock_result

        adapter = ArxivAdapter()
        results = adapter.search(query="sdlkfjsdlkfjdslkfj", max_results=2)

        self.assertEqual(len(results), 0)

    @patch('arxiv.Search')
    def test_error_handling(self, mock_search):
        # Mock the search results
        mock_search.side_effect = Exception("External service down")

        adapter = ArxivAdapter()

        with self.assertRaises(Exception):
            adapter.search(query="machine learning", max_results=2)

if __name__ == '__main__':
    unittest.main()
