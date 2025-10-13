
import pytest
from unittest.mock import MagicMock, patch
from agent.database import init_db
from agent.state import AgentState
from langgraph.graph import StateGraph, END, START
from agent.graph import (
    generate_initial_queries,
    execute_searches,
    reflection_and_refinement,
    automated_resource_management,
    ingest_and_embed_documents,
    retrieve_and_synthesize_report,
    should_continue_searching,
    continue_to_web_research,
)

@pytest.fixture(scope='session', autouse=True)
def db_session():
    """Initializes the database before the test session."""
    init_db()

@pytest.fixture(autouse=True)
def reset_graph_globals():
    from agent import graph
    graph.embeddings = None
    yield

@pytest.fixture
def test_graph():
    """
    Provides a graph compiled WITHOUT checkpointer for testing.
    This avoids PostgresSaver dependency in unit tests.
    """
    builder = StateGraph(AgentState)
    builder.add_node("generate_initial_queries", generate_initial_queries)
    builder.add_node("execute_searches", execute_searches)
    builder.add_node("reflection_and_refinement", reflection_and_refinement)
    builder.add_node("automated_resource_management", automated_resource_management)
    builder.add_node("ingest_and_embed_documents", ingest_and_embed_documents)
    builder.add_node("retrieve_and_synthesize_report", retrieve_and_synthesize_report)
    
    builder.add_edge(START, "generate_initial_queries")
    builder.add_conditional_edges("generate_initial_queries", continue_to_web_research)
    builder.add_edge("execute_searches", "reflection_and_refinement")
    builder.add_conditional_edges("reflection_and_refinement", should_continue_searching)
    builder.add_edge("automated_resource_management", "ingest_and_embed_documents")
    builder.add_edge("ingest_and_embed_documents", "retrieve_and_synthesize_report")
    builder.add_edge("retrieve_and_synthesize_report", END)
    
    return builder.compile()  # No checkpointer for tests

@pytest.fixture
def agent_test_context():
    """
    Provides a testing context with mocked external services for the agent.

    This fixture patches the key external dependencies of the agent graph:
    - litellm.completion: To simulate responses from the Gemini LLM.
    - arxiv_tool: To simulate responses from the Arxiv API.
    - unpaywall_tool: To simulate responses from the Unpaywall API.
    - zotero_tool: To simulate adding papers to Zotero.

    It yields a dictionary of mocks so that individual test steps can
    configure their return values and assert that they were called correctly.
    """
    with patch('agent.graph.completion') as mock_litellm_completion, \
     patch('agent.graph.embeddings') as mock_litellm_embedding, \
         patch('agent.graph.arxiv_tool') as mock_arxiv_tool, \
         patch('agent.graph.unpaywall_tool') as mock_unpaywall_tool, \
         patch('agent.graph.zotero_tool') as mock_zotero_tool, \
         patch('requests.get') as mock_requests_get:

        # Generic mock for all tools
        mock_arxiv_tool.invoke = MagicMock(return_value={"documents": []})
        mock_unpaywall_tool.invoke = MagicMock(return_value="No open access version found.")
        mock_zotero_tool.invoke = MagicMock(return_value="Successfully added paper to Zotero.")
        
        # Mock for embeddings
        mock_litellm_embedding.return_value = MagicMock(data=[MagicMock(embedding=[0.1, 0.2, 0.3])])

        # The context object that will be passed to the test steps
        context = {
            "mock_completion": mock_litellm_completion,
            "mock_arxiv": mock_arxiv_tool,
            "mock_unpaywall": mock_unpaywall_tool,
            "mock_zotero": mock_zotero_tool,
            "mock_requests_get": mock_requests_get,
            "mock_embedding": mock_litellm_embedding,
            "mock_embeddings": mock_litellm_embedding,  # alias for step_defs expecting plural key
            "final_state": None,  # To store the result of the agent run
        }
        # Provide plural alias used in some step definitions
        context["mock_embeddings"] = mock_litellm_embedding
        yield context

