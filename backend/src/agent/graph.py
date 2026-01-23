"""
LangGraph compilation and graph objects for the research agent.

These objects are imported by the FastAPI app to serve the agent endpoints.
"""

from agent.application.workflows.research_workflow import graph, async_graph

# Re-export for compatibility with app.py
__all__ = ["graph", "async_graph"]