"""
Librarian Node for Co-STORM Discourse Loop

This module implements the Librarian node that searches academic papers for each mind map perspective.
The Librarian processes nodes sequentially (or in parallel via LangGraph fan-out), using the PaperSearcher port
to populate node.papers from query_keywords.

@Co-STORM Algorithm:
Part of Sprint 2: From MindMap with 3-5 perspectives -> populate papers -> enable Analyst node synthesis

@Hexagonal Architecture:
- Application layer: Orchestrates port usage, domain logic
- Uses PaperSearcherPort: Can be mocked for testing, supports Arxiv/Multi-provider
- State Updates: Populates perspectives' node.papers and state.documents dict
"""

from typing import Dict, List

from agent.domain.schemas.mindmap import MindMap, PerspectiveNode
from agent.domain.schemas.paper import Paper
from agent.domain.ports.paper_searcher import get_paper_searcher
from agent.application.nodes.costorm import CoStormState


async def librarian_node(state: CoStormState) -> CoStormState:
    """Search for papers across all MindMap perspectives.

    Iterates over mindmap.nodes, calling PaperSearcher for each node's query_keywords.
    Updates both node.papers and state.documents dictionary for inter-node communication.

    @TestScenarios
    - mindmap with 3 nodes: each node gets papers populated in node.papers
    - state.documents: populated with {node_id: papers} for analyst consumption
    - empty keywords: handles gracefully without crashing workflow
    - search error: partial failures don't block other nodes

    Args:
        state: Co-STORM state containing populated mindmap

    Returns:
        Updated state with papers populated in mindmap.nodes and documents dict
    """
    print("---CO-STORM NODE: librarian---")

    if not state.get("mindmap"):
        print("WARNING: No mindmap in state, librarian has nothing to search")
        return {**state, "documents": {}}

    mindmap: MindMap = state["mindmap"]
    searcher = get_paper_searcher()  # Factory: gets port implementation

    updated_documents: Dict[str, List[Paper]] = state.get("documents", {}).copy()

    for node in mindmap.nodes:
        if not node.papers:  # Only search if not already populated
            print(f"Searching for node '{node.id}': {node.query_keywords}")

            try:
                papers = await searcher.search_papers(node.query_keywords)  # Port usage
                node.papers = papers  # Update node in-place (MindMap mutable)

                # Add to documents dict for analyst consumption
                updated_documents[node.id] = papers

                print(f"✓ Found {len(papers)} papers for '{node.id}'")

            except Exception as e:
                print(f"ERROR: Failed to search for '{node.id}': {e}")
                # Graceful degradation: empty papers list allows workflow continuation
                node.papers = []
                updated_documents[node.id] = []

    print(f"✓ Librarian completed: {len(updated_documents)} perspectives processed")

    return {
        **state,
        "documents": updated_documents
    }


# Placeholder for future parallel implementation via LangGraph fan-out
async def search_node_papers(node: PerspectiveNode) -> Dict[str, List[Paper]]:
    """Search papers for a single node (for future parallel processing).

    This function would be used with LangGraph.to_run or similar
    for parallel paper searching across multiple nodes simultaneously.
    """
    searcher = get_paper_searcher()
    papers = await searcher.search_papers(node.query_keywords)
    node.papers = papers  # Update in-place
    return {node.id: papers}
