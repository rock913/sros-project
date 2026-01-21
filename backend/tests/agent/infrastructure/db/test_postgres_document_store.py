"""
Unit tests for PostgresDocumentStore.
"""

import unittest
from unittest.mock import MagicMock, patch

from agent.database import Document as DbDocument
from agent.domain.schemas.paper import Paper
from agent.infrastructure.db.postgres_document_store import PostgresDocumentStore


class TestPostgresDocumentStore(unittest.TestCase):
    @patch('agent.infrastructure.db.postgres_document_store.get_db_connection')
    def test_save_document(self, mock_get_db_connection):
        # Arrange
        mock_session = MagicMock()
        mock_get_db_connection.return_value = mock_session
        store = PostgresDocumentStore()
        paper = Paper(doi="10.1234/5678", title="Test Paper", authors=["Author A"], publication_date="2023-01-01")
        content = "This is a test paper content."
        embedding = [0.1, 0.2, 0.3, 0.4]

        # Act
        store.save_document(paper, content, embedding)

        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('agent.infrastructure.db.postgres_document_store.get_db_connection')
    def test_search(self, mock_get_db_connection):
        # Arrange
        mock_session = MagicMock()
        mock_get_db_connection.return_value = mock_session
        store = PostgresDocumentStore()
        query_embedding = [0.1, 0.2, 0.3, 0.4]
        k = 5

        # Act
        store.search(query_embedding, k)

        # Assert
        mock_session.query.assert_called_once_with(DbDocument)
        mock_session.execute.assert_called_once()

    @patch('agent.infrastructure.db.postgres_document_store.get_db_connection')
    def test_exists(self, mock_get_db_connection):
        # Arrange
        mock_session = MagicMock()
        mock_get_db_connection.return_value = mock_session
        store = PostgresDocumentStore()
        source_id = "10.1234/5678"

        # Act
        store.exists(source_id)

        # Assert
        mock_session.query.assert_called_once_with(DbDocument)
        mock_session.scalar.assert_called_once()
