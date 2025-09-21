
import pytest
from unittest.mock import MagicMock, patch
from agent.database import init_db

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
    with patch('agent.graph.completion') as mock_completion, \
         patch('agent.graph.arxiv_tool') as mock_arxiv_tool, \
         patch('agent.graph.unpaywall_tool') as mock_unpaywall_tool, \
         patch('agent.graph.zotero_tool') as mock_zotero_tool, \
         patch('requests.get') as mock_requests_get, \
         patch('agent.graph.GoogleGenerativeAIEmbeddings') as mock_google_generative_ai_embeddings:

        # Generic mock for all tools
        mock_arxiv_tool.invoke = MagicMock(return_value={"documents": []})
        mock_unpaywall_tool.invoke = MagicMock(return_value="No open access version found.")
        mock_zotero_tool.invoke = MagicMock(return_value="Successfully added paper to Zotero.")
        
        # Mock for embeddings
        mock_google_generative_ai_embeddings.return_value.embed_documents = MagicMock(return_value=[[0.1, 0.2, 0.3]] * 5) # Return some dummy vectors

        # The context object that will be passed to the test steps
        context = {
            "mock_completion": mock_completion,
            "mock_arxiv": mock_arxiv_tool,
            "mock_unpaywall": mock_unpaywall_tool,
            "mock_zotero": mock_zotero_tool,
            "mock_requests_get": mock_requests_get,
            "mock_embeddings": mock_google_generative_ai_embeddings.return_value,
            "final_state": None,  # To store the result of the agent run
        }
        yield context

