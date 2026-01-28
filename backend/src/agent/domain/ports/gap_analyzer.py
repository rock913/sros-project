from abc import ABC, abstractmethod
from typing import List
from agent.domain.schemas.draft import DraftContext, EvidenceGap


class IGapAnalyzer(ABC):
    """
    Protocol for analyzing research drafts to identify evidence gaps.

    This analyzer acts as an "Academic Reviewer" that critically examines
    draft content to find places where claims lack supporting evidence.

    @TestScenarios:
    1. Empty draft returns empty gap list:
       - Input: DraftContext(content="")
       - Output: []

    2. Claim without evidence creates gap:
       - Input: DraftContext(content="Transformer models are very fast.")
       - Output: [EvidenceGap(missing='data supporting speed claim', confidence=0.8)]

    3. Well-cited content returns no gaps:
       - Input: DraftContext(content="Transformer speed is proven [@Vaswani2017, @Brown2020]")
       - Output: []

    4. Multiple gaps identified:
       - Input: DraftContext with 3 unsupported claims
       - Output: Exactly 3 EvidenceGap objects

    5. Focus cursor analysis:
       - Input: DraftContext with cursor on specific line
       - Output: Gaps prioritized near cursor position

    6. Invalid draft-handling:
       - Input: DraftContext(content=None) -> raises ValueError
       - Note: Domain validation handles this before reaching analyzer
    """

    @abstractmethod
    async def analyze(self, context: DraftContext) -> List[EvidenceGap]:
        """
        Analyze the provided draft context for evidence gaps.

        Args:
            context: The draft content and optional cursor position to analyze.

        Returns:
            List of identified evidence gaps that should be filled via Co-STORM.

        Note:
            This is pure domain logic - no I/O. Implementation may use LLM
            adapters injected during construction, but calls are awaitable
            to support async LLM services.
        """
        pass