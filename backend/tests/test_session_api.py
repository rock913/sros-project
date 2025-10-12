"""
Unit tests for Session Management API endpoints
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from agent.app import app

client = TestClient(app)


def test_list_sessions_empty_initially():
    """Test that we can list sessions (may be empty or populated)"""
    response = client.get("/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_session():
    """Test creating a new research session"""
    thread_id = str(uuid.uuid4())
    payload = {
        "thread_id": thread_id,
        "title": "Test Session",
        "research_topic": "Test Topic",
        "tags": ["test", "api"],
        "notes": "Unit test session"
    }
    
    response = client.post("/sessions", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    assert data["thread_id"] == thread_id
    assert data["title"] == "Test Session"
    assert data["research_topic"] == "Test Topic"
    assert data["status"] == "active"
    assert data["tags"] == ["test", "api"]
    assert data["paper_count"] == 0
    assert data["report_count"] == 0
    
    # Store session_id for cleanup
    return data["id"]


def test_get_session_by_id():
    """Test retrieving a session by ID"""
    # Create a session first
    thread_id = str(uuid.uuid4())
    create_response = client.post("/sessions", json={
        "thread_id": thread_id,
        "title": "Get Test Session",
        "research_topic": "Get Test Topic"
    })
    session_id = create_response.json()["id"]
    
    # Retrieve it
    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["title"] == "Get Test Session"


def test_update_session():
    """Test updating a session"""
    # Create a session first
    thread_id = str(uuid.uuid4())
    create_response = client.post("/sessions", json={
        "thread_id": thread_id,
        "title": "Original Title",
        "status": "active"
    })
    session_id = create_response.json()["id"]
    
    # Update it
    update_payload = {
        "title": "Updated Title",
        "status": "completed",
        "notes": "Test notes"
    }
    response = client.patch(f"/sessions/{session_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "completed"
    assert data["notes"] == "Test notes"


def test_delete_session():
    """Test deleting a session"""
    # Create a session first
    thread_id = str(uuid.uuid4())
    create_response = client.post("/sessions", json={
        "thread_id": thread_id,
        "title": "Delete Test Session"
    })
    session_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/sessions/{session_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/sessions/{session_id}")
    assert get_response.status_code == 404


def test_list_session_events():
    """Test listing session events (should be empty for new session)"""
    # Create a session first
    thread_id = str(uuid.uuid4())
    create_response = client.post("/sessions", json={
        "thread_id": thread_id,
        "title": "Events Test Session"
    })
    session_id = create_response.json()["id"]
    
    # List events
    response = client.get(f"/sessions/{session_id}/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_sessions_by_status():
    """Test filtering sessions by status"""
    # Create sessions with different statuses
    thread_id_1 = str(uuid.uuid4())
    thread_id_2 = str(uuid.uuid4())
    
    client.post("/sessions", json={
        "thread_id": thread_id_1,
        "title": "Active Session"
    })
    
    create_response_2 = client.post("/sessions", json={
        "thread_id": thread_id_2,
        "title": "Completed Session"
    })
    session_id_2 = create_response_2.json()["id"]
    
    # Update second to completed
    client.patch(f"/sessions/{session_id_2}", json={"status": "completed"})
    
    # Filter by status
    response = client.get("/sessions?status=completed")
    assert response.status_code == 200
    sessions = response.json()
    assert all(s["status"] == "completed" for s in sessions)


def test_invalid_session_id():
    """Test error handling for invalid UUID"""
    response = client.get("/sessions/invalid-uuid")
    assert response.status_code == 400
    assert "Invalid UUID format" in response.json()["detail"]


def test_nonexistent_session():
    """Test error handling for nonexistent session"""
    fake_uuid = str(uuid.uuid4())
    response = client.get(f"/sessions/{fake_uuid}")
    assert response.status_code == 404
