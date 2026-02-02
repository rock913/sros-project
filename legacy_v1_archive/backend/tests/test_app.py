"""
Tests for the FastAPI app endpoints.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from agent.app import app
from agent.database import Document


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_documents():
    """Mock documents to be returned by get_all_documents."""
    doc1 = MagicMock(spec=Document)
    doc1.source = "Paper Title 1"
    doc1.content = "This is the summary of paper 1"
    
    doc2 = MagicMock(spec=Document)
    doc2.source = "Paper Title 2"
    doc2.content = "This is the summary of paper 2"
    
    return [doc1, doc2]


class TestHealthEndpoint:
    """Tests for the /ok health check endpoint."""
    
    def test_health_check(self, client):
        """Test that the health check endpoint returns OK."""
        response = client.get("/ok")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAgentStateEndpoint:
    """Tests for the /agent/state endpoint."""
    
    @patch('agent.app.get_all_documents')
    def test_get_agent_state_success(self, mock_get_all_docs, client, mock_documents):
        """Test that GET /agent/state returns the correct structure."""
        mock_get_all_docs.return_value = mock_documents
        
        response = client.get("/agent/state")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure matches OpenAPI schema
        assert "messages" in data
        assert "research_topic" in data
        assert "search_queries" in data
        assert "literature_abstracts" in data
        assert "literature_full_text" in data
        assert "is_sufficient" in data
        assert "knowledge_gap" in data
        assert "report" in data
        
        # Verify literature_abstracts contains the mocked documents
        assert len(data["literature_abstracts"]) == 2
        assert data["literature_abstracts"][0]["title"] == "Paper Title 1"
        assert data["literature_abstracts"][0]["summary"] == "This is the summary of paper 1"
    
    @patch('agent.app.get_all_documents')
    def test_get_agent_state_empty(self, mock_get_all_docs, client):
        """Test that GET /agent/state handles empty database gracefully."""
        mock_get_all_docs.return_value = []
        
        response = client.get("/agent/state")
        
        assert response.status_code == 200
        data = response.json()
        assert data["literature_abstracts"] == []


class TestAgentStateByThreadEndpoint:
    """Tests for the /agent/state/{thread_id} endpoint."""
    
    @patch('agent.app.get_all_documents')
    def test_get_agent_state_by_thread_success(self, mock_get_all_docs, client, mock_documents):
        """Test that GET /agent/state/{thread_id} returns the correct structure."""
        mock_get_all_docs.return_value = mock_documents
        thread_id = "test-thread-123"
        
        response = client.get(f"/agent/state/{thread_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure matches OpenAPI schema
        assert "messages" in data
        assert "research_topic" in data
        assert "search_queries" in data
        assert "literature_abstracts" in data
        assert len(data["literature_abstracts"]) == 2
    
    @patch('agent.app.get_all_documents')
    def test_get_agent_state_by_thread_not_found(self, mock_get_all_docs, client):
        """Test that GET /agent/state/{thread_id} returns 404 when no data exists."""
        mock_get_all_docs.return_value = []
        thread_id = "non-existent-thread"
        
        response = client.get(f"/agent/state/{thread_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_agent_state_by_thread_valid_path_param(self, client):
        """Test that thread_id path parameter is correctly parsed."""
        with patch('agent.app.get_all_documents') as mock_get_all_docs:
            mock_doc = MagicMock(spec=Document)
            mock_doc.source = "Test Paper"
            mock_doc.content = "Test content"
            mock_get_all_docs.return_value = [mock_doc]
            
            # Test with various thread_id formats
            valid_thread_ids = [
                "simple-id",
                "thread_with_underscore",
                "thread-123-456",
                "uuid-4abc-1234-5678"
            ]
            
            for thread_id in valid_thread_ids:
                response = client.get(f"/agent/state/{thread_id}")
                assert response.status_code == 200, f"Failed for thread_id: {thread_id}"
