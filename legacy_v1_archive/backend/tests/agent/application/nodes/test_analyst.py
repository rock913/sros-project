"""
Tests for Analyst Node Refactoring

TDD implementation to verify AnalystNode class uses hexagonal architecture properly.

@TDD Process:
1. Initial failing test: AnalystNode is imported and instantiates correctly
2. Implementation: Refactor analyst_node function to AnalystNode class
3. Migration test: Verify no breaking changes to workflow graph

@Hexagonal Architecture Test Scenarios:
- Class instantiation: Accepts LLMProviderPort dependency injection
- LLM provider usage: Calls generate_text() via mocked provider
- Error handling: Graceful degradation when LLM fails
- State updates: Populates node.summary field correctly
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

# Test will initially fail - AnalystNode class doesn't exist yet
try:
    from agent.application.nodes.analyst import AnalystNode
    ANALYST_NODE_EXISTS = True
except ImportError:
    ANALYST_NODE_EXISTS = False


@pytest.mark.asyncio
class TestAnalystNodeTDD:
    """Test suite for AnalystNode class following hexagonal architecture principles."""

    def test_analyst_node_class_exists(self):
        """TDD Step 1: Initially failing test - AnalystNode class should exist."""
        # This test should fail initially until we implement AnalystNode
        assert ANALYST_NODE_EXISTS, "AnalystNode class must be implemented. Run: aider --read $INTERFACE --read $SCHEMA analyst_node.py"

    def test_analyst_node_instantiation(self):
        """Test that AnalystNode can be instantiated with required dependencies."""
        mock_llm_provider = AsyncMock()
        analyst = AnalystNode(llm_provider=mock_llm_provider)
        assert hasattr(analyst, 'llm_provider')
        assert analyst.llm_provider == mock_llm_provider

    @pytest.mark.asyncio
    async def test_analyst_node_uses_llm_provider(self):
        """Test that AnalystNode uses injected LLM provider instead of direct litellm calls."""
        from agent.domain.schemas.mindmap import PerspectiveNode
        from agent.domain.schemas.paper import Paper

        mock_llm_provider = AsyncMock()
        mock_llm_provider.generate_text.return_value = "Synthesized summary text"
        analyst = AnalystNode(llm_provider=mock_llm_provider)

        # Test node with papers
        node = PerspectiveNode(
            id="test_perspective",
            name="Test Perspective",
            description="A test perspective",
            query_keywords=["test"]
        )
        node.papers = [MagicMock(title="Test Paper", authors=["Test Author"])]
        node.summary = None

        # Test state (needed for process_node call)
        state = {"session_id": "test123"}

        await analyst.process_node(node, state)
        mock_llm_provider.generate_text.assert_called_once()
        assert node.summary == "Synthesized summary text"

    @pytest.mark.asyncio
    async def test_analyst_node_error_handling(self):
        """Test graceful error handling when LLM provider fails."""
        pytest.skip("Implement AnalystNode class first")
        # Should populate fallback summary on LLM errors

    @pytest.mark.asyncio
    async def test_analyst_node_backwards_compatibility(self):
        """Test that AnalystNode maintains same interface as original analyst_node function."""
        pytest.skip("Implement AnalystNode class first")
        # Should be callable from CoStormState -> CoStormState


# Integration test for backward compatibility - analyst_node wrapper
@pytest.mark.asyncio
async def test_backward_compatibility_analyst_node_wrapper():
    """Test that analyst_node wrapper function maintains backward compatibility."""
    from agent.application.nodes.analyst import analyst_node

    # Verify it's a callable function (backward compatibility wrapper)
    assert callable(analyst_node), "analyst_node wrapper should be callable"

    # Verify it can be called (smoke test)
    state = {"mindmap": None}  # Empty state
    result = await analyst_node(state)
    assert result is state or isinstance(result, dict), "Function should return dict-like state"
