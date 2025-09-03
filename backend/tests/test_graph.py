import pytest
from unittest.mock import patch, MagicMock

from agent.graph import graph, generate_initial_queries, execute_searches, reflection_and_refinement, automated_resource_management, rag_based_knowledge_synthesis, automated_report_generation
from agent.state import AgentState
from agent.database import init_db, upsert_documents, query_documents, Document, Base, get_db_connection
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
import os

# Fixture for PostgreSQL test container
@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        yield postgres
    del os.environ["DATABASE_URL"]

# Fixture for database session, ensuring a clean state for each test
@pytest.fixture(scope="function")
def db_session(postgres_container):
    init_db()
    session = get_db_connection()
    yield session
    session.close()
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as connection:
        Base.metadata.drop_all(bind=engine)
        connection.commit()

def test_graph_creation():
    """
    Tests that the graph is created successfully and is a compiled graph.
    """
    assert hasattr(graph, 'invoke')

def test_graph_nodes():
    """
    Tests that the graph has the expected nodes.
    """
    expected_nodes = [
        "generate_initial_queries",
        "execute_searches",
        "run_single_search",
        "reflection_and_refinement",
        "automated_resource_management",
        "rag_based_knowledge_synthesis",
        "automated_report_generation",
    ]
    for node in expected_nodes:
        assert node in graph.nodes

@patch('litellm.completion')
@patch('agent.tools_and_schemas.arxiv_tool.invoke')
@patch('agent.tools_and_schemas.unpaywall_tool.invoke')
@patch('agent.tools_and_schemas.zotero_tool.invoke')
@patch('requests.get')
@patch('agent.graph.GoogleGenerativeAIEmbeddings.embed_documents')
def test_full_agent_workflow_success(mock_embed_documents, mock_requests_get, mock_zotero_tool, mock_unpaywall_tool, mock_arxiv_tool, mock_litellm_completion, db_session):
    """
    Tests the full agent workflow for a successful run, mocking external services.
    """
    # Mock external tool and LLM responses
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1", "q2"], "rationale": "test"}'))]), # generate_initial_queries
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]), # reflection_and_refinement
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]), # automated_report_generation
    ]
    mock_arxiv_tool.return_value = {"documents": [MagicMock(page_content="abstract1"), MagicMock(page_content="abstract2")]}
    mock_unpaywall_tool.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
    mock_zotero_tool.return_value = "Successfully added paper to Zotero."
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.content = b"fake pdf content"
    mock_embed_documents.return_value = [[0.1]*1024, [0.2]*1024] # Mock embeddings

    # Define the initial state
    initial_state = {"messages": [MagicMock(content="test topic")]}

    # Invoke the graph
    final_state = graph.invoke(initial_state)

    # Assertions
    mock_litellm_completion.assert_called()
    mock_arxiv_tool.assert_called()
    mock_unpaywall_tool.assert_called()
    mock_zotero_tool.assert_called()
    mock_requests_get.assert_called_with("http://example.com/paper.pdf")
    mock_embed_documents.assert_called()

    # Verify documents are stored in the database
    docs_in_db = db_session.query(Document).all()
    assert len(docs_in_db) > 0
    assert final_state["report"] == "Final Report"

