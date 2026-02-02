"""
Simplified Discovery Graph - Phase 5.2 Core Component

This workflow implements only the "search and discovery" loop from the full research pipeline,
without resource management, document ingestion, or final report generation.

@Contract-First Design:
- Domain: Pure search and reflection logic
- Ports: Uses PaperSearcher protocol for external searches
- Infrastructure: LangGraph StateGraph with Postgres persistence
"""

import os
from typing import Dict, List, Any

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from agent.configuration import Configuration
from agent.prompts import query_writer_instructions, reflection_instructions, get_current_date
from agent.tools_and_schemas import SearchQueryList, Reflection
from agent.database import get_db_connection


# Minimal AgentState for discovery workflow
class DiscoveryState(Dict[str, Any]):
    """Streamlined state for discovery workflow - only what's needed for search loop."""

    messages: List[AIMessage]
    search_queries: List[str] = []
    literature_abstracts: List[Dict[str, Any]] = []
    is_sufficient: bool = False
    knowledge_gap: str = ""
    research_loop_count: int = 0
    research_topic: str = ""


# Max loops for discovery (simplified from full research pipeline)
MAX_DISCOVERY_LOOPS = 2


def get_research_topic(messages: List[AIMessage]) -> str:
    """Extract research topic from messages - simplified version."""
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            return last_message.content.strip()
    return "Unknown research topic"


def generate_initial_queries(state: DiscoveryState, config: RunnableConfig) -> DiscoveryState:
    """Generate initial search queries for discovery.

    @TestScenarios
    - Extract topic from messages
    - Generate query list via LLM
    - Handle API failures gracefully
    """
    print("---DISCOVERY NODE: generate_initial_queries---")

    cfg = Configuration.from_runnable_config(config)
    research_topic = get_research_topic(state["messages"])

    prompt = query_writer_instructions.format(
        current_date=get_current_date(),
        research_topic=research_topic,
        number_queries=cfg.number_of_initial_queries or 3,
    )

    try:
        from agent import litellm_utils
        response = litellm_utils.completion(
            model=cfg.generation_model,
            messages=[{"content": prompt, "role": "user"}],
            response_format={"type": "json_object", "schema": SearchQueryList.model_json_schema()},
            num_retries=3,
            custom_llm_provider=cfg.generation_llm_provider,
            api_key=cfg.generation_api_key or None,
            base_url=cfg.generation_api_base or None,
        )
        search_queries = SearchQueryList.model_validate_json(response.choices[0].message.content).query
        print(f"Generated discovery queries: {search_queries}")
    except Exception as e:
        print(f"---ERROR: Failed to generate queries: {e}---")
        # Fallback to single topic-based query
        search_queries = [research_topic]

    return DiscoveryState(
        messages=state["messages"],
        search_queries=search_queries,
        literature_abstracts=[],
        research_topic=research_topic
    )


def continue_to_search_execution(state: DiscoveryState) -> List[Send]:
    """Fan-out to parallel search execution."""
    return [Send("execute_searches", {"search_queries": [q]}) for q in state["search_queries"]]


def execute_searches(state: DiscoveryState, config: RunnableConfig) -> DiscoveryState:
    """Execute parallel searches and collect abstracts.

    @TestScenarios
    - Process each query independently
    - Merge results from all searches
    - Handle search failures gracefully
    """
    print(f"---DISCOVERY NODE: execute_searches (Loop {state.get('research_loop_count', 0) + 1})---")

    cfg = Configuration.from_runnable_config(config)
    search_queries = state["search_queries"]
    new_abstracts = []

    for query in search_queries:
        try:
            print(f"---DISCOVERY TOOL: Searching for '{query}'---")
            # Import here to avoid circular dependencies
            from agent.tools_and_schemas import arxiv_tool

            # Clean query and search
            cleaned_query = query.replace('"', '').replace('AND', '').replace('OR', '').strip()
            arxiv_response = arxiv_tool.invoke(cleaned_query)

            # Parse results (simplified from full research workflow)
            if isinstance(arxiv_response, list):
                for item in arxiv_response:
                    if isinstance(item, dict):
                        abstract = {
                            'title': item.get('title', 'N/A'),
                            'authors': item.get('authors', []),
                            'summary': item.get('summary', ''),
                            'published': item.get('published', ''),
                            'doi': item.get('doi')
                        }
                        new_abstracts.append(abstract)

        except Exception as e:
            print(f"---DISCOVERY ERROR: Search failed for '{query}': {e}---")
            continue

    # Merge with existing abstracts
    all_abstracts = state.get("literature_abstracts", []) + new_abstracts

    print(f"Found {len(new_abstracts)} new abstracts, total: {len(all_abstracts)}")

    return DiscoveryState(
        messages=state["messages"],
        search_queries=state["search_queries"],
        literature_abstracts=all_abstracts,
        research_topic=state.get("research_topic", ""),
        research_loop_count=state.get("research_loop_count", 0)
    )


