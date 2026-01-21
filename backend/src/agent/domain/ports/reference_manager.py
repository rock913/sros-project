from typing import Protocol, Optional
from agent.domain.schemas.paper import Paper

class ReferenceManager(Protocol):
    """
    Protocol for managing bibliographic references (e.g., Zotero, Mendeley).
    
    @TestScenarios
    1. Save Valid Paper:
       - Input: Complete Paper object.
       - Expected: Returns a success message or ID.
       
    2. Missing Config:
       - Input: API Keys missing in env.
       - Expected: Raises ConfigurationError (or specific equivalent).
       
    3. Duplicate Handling (Optional):
       - Input: Paper already exists.
       - Expected: Updates or returns existing ID.
    """
    
    def save_paper(self, paper: Paper) -> str:
        """
        Save a paper to the reference manager.
        
        Args:
            paper: The domain Paper object to save.
            
        Returns:
            str: The ID or Status of the saved item.
        """
        ...
