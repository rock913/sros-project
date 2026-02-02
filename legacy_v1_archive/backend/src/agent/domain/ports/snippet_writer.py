from abc import ABC, abstractmethod
from typing import List
from agent.domain.schemas.draft import EvidenceGap, DraftImprovement
from agent.domain.schemas.mindmap import CoStormState


class ISnippetWriter(ABC):
    """
    Protocol for writing improved text snippets to fill evidence gaps.

    This writer specializes in scholarly text improvement by:
    - Taking an evidence gap and supporting Co-STORM research results
    - Synthesizing a natural-looking paragraph with citations
    - Maintaining the original draft's academic tone and style

    @TestScenarios:
    1. Empty gap list returns empty improvements:
       - Input: [] gaps, CoStormState with papers
       - Output: []

    2. Single gap produces cited improvement:
       - Input: [EvidenceGap], CoStormState with 3 relevant papers
       - Output: [DraftImprovement] with citations matching paper sources

    3. Multiple gaps produce multiple targeted improvements:
       - Input: [Gap1, Gap2], CoStormState with diverse papers
       - Output: [Improvement1, Improvement2] addressing respective gaps

    4. Insufficient research produces low-quality suggestion:
       - Input: EvidenceGap, CoStormState with irrelevant papers
       - Output: DraftImprovement with disclaimers about weak evidence

    5. Citation integration maintains academic standards:
       - Input: Gap about Transformer speed
       - Output: Text with proper [@AuthorYear] citations

    6. Style preservation matches original draft tone:
       - Input: Original text "Transformers are fast."
       - Output: Improved text using similar academic language
    """

    @abstractmethod
    async def write_for_gap(self, gap: EvidenceGap, costorm_state: CoStormState) -> DraftImprovement:
        """
        Write an improved text snippet for a single evidence gap.

        Args:
            gap: The evidence gap to address with writing.
            costorm_state: Research results from Co-STORM analysis.

        Returns:
            DraftImprovement containing the patch text and citations.

        Note:
            This operation is asynchronous to support LLM-based synthesis
            and potential nested Co-STORM workflow calls.
        """
        pass

    @abstractmethod
    async def write_for_gaps(self, gaps: List[EvidenceGap], costorm_state: CoStormState) -> List[DraftImprovement]:
        """
        Write improved text snippets for multiple evidence gaps.

        Args:
            gaps: List of evidence gaps to address.
            costorm_state: Research results from Co-STORM analysis.

        Returns:
            List of draft improvements, one per gap.

        Note:
            Default implementation processes gaps sequentially.
            Subclasses may optimize with batch processing if LLM allows.
        """
        pass