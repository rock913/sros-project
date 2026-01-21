"""Module to build the LangGraph application.
"""

from agent.infrastructure.tools.scholar_adapter import get_scholar_tool
from langchain.graphs import (
    CompiledStateGraph,  # Assuming this is a placeholder for the actual graph type
)
from pydantic import BaseModel

from agent.infrastructure.mcp.server import FastMcpServer
from agent.infrastructure.tools.unpaywall_adapter import get_unpaywall_tool


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

    # For now, return a dummy graph (mocked or placeholder)
    dummy_graph = CompiledStateGraph()  # Placeholder for the actual graph
    return dummy_graph
