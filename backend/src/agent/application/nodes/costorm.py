"""
Co-STORM Discovery Nodes

This module contains the LangGraph nodes for the Co-STORM (Collaborative STORM) discovery engine.
Co-STORM generates diverse research perspectives while avoiding single-keyword searches.

@Co-STORM Algorithm:
1. Perspective Generation: Generate 3-5 distinct research perspectives via LLM
2. Mind Map Construction: Build structured knowledge map from perspectives
3. Discourse Loop: Librarian-Analyst collaborative discussion (future Sprint 2)
4. Gap Analysis: Compare Outline vs Content, identify missing evidence
5. Incremental Writing: Fill gaps with cited paragraphs

@Hexagonal Architecture:
- Application layer: Orchestrates domain logic via ports (prompts, schemas)
- Uses litellm_utils for LLM calls (infrastructure abstraction)
- Pure business logic, testable by mocking LLM responses
"""

import os
from typing import Dict, List, Any

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

from agent.domain.schemas.mindmap import MindMap
from agent.domain.schemas.paper import Paper
from agent.domain.prompts.costorm import PERSPECTIVE_GEN_PROMPT


# Co-STORM State (extended for Sprint 2 discourse loop)
class CoStormState(Dict[str, Any]):
    """State management for Co-STORM workflow.

    Extends discovery pattern but focuses on perspective generation
    rather than direct searching. Evolves naturally into multi-agent
    discourse in future sprints.

    @TestScenarios
    - perspective_gen: topic -> mindmap + perspectives
    - librarian_search: mindmap -> documents dict populated
    - analyst_synthesis: documents -> summaries in mindmap.nodes
    - discourse_loop: perspectives -> enhanced understanding (future)
    - gap_analysis: outline + content -> evidence_gaps (future)
    """
    messages: List[AIMessage] = []
    topic: str = ""
    mindmap: MindMap = None
    perspectives: List[Dict[str, Any]] = []  # For inter-node communication
    documents: Dict[str, List[Paper]] = {}  # Librarian's search results by node_id


def generate_perspectives(state: CoStormState, config: RunnableConfig) -> CoStormState:
    """Generate 3-5 distinct research perspectives via LLM structured output.

    This is the core Co-STORM node that enables "unknown unknowns" discovery
    by generating diverse perspectives instead of single-keyword searches.

    @TestScenarios
    - Input: topic="Quantum Computing"
    - LLM Call: Uses structured output (Pydantic schema) for guaranteed valid MindMap
    - Output: MindMap with 3-5 PerspectiveNodes, each with id/name/description/keywords
    - Error Handling: Fallback to empty MindMap if LLM fails
    - Metrics: Perspective diversity ensures comprehensive coverage

    @Co-STORM Rules:
    - Minimum 3, maximum 5 perspectives for discourse efficiency
    - Each perspective different angle (methodological vs historical vs theoretical)
    - Keywords drive Librarian search, descriptions guide Analyst insight
    """
    print("---CO-STORM NODE: generate_perspectives---")

    topic = state.get("topic", "")
    if not topic:
        print("ERROR: No topic provided for perspective generation")
        # Fallback: create minimal valid MindMap with 3 default nodes
        from agent.domain.schemas.mindmap import PerspectiveNode
        default_nodes = [
            PerspectiveNode(
                id="missing_topic_general",
                name="General Introduction",
                description="General introduction to the research topic",
                query_keywords=["introduction", "overview", "basics"]
            ),
            PerspectiveNode(
                id="missing_topic_background",
                name="Background Information",
                description="Historical and background context",
                query_keywords=["background", "history", "context"]
            ),
            PerspectiveNode(
                id="missing_topic_current",
                name="Current Understanding",
                description="Current state of knowledge and research",
                query_keywords=["current", "state", "understanding"]
            )
        ]
        fallback_mindmap = MindMap(
            root_topic="unknown_topic",
            nodes=default_nodes
        )
        fallback_perspectives = [node.model_dump() for node in default_nodes]
        return {**state, "mindmap": fallback_mindmap, "perspectives": fallback_perspectives}

    print(f"Generating perspectives for topic: '{topic}'")

    # Format prompt with Pydantic schema for structured output
    schema_json = MindMap.model_json_schema()
    prompt = PERSPECTIVE_GEN_PROMPT.format(topic=topic, schema=schema_json)

    try:
        # Application layer calls infrastructure via direct litellm
        from litellm import completion

        # Get configuration from runnable config
        # Simple fallback: use environment variables directly (temporary)
        from agent.configuration import Configuration
        cfg = Configuration.from_runnable_config(config)

        # Ensure the model name has a provider prefix (Fix for litellm.BadRequestError)
        model_name = cfg.generation_model or "gemini/gemini-1.5-flash"
        if model_name.startswith("qwen") and not model_name.startswith("dashscope/"):
            model_name = f"dashscope/{model_name}"

        # Structured output ensures valid MindMap
        # Use simple json_object mode which is better supported across providers than strict json_schema
        response = completion(
            model=model_name,
            messages=[{"content": prompt, "role": "user"}],
            response_format={"type": "json_object"},
            num_retries=3,
            api_key=cfg.generation_api_key or None,
            base_url=cfg.generation_api_base or None,
        )

        # Pydantic validates and constructs MindMap (domain logic guarantees)
        mindmap = MindMap.model_validate_json(response.choices[0].message.content)

        print(f"✓ Generated MindMap with {len(mindmap.nodes)} perspectives:")
        for node in mindmap.nodes:
            print(f"  - {node.id}: {node.name} ({len(node.query_keywords)} keywords)")

        # Extract perspectives for inter-node communication
        perspectives = [node.model_dump() for node in mindmap.nodes]

        # Return updated state (LangGraph immutability pattern)
        return {
            **state,
            "mindmap": mindmap,
            "perspectives": perspectives
        }

    except Exception as e:
        print(f"---ERROR: Perspective generation failed: {e}---")
        # Graceful degradation: create minimal valid MindMap with 3 fallback nodes
        from agent.domain.schemas.mindmap import PerspectiveNode
        fallback_nodes = [
            PerspectiveNode(
                id="fallback_basic",
                name="Basic Overview",
                description=f"Basic introduction and overview of {topic}",
                query_keywords=["overview", "introduction", "basics"]
            ),
            PerspectiveNode(
                id="fallback_applications",
                name="Practical Applications",
                description=f"Real-world applications and use cases of {topic}",
                query_keywords=["applications", "use cases", "practical"]
            ),
            PerspectiveNode(
                id="fallback_future",
                name="Future Developments",
                description=f"Future trends and developments in {topic}",
                query_keywords=["future", "trends", "development"]
            )
        ]
        fallback_mindmap = MindMap(
            root_topic=topic,
            nodes=fallback_nodes
        )
        fallback_perspectives = [node.model_dump() for node in fallback_nodes]
        return {**state, "mindmap": fallback_mindmap, "perspectives": fallback_perspectives}