@patch('litellm.completion')
@patch('agent.tools_and_schemas.arxiv_tool.invoke')
def test_reflection_loop(mock_arxiv_tool, mock_litellm_completion, db_session):
    """
    Tests the reflection loop where the agent searches again.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]), # generate_initial_queries
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": false, "knowledge_gap": "more info", "follow_up_queries": ["q2"]}'))]), # reflection_and_refinement (search again)
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]), # reflection_and_refinement (sufficient)
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]), # automated_report_generation
    ]
    mock_arxiv_tool.return_value = {"documents": [MagicMock(page_content="abstract")]}

    initial_state = {"messages": [MagicMock(content="test topic")]}

    with patch('agent.tools_and_schemas.unpaywall_tool.invoke'), \
         patch('agent.tools_and_schemas.zotero_tool.invoke'), \
         patch('requests.get'), \
         patch('agent.graph.GoogleGenerativeAIEmbeddings.embed_documents'):
        final_state = graph.invoke(initial_state)

    # generate_initial_queries (1) + execute_searches (2) + reflection_and_refinement (2) + automated_report_generation (1)
    assert mock_litellm_completion.call_count == 4
    assert mock_arxiv_tool.call_count == 2 # Called twice due to reflection loop
    assert final_state["report"] == "Final Report"

@patch('litellm.completion')
@patch('agent.tools_and_schemas.arxiv_tool.invoke')
@patch('agent.tools_and_schemas.unpaywall_tool.invoke')
@patch('agent.tools_and_schemas.zotero_tool.invoke')
@patch('requests.get')
@patch('agent.graph.GoogleGenerativeAIEmbeddings.embed_documents')
def test_full_agent_workflow_no_unpaywall_pdf(mock_embed_documents, mock_requests_get, mock_zotero_tool, mock_unpaywall_tool, mock_arxiv_tool, mock_litellm_completion, db_session):
    """
    Tests the workflow when Unpaywall does not find an open-access PDF.
    The agent should continue the workflow without downloading or adding to Zotero.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool.return_value = {"documents": [MagicMock(page_content="abstract")]}
    mock_unpaywall_tool.return_value = "No open access version found for this DOI."

    initial_state = {"messages": [MagicMock(content="test topic")]}
    final_state = graph.invoke(initial_state)

    mock_unpaywall_tool.assert_called_once()
    mock_requests_get.assert_not_called() # Should not try to download
    mock_zotero_tool.assert_not_called() # Should not try to add to Zotero
    mock_embed_documents.assert_not_called() # Should not try to embed
    assert final_state["report"] == "Final Report"

@patch('litellm.completion')
@patch('agent.tools_and_schemas.arxiv_tool.invoke')
@patch('agent.tools_and_schemas.unpaywall_tool.invoke')
@patch('agent.tools_and_schemas.zotero_tool.invoke')
@patch('requests.get')
@patch('agent.graph.GoogleGenerativeAIEmbeddings.embed_documents')
def test_full_agent_workflow_zotero_fails(mock_embed_documents, mock_requests_get, mock_zotero_tool, mock_unpaywall_tool, mock_arxiv_tool, mock_litellm_completion, db_session):
    """
    Tests the workflow when the Zotero tool fails.
    The agent should log the error and continue to generate the report.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool.return_value = {"documents": [MagicMock(page_content="abstract")]}
    mock_unpaywall_tool.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
    mock_zotero_tool.return_value = "Failed to add paper to Zotero: some error"
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.content = b"fake pdf content"
    mock_embed_documents.return_value = [[0.1]*1024]

    initial_state = {"messages": [MagicMock(content="test topic")]}
    final_state = graph.invoke(initial_state)

    mock_zotero_tool.assert_called_once()
    assert final_state["report"] == "Final Report"

@patch('litellm.completion')
@patch('agent.tools_and_schemas.arxiv_tool.invoke')
@patch('agent.tools_and_schemas.unpaywall_tool.invoke')
@patch('agent.tools_and_schemas.zotero_tool.invoke')
@patch('requests.get', side_effect=Exception("Download Error"))
@patch('agent.graph.GoogleGenerativeAIEmbeddings.embed_documents')
def test_full_agent_workflow_pdf_download_fails(mock_embed_documents, mock_requests_get, mock_zotero_tool, mock_unpaywall_tool, mock_arxiv_tool, mock_litellm_completion, db_session):
    """
    Tests the workflow when downloading a PDF fails.
    The agent should handle the error and continue.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool.return_value = {"documents": [MagicMock(page_content="abstract")]}
    mock_unpaywall_tool.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"

    initial_state = {"messages": [MagicMock(content="test topic")]}
    final_state = graph.invoke(initial_state)

    mock_requests_get.assert_called_once_with("http://example.com/paper.pdf")
    mock_zotero_tool.assert_called_once() # Zotero is still called even if download fails
    mock_embed_documents.assert_not_called() # Should not embed if download fails
    assert final_state["report"] == "Final Report"
