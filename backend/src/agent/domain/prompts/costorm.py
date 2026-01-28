"""
Co-STORM (Collaborative STORM) Prompts

This module contains the prompt templates used by the Co-STORM discovery engine
for generating research perspectives and conducting collaborative analysis.

@Co-STORM Algorithm:
1. Perspective Generation: Generate diverse research perspectives (Methodological, Historical, etc.)
2. Mind Map Construction: Build structured knowledge map from perspectives
3. Discourse Loop: Librarian-Analyst collaborative discussion to unearth unknowns
4. Gap Analysis: Identify missing evidence in drafts
5. Incremental Writing: Fill gaps with cited content

@Hexagonal Architecture:
- Pure domain logic (no I/O)
- Used by application layer via litellm_utils.completion()
- Testable without external dependencies
"""

import json
from typing import Any, Dict


PERSPECTIVE_GEN_PROMPT = """You are an expert research strategist specializing in Co-STORM (Collaborative STORM) methodology. Your task is to analyze a research topic and generate 3-5 distinct, complementary research perspectives that would enable a comprehensive investigation through collaborative discourse.

Co-STORM Perspective Generation Rules:
- **Diversity First**: Perspectives must be fundamentally different angles (e.g., theoretical vs. practical, historical vs. contemporary)
- **Complementary Coverage**: Together, perspectives should cover all major aspects of the topic
- **Discovery-Oriented**: Design perspectives to unearth both "known unknowns" and "unknown unknowns"
- **Actionable Keywords**: Each perspective needs 3-5 specific search keywords for Librarian
- **Balanced Depth**: Each perspective should be equally important (no primary/secondary hierarchy)

For topic: "{topic}"

Generate perspectives that would enable a Librarian and Analyst to have a rich, multi-faceted discussion. Consider angles like:
- **Methodological**: How the topic is approached, techniques, frameworks
- **Historical**: Evolution, timeline, paradigm shifts
- **Theoretical**: Foundations, concepts, mathematical formulations
- **Application**: Real-world usage, case studies, implementations
- **Policy/Social**: Ethics, regulation, societal impact
- **Emerging/Trends**: Cutting-edge developments, future directions

Output Format:
Return a JSON object with this exact structure:
{schema}

Ensure the output is valid JSON that matches the MindMap schema exactly, with 3-5 perspectives covering diverse angles for thorough collaborative discovery.

Research Topic: {topic}"""


# Prompt for synthesizing perspective summaries from papers (Sprint 2)
ANALYST_PROMPT = """You are a Research Analyst synthesizing information from multiple academic papers into a coherent perspective summary.

Given a set of papers about a research perspective, create a concise summary (200-300 words) that:

1. **Key Themes & Findings**: Identify the main themes, findings, and insights across the papers
2. **Consensus & Controversies**: Highlight areas of agreement and ongoing debates
3. **Major Research Gaps**: Note unsolved problems, contradictory results, or understudied areas
4. **Implications**: Discuss the broader implications for theory and practice
5. **Future Directions**: Suggest promising avenues for future research

Structure your response as a cohesive narrative that synthesizes the collective knowledge from these papers. Write in academic style suitable for inclusion in a research report.

Papers data: {papers_json}

Write the summary for the "{perspective_name}" perspective in 250-350 words:"""
