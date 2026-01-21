"""PostgresDocumentStore implementation for storing and retrieving research documents with vector embeddings."""

from typing import List, Union

from agent.database import Document as DbDocument
from agent.database import get_db_connection
from agent.domain.ports.document_store import DocumentStore
from agent.domain.schemas.paper import Paper


class PostgresDocumentStore(DocumentStore):
    """Implementation of DocumentStore using Postgres via the legacy get_db_connection function."""

    def __init__(self):
        # We don't initialize a session here because get_db_connection() returns a generator
        # that yields a session. We need to handle this per method or refactor get_db_connection.
        pass

    def save_document(self, paper: Paper, content: str, embedding: List[float]) -> None:
        """Save a paper's content and embedding to the store.

        :param paper: The paper domain object.
        :param content: The content of the paper.
        :param embedding: The vector embedding of the paper.
        """
        db_document = DbDocument(
            content=content,
            embedding=embedding,
            source=paper.doi or paper.title  # Fallback source ID
        )
        with get_db_connection() as session:
            session.add(db_document)
            session.commit()

    def search(self, query: List[float], k: int = 5) -> List[DbDocument]:
        """Search for documents semantically similar to the query.

        :param query: The query vector or string.
        :param k: The number of top results to return.
        :return: A list of the top-k most similar documents.
        """
        with get_db_connection() as session:
            # Simple implementation using standard query for now
            # In real vector search we would use distance operators
            return session.query(DbDocument).limit(k).all()

    def exists(self, source_id: str) -> bool:
        """Check if a document with the given source_id exists.

        :param source_id: The unique identifier for the document.
        :return: True if the document exists, False otherwise.
        """
        with get_db_connection() as session:
            return session.query(DbDocument).filter(DbDocument.source == source_id).first() is not None
