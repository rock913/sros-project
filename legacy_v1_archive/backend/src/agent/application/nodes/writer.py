import logging
from typing import List
from agent.domain.ports.snippet_writer import ISnippetWriter
from agent.domain.schemas.draft import EvidenceGap, DraftImprovement
from agent.domain.schemas.mindmap import CoStormState
from agent.application.workflows.costorm_graph import CoStormGraph


logger = logging.getLogger(__name__)


class WriterNode:
    """
    Application node for incremental writing with nested Co-STORM integration.

    This node enables "Agentic Editor" capabilities by:
    - Taking evidence gaps identified from draft analysis
    - Running nested Co-STORM workflows to gather research for each gap
    - Synthesizing improved text snippets with citations
    - Returning targeted improvements for gap filling
    """

    def __init__(self, snippet_writer: ISnippetWriter, costorm_graph: CoStormGraph):
        """
        Initialize the writer node with dependencies.

        Args:
            snippet_writer: Port for writing improved text snippets.
            costorm_graph: Nested Co-STORM workflow for gap-specific research.
        """
        self.snippet_writer = snippet_writer
        self.costorm_graph = costorm_graph

    async def fill_gaps_with_research(self, gaps: List[EvidenceGap]) -> List[DraftImprovement]:
        """
        Fill multiple evidence gaps by executing nested Co-STORM research.

        This is the main entry point for incremental writing in the research workflow.

        Args:
            gaps: Evidence gaps identified from draft analysis.

        Returns:
            List of draft improvements with synthesized text and citations.
        """
        logger.info(f"Starting incremental writing for {len(gaps)} gaps")

        if not gaps:
            logger.info("No gaps to fill, returning empty list")
            return []

        improvements = []

        for gap in gaps:
            logger.debug(f"Processing gap: {gap.missing_information}")
            try:
                improvement = await self._fill_single_gap(gap)
                improvements.append(improvement)

            except Exception as e:
                logger.error(f"Failed to fill gap {gap.id}: {e}")
                # Create a fallback improvement
                fallback = DraftImprovement(
                    gap_id=gap.id,
                    original_snippet=gap.context_snippet,
                    suggested_insertion=f"[{gap.missing_information}]",
                    citations=[],
                    rationale=f"Gap filling failed: {str(e)}"
                )
                improvements.append(fallback)

        logger.info(f"Completed incremental writing: {len(improvements)} improvements generated")
        return improvements

    async def _fill_single_gap(self, gap: EvidenceGap) -> DraftImprovement:
        """
        Fill a single evidence gap with targeted research.

        Strategy:
        1. Use gap's search_queries as topics for nested Co-STORM
        2. Execute mini Co-STORM workflow to gather relevant papers
        3. Synthesize improved text using paper findings

        Args:
            gap: The evidence gap to address.

        Returns:
            DraftImprovement with synthesized content.
        """
        logger.debug(f"Executing nested Co-STORM for gap queries: {gap.search_queries}")

        # Prepare mini-research topic from gap queries
        research_topic = gap.search_queries[0] if gap.search_queries else gap.missing_information

        try:
            # Execute nested Co-STORM workflow
            costorm_state = await self.costorm_graph.execute_research_workflow(
                topic=research_topic,
                max_iterations=3  # Limit nested execution depth
            )

            # Use results to write improved snippet
            improvement = await self.snippet_writer.write_for_gap(gap, costorm_state)

            return improvement

        except Exception as e:
            logger.warning(f"Nested Co-STORM failed for gap {gap.id}, using empty state: {e}")
            # Fallback: try to write without research
            empty_state = CoStormState(
                topic=research_topic,
                perspectives=[],
                mindmap_nodes=[],
                papers=[],
                summaries=[],
                final_report=""
            )

            return await self.snippet_writer.write_for_gap(gap, empty_state)