"""PostgresDocumentStore implementation for storing and retrieving research documents with vector embeddings."""

from typing import List

from agent.database import Document as DbDocument
from agent.database import get_db_connection
from agent.domain.ports.document_store import DocumentStore
from agent.domain.schemas.paper import Paper


class PostgresDocumentStore(DocumentStore):
    """
    Implementation of the DocumentStore protocol using PostgreSQL with vector embeddings.
    """

    def save_document(self, paper: Paper, content: str, embedding: List[float]) -> None:
        """
        Save a paper's content and embedding to the store.

        :param paper: The paper domain object.
        :param content: The content of the paper.
        :param embedding: The vector embedding of the paper.
        """
        db_document = DbDocument(
            content=content,
            embedding=embedding,
            source=paper.doi
        )
        with get_db_connection() as session:
            session.add(db_document)
            session.commit()

    def search(self, query: List[float], k: int = 5) -> List[DbDocument]:
        """
        Search for documents semantically similar to the query.

        :param query: The query vector.
        :param k: The number of top results to return.
        :return: A list of the top-k most similar documents.
        """
        with get_db_connection() as session:
            results = session.query(DbDocument).order_by(DbDocument._embedding.cosine_distance(query)).limit(k).all()
            return results

    def exists(self, source_id: str) -> bool:
        """
        Check if a document with the given source_id (e.g., DOI) exists.

        :param source_id: The unique identifier for the document.
        :return: True if the document exists, False otherwise.
        """
        with get_db_connection() as session:
            result = session.query(DbDocument).filter(DbDocument.source == source_id).scalar()
            return result is not None
