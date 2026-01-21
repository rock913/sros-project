"""
PostgresDocumentStore implementation for storing and retrieving research documents with vector embeddings.
"""

from typing import List, Optional

from agent.domain.ports.document_store import DocumentStore
from agent.database import Document as DbDocument, get_db_connection
from agent.domain.schemas.paper import Paper

class PostgresDocumentStore(DocumentStore):
    def save_document(self, paper: Paper, content: str, embedding: List[float]) -> None:
        db_document = DbDocument(
            content=content,
            embedding=embedding,
            source=paper.doi
        )
        with get_db_connection() as session:
            session.add(db_document)
            session.commit()

    def search(self, query: List[float], k: int = 5) -> List[DbDocument]:
        with get_db_connection() as session:
            results = session.query(DbDocument).order_by(DbDocument._embedding.cosine_distance(query)).limit(k).all()
            return results

    def exists(self, source_id: str) -> bool:
        with get_db_connection() as session:
            result = session.query(DbDocument).filter(DbDocument.source == source_id).scalar()
            return result is not None
