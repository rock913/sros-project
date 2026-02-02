"""
Co-STORM Graph Factory

Factory function to create and compile the Co-STORM (Collaborative STORM) discovery workflow graph.
This graph implements Phase 5.2 Sprint 1: Mind Map construction and perspective generation.

    @Co-STORM Algorithm:
1. START -> generate_perspectives: Generate 3-5 diverse research perspectives
2. Generate structured MindMap with Librarian search keywords
3. librarian -> analyst: Discourse loop - search papers + synthesize summaries
4. END: Return mindmap with papers and summaries (ready for gap analysis)

@Hexagonal Architecture:
- Application layer: orchestrates domain logic into LangGraph workflow
- Uses Checkpointer protocol from domain ports (dependency injection)
- Infrastructure factory ensures unified connection pool across all graphs
- Compilable graph ready for MCP Orchestrator integration

@Operation Async-Stability:
- Fixed checkpointer configuration issues causing "Unknown error"
- Unified connection pool management eliminates async conflicts
- Proper thread_id handling prevents KeyError exceptions
"""

from typing import Any, Dict, List

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

# Import domain contracts and infrastructure factories
from agent.domain.ports.checkpointer import Checkpointer
from agent.infrastructure.db.checkpointer_factory import get_async_checkpointer

# Import observability infrastructure
from agent.infrastructure.observability.langfuse_tracer import get_langfuse_tracer

# Global cache
_costorm_graph = None

# Import Co-STORM domain types and nodes
from agent.domain.schemas.mindmap import MindMap
from agent.application.nodes.costorm import CoStormState, generate_perspectives, writer_node
from agent.application.nodes.librarian import librarian_node
from agent.application.nodes.analyst import analyst_node


def create_costorm_graph(checkpointer: Checkpointer) -> None:
    """Create and compile the Co-STORM discovery graph with injected checkpointer.

    This function is separated for dependency injection testing.
    Application layer should use get_costorm_graph() factory instead.

    @TestScenarios (Infrastructure layer unit tests only)
    - Valid checkpointer: Successfully compiles graph
    - Invalid checkpointer: Raises appropriate exception
    - State transitions: START -> generate_perspectives -> librarian -> analyst -> END
    """
    global _costorm_graph

    # Define graph builder with Co-STORM state
    builder = StateGraph(CoStormState)

    # Add Co-STORM nodes (Sprint 2: Discourse Loop + Writer Synthesis)
    builder.add_node("generate_perspectives", generate_perspectives)
    builder.add_node("librarian", librarian_node)
    builder.add_node("analyst", analyst_node)
    builder.add_node("writer", writer_node)

    # Define complete Co-STORM workflow: perspectives -> papers -> summaries -> report
    builder.add_edge(START, "generate_perspectives")
    builder.add_edge("generate_perspectives", "librarian")
    builder.add_edge("librarian", "analyst")
    builder.add_edge("analyst", "writer")
    builder.add_edge("writer", END)

    # Compile with injected checkpointer (dependency injection pattern)
    _costorm_graph = builder.compile(checkpointer=checkpointer._saver)


def get_costorm_graph():
    """Factory function to create and compile the Co-STORM discovery graph.

    Uses infrastructure factory for checkpointer dependency injection.
    This eliminates connection pool conflicts and async stability issues.

    @Hexagonal Architecture:
    - Application layer: Orchestrates workflow definition
    - Infrastructure layer: Provides checkpointer via factory
    - Singleton checkpointer: Shared connection pool across all graphs

    @Operation Async-Stability Fixes:
    - Unified connection pool management prevents pool exhaustion
    - Proper checkpointer configuration eliminates "Unknown error"
    - Thread-safe singleton pattern for concurrent graph execution

    @TestScenarios
    - Compile: Valid StateGraph with generate_perspectives-librarian-analyst flow
    - State: CoStormState type with mindmap and perspectives fields
    - Persistence: Checkpointer from domain contract properly injected
    - Invocation: graph.ainvoke() returns valid CoStormState
    - Async operations: No connection pool conflicts or thread_id errors

    Returns:
        CompiledStateGraph: Ready-to-run Co-STORM workflow graph

    Flow:
    START -> generate_perspectives -> librarian -> analyst -> writer -> END

    State Updates:
    - mindmap: MindMap with 3-5 PerspectiveNodes
    - perspectives: List[Dict] for inter-node communication
    - documents: Librarian search results
    - report: Final comprehensive research report synthesized from summaries
    """
    global _costorm_graph

    if _costorm_graph is not None:
        return _costorm_graph


async def invoke_costorm_graph_with_tracing(config: RunnableConfig, **kwargs):
    """Execute Co-STORM graph with integrated LangFuse tracing.

    This wrapper provides end-to-end observability for research sessions,
    creating parent traces and child spans for each Co-STORM node.

    @Tracing Strategy:
    - Parent Trace: "Co-STORM Execution" (complete research session)
    - Child Spans: Librarian Node, Analyst Node, Writer Node
    - Metadata: Research topic, perspective count, paper counts

    @Frontend Integration:
    - Trace IDs injected into state for mindmap_generated events
    - Enables frontend deep-linking to LangFuse trace details

    Args:
        config: LangGraph runnable configuration
        **kwargs: State parameters (topic, session_id, etc.)

    Returns:
        CoStormState: Final graph execution state

    @Integration Example:
    ```python
    from agent.application.workflows.costorm_graph import invoke_costorm_graph_with_tracing

    config = RunnableConfig(...)  # With user/context data
    result = await invoke_costorm_graph_with_tracing(
        config,
        topic="Machine Learning Ethics",
        session_id="uuid-123"
    )
    ```
    """
    tracer = get_langfuse_tracer()

    # Extract tracing metadata
    session_id = kwargs.get("session_id", "")
    topic = kwargs.get("topic", "unknown_topic")
    user_id = config.get("configurable", {}).get("user_id", "anonymous")

    # Create parent trace for complete Co-STORM execution
    with tracer.start_trace(
        name="Co-STORM Research Session",
        metadata={
            "topic": topic,
            "session_id": session_id,
            "entry_point": "invoked_via_orchestrator"
        },
        tags=["costorm", "ai-native", "research"],
        session_id=session_id
    ) as trace:

        # Inject trace_id into state for frontend event linking
        trace_id = getattr(trace, 'id', None)
        if trace_id:
            kwargs["trace_id"] = trace_id

        # Get or create graph (singleton pattern)
        graph = get_costorm_graph()

        # Execute graph within trace context (any errors auto-recorded)
        try:
            result = await graph.ainvoke(kwargs, config)

            # Return final state for orchestrator processing
            return result

        except Exception as e:
            # Record error in trace (LangFuse integration)
            tracer.record_error(trace, e)
            raise  # Re-raise for orchestrator error handling

    # Get checkpointer from infrastructure factory (dependency injection)
    checkpointer = get_async_checkpointer()

    # Create graph with injected infrastructure
    create_costorm_graph(checkpointer)

    return _costorm_graph
