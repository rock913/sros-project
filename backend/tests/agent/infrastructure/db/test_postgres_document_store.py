import unittest
from unittest.mock import MagicMock, patch

from agent.infrastructure.db.postgres_document_store import PostgresDocumentStore
from agent.domain.ports.document_store import DocumentStore
from agent.domain.schemas.paper import Paper
from agent.database import Document as DbDocument
