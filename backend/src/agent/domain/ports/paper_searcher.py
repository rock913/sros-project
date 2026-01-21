from typing import List, Protocol
from agent.domain.schemas.paper import Paper

class PaperSearcher(Protocol):
    """
    Protocol for searching academic papers from external repositories (e.g., Arxiv, PubMed).
    
    @TestScenarios
    1. Basic Search:
       - Input: query="machine learning", max_results=2
       - Expected: Returns a list of <= 2 Paper objects.
       
    2. Empty Results:
       - Input: query="sdlkfjsdlkfjdslkfj" (nonsense)
       - Expected: Returns empty list [].
       
    3. Error Handling:
       - Input: External service down.
       - Expected: Raises specific domain exception or ConnectionError.
    """
    
    def search(self, query: str, max_results: int = 5) -> List[Paper]:
        """
        Search for papers matching the query.
        
        Args:
            query: The search string (supports basic operators depending on backend).
            max_results: Maximum number of papers to return.
            
        Returns:
            List[Paper]: List of domain model Paper objects.
        """
        ...
