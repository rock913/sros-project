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
from agent.domain.ports.llm_provider import LLMProviderPort


class CoStormNode:
    """Co-STORM Node with observability and hexagonal dependencies.

    @Hexagonal Architecture:
    - Pure domain logic with injected infrastructure ports
    - Observability through log_event calls (ensures frontend data flow)
    - Dependency injection enables isolated testing

    @TestScenarios
    - generate_perspectives: topic -> mindmap + perspectives + log_event
    - log_event persisted: ensures backend observability contract fulfilled
    - LLM interactions abstracted: infrastructure provider easily swappable
    """
    def __init__(self, db_manager, llm_provider: LLMProviderPort):
        self.db_manager = db_manager
        self.llm_provider = llm_provider

    async def generate_perspectives(self, state):
        """Generate perspectives via LLM provider and log the event for observability.

        @Hexagonal Architecture:
        - Uses injected LLM provider port for domain separation
        - Maintains observability contract through log_event
        - Pure business logic with infrastructure abstraction

        @TestScenarios
        - topic provided -> mindmap + perspectives generated + event logged
        - no topic -> fallback mindmap created + event logged
        - LLM error -> fallback mindmap + event logged (graceful degradation)
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

            # Log event for observability (even with fallback) - include trace ID for frontend linking
            session_id = state.get('session_id', '')
            if session_id:
                # Get trace ID from state if available (injected by orchestration layer)
                trace_id = state.get('trace_id')
                payload = {"perspectives": fallback_perspectives, "fallback": True}
                if trace_id:
                    payload["trace_id"] = trace_id

                await self.db_manager.log_event(
                    session_id=session_id,
                    event_type="mindmap_generated",
                    payload=payload
                )

            return {**state, "mindmap": fallback_mindmap, "perspectives": fallback_perspectives}

        print(f"Generating perspectives for topic: '{topic}'")

        # Format prompt with topic only (schema guidance now built into prompt template)
        prompt = PERSPECTIVE_GEN_PROMPT.format(topic=topic)

        try:
            # Application layer calls infrastructure via port (hexagonal architecture)
            mindmap = await self.llm_provider.generate_structured_output(prompt, MindMap)

            print(f"✓ Generated MindMap with {len(mindmap.nodes)} perspectives:")
            for node in mindmap.nodes:
                print(f"  - {node.id}: {node.name} ({len(node.query_keywords)} keywords)")

            # Extract perspectives for inter-node communication
            perspectives = [node.model_dump() for node in mindmap.nodes]

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
            mindmap = MindMap(root_topic=topic, nodes=fallback_nodes)
            perspectives = [node.model_dump() for node in fallback_nodes]

        # Log event for observability (CRITICAL for frontend data flow) - include trace ID for frontend linking
        session_id = state.get('session_id', '')
        if session_id:
            # Get trace ID from state if available (injected by orchestration layer)
            trace_id = state.get('trace_id')
            payload = {"perspectives": perspectives}
            if trace_id:
                payload["trace_id"] = trace_id

            await self.db_manager.log_event(
                session_id=session_id,
                event_type="mindmap_generated",
                payload=payload
            )

        # Return updated state (LangGraph immutability pattern)
        return {
            **state,
            "mindmap": mindmap,
            "perspectives": perspectives
        }


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

    # Format prompt with topic only (schema guidance now built into prompt template)
    prompt = PERSPECTIVE_GEN_PROMPT.format(topic=topic)

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


def writer_node(state: CoStormState) -> CoStormState:
    """Synthesize comprehensive report from all perspective summaries.

    This final node combines all individual perspective summaries into a coherent,
    comprehensive research report that meets the trace.update expectations.
    CRITICALLY: Also persists all discovered papers and the final report to the database.

    @TestScenarios
    - mindmap with summaries -> generates unified report with citations + DB persistence
    - missing summaries -> fallback with partial content
    - LLM errors -> basic summary compilation without synthesis
    - Database persistence -> all papers and reports saved with session_id references

    Args:
        state: Co-STORM state with mindmap containing perspective summaries

    Returns:
        Updated state with final_report field and confirmed database persistence
    """
    print("---CO-STORM NODE: writer---")

    session_id = state.get("session_id")
    if not session_id:
        print("ERROR: No session_id in state, cannot persist data")
        # Continue without persistence (legacy behavior)
        session_id = None

    if not state.get("mindmap"):
        print("WARNING: No mindmap in state, writer has nothing to synthesize")
        return state

    mindmap = state["mindmap"]

    # Collect all summaries from mindmap nodes
    summaries = []
    total_papers = 0

    for node in mindmap.nodes:
        if node.summary:
            summaries.append({
                'perspective': node.name,
                'summary': node.summary
            })
            total_papers += len(node.papers) if hasattr(node, 'papers') and node.papers else 0

    if not summaries:
        print("WARNING: No summaries available to synthesize")
        fallback_report = f"# {mindmap.root_topic}\n\nResearch initiated but no content was generated due to analysis errors."
        return {**state, "report": fallback_report}

    print(f"Synthesizing {len(summaries)} perspective summaries into comprehensive report")

    try:
        # Format summaries for LLM context
        summaries_text = "\n\n".join([
            f"## {s['perspective']}\n{s['summary']}"
            for s in summaries
        ])

        # Use domain prompt for report synthesis
        from agent.domain.prompts.costorm import WRITER_PROMPT
        prompt = WRITER_PROMPT.format(
            topic=mindmap.root_topic,
            summaries=summaries_text,
            total_papers=total_papers
        )

        # Application layer calls infrastructure via litellm
        from litellm import completion
        from agent.configuration import Configuration

        config = {}
        cfg = Configuration.from_runnable_config(config)

        # Fix for DashScope model prefix
        model = cfg.generation_model
        if (cfg.generation_llm_provider == "dashscope" or "qwen" in model.lower()) and not model.startswith("dashscope/"):
            model = f"dashscope/{model}"

        # LLM call for synthesis
        response = completion(
            model=model,
            messages=[{"content": prompt, "role": "user"}],
            num_retries=2,
            api_key=cfg.generation_api_key or None,
            base_url=cfg.generation_api_base or None,
        )

        final_report = response.choices[0].message.content.strip()
        print(f"✓ Generated comprehensive report: {len(final_report)} characters")

        # CRITICAL: Persist papers and report to database if session_id available
        session_id = state.get("session_id")
        print(f"[Co-STORM] Writer Node - Session: {session_id} | MindMap Nodes: {len(mindmap.nodes) if mindmap else 0}")

        if session_id:
            try:
                # Import db_manager
                import agent.db_manager as db_manager
                from uuid import UUID

                session_uuid = UUID(session_id)
                papers_persisted = 0
                errors = []
         
                # Persist all papers from mindmap nodes
                if mindmap and mindmap.nodes:
                    print(f"[Co-STORM] Persisting papers for {len(mindmap.nodes)} perspectives...")
                    for node in mindmap.nodes:
                        if hasattr(node, 'papers') and node.papers:
                            for paper in node.papers:
                                try:
                                    # Convert Paper schema to db_manager format
                                    authors = paper.authors if isinstance(paper.authors, list) else []
                                    extra_metadata = {"source": paper.source} if hasattr(paper, 'source') else {}

                                    db_manager.add_paper(
                                        session_id=session_uuid,
                                        title=paper.title,
                                        authors=authors,
                                        abstract=getattr(paper, 'abstract', None),
                                        doi=getattr(paper, 'doi', None),
                                        arxiv_id=getattr(paper, 'arxiv_id', None),
                                        url=getattr(paper, 'url', None),
                                        extra_metadata=extra_metadata
                                    )
                                    papers_persisted += 1
                                except Exception as e:
                                    errors.append(f"Failed to persist paper '{paper.title}': {e}")
                                    print(f"[Co-STORM] Error persisting paper: {e}")

                print(f"✓ Persisted {papers_persisted} papers to database")

                if errors:
                    print(f"⚠️  {len(errors)} papers failed to persist: {errors[:3]}")

                # Persist the final report
                db_manager.create_report(
                    session_id=session_uuid,
                    content=final_report,
                    format="markdown",
                    version=1,
                    extra_metadata={"costorm_version": "2.1", "total_papers": papers_persisted}
                )
                print(f"✓ Persisted final report to database for session {session_id}")

            except Exception as db_error:
                print(f"❌ Database persistence failed: {db_error}")
                import traceback
                traceback.print_exc()
                # Don't fail the entire node - continue with report generation
        else:
            print("⚠️  No session_id available, skipping database persistence")

        # Return state with final_report for trace.update compatibility
        return {**state, "report": final_report}

    except Exception as e:
        print(f"ERROR: Failed to synthesize final report: {e}")
        # Fallback: compile summaries manually without LLM synthesis
        fallback_report = f"# {mindmap.root_topic}\n\n## Summary\n\n"
        for s in summaries:
            fallback_report += f"### {s['perspective']}\n{s['summary']}\n\n"
        return {**state, "report": fallback_report}