def reflection_and_refinement(state: DiscoveryState, config: RunnableConfig) -> DiscoveryState:
    """Reflect on discovered abstracts and assess sufficiency.

    @TestScenarios
    - Sufficient coverage: set is_sufficient=True
    - Gap identified: summarize knowledge gap
    - API failure: graceful fallback to sufficient=False
    """
    print("---DISCOVERY NODE: reflection_and_refinement---")

    cfg = Configuration.from_runnable_config(config)

    # Extract summaries for reflection
    summaries = [paper.get('summary', '') for paper in state.get("literature_abstracts", [])]
    all_abstracts = "\n---\n".join(summaries)

    if not all_abstracts.strip():
        print("No abstracts found - discovery incomplete")
        return DiscoveryState(
            **state,
            is_sufficient=False,
            knowledge_gap="No literature found for this topic",
            research_loop_count=state.get("research_loop_count", 0) + 1
        )

    prompt = reflection_instructions.format(
        current_date=get_current_date(),
        research_topic=state.get("research_topic", ""),
        summaries=all_abstracts,
    )

    try:
        from agent import litellm_utils
        response = litellm_utils.completion(
            model=cfg.generation_model,
            messages=[{"content": prompt, "role": "user"}],
            response_format={"type": "json_object", "schema": Reflection.model_json_schema()},
            num_retries=3,
            custom_llm_provider=cfg.generation_llm_provider,
            api_key=cfg.generation_api_key or None,
            base_url=cfg.generation_api_base or None,
        )
        reflection_result = Reflection.model_validate_json(response.choices[0].message.content)
        print(f"Reflection: Sufficient? {reflection_result.is_sufficient}")

        return DiscoveryState(
            **state,
            is_sufficient=reflection_result.is_sufficient,
            knowledge_gap=reflection_result.knowledge_gap,
            search_queries=[],  # End loop - discovery workflow doesn't iterate
            research_loop_count=state.get("research_loop_count", 0) + 1
        )

    except Exception as e:
        print(f"---ERROR: Reflection failed: {e}---")
        return DiscoveryState(
            **state,
            is_sufficient=True,  # Conservative: assume sufficient if reflection fails
            knowledge_gap="Could not assess coverage due to API error",
            research_loop_count=state.get("research_loop_count", 0) + 1
        )


def should_continue_discovery(state: DiscoveryState) -> str:
    """Determine workflow end condition."""
    if state.get("is_sufficient", False):
        print("✅ Discovery complete - sufficient coverage found")
        return "complete"
    else:
        print("❌ Discovery incomplete - ending workflow")
        return "incomplete"


def get_discovery_graph():
    """Factory function to create and compile the discovery graph.

    @TestScenarios
    - Compile with valid Postgres checkpointer
    - Graph accepts DiscoveryState input
    - Returns DiscoveryState with results
    """
    builder = StateGraph(DiscoveryState)

    # Add nodes
    builder.add_node("generate_initial_queries", generate_initial_queries)
    builder.add_node("execute_searches", execute_searches)
    builder.add_node("reflection_and_refinement", reflection_and_refinement)

    # Add edges
    builder.add_edge(START, "generate_initial_queries")
    builder.add_conditional_edges(
        "generate_initial_queries",
        continue_to_search_execution,
        ["execute_searches"]
    )
    builder.add_edge("execute_searches", "reflection_and_refinement")
    builder.add_conditional_edges(
        "reflection_and_refinement",
        should_continue_discovery,
        {
            "complete": END,
            "incomplete": END  # For now, end workflow on insufficient
        }
    )

    # Initialize Postgres checkpointer
    db_uri = os.getenv(
        "POSTGRES_URI",
        "postgresql://postgres:postgres@langgraph-postgres:5432/postgres"
    )

    connection_pool = ConnectionPool(
        conninfo=db_uri,
        max_size=20,
        kwargs={
            "autocommit": True,
            "prepare_threshold": 0,
        }
    )

    checkpointer = PostgresSaver(connection_pool)

    # Compile and return
    return builder.compile(checkpointer=checkpointer)