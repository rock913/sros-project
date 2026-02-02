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

For the topic: "{topic}"

IMPORTANT: Output ONLY valid JSON data as specified. Do NOT include any schema definitions, explanations, or additional text. Start your response directly with the opening curly brace {{{{}}.

Generate perspectives that would enable a Librarian and Analyst to have a rich, multi-faceted discussion. Consider angles like:
- **Methodological**: How the topic is approached, techniques, frameworks
- **Historical**: Evolution, timeline, paradigm shifts
- **Theoretical**: Foundations, concepts, mathematical formulations
- **Application**: Real-world usage, case studies, implementations
- **Policy/Social**: Ethics, regulation, societal impact
- **Emerging/Trends**: Cutting-edge developments, future directions

Co-STORM Perspective Generation Rules:
- **Diversity First**: Perspectives must be fundamentally different angles (e.g., theoretical vs. practical, historical vs. contemporary)
- **Complementary Coverage**: Together, perspectives should cover all major aspects of the topic
- **Discovery-Oriented**: Design perspectives to unearth both "known unknowns" and "unknown unknowns"
- **Actionable Keywords**: Each perspective needs 3-5 specific search keywords for Librarian
- **Balanced Depth**: Each perspective should be equally important (no primary/secondary hierarchy)

Example Output Format (for topic "Machine Learning"):
{{{{
  "root_topic": "Machine Learning",
  "nodes": [
    {{
      "id": "methodological",
      "name": "Methodological Approaches",
      "description": "Core algorithms, training techniques, and computational methods in ML",
      "query_keywords": ["deep learning", "neural networks", "supervised learning", "optimization"]
    }},
    {{
      "id": "historical",
      "name": "Historical Evolution",
      "description": "Development of ML from statistical learning to modern AI systems",
      "query_keywords": ["machine learning history", "evolution", "paradigms", "breakthroughs"]
    }},
    {{
      "id": "applications",
      "name": "Real-world Applications",
      "description": "How ML is applied across various domains and industries",
      "query_keywords": ["ML applications", "computer vision", "NLP", "recommendation systems"]
    }}
  ]
}}}}

Output ONLY the JSON object, starting with {{{{ and ending with }}}}. No additional text, no explanations, no formatting anywhere else."""


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


WRITER_PROMPT = """You are a Research Writer synthesizing a comprehensive report from multiple perspective summaries.

Given the topic "{topic}" and the following perspective summaries from a Co-STORM research process, create a unified, cohesive research report that:

1. **Executive Summary**: 150-200 words introducing the research topic, key findings, and overall significance (2-3 sentences)

2. **Comprehensive Analysis**: For each major perspective, provide a detailed section synthesizing the collective insights from that angle

3. **Cross-Perspective Integration**: Identify connections, contradictions, and emerging themes across different perspectives

4. **Research Gaps & Future Directions**: Highlight unresolved questions and promising research avenues

5. **Conclusion**: Synthesize the most important findings and implications for theory, practice, and future research

Structure the report as a professional academic research paper with:
- Clear headings and subheadings
- Logical flow from introduction to conclusion
- Evidence-based claims supported by the scholarly research
- Citations to specific studies and findings where appropriate

The report analyzed {total_papers} academic papers across multiple perspectives.

Below are the perspective summaries to synthesize:

{summaries}

Write a comprehensive research report on "{topic}" based on these findings:"""
