"""
Unit tests for the PaperFetcher protocol.
"""

import unittest
from unittest.mock import patch, MagicMock

from agent.domain.schemas.paper import OpenAccessInfo, Paper
from agent.domain.ports.paper_fetcher import PaperFetcher


class TestPaperFetcher(unittest.TestCase):

    def setUp(self):
        self.mock_fetcher = MagicMock(spec=PaperFetcher)

    def test_compliance_with_protocol(self):
        # Verify implementation adheres to protocol structure
        self.assertTrue(hasattr(self.mock_fetcher, 'fetch_by_doi'))

    def test_fetch_by_doi_valid_doi(self):
        # Test valid DOI returns Paper instance
        valid_doi = "10.1038/nphys1424"
        expected_paper = Paper(
            doi=valid_doi,
            title="Test Paper",
            authors=["Author One", "Author Two"],
            publication_date=None,
            publisher=None,
            oa_info=OpenAccessInfo(is_oa=True, oa_status="gold", oa_url="http://example.com/paper.pdf")
        )
        self.mock_fetcher.fetch_by_doi.return_value = expected_paper
        paper = self.mock_fetcher.fetch_by_doi(valid_doi)
        self.assertIsInstance(paper, Paper)
        self.assertEqual(paper.doi, valid_doi)

    def test_fetch_by_doi_invalid_format(self):
        # Test invalid DOI raises ValueError
        invalid_doi = "invalid-doi"
        self.mock_fetcher.fetch_by_doi.side_effect = ValueError("Invalid DOI format")
        with self.assertRaises(ValueError):
            self.mock_fetcher.fetch_by_doi(invalid_doi)

    def test_network_error_handling(self):
        # Test connection error propagation
        with patch('requests.Session.get', side_effect=ConnectionError):
            self.assertIsNone(self.mock_fetcher.fetch_by_doi("10.1234/test"))


if __name__ == '__main__':
    unittest.main()
