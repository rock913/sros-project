"""Module to build the LangGraph application."""

from agent.infrastructure.tools.scholar import get_scholar_tool
from langgraph.graph import (
    StateGraph,  # Updated Import
    END,
    START
)
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from agent.infrastructure.mcp.server import FastMcpServer
from agent.infrastructure.tools.unpaywall import get_unpaywall_tool


class AppConfig(BaseModel):
    """Configuration for the application.
    
    For now, we don't need any specific configuration.
    """
    pass

def build_graph(config: AppConfig) -> CompiledStateGraph:
    """Build the graph for the LangGraph application.

    Args:
        config (AppConfig): The application configuration.

    Returns:
        CompiledStateGraph: The compiled state graph.
    """
    # Initialize the MCP server
    mcp_server = FastMcpServer()

    # Get the tools
    scholar_tool = get_scholar_tool()
    unpaywall_tool = get_unpaywall_tool()

    # Register the tools to the MCP server
    mcp_server.register_tool(scholar_tool)
    mcp_server.register_tool(unpaywall_tool)

    # Create a simple graph
    workflow = StateGraph(dict)

    # Add a dummy node
    def dummy_node(state):
        return state

    workflow.add_node("agent", dummy_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add edge to END
    workflow.add_edge("agent", END)

    # Compile the graph
    return workflow.compile()
