"""
Tests for Librarian Node in Co-STORM Discourse Loop

Tests the librarian_node function that searches papers for mind map perspectives.
Mocks the PaperSearcherPort to avoid external API dependencies.

@Hexagonal Testing:
-Mocks infrastructure (PaperSearcherPort) for isolation
-Tests domain behavior and state updates
-Verifies error handling and edge cases
"""

import pytest
from unittest.mock import Mock, patch

from agent.domain.schemas.mindmap import MindMap, PerspectiveNode
from agent.domain.schemas.paper import Paper, OpenAccessInfo
from agent.application.nodes.librarian import librarian_node
from agent.application.nodes.costorm import CoStormState


class TestLibrarianNode:
    """Test suite for librarian_node function."""

    @pytest.fixture
    def mock_paper_searcher(self):
        """Mock the PaperSearcherPort for testing."""
        mock_searcher = Mock()
        mock_searcher.search_papers.return_value = [
            Paper(
                doi="10.1234/test.001",
                title="Test Paper 1",
                authors=["Author One"],
                publication_date=None,
                publisher="Test Publisher",
                abstract="Abstract 1",
                oa_info=OpenAccessInfo(is_oa=True, oa_status="gold", oa_url="http://example.com/1")
            ),
            Paper(
                doi="10.1234/test.002",
                title="Test Paper 2",
                authors=["Author Two"],
                publication_date=None,
                publisher="Test Publisher",
                abstract="Abstract 2",
                oa_info=OpenAccessInfo(is_oa=False, oa_status="closed")
            )
        ]
        return mock_searcher

    @pytest.fixture
    def sample_mindmap(self):
        """Sample mindmap for testing."""
        return MindMap(
            root_topic="Test Topic",
            nodes=[
                PerspectiveNode(
                    id="methodological",
                    name="Methodological Perspective",
                    description="Methods description",
                    query_keywords=["methods", "algorithms", "techniques"]
                ),
                PerspectiveNode(
                    id="historical",
                    name="Historical Perspective",
                    description="History description",
                    query_keywords=["history", "evolution"]
                )
            ]
        )

    @patch('agent.application.nodes.librarian.get_paper_searcher')
    def test_populates_empty_papers_from_mindmap(self, mock_get_searcher, mock_paper_searcher, sample_mindmap):
        """Test that librarian populates papers for nodes without existing papers."""
        # Setup
        mock_get_searcher.return_value = mock_paper_searcher
        state = CoStormState(
            topic="Test Topic",
            mindmap=sample_mindmap
        )

        # Execute
        result = librarian_node(state)

        # Verify
        assert len(result["mindmap"].nodes[0].papers) == 2  # Mock returns 2 papers
        assert len(result["mindmap"].nodes[1].papers) == 2
        assert result["documents"]["methodological"][0].doi == "10.1234/test.001"
        assert result["documents"]["historical"][1].doi == "10.1234/test.002"
        mock_paper_searcher.search_papers.assert_any_call(["methods", "algorithms", "techniques"])
        mock_paper_searcher.search_papers.assert_any_call(["history", "evolution"])

    @patch('agent.application.nodes.librarian.get_paper_searcher')
    def test_skips_nodes_with_existing_papers(self, mock_get_searcher, mock_paper_searcher, sample_mindmap):
        """Test that librarian skips nodes that already have papers."""
        # Setup: Pre-populate first node with papers
        mock_get_searcher.return_value = mock_paper_searcher
        existing_papers = [
            Paper(doi="10.9999/existing.001", title="Existing Paper", authors=["Existing Author"])
        ]
        sample_mindmap.nodes[0].papers = existing_papers

        state = CoStormState(
            topic="Test Topic",
            mindmap=sample_mindmap
        )

        # Execute
        result = librarian_node(state)

        # Verify: First node unchanged, second node gets new papers
        assert result["mindmap"].nodes[0].papers == existing_papers  # Unchanged
        assert len(result["mindmap"].nodes[1].papers) == 2  # New papers
        assert mock_paper_searcher.search_papers.call_count == 1  # Only called once

    @patch('agent.application.nodes.librarian.get_paper_searcher')
    def test_handles_empty_mindmap_gracefully(self, mock_get_searcher):
        """Test librarian handles missing mindmap gracefully."""
        # Setup
        mock_get_searcher.return_value = Mock()

        state = CoStormState(
            topic="Test Topic"
            # No mindmap
        )

        # Execute
        result = librarian_node(state)

        # Verify
        assert result["documents"] == {}
        # Should not crash

    @patch('agent.application.nodes.librarian.get_paper_searcher')
    def test_handles_search_errors_gracefully(self, mock_get_searcher, sample_mindmap):
        """Test that search errors don't crash the workflow."""
        # Setup: Mock searcher raises exception for first node
        mock_searcher = Mock()
        mock_searcher.search_papers.side_effect = [
            Exception("Search failed"),  # First call fails
            []  # Second call succeeds but returns empty
        ]
        mock_get_searcher.return_value = mock_searcher

        state = CoStormState(
            topic="Test Topic",
            mindmap=sample_mindmap
        )

        # Execute
        result = librarian_node(state)

        # Verify: Workflow continues with empty lists
        assert result["mindmap"].nodes[0].papers == []  # Failed search
        assert result["mindmap"].nodes[1].papers == []  # Empty results
        assert result["documents"]["methodological"] == []
        assert result["documents"]["historical"] == []

    @patch('agent.application.nodes.librarian.get_paper_searcher')
    def test_preserves_existing_documents_dict(self, mock_get_searcher, mock_paper_searcher, sample_mindmap):
        """Test that existing documents are preserved."""
        # Setup: Existing documents in state
        mock_get_searcher.return_value = mock_paper_searcher

        existing_docs = {"existing_key": [Paper(doi="10.9999/old.001", title="Old Paper")]}

        state = CoStormState(
            topic="Test Topic",
            mindmap=sample_mindmap,
            documents=existing_docs  # Already has some documents
        )

        # Execute
        result = librarian_node(state)

        # Verify: Both old and new documents present
        assert result["documents"]["existing_key"][0].doi == "10.9999/old.001"  # Preserved
        assert len(result["documents"]["methodological"]) == 2  # New
        assert len(result["documents"]["historical"]) == 2  # New