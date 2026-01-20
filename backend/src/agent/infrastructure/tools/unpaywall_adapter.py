import unpywall
from agent.domain.ports.paper_fetcher import PaperFetcher
from agent.domain.schemas.paper import OpenAccessInfo, Paper


class UnpaywallAdapter(PaperFetcher):
    """Adapter for fetching paper metadata and full-text availability using Unpaywall.
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
        try:
            # Fetch paper data from Unpaywall
            paper_data = unpywall.Unpaywall.doi(dois=[doi])
            
            if paper_data.empty:
                return None
            
            # Extract relevant information
            first_paper = paper_data.iloc[0]
            title = first_paper.get('title', None)
            authors = first_paper.get('z_authors', [])
            publication_date = first_paper.get('published_date', None)
            publisher = first_paper.get('publisher', None)
            
            # Open Access Information
            oa_info = None
            if 'is_oa' in first_paper and first_paper['is_oa']:
                oa_info = OpenAccessInfo(
                    is_oa=first_paper['is_oa'],
                    oa_status=first_paper['oa_status'],
                    oa_url=first_paper.get('best_oa_location.url', None),
                    version=first_paper.get('best_oa_location.version', None)
                )
            
            # Create and return the Paper object
            return Paper(
                doi=doi,
                title=title,
                authors=authors,
                publication_date=publication_date,
                publisher=publisher,
                oa_info=oa_info
            )
        
        except ValueError as ve:
            raise ValueError("Invalid DOI format") from ve
        except Exception as e:
            raise ConnectionError(f"An error occurred while fetching the paper: {e}")
