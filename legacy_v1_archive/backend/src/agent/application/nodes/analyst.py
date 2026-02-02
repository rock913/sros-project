"""
Analyst Node for Co-STORM Discourse Loop

This module implements the Analyst node that reads papers collected by Librarian
and synthesizes perspective summaries through LLM analysis.

@Co-STORM Algorithm:
Part of Sprint 2: From papers -> synthesize perspective summaries -> enable gap analysis
Each perspective gets a coherent summary combining insights from multiple papers.

@Hexagonal Architecture (Refactored):
- Application layer: AnalystNode class with dependency-injected LLMProviderPort
- Domain isolation: Uses domain prompts only, no direct infrastructure calls
- Infrastructure abstraction: Replaces litellm direct calls with port-based composition
- Testable design: All dependencies mockable for isolated unit testing

@Refactoring History:
- Before: Function-based, direct litellm calls (violated hexagonal architecture)
- After: Class-based, dependency injection compliant
"""

from typing import List

from agent.domain.prompts.costorm import ANALYST_PROMPT
from agent.domain.schemas.paper import Paper
from agent.domain.ports.llm_provider import LLMProviderPort
from agent.infrastructure.observability.langfuse_tracer import get_langfuse_tracer
from agent.application.nodes.costorm import CoStormState


class AnalystNode:
    """Refactored Analyst Node using hexagonal architecture principles.

    @Hexagonal Architecture:
    - Constructor injection: LLMProviderPort dependency for infrastructure abstraction
    - Domain purity: Uses only configuration-free domain logic
    - Error resilience: Graceful degradation with meaningful fallback summaries
    - Observable: Structured logging for monitoring node execution

    @TestScenarios (verified via TDD)
    - Constructor: Accepts LLMProviderPort, validates injection
    - State processing: Returns updated CoStormState with populated summaries
    - LLM integration: Uses port.generate_text() instead of direct litellm calls
    - Error handling: Fallback summaries for failed LLM operations
    """

    def __init__(self, llm_provider: LLMProviderPort):
        """Initialize AnalystNode with injected infrastructure dependencies.

        Args:
            llm_provider: Domain port for LLM operations (dependency injection)
        """
        self.llm_provider = llm_provider

    async def process_node(self, node, state: CoStormState) -> None:
        """Process a single mindmap node to generate LLM summary.

        This method analyzes papers for a specific perspective and generates
        a coherent summary using the injected LLM provider.

        Args:
            node: MindMap perspective node with papers to analyze
            state: CoStormState for accessing session context

        @Internal Test Scenarios:
        - Populates node.summary with LLM-generated content
        - Handles papers array correctly
        - Fallback behavior on LLM errors
        """
        if not node.papers or node.summary:  # Skip if no papers or already summarized
            return

        print(f"Analyzing papers for node '{node.id}': {len(node.papers)} papers")

        try:
            # Format papers for LLM context (domain model serialization)
            papers_data = [paper.model_dump() for paper in node.papers]
            papers_json = str(papers_data)

            # Use domain prompt for structured synthesis
            prompt = ANALYST_PROMPT.format(
                papers_json=papers_json,
                perspective_name=node.name
            )

            # Hexagonal architecture: Call infrastructure via port (not direct litellm)
            summary = await self.llm_provider.generate_text(prompt)

            # Update node in-place (mutable for LangGraph compatibility)
            node.summary = summary.strip()
            print(f"✓ Generated {len(summary)} char summary for '{node.id}'")

        except Exception as e:
            print(f"ERROR: Failed to analyze '{node.id}': {e}")
            # Graceful degradation maintains workflow continuity
            node.summary = f"Unable to synthesize summary for {node.name}: {str(e)}"

    async def __call__(self, state: CoStormState) -> CoStormState:
        """LangGraph-compatible interface for state transformation.

        This method allows AnalystNode to be used directly as a LangGraph node,
        maintaining backward compatibility with the existing graph structure.

        Args:
            state: Co-STORM state containing mindmap with nodes to analyze

        Returns:
            Updated state with populated perspective summaries

        @State Transformation:
        - Input: mindmap with nodes containing papers
        - Output: mindmap with nodes containing synthesized summaries
        """
        print("---CO-STORM NODE: AnalystNode---")

        if not state.get("mindmap"):
            print("WARNING: No mindmap in state, analyst has nothing to analyze")
            return state

        mindmap = state["mindmap"]

        # Process each node that needs summarization
        for node in mindmap.nodes:
            await self.process_node(node, state)

        print("✓ AnalystNode completed: perspective summaries generated")
        return state


# Backward compatibility function - delegates to AnalystNode
# Allows gradual migration of graph dependencies
async def analyst_node(state: CoStormState) -> CoStormState:
    """Backward compatible wrapper for AnalystNode.

    This function maintains API compatibility while transitioning to
    the refactored hexagonal architecture. Long-term plan: update
    costorm_graph.py to use AnalystNode directly.

    @Migration Strategy:
    - Current: analyst_node function delegates to AnalystNode
    - Future: costorm_graph.py directly imports and configures AnalystNode
    - Removal: analyst_node function will be removed once all usages migrated
    """
    # Factory function for AnalystNode will be injected later
    from agent.infrastructure.llm.provider import create_llm_provider
    llm_provider = create_llm_provider("dashscope")  # Default configuration

    analyst = AnalystNode(llm_provider)
    return await analyst(state)
