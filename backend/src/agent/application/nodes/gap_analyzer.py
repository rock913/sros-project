import logging
from typing import List
from agent.domain.ports.gap_analyzer import IGapAnalyzer
from agent.domain.schemas.draft import DraftContext, EvidenceGap
from agent.domain.ports.llm import LanguageModel


logger = logging.getLogger(__name__)


class GapAnalyzerNode:
    """
    Application node for gap analysis in the research workflow.

    This node coordinates the gap analysis process by:
    - Taking draft context as input
    - Delegating analysis to the infrastructure gap analyzer
    - Returning the list of identified evidence gaps
    """

    def __init__(self, gap_analyzer: IGapAnalyzer):
        """
        Initialize the Gap Analyzer node.

        Args:
            gap_analyzer: Injected infrastructure gap analyzer implementation.
        """
        self.gap_analyzer = gap_analyzer

    async def analyze_draft_gaps(self, draft_context: DraftContext) -> List[EvidenceGap]:
        """
        Analyze the provided draft for evidence gaps.

        This is the main entry point for gap analysis in the research workflow.

        Args:
            draft_context: Context of the research draft to analyze.

        Returns:
            List of identified evidence gaps that should be filled via Co-STORM.
        """
        logger.info("Starting evidence gap analysis for draft")
        logger.debug(f"Draft length: {len(draft_context.content)} characters")

        try:
            gaps = await self.gap_analyzer.analyze(draft_context)

            logger.info(f"Gap analysis complete: identified {len(gaps)} evidence gaps")
            if gaps:
                high_confidence = [g for g in gaps if g.is_high_confidence]
                logger.info(f"High confidence gaps: {len(high_confidence)}")

            return gaps

        except Exception as e:
            logger.error(f"Gap analysis failed: {e}", exc_info=True)
            raise