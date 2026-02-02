"""
Integration Test for Librarian Node

Validates librarian_node integration within Co-STORM workflow.
Tests the Librarian -> Analyst data flow using PaperSearcherPort.

@Integration Test Scenarios:
- librarian_node calls PaperSearcher.search_papers()
- Updates mindmap.nodes.papers and state.documents
- Handles search failures gracefully
- Supports multiple nodes processing
"""

import pytest
from unittest.mock import AsyncMock, patch

from agent.domain.schemas.mindmap import MindMap, PerspectiveNode
from agent.domain.schemas.paper import Paper
from agent.application.nodes.costorm import CoStormState


@pytest.mark.asyncio
async def test_librarian_node_integration_with_mock_searcher():
    """Integration test: librarian_node connects PaperSearcherPort correctly."""
    from agent.application.nodes.librarian import librarian_node

    # Create fake papers that would typically come from Arxiv
    fake_papers = [
        Paper(
            title="Paper One: Deep Learning Methods",
            authors=["Author A", "Author B"],
            doi="10.1234/paper1"
        ),
        Paper(
            title="Paper Two: Neural Network Optimization",
            authors=["Author C"],
            doi="10.1234/paper2"
        )
    ]

    # Mock the PaperSearcher.get_paper_searcher() factory
    with patch('agent.application.nodes.librarian.get_paper_searcher') as mock_get_searcher:
        mock_searcher = AsyncMock()
        mock_searcher.search_papers.return_value = fake_papers
        mock_get_searcher.return_value = mock_searcher

        # Create mindmap with three nodes (minimum required)
        mindmap = MindMap(
            root_topic="Machine Learning",
            nodes=[
                PerspectiveNode(
                    id="methodological",
                    name="Methodological Approaches",
                    description="Core algorithms and techniques",
                    query_keywords=["deep learning", "neural networks"]
                ),
                PerspectiveNode(
                    id="applications",
                    name="Applications",
                    description="Real-world applications",
                    query_keywords=["machine learning applications"]
                ),
                PerspectiveNode(
                    id="theoretical",
                    name="Theoretical Foundations",
                    description="Mathematical and theoretical foundations",
                    query_keywords=["machine learning theory", "mathematical foundations"]
                )
            ]
        )

        # Initial state with mindmap, no papers populated
        state: CoStormState = {
            "mindmap": mindmap,
            "documents": {}
        }

        # Execute librarian_node
        updated_state = await librarian_node(state)

        # Verify PaperSearcher was called for each node that doesn't have papers
        assert mock_searcher.search_papers.call_count == 3

        # Verify papers were populated in mindmap nodes
        assert updated_state["mindmap"].nodes[0].papers == fake_papers
        assert updated_state["mindmap"].nodes[1].papers == fake_papers

        # Verify documents dict was populated
        documents = updated_state.get("documents", {})
        assert "methodological" in documents
        assert "applications" in documents
        assert all(isinstance(paper, Paper) for paper in documents["methodological"])


@pytest.mark.asyncio
async def test_librarian_node_handles_search_failures():
    """Test graceful handling of PaperSearcher failures."""
    from agent.application.nodes.librarian import librarian_node

    # Create mindmap with three nodes (minimum required)
    mindmap = MindMap(
        root_topic="Test Topic",
        nodes=[
            PerspectiveNode(
                id="test_node",
                name="Test Node",
                description="Test description",
                query_keywords=["test"]
            ),
            PerspectiveNode(
                id="secondary",
                name="Secondary Perspective",
                description="Additional test perspective",
                query_keywords=["secondary", "test"]
            ),
            PerspectiveNode(
                id="tertiary",
                name="Tertiary Perspective",
                description="Third test perspective",
                query_keywords=["tertiary"]
            )
        ]
    )

    # Mock searcher that raises exception
    with patch('agent.application.nodes.librarian.get_paper_searcher') as mock_get_searcher:
        mock_searcher = AsyncMock()
        mock_searcher.search_papers.side_effect = Exception("Network timeout")
        mock_get_searcher.return_value = mock_searcher

        state: CoStormState = {
            "mindmap": mindmap,
            "documents": {}
        }

        # Execute librarian_node
        updated_state = await librarian_node(state)

        # Verify graceful degradation: empty papers list
        assert updated_state["mindmap"].nodes[0].papers == []
        assert updated_state["documents"]["test_node"] == []


@pytest.mark.asyncio
async def test_librarian_node_skips_already_populated_nodes():
    """Test that librarian_node skips nodes with existing papers."""
    from agent.application.nodes.librarian import librarian_node

    # Create mindmap with pre-populated node
    existing_paper = Paper(
        title="Existing Paper",
        authors=["Test Author"],
        doi="10.1234/existing"
    )

    mindmap = MindMap(
        root_topic="Test Topic",
        nodes=[
            PerspectiveNode(
                id="existing_node",
                name="Existing Node",
                description="Already has papers",
                query_keywords=["existing"],
                papers=[existing_paper]  # Already populated
            ),
            PerspectiveNode(
                id="empty_node",
                name="Empty Node",
                description="Needs papers",
                query_keywords=["new"]
            ),
            PerspectiveNode(
                id="third_node",
                name="Third Node",
                description="Unpopulated third node",
                query_keywords=["third"]
            )
        ]
    )

    fake_papers = [Paper(title="New Paper", authors=["New Author"], doi="10.1234/new")]

    with patch('agent.application.nodes.librarian.get_paper_searcher') as mock_get_searcher:
        mock_searcher = AsyncMock()
        mock_searcher.search_papers.return_value = fake_papers
        mock_get_searcher.return_value = mock_searcher

        state: CoStormState = {
            "mindmap": mindmap,
            "documents": {}
        }

        updated_state = await librarian_node(state)

        # Existing node unchanged, empty node populated
        assert updated_state["mindmap"].nodes[0].papers == [existing_paper]
        assert updated_state["mindmap"].nodes[1].papers == fake_papers

        # Should search for the nodes that don't have papers
        assert mock_searcher.search_papers.call_count == 2
