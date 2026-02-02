"""
Tests for Co-STORM Node Observability

This module tests the CoStormNode class using strict hexagonal architecture principles.
All infrastructure dependencies (LLM provider, DB manager) are mocked using unittest.mock.

@Infrastructure Testing Principles:
- Unit tests must be environment-agnostic (no API keys, no network calls)
- Mock ALL infrastructure ports: LLMProviderPort, DBManager
- Test failure scenarios: LLM errors, missing topics, DB errors
- Focus on observability contract: log_event called correctly

@TestScenarios (Contract Verification):
- generate_perspectives: topic provided -> LLM called + mindmap generated + log_event called
- generate_perspectives: no topic -> fallback mindmap + log_event called
- generate_perspectives: LLM fails -> fallback mindmap + log_event called (graceful degradation)
- log_event payload: contains perspectives list and metadata
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from agent.application.nodes.costorm import CoStormNode
from agent.domain.schemas.mindmap import MindMap, PerspectiveNode


@pytest.mark.asyncio
async def test_costorm_generate_perspectives_success():
    """Test successful perspective generation with observability logging."""
    # Setup infrastructure mocks
    mock_db = AsyncMock()
    mock_llm_provider = AsyncMock()

    # Mock LLM provider to return a valid MindMap (minimum 3 nodes required)
    mock_mindmap = MindMap(
        root_topic="AI Safety",
        nodes=[
            PerspectiveNode(
                id="safety_technical",
                name="Technical Challenges",
                description="Technical aspects of AI safety",
                query_keywords=["technical", "challenges", "safety"]
            ),
            PerspectiveNode(
                id="safety_ethical",
                name="Ethical Considerations",
                description="Moral and ethical implications of AI safety",
                query_keywords=["ethics", "morality", "responsibility"]
            ),
            PerspectiveNode(
                id="safety_applications",
                name="Real-world Applications",
                description="Practical applications of AI safety measures",
                query_keywords=["deployment", "safety_measures", "implementation"]
            )
        ]
    )
    mock_llm_provider.generate_structured_output.return_value = mock_mindmap

    # Create node with mocked dependencies (hexagonal architecture)
    node = CoStormNode(db_manager=mock_db, llm_provider=mock_llm_provider)

    # Test state
    state = {
        "topic": "AI Safety",
        "session_id": "test_session_123"
    }

    # Action: Generate perspectives
    result = await node.generate_perspectives(state)

    # Assertions: Domain behavior verified
    assert "mindmap" in result
    assert "perspectives" in result
    assert len(result["perspectives"]) == 3  # CoStorm generates all perspectives from MindMap
    assert result["perspectives"][0]["id"] == "safety_technical"
    assert result["perspectives"][1]["id"] == "safety_ethical"
    assert result["perspectives"][2]["id"] == "safety_applications"

    # Assertions: Infrastructure contracts fulfilled
    mock_llm_provider.generate_structured_output.assert_called_once()
    mock_db.log_event.assert_called_once()

    # Assertions: Observability payload correct
    call_args = mock_db.log_event.call_args[1]
    assert call_args['session_id'] == "test_session_123"
    assert call_args['event_type'] == "mindmap_generated"
    assert 'perspectives' in call_args['payload']
    assert len(call_args['payload']['perspectives']) == 3  # All perspectives logged for complete observability


@pytest.mark.asyncio
async def test_costorm_generate_perspectives_no_topic():
    """Test perspective generation fallback when no topic provided."""
    # Setup mocks
    mock_db = AsyncMock()
    mock_llm_provider = AsyncMock()  # Won't be called in this case

    node = CoStormNode(db_manager=mock_db, llm_provider=mock_llm_provider)

    # Test state with no topic
    state = {
        "session_id": "test_session_123"
        # No 'topic' key
    }

    # Action
    result = await node.generate_perspectives(state)

    # Assertions: Fallback behavior
    assert result["mindmap"].root_topic == "unknown_topic"
    assert len(result["perspectives"]) == 3  # Default fallback nodes

    # Assertions: Observability (still logged even with fallback)
    mock_db.log_event.assert_called_once()
    call_args = mock_db.log_event.call_args[1]
    assert call_args['payload']['fallback'] is True

    # Assertions: LLM provider NOT called
    mock_llm_provider.generate_structured_output.assert_not_called()


@pytest.mark.asyncio
async def test_costorm_generate_perspectives_llm_failure():
    """Test graceful degradation when LLM provider fails."""
    # Setup mocks
    mock_db = AsyncMock()
    mock_llm_provider = AsyncMock()
    mock_llm_provider.generate_structured_output.side_effect = Exception("API timeout")

    node = CoStormNode(db_manager=mock_db, llm_provider=mock_llm_provider)

    # Test state
    state = {
        "topic": "AI Safety",
        "session_id": "test_session_123"
    }

    # Action
    result = await node.generate_perspectives(state)

    # Assertions: Graceful degradation - fallback mindmap still created
    assert result["mindmap"].root_topic == "AI Safety"  # Topic preserved
    assert len(result["perspectives"]) == 3  # Default fallback nodes

    # Assertions: Infrastructure contracts fulfilled despite error
    mock_llm_provider.generate_structured_output.assert_called_once()
    mock_db.log_event.assert_called_once()

    # Assertions: Observability payload contains fallback data
    call_args = mock_db.log_event.call_args[1]
    assert 'perspectives' in call_args['payload']
    assert len(call_args['payload']['perspectives']) == 3


@pytest.mark.asyncio
async def test_costorm_log_event_payload_structure():
    """Test that log_event payload contains properly structured perspectives data."""
    mock_db = AsyncMock()
    mock_llm_provider = AsyncMock()

    # Mock with minimum valid perspectives (3 nodes) for realistic payload testing
    mock_mindmap = MindMap(
        root_topic="Quantum Computing",
        nodes=[
            PerspectiveNode(
                id="quantum_hardware",
                name="Hardware Implementation",
                description="Physical quantum computers and qubits",
                query_keywords=["hardware", "qubits", "implementation"]
            ),
            PerspectiveNode(
                id="quantum_algorithms",
                name="Quantum Algorithms",
                description="Algorithms designed for quantum computers",
                query_keywords=["algorithms", "quantum computing", "complexity"]
            ),
            PerspectiveNode(
                id="quantum_applications",
                name="Real-world Applications",
                description="Practical applications of quantum computing",
                query_keywords=["applications", "industry", "quantum computing"]
            )
        ]
    )
    mock_llm_provider.generate_structured_output.return_value = mock_mindmap

    node = CoStormNode(db_manager=mock_db, llm_provider=mock_llm_provider)

    state = {
        "topic": "Quantum Computing",
        "session_id": "session_456"
    }

    await node.generate_perspectives(state)

    # Verify log_event payload structure for frontend consumption
    call_args = mock_db.log_event.call_args[1]
    assert call_args['event_type'] == "mindmap_generated"

    perspectives_payload = call_args['payload']['perspectives']
    assert len(perspectives_payload) == 3  # All perspectives are logged

    # Verify each perspective has required fields for frontend
    assert perspectives_payload[0]['id'] == "quantum_hardware"
    assert perspectives_payload[0]['name'] == "Hardware Implementation"
    assert "query_keywords" in perspectives_payload[0]

    assert perspectives_payload[1]['id'] == "quantum_algorithms"
    assert perspectives_payload[1]['name'] == "Quantum Algorithms"
    assert "query_keywords" in perspectives_payload[1]

    assert perspectives_payload[2]['id'] == "quantum_applications"
    assert perspectives_payload[2]['name'] == "Real-world Applications"
    assert "query_keywords" in perspectives_payload[2]


@pytest.mark.asyncio
async def test_costorm_generate_perspectives_no_session_logging():
    """Test that logging is skipped when no session_id provided."""
    # Setup mocks
    mock_db = AsyncMock()
    mock_llm_provider = AsyncMock()

    mock_mindmap = MindMap(
        root_topic="Test Topic",
        nodes=[
            PerspectiveNode(
                id="test1",
                name="Test Node 1",
                description="Test description 1",
                query_keywords=["test1"]
            ),
            PerspectiveNode(
                id="test2",
                name="Test Node 2",
                description="Test description 2",
                query_keywords=["test2"]
            ),
            PerspectiveNode(
                id="test3",
                name="Test Node 3",
                description="Test description 3",
                query_keywords=["test3"]
            )
        ]
    )
    mock_llm_provider.generate_structured_output.return_value = mock_mindmap

    node = CoStormNode(db_manager=mock_db, llm_provider=mock_llm_provider)

    # Test state without session_id
    state = {
        "topic": "Test Topic"
        # No session_id
    }

    # Action
    result = await node.generate_perspectives(state)

    # Assertions: Generation still works
    assert "mindmap" in result
    assert "perspectives" in result
    assert len(result["perspectives"]) == 3  # All perspectives returned even without logging

    # Assertions: Logging skipped (no session_id)
    mock_db.log_event.assert_not_called()
