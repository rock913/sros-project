from unittest.mock import patch

import pandas as pd
import pytest

from agent.infrastructure.tools.unpaywall_adapter import UnpaywallAdapter
from agent.domain.schemas.paper import OpenAccessInfo, Paper

# Mock data for testing
mock_oa_paper_data = pd.DataFrame({
    'doi': ['10.1000/123456'],
    'title': ['Test OA Paper'],
    'z_authors': [['Author A', 'Author B']],
    'published_date': ['2023-01-01'],
    'publisher': ['Test Publisher'],
    'is_oa': [True],
    'oa_status': ['gold'],
    'best_oa_location.url': ['http://example.com/paper.pdf'],
    'best_oa_location.version': ['publishedVersion']
})

mock_non_oa_paper_data = pd.DataFrame({
    'doi': ['10.1000/789012'],
    'title': ['Test Non-OA Paper'],
    'z_authors': [['Author C', 'Author D']],
    'published_date': ['2023-01-01'],
    'publisher': ['Test Publisher'],
    'is_oa': [False]
})

mock_empty_paper_data = pd.DataFrame()

class TestUnpaywallAdapter:
    @patch('unpywall.Unpywall.doi')
    def test_fetch_by_doi_success_oa(self, mock_unpywall_doi):
        """
        Test fetching a paper that is Open Access.
        
        This test ensures that the adapter correctly handles a successful fetch
        of an Open Access paper and returns the expected Paper object.
        """
        mock_unpywall_doi.return_value = mock_oa_paper_data
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi('10.1000/123456')
        
        assert paper is not None
        assert paper.doi == '10.1000/123456'
        assert paper.title == 'Test OA Paper'
        assert paper.authors == ['Author A', 'Author B']
        assert paper.publication_date == pd.to_datetime('2023-01-01').date()
        assert paper.publisher == 'Test Publisher'
        assert paper.oa_info.is_oa is True
        assert paper.oa_info.oa_status == 'gold'
        assert paper.oa_info.oa_url == 'http://example.com/paper.pdf'
        assert paper.oa_info.version == 'publishedVersion'

    @patch('unpywall.Unpywall.doi')
    def test_fetch_by_doi_success_non_oa(self, mock_unpywall_doi):
        """
        Test fetching a paper that is not Open Access.
        
        This test ensures that the adapter correctly handles a successful fetch
        of a non-Open Access paper and returns the expected Paper object without OA info.
        """
        mock_unpywall_doi.return_value = mock_non_oa_paper_data
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi('10.1000/789012')
        
        assert paper is not None
        assert paper.doi == '10.1000/789012'
        assert paper.title == 'Test Non-OA Paper'
        assert paper.authors == ['Author C', 'Author D']
        assert paper.publication_date == pd.to_datetime('2023-01-01').date()
        assert paper.publisher == 'Test Publisher'
        assert paper.oa_info is None

    @patch('unpywall.Unpywall.doi')
    def test_fetch_by_doi_not_found(self, mock_unpywall_doi):
        """
        Test fetching a paper that does not exist.
        
        This test ensures that the adapter correctly handles a case where the
        paper is not found and returns None.
        """
        mock_unpywall_doi.return_value = mock_empty_paper_data
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi('10.1000/unknown')
        
        assert paper is None

    @patch('unpywall.Unpywall.doi')
    def test_fetch_by_doi_service_error(self, mock_unpywall_doi):
        """
        Test fetching a paper when the external service raises an error.
        
        This test ensures that the adapter correctly handles an error from the
        external service and raises a ConnectionError.
        """
        mock_unpywall_doi.side_effect = Exception("Service unavailable")
        adapter = UnpaywallAdapter()
        
        with pytest.raises(ConnectionError) as exc_info:
            adapter.fetch_by_doi('10.1000/123456')
        
        assert str(exc_info.value) == "An error occurred while fetching the paper: Service unavailable"

    @patch('unpywall.Unpywall.doi')
    def test_fetch_by_doi_invalid_doi(self, mock_unpywall_doi):
        """
        Test fetching a paper with an invalid DOI.
        
        This test ensures that the adapter correctly handles an invalid DOI and raises a ValueError.
        """
        mock_unpywall_doi.side_effect = ValueError("Invalid DOI format")
        adapter = UnpaywallAdapter()
        
        with pytest.raises(ValueError) as exc_info:
            adapter.fetch_by_doi('invalid-doi')
        
        assert str(exc_info.value) == "Invalid DOI format"
