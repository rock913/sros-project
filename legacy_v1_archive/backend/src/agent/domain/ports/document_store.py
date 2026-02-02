from typing import List, Optional, Protocol, Union

from agent.domain.schemas.paper import Paper
from agent.database import Document as DbDocument

class DocumentStore(Protocol):
    """
    Protocol for storing and retrieving research documents with vector embeddings.
    
    @TestScenarios
    1. Save Document:
       - Input: Paper domain object + content string + embedding vector.
       - Expected: Document persisted to DB with correct vector.
       
    2. Search Similar:
       - Input: Query vector, limit k.
       - Expected: List of top-k most similar documents based on cosine similarity.
       
    3. Check Existence:
       - Input: DOI or Source ID.
       - Expected: Boolean indicating if document is already indexed.
    """
    
    def save_document(self, paper: Paper, content: str, embedding: List[float]) -> None:
        """Save a paper's content and embedding to the store."""
        
    def search(self, query: str, k: int = 5) -> List[DbDocument]:
        """Search for documents semantically similar to the query."""
        
    def exists(self, source_id: str) -> bool:
        """Check if a document with the given source_id (e.g., DOI) exists."""
