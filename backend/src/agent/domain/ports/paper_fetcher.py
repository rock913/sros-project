from typing import Protocol

from agent.domain.schemas.paper import Paper


class PaperFetcher(Protocol):
    """Protocol for fetching paper metadata and full-text availability.
    
    This acts as a Port in the Hexagonal Architecture, decoupling the
    application from specific providers like Unpaywall, Crossref, or Semantic Scholar.
    
    @TestScenarios
    def test_compliance_with_protocol():
        # Verify implementation adheres to protocol structure
        assert hasattr(implementation, 'fetch_by_doi')
        
    @TestScenarios
    def test_fetch_by_doi_valid_doi():
        # Test valid DOI returns Paper instance
        paper = implementation.fetch_by_doi("10.1038/nphys1424")
        assert isinstance(paper, Paper)
        
    @TestScenarios
    def test_fetch_by_doi_invalid_format():
        # Test invalid DOI raises ValueError
        with pytest.raises(ValueError):
            implementation.fetch_by_doi("invalid-doi")
            
    @TestScenarios
    def test_network_error_handling():
        # Test connection error propagation
        with mock.patch('session.get', side_effect=RequestException):
            assert implementation.fetch_by_doi("10.1234/test") is None
    """

    def fetch_by_doi(self, doi: str) -> Paper | None:
        """Fetch paper details using its DOI.

        Args:
            doi (str): The Digital Object Identifier of the paper.

        Returns:
            Optional[Paper]: The Paper domain model if found, None otherwise.
        
        Raises:
            ValueError: If the DOI format is invalid.
            ConnectionError: If the upstream service is unreachable.
        """
        ...
