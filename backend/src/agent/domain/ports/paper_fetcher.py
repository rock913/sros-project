from typing import Protocol

from ..schemas.paper import Paper


class PaperFetcher(Protocol):
    """Protocol for fetching paper metadata and full-text availability.
    
    This acts as a Port in the Hexagonal Architecture, decoupling the
    application from specific providers like Unpaywall, Crossref, or Semantic Scholar.
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
