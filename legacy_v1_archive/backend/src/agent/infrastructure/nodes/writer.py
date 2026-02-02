import json
import logging
from typing import List
import asyncio
from agent.domain.ports.snippet_writer import ISnippetWriter
from agent.domain.schemas.draft import EvidenceGap, DraftImprovement
from agent.domain.schemas.mindmap import CoStormState
from agent.domain.ports.llm import LanguageModel


logger = logging.getLogger(__name__)


class SnippetWriterAdapter(ISnippetWriter):
    """
    Infrastructure adapter implementing snippet writing with nested Co-STORM integration.

    This adapter writes improved text snippets that fill evidence gaps by:
    - Analyzing Co-STORM research results
    - Synthesizing natural scholarly paragraphs
    - Integrating proper academic citations
    - Maintaining original draft tone and style
    """

    def __init__(self, llm_adapter: LanguageModel):
        """
        Initialize the snippet writer with dependencies.

        Args:
            llm_adapter: LLM adapter for text synthesis.
        """
        self.llm_adapter = llm_adapter

    async def write_for_gap(self, gap: EvidenceGap, costorm_state: CoStormState) -> DraftImprovement:
        """
        Write an improved snippet for a single evidence gap.

        Args:
            gap: The gap to address with improved writing.
            costorm_state: Research results from Co-STORM analysis.

        Returns:
            DraftImprovement with synthesized text and citations.
        """
        logger.debug(f"Writing snippet for gap: {gap.missing_information}")

        # Extract relevant papers from Co-STORM state
        relevant_papers = self._find_relevant_papers(gap, costorm_state)

        # Build synthesis prompt
        prompt = self._build_synthesis_prompt(gap, relevant_papers)

        try:
            # Call LLM for synthesis
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.llm_adapter.generate(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4o",  # TODO: Make configurable
                )
            )

            # Parse and validate response
            improvement = self._parse_writer_response(gap, response.content, relevant_papers)

            logger.info(f"Generated improvement for gap: {len(improvement.suggested_insertion)} chars")
            return improvement

        except Exception as e:
            logger.error(f"Snippet writing failed for gap {gap.id}: {e}")
            # Return a minimal improvement as fallback
            return DraftImprovement(
                gap_id=gap.id,
                original_snippet=gap.context_snippet,
                suggested_insertion=f"[Note: Could not generate improvement due to error: {str(e)}]",
                citations=[],
                rationale=f"Error during synthesis: {str(e)}"
            )

    async def write_for_gaps(self, gaps: List[EvidenceGap], costorm_state: CoStormState) -> List[DraftImprovement]:
        """
        Write improvements for multiple gaps sequentially.

        Args:
            gaps: List of gaps to address.
            costorm_state: Research state containing relevant papers.

        Returns:
            List of improvements, one per gap.
        """
        logger.info(f"Writing snippets for {len(gaps)} gaps")
        improvements = []

        for gap in gaps:
            improvement = await self.write_for_gap(gap, costorm_state)
            improvements.append(improvement)

        return improvements

    def _find_relevant_papers(self, gap: EvidenceGap, costorm_state: CoStormState) -> List[dict]:
        """
        Find papers relevant to the gap from Co-STORM state.

        This is a simple relevance scoring based on keywords.
        Advanced implementations could use semantic similarity.
        """
        if not costorm_state.papers:
            return []

        relevant = []
        gap_keywords = set(gap.missing_information.lower().split() +
                          ' '.join(gap.search_queries).lower().split())

        for paper in costorm_state.papers:
            paper_text = (paper.get('title', '') + ' ' +
                         paper.get('abstract', '')).lower()

            # Simple keyword matching
            matches = sum(1 for keyword in gap_keywords if keyword in paper_text)
            if matches >= 2:  # Require at least 2 keyword matches
                relevant.append({
                    'id': paper.get('id', paper.get('title', 'Unknown')),
                    'title': paper.get('title', ''),
                    'authors': paper.get('authors', []),
                    'year': paper.get('year'),
                    'relevance_score': matches
                })

        # Sort by relevance and return top 5
        relevant.sort(key=lambda p: p['relevance_score'], reverse=True)
        return relevant[:5]

    def _build_synthesis_prompt(self, gap: EvidenceGap, relevant_papers: List[dict]) -> str:
        """Build the synthesis prompt for the LLM writer."""
        prompt = f"""You are a senior research writer improving a scholarly manuscript.

TASK: Fill this evidence gap with a natural, academic paragraph that integrates research findings.

GAP TO ADDRESS: {gap.missing_information}

ORIGINAL TEXT CONTEXT: {gap.context_snippet}

"""

        if relevant_papers:
            prompt += "\nRELEVANT RESEARCH PAPERS:\n"
            for i, paper in enumerate(relevant_papers, 1):
                authors = ', '.join(paper.get('authors', ['Unknown']))
                year = paper.get('year', 'Unknown')
                citation = f"[{authors}{year}]" if authors != 'Unknown' else f"[Research {i}]"

                prompt += f"{i}. {citation}: {paper['title']}\n"

            prompt += "\nINSTRUCTIONS:\n"
            prompt += "- Write 1-3 natural sentences that address the gap\n"
            prompt += "- Use the research findings to support claims\n"
            prompt += "- Cite sources using academic format: [@AuthorYear]\n"
            prompt += "- Match the tone and style of the original text\n"
            prompt += "- Focus on evidence, not opinions\n"
        else:
            prompt += "\nNOTE: No highly relevant papers found. Write a brief note suggesting what research would help."

        prompt += "\n\nProvide your response as a JSON object with these fields:"
        prompt += "\n- suggested_insertion: The improved text with citations"
        prompt += "\n- citations: Array of citation keys used (e.g., ['@Smith2023', '@Johnson2022'])"
        prompt += "\n- rationale: Brief explanation of the improvement"

        return prompt

    def _parse_writer_response(self, gap: EvidenceGap, response_content: str,
                              relevant_papers: List[dict]) -> DraftImprovement:
        """
        Parse the LLM response into a DraftImprovement object.

        Args:
            gap: The original gap being addressed.
            response_content: Raw LLM response.
            relevant_papers: Papers that were provided to the LLM.

        Returns:
            Validated DraftImprovement object.
        """
        try:
            # Clean response
            content = response_content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:].strip()

            # Parse JSON
            data = json.loads(content)

            # Extract and validate fields
            suggested_insertion = data.get('suggested_insertion', '')
            citations = data.get('citations', [])
            rationale = data.get('rationale', 'AI-generated improvement')

            # Validate citations are likely real
            cleaned_citations = []
            for citation in citations:
                if isinstance(citation, str) and citation.startswith('@'):
                    cleaned_citations.append(citation)

            return DraftImprovement(
                gap_id=gap.id,
                original_snippet=gap.context_snippet,
                suggested_insertion=suggested_insertion,
                citations=cleaned_citations,
                rationale=rationale
            )

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse writer response: {e}")
            # Fallback improvement
            return DraftImprovement(
                gap_id=gap.id,
                original_snippet=gap.context_snippet,
                suggested_insertion=f"[AI Suggestion: {gap.missing_information}]",
                citations=[],
                rationale="Fallback suggestion due to parsing error"
            )