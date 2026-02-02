from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from agent.domain.schemas.session import ResearchSession
from agent.infrastructure.db.session_adapter import PostgresSessionAdapter


def test_create_session_with_valid_data():
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = mock_session
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        session = adapter.create_session(
            topic="Quantum Computing",
            description="Research on quantum algorithms"
        )
        assert isinstance(session, ResearchSession)
        assert session.id is not None
        assert session.status == "active"

def test_create_session_duplicate_topic_handling():
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [None, None]
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = mock_session
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        session1 = adapter.create_session(topic="Test")
        session2 = adapter.create_session(topic="Test")
        assert session1.id != session2.id
        assert session1.created_at != session2.created_at

def test_database_connection_failure():
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = MagicMock()
        mock_sessionmaker.return_value.return_value.add.side_effect = SQLAlchemyError("DB down")
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        with pytest.raises(ConnectionError):
            adapter.create_session(topic="Test")

def test_get_session_by_id():
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = MagicMock(
        id=str(uuid4()),
        topic="Test",
        description="",
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = mock_session
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        created = adapter.create_session(topic="Test")
        retrieved = adapter.get_session(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.topic == "Test"

def test_get_nonexistent_session():
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = mock_session
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        retrieved = adapter.get_session("non-existent-uuid")
        assert retrieved is None

def test_list_sessions_pagination():
    mock_session = MagicMock()
    mock_session.query.return_value.order_by.return_value.limit.return_value.offset.return_value.all.return_value = [
        MagicMock(
            id=str(uuid4()),
            topic=f"Test{i}",
            description="",
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ) for i in range(5)
    ]
    with patch('agent.infrastructure.db.session_adapter.create_engine') as mock_create_engine, \
         patch('agent.infrastructure.db.session_adapter.sessionmaker') as mock_sessionmaker:
        mock_sessionmaker.return_value.return_value = mock_session
        adapter = PostgresSessionAdapter("sqlite:///:memory:")
        for i in range(5):
            adapter.create_session(topic=f"Test{i}")
        sessions = adapter.list_sessions(limit=3, offset=0)
        assert len(sessions) == 3
        sessions2 = adapter.list_sessions(limit=3, offset=3)
        assert len(sessions2) == 2
