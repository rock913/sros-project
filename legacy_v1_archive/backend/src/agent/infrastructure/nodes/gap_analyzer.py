import json
import logging
from typing import List
import asyncio
from agent.domain.ports.gap_analyzer import IGapAnalyzer
from agent.domain.schemas.draft import DraftContext, EvidenceGap
from agent.domain.ports.llm import LanguageModel


logger = logging.getLogger(__name__)


class GapAnalyzerAdapter(IGapAnalyzer):
    """
    Infrastructure adapter implementing evidence gap analysis using LLM.

    Acts as an "Academic Reviewer" that critically examines research drafts
    to identify places where claims lack supporting evidence.
    """

    def __init__(self, llm_adapter: LanguageModel):
        """
        Initialize the gap analyzer with LLM dependency.

        Args:
            llm_adapter: Injected LLM adapter for making completion calls.
        """
        self.llm_adapter = llm_adapter

    async def analyze(self, context: DraftContext) -> List[EvidenceGap]:
        """
        Analyze draft context for evidence gaps using LLM.

        Args:
            context: The draft content and optional cursor position to analyze.

        Returns:
            List of identified evidence gaps that should be filled via Co-STORM.
        """
        if not context.content.strip():
            return []

        # Construct academic reviewer prompt
        prompt = self._build_analysis_prompt(context)

        try:
            # Call LLM with structured output request (run sync generate in executor)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.llm_adapter.generate(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4o",  # TODO: Make configurable
                )
            )

            # Parse JSON response
            gaps_data = self._parse_llm_response(response.content)

            # Convert to EvidenceGap objects
            gaps = [EvidenceGap(**gap_data) for gap_data in gaps_data]

            logger.info(f"Identified {len(gaps)} evidence gaps in draft")
            return gaps

        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            return []

    def _build_analysis_prompt(self, context: DraftContext) -> str:
        """Build the academic reviewer prompt for gap analysis."""
        base_prompt = """You are an Academic Reviewer critically examining a research manuscript draft.

Your task is to identify "evidence gaps" - places where the author makes claims, describes advantages, or presents facts without sufficient supporting evidence, data, or citations.

Focus areas:
- Claims about performance, accuracy, speed, or other metrics
- Advantages or disadvantages of methods
- Historical or scientific facts
- Statistical claims or measurements

For each gap you find, provide:
- context_snippet: 2-3 sentences of surrounding text (max 500 chars)
- missing_information: What specific evidence/data would strengthen this claim
- search_queries: 1-3 targeted search terms for finding supporting evidence
- confidence: How confident you are this is a real gap (0.0-1.0)

IMPORTANT:
- Only identify REAL gaps - do not criticize writing style, grammar, or clarity
- If the draft is well-cited, return []
- Return ONLY a JSON array of gap objects
- No additional text or explanation
"""

        if context.cursor_position:
            cursor_info = f"\nFocus your analysis on content near line {context.cursor_position[0]}, as this is where the author is currently working."
            base_prompt += cursor_info

        draft_section = f"""

DRAFT CONTENT TO ANALYZE:
{context.content}

Return your analysis as a JSON array:"""

        return base_prompt + draft_section

    def _parse_llm_response(self, response_content: str) -> List[dict]:
        """
        Parse LLM response into structured gap data.

        Args:
            response_content: Raw LLM response text.

        Returns:
            List of gap dictionaries ready for EvidenceGap construction.
        """
        try:
            # Clean response content
            content = response_content.strip()

            # Remove any markdown code blocks
            if content.startswith("```"):
                lines = content.split("\n")
                # Find JSON start
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip() in ["```", "```json"]:
                        continue
                    if line.strip() and not line.startswith("```"):
                        json_start = i
                        break

                if json_start >= 0:
                    content = "\n".join(lines[json_start:])

                # Remove closing ```
                if content.endswith("```"):
                    content = content[:-3].strip()

            # Parse JSON
            gaps_data = json.loads(content)

            if not isinstance(gaps_data, list):
                logger.warning("LLM response was not a JSON array")
                return []

            # Validate structure
            validated_gaps = []
            for gap in gaps_data:
                if isinstance(gap, dict) and self._validate_gap_structure(gap):
                    validated_gaps.append(gap)
                else:
                    logger.warning(f"Skipping invalid gap structure: {gap}")

            return validated_gaps

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            return []

    def _validate_gap_structure(self, gap: dict) -> bool:
        """Validate that a gap dict has required EvidenceGap fields."""
        required_fields = ["context_snippet", "missing_information", "search_queries", "confidence"]

        for field in required_fields:
            if field not in gap:
                return False

        # Additional validations
        if not isinstance(gap["search_queries"], list) or not gap["search_queries"]:
            return False

        if not isinstance(gap["confidence"], (int, float)) or not (0.0 <= gap["confidence"] <= 1.0):
            return False

        return True