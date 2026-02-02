from typing import Any, AsyncIterable, Dict
from datetime import datetime
from pydantic import BaseModel, Field
import os
import asyncio

from agent.domain.schemas.mcp import McpTool
from agent.domain.schemas.mcp_protocol import ResearchUpdate
from agent.infrastructure.db.session_adapter import PostgresSessionAdapter
from agent.application.workflows.costorm_graph import get_costorm_graph


class OrchestratorInput(BaseModel):
    """Input schema for research orchestrator MCP tool."""
    topic: str = Field(..., description="The research topic")


async def start_research(ctx: Any, input_data: dict) -> AsyncIterable[ResearchUpdate]:
    """Handler for starting a research session using Co-STORM graph.

    @TestScenarios
    - Create session and stream real Co-STORM events (mindmap_update, thought, etc.)
    - Handle graph execution errors gracefully
    - Properly serialize MindMap to payload JSON
    """
    # Convert input data to Pydantic model if needed
    if isinstance(input_data, dict):
        input_model = OrchestratorInput(**input_data)
    else:
        input_model = input_data

    try:
        # Initialize Co-STORM graph
        graph = get_costorm_graph()

        # Yield initialization
        yield ResearchUpdate(type="status_change", content="initializing", timestamp=datetime.utcnow())

        # Stream graph execution with real event mapping (per Sprint 3)
        initial_state = {"topic": input_model.topic}

        # Use astream for updates (async-compatible pattern)
        async for event in graph.astream(initial_state, stream_mode="updates"):
            # Event mapping: Detect MindMap updates
            if "mindmap" in event:
                mindmap = event["mindmap"]
                if mindmap:
                    # Serialize MindMap to JSON for MCP payload
                    mindmap_json = mindmap.model_dump_json()
                    yield ResearchUpdate(
                        type="mindmap_update",
                        content=f"Graph Expanded: {len(mindmap.nodes)} perspectives",
                        payload={"mindmap": mindmap_json},
                        timestamp=datetime.utcnow()
                    )

            # Event mapping: Detect LLM thoughts/messages
            if "messages" in event:
                messages = event.get("messages", [])
                if messages:
                    last_msg = messages[-1] if isinstance(messages, list) else messages
                    if hasattr(last_msg, 'content'):
                        yield ResearchUpdate(
                            type="thought",
                            content=last_msg.content,
                            timestamp=datetime.utcnow()
                        )

        # Final completion event
        yield ResearchUpdate(type="status_change", content="completed", timestamp=datetime.utcnow())

    except Exception as e:
        # Error handling with proper event
        yield ResearchUpdate(
            type="error",
            content=f"Research failed: {str(e)}",
            timestamp=datetime.utcnow()
        )


def get_orchestrator_mcp_tool() -> McpTool:
    """Create and return MCP tool for research orchestration.

    @TestScenarios
    - Factory creates McpTool with correct name, description, schema
    - Tool can be registered with MCP server successfully
    """
    return McpTool(
        name="orchestrator",
        description="Orchestrates a research session",
        input_schema=OrchestratorInput.model_json_schema(),
        handler=start_research
    )