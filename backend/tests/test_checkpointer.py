"""
Unit tests for LangGraph Checkpointer functionality
Tests the basic checkpoint save/load without running full research workflow
"""

import pytest
import uuid
from agent.graph import graph
from langgraph.checkpoint.postgres import PostgresSaver


def test_checkpointer_is_configured():
    """Test that the graph has a checkpointer configured"""
    assert graph.checkpointer is not None, "Graph should have a checkpointer"
    assert isinstance(graph.checkpointer, PostgresSaver), "Checkpointer should be PostgresSaver"


def test_checkpointer_can_get_state():
    """Test that checkpointer can retrieve state for a thread"""
    thread_id = str(uuid.uuid4())  # Use UUID format
    config = {"configurable": {"thread_id": thread_id}}
    
    # Get state (should not raise an error even if empty)
    state = graph.get_state(config)
    assert state is not None, "Should be able to retrieve state"


def test_multiple_threads_can_have_separate_states():
    """Test that different threads can maintain separate states"""
    config1 = {"configurable": {"thread_id": str(uuid.uuid4())}}
    config2 = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    # Both should be accessible
    state1 = graph.get_state(config1)
    state2 = graph.get_state(config2)
    
    assert state1 is not None, "Thread A state should be accessible"
    assert state2 is not None, "Thread B state should be accessible"


def test_checkpointer_has_database_connection():
    """Test that checkpointer has a valid database connection"""
    checkpointer = graph.checkpointer
    assert checkpointer.conn is not None, "Checkpointer should have a database connection"

