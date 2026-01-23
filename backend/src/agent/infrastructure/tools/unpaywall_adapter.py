import unpywall
from agent.domain.ports.paper_fetcher import PaperFetcher
from agent.domain.schemas.paper import OpenAccessInfo, Paper

try:
    from unpywall import Unpywall
except ImportError:
    Unpywall = None


def _extract_author_names(raw_authors: list) -> list[str]:
    """Extract author names from Unpaywall's raw author data.
    
    Unpaywall returns authors as a list of dictionaries with keys like:
    - raw_author_name: The author's name as a string
    - author_name: Alternative key for author name
    - author_position: Position in author list (first, middle, last)
    - is_corresponding: Whether author is corresponding author
    - raw_affiliation_strings: List of affiliation strings
    
    Args:
        raw_authors: List of author dictionaries from Unpaywall
        
    Returns:
        List of author names as strings
    """
    author_names = []
    for author in raw_authors:
        if isinstance(author, dict):
            # Try different possible keys for author name
            name = author.get('raw_author_name') or author.get('author_name') or str(author)
            author_names.append(name)
        else:
            author_names.append(str(author))
    return author_names


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
        if Unpywall is None:
            raise RuntimeError("Unpywall is not available. Please ensure the unpywall package is installed.")

        try:
            # Fetch paper data from Unpaywall
            paper_data = Unpywall.doi(dois=[doi])
            
            if paper_data.empty:
                return None
            
            # Extract relevant information
            first_paper = paper_data.iloc[0]
            title = first_paper.get('title', None)
            raw_authors = first_paper.get('z_authors', [])
            publication_date = first_paper.get('published_date', None)
            publisher = first_paper.get('publisher', None)
            
            # Extract author names from raw author data
            authors = _extract_author_names(raw_authors)
            
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
