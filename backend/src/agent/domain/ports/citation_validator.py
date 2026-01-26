from typing import List, Protocol
from pydantic import BaseModel

class CitationError(BaseModel):
    cite_key: str
    error_type: str  # e.g., "NOT_FOUND", "CONTEXT_MISMATCH"
    suggestion: str | None = None

class CitationValidator(Protocol):
    """
    Protocol for validating citations in text against a knowledge base.
    
    @TestScenarios
    1. Valid Citations:
       - Input: Text with "[@valid_key]", Available keys ["valid_key"].
       - Expected: Returns empty list [].
       
    2. Missing Citation:
       - Input: Text with "[@missing_key]", Available keys [].
       - Expected: Returns [CitationError(cite_key="missing_key", error_type="NOT_FOUND")].
    """
    
    def validate(self, text: str, available_keys: List[str]) -> List[CitationError]:
        """
        Parse text for citation keys and verify they exist in the provided list.
        """
        ...
        
    def verify_grounding(self, text_segment: str, cite_key: str) -> bool:
        """
        (Advanced) Verify if the cited paper actually supports the text segment.
        This represents the 'Reflexion' step.
        """
        ...
