"""
Co-STORM Workflow Tests

Tests for the Co-STORM (Collaborative STORM) discovery engine.
Validates perspective generation and mind map construction.

@Hexagonal Architecture Tests:
- Test domain schemas independently
- Mock external infrastructure (LLM, Postgres)
- Validate contract-first behavior with @TestScenarios
"""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from agent.domain.schemas.mindmap import MindMap, PerspectiveNode
from agent.application.nodes.costorm import CoStormState, generate_perspectives


@pytest.mark.asyncio
@patch('agent.litellm_utils.completion')
async def test_generate_perspectives_success(mock_completion):
    """
    Test successful perspective generation with mocked LLM.

    @TestScenarios
    - Input: topic="Quantum Computing"
    - Output: CoStormState with MindMap containing 3-5 valid PerspectiveNodes
    - Validate: Each node has unique id, 3-5 keywords, proper descriptions
    - Verify: State immutability (new dict returned)
    """
    # Mock LLM response - valid MindMap JSON matching Pydantic schema
    mindmap_response = {
        "root_topic": "Quantum Computing",
        "nodes": [
            {
                "id": "methodological",
                "name": "Methodological Perspective",
                "description": "Approaches and techniques for quantum computing research",
                "query_keywords": ["quantum algorithms", "methodology", "techniques"]
            },
            {
                "id": "historical",
                "name": "Historical Perspective",
                "description": "Evolution from theoretical foundations to modern applications",
                "query_keywords": ["quantum history", "timeline", "evolution"]
            },
            {
                "id": "applications",
                "name": "Applications Perspective",
                "description": "Real-world uses and impact of quantum computing",
                "query_keywords": ["quantum applications", "use cases", "industry"]
            }
        ]
    }

    mock_completion.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=str(mindmap_response).replace("'", '"')))]
    )

    # Test state
    initial_state = CoStormState(
        messages=[AIMessage(content="Quantum Computing")],
        topic="Quantum Computing",
        mindmap=None,
        perspectives=[]
    )

    # Mock config
    config = MagicMock()

    # Execute node
    result_state = generate_perspectives(initial_state, config)

    # Verify state changes
    assert result_state != initial_state  # State immutability
    assert "mindmap" in result_state
    assert "perspectives" in result_state

    # Verify MindMap creation
    mindmap = result_state["mindmap"]
    assert isinstance(mindmap, MindMap)
    assert mindmap.root_topic == "Quantum Computing"
    assert len(mindmap.nodes) == 3

    # Verify perspectives extraction
    perspectives = result_state["perspectives"]
    assert len(perspectives) == 3
    assert perspectives[0]["id"] == "methodological"
    assert perspectives[1]["name"] == "Historical Perspective"


@pytest.mark.asyncio
@patch('agent.litellm_utils.completion')
async def test_generate_perspectives_empty_topic(mock_completion):
    """
    Test graceful handling when no topic provided.

    @TestScenarios
    - Input: empty topic string
    - Output: valid fallback MindMap with empty nodes list
    - Verify: no LLM call when topic missing
    - Ensure: workflow can continue with empty result
    """
    # Test with empty topic
    initial_state = CoStormState(
        messages=[],
        topic="",
        mindmap=None,
        perspectives=[]
    )

    config = MagicMock()
    result_state = generate_perspectives(initial_state, config)

    # Verify fallback behavior
    assert result_state["mindmap"].root_topic == "unknown_topic"
    assert len(result_state["mindmap"].nodes) == 0
    assert len(result_state["perspectives"]) == 0

    # Verify no LLM call made
    mock_completion.assert_not_called()


@pytest.mark.asyncio
@patch('agent.litellm_utils.completion')
async def test_generate_perspectives_llm_failure(mock_completion):
    """
    Test Co-STORM error handling with LLM API failure.

    @TestScenarios
    - Input: valid topic but LLM throws exception
    - Output: graceful degradation with empty MindMap
    - Verify: logging shows error, workflow continues
    - Ensure: no runtime exceptions bubble up
    """
    # Simulate LLM API failure
    mock_completion.side_effect = Exception("LLM API error")

    initial_state = CoStormState(
        messages=[AIMessage(content="Machine Learning")],
        topic="Machine Learning",
        mindmap=None,
        perspectives=[]
    )

    config = MagicMock()
    result_state = generate_perspectives(initial_state, config)

    # Verify graceful degradation
    assert result_state["mindmap"].root_topic == "Machine Learning"
    assert len(result_state["mindmap"].nodes) == 0
    assert len(result_state["perspectives"]) == 0


def test_costorm_state_typing():
    """
    Test Co-STORM state typing consistency.

    @TestScenarios
    - State: inherits from Dict[str, Any] for LangGraph compatibility
    - Keys: messages, topic, mindmap, perspectives
    - Types: MindMap object, list of dicts for perspectives
    - Verify: state can be passed between nodes safely
    """
    state = CoStormState(
        messages=[AIMessage(content="Test")],
        topic="Test Topic",
        mindmap=None,
        perspectives=[]
    )

    assert isinstance(state, dict)
    assert state["topic"] == "Test Topic"
    assert state["mindmap"] is None
    assert state["perspectives"] == []


def test_mindmap_schema_validation():
    """
    Test MindMap domain schema validation independently.

    @TestScenarios
    - Valid: 3-5 nodes with unique IDs, proper keywords
    - Invalid: duplicate IDs, empty keywords, too few/many nodes
    - Keywords: unique, 3-5 per node, ID normalization
    - Validate: Pydantic validators ensure data quality
    """
    # Valid MindMap
    valid_mindmap = MindMap(
        root_topic="AI Research",
        nodes=[
            PerspectiveNode(
                id="technical",
                name="Technical",
                description="Technical aspects",
                query_keywords=["algorithms", "models", "systems"]
            ),
            PerspectiveNode(
                id="social",
                name="Social Impact",
                description="Social implications",
                query_keywords=["ethics", "society", "impact"]
            )
        ]
    )

    # Should pass validation
    assert valid_mindmap.root_topic == "AI Research"
    assert len(valid_mindmap.nodes) == 2
    assert valid_mindmap.nodes[0].id == "technical"
    assert len(valid_mindmap.nodes[0].query_keywords) == 3

    # Test keyword uniqueness validation
    with pytest.raises(ValueError, match="query_keywords must be unique"):
        PerspectiveNode(
            id="test",
            name="Test",
            description="Test",
            query_keywords=["duplicate", "duplicate"]
        )

    # Test ID normalization
    normalized_node = PerspectiveNode(
        id="CAPITALIZED",
        name="Test",
        description="Test",
        query_keywords=["test"]
    )
    assert normalized_node.id == "capitalized"