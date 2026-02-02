import os
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph
from sqlalchemy import create_engine

from agent.database import Base, Document, SessionLocal, init_db
from agent.application.workflows.research_workflow import (
    automated_resource_management,
    execute_searches,
    generate_initial_queries,
    ingest_and_embed_documents,
    reflection_and_refinement,
    retrieve_and_synthesize_report,
    should_continue_searching,
)
from agent.state import AgentState

# Load environment variables from .env file
load_dotenv()

# Fixture for database setup and teardown
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    database_url = os.getenv("POSTGRES_URI")
    if not database_url:
        pytest.fail("POSTGRES_URI environment variable not set. Please create a .env file with the variable.")
    
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.query(Document).delete()
    session.commit()
    session.close()

@pytest.fixture
def mocked_graph():
    """Provides a freshly compiled graph for each test."""
    builder = StateGraph(AgentState)
    builder.add_node("generate_initial_queries", generate_initial_queries)
    builder.add_node("execute_searches", execute_searches)
    builder.add_node("reflection_and_refinement", reflection_and_refinement)
    builder.add_node("automated_resource_management", automated_resource_management)
    builder.add_node("ingest_and_embed_documents", ingest_and_embed_documents)
    builder.add_node("retrieve_and_synthesize_report", retrieve_and_synthesize_report)
    builder.add_edge(START, "generate_initial_queries")
    builder.add_edge("generate_initial_queries", "execute_searches")
    builder.add_edge("execute_searches", "reflection_and_refinement")
    builder.add_conditional_edges(
        "reflection_and_refinement",
        should_continue_searching,
        {
            "execute_searches": "execute_searches",
            "automated_resource_management": "automated_resource_management",
        },
    )
    builder.add_edge("automated_resource_management", "ingest_and_embed_documents")
    builder.add_edge("ingest_and_embed_documents", "retrieve_and_synthesize_report")
    builder.add_edge("retrieve_and_synthesize_report", END)
    return builder.compile()

@pytest.mark.asyncio
@patch('agent.application.workflows.research_workflow.completion')
@patch('agent.application.workflows.research_workflow.arxiv_tool')
@patch('agent.application.workflows.research_workflow.unpaywall_tool')
@patch('agent.application.workflows.research_workflow.zotero_tool')
@patch('requests.get')
@patch('agent.application.workflows.research_workflow.embeddings')
async def test_full_agent_workflow_success(mock_embedding, mock_requests_get, mock_zotero_tool_instance, mock_unpaywall_tool_instance, mock_arxiv_tool_instance, mock_litellm_completion, db_session, mocked_graph):
    """
    Tests the full agent workflow for a successful run, mocking external services.
    """
    # Set TEST_MODE environment variable
    import os
    os.environ['TEST_MODE'] = '1'
    # Mock external tool and LLM responses
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1", "q2"], "rationale": "test"}'))]), # generate_initial_queries
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]), # reflection_and_refinement
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]), # automated_report_generation
    ]
    # Debug: print mock object
    print(f"DEBUG: mock_arxiv_tool_instance = {mock_arxiv_tool_instance}")
    print(f"DEBUG: mock_arxiv_tool_instance.invoke = {mock_arxiv_tool_instance.invoke}")
    
    # Track calls to arxiv_tool.invoke
    call_count = 0
    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"DEBUG: arxiv_tool.invoke called with args={args}, kwargs={kwargs}")
        return """Published: 2024-01-01
Title: Test Paper 1
Authors: Author A, Author B
Summary: This is a test abstract for paper 1. DOI: 10.1234/test.001

Published: 2024-01-02
Title: Test Paper 2
Authors: Author C, Author D
Summary: This is a test abstract for paper 2. DOI: 10.1234/test.002"""
    
    mock_arxiv_tool_instance.invoke.side_effect = side_effect
    mock_unpaywall_tool_instance.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
    mock_zotero_tool_instance.invoke.return_value = "Successfully added paper to Zotero."
    
    # Mock requests.get for PDF download
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
    
    # Mock requests.get for Crossref API (called by get_doi_from_title)
    # Create a mock response that returns a valid Crossref JSON structure
    mock_crossref_response = MagicMock()
    mock_crossref_response.json.return_value = {
        'message': {
            'items': [{'DOI': '10.1234/test.001'}]
        }
    }
    mock_crossref_response.raise_for_status.return_value = None
    
    # Make requests.get return different mocks based on URL
    def side_effect_requests(url, **kwargs):
        if 'crossref.org' in url:
            return mock_crossref_response
        else:
            # Return the PDF download mock
            return mock_requests_get.return_value
    mock_requests_get.side_effect = side_effect_requests
    
    mock_embedding.return_value = MagicMock(data=[MagicMock(embedding=[0.1]*1024), MagicMock(embedding=[0.2]*1024)]) # Mock embeddings

    # Define the initial state
    initial_state = {"messages": [HumanMessage(content="test topic")]}

    # Invoke the graph
    final_state = await mocked_graph.ainvoke(initial_state)

    # Assertions
    mock_litellm_completion.assert_called()
    mock_arxiv_tool_instance.invoke.assert_called()
    mock_unpaywall_tool_instance.invoke.assert_called()
    mock_zotero_tool_instance.invoke.assert_called()
    # Check that requests.get was called for PDF download
    assert any('example.com' in str(call) for call in mock_requests_get.call_args_list)
    mock_embedding.assert_called()

    # Verify documents are stored in the database
    docs_in_db = db_session.query(Document).all()
    assert len(docs_in_db) > 0
    assert final_state["report"] == "Final Report"

@pytest.mark.asyncio
@patch('agent.application.workflows.research_workflow.completion')
@patch('agent.application.workflows.research_workflow.arxiv_tool')
async def test_reflection_loop(mock_arxiv_tool_instance, mock_litellm_completion, db_session, mocked_graph):
    """
    Tests the reflection loop where the agent searches again.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]), # generate_initial_queries
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": false, "knowledge_gap": "more info", "follow_up_queries": ["q2"]}'))]), # reflection_and_refinement (search again)
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]), # reflection_and_refinement (sufficient)
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]), # automated_report_generation
    ]
    mock_arxiv_tool_instance.invoke.return_value = """Published: 2024-01-01
Title: Test Paper
Authors: Author A, Author B
Summary: This is a test abstract for paper. DOI: 10.1234/test.001"""

    initial_state = {"messages": [HumanMessage(content="test topic")]}

    with patch('agent.application.workflows.research_workflow.unpaywall_tool') as mock_unpaywall_tool_instance, \
         patch('agent.application.workflows.research_workflow.zotero_tool') as mock_zotero_tool_instance, \
         patch('requests.get') as mock_requests_get, \
         patch('litellm.embedding'):
        # Mock requests.get for PDF download
        mock_requests_get.return_value.raise_for_status.return_value = None
        mock_requests_get.return_value.content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
        # Mock requests.get for Crossref API (called by get_doi_from_title)
        # Create a mock response that returns a valid Crossref JSON structure
        mock_crossref_response = MagicMock()
        mock_crossref_response.json.return_value = {
            'message': {
                'items': [{'DOI': '10.1234/test.001'}]
            }
        }
        mock_crossref_response.raise_for_status.return_value = None
        # Make requests.get return different mocks based on URL
        def side_effect(url, **kwargs):
            if 'crossref.org' in url:
                return mock_crossref_response
            else:
                # Return the PDF download mock
                return mock_requests_get.return_value
        mock_requests_get.side_effect = side_effect
        
        final_state = await mocked_graph.ainvoke(initial_state)

    # generate_initial_queries (1) + reflection_and_refinement (2) + automated_report_generation (1) = 4
    # execute_searches is not mocked, so we can't count it.
    # But we can check the number of times the arxiv_tool is called.
    assert mock_arxiv_tool_instance.invoke.call_count == 2 # Called twice due to reflection loop
    assert final_state["report"] == "Final Report"


@pytest.mark.asyncio
@patch('agent.application.workflows.research_workflow.completion')
@patch('agent.application.workflows.research_workflow.arxiv_tool')
@patch('agent.application.workflows.research_workflow.unpaywall_tool')
@patch('agent.application.workflows.research_workflow.zotero_tool')
@patch('requests.get')
@patch('agent.application.workflows.research_workflow.embeddings')
async def test_full_agent_workflow_no_unpaywall_pdf(mock_embedding, mock_requests_get, mock_zotero_tool_instance, mock_unpaywall_tool_instance, mock_arxiv_tool_instance, mock_litellm_completion, db_session, mocked_graph):
    """
    Tests the workflow when Unpaywall does not find an open-access PDF.
    The agent should continue the workflow without downloading or adding to Zotero.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool_instance.invoke.return_value = """Published: 2024-01-01
Title: Test Paper
Authors: Author A, Author B
Summary: This is a test abstract for paper. DOI: 10.1234/test.001"""
    mock_unpaywall_tool_instance.invoke.return_value = "No open access version found for this DOI."

    initial_state = {"messages": [HumanMessage(content="test topic")]}
    final_state = await mocked_graph.ainvoke(initial_state)

    assert mock_unpaywall_tool_instance.invoke.call_count == 1
    mock_requests_get.assert_not_called() # Should not try to download
    mock_zotero_tool_instance.invoke.assert_not_called() # Should not try to add to Zotero
    mock_embedding.assert_not_called() # Should not embed if download fails
    assert final_state["report"] == "Final Report"

@pytest.mark.asyncio
@patch('agent.application.workflows.research_workflow.completion')
@patch('agent.application.workflows.research_workflow.arxiv_tool')
@patch('agent.application.workflows.research_workflow.unpaywall_tool')
@patch('agent.application.workflows.research_workflow.zotero_tool')
@patch('requests.get', side_effect=Exception("Download Error"))
@patch('agent.application.workflows.research_workflow.embeddings')
async def test_full_agent_workflow_pdf_download_fails(mock_embedding, mock_requests_get, mock_zotero_tool_instance, mock_unpaywall_tool_instance, mock_arxiv_tool_instance, mock_litellm_completion, db_session, mocked_graph):
    """
    Tests the workflow when downloading a PDF fails.
    The agent should handle the error and continue.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool_instance.invoke.return_value = """Published: 2024-01-01
Title: Test Paper
Authors: Author A, Author B
Summary: This is a test abstract for paper. DOI: 10.1234/test.001"""
    mock_unpaywall_tool_instance.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"

    initial_state = {"messages": [HumanMessage(content="test topic")]}
    final_state = await mocked_graph.ainvoke(initial_state)

    assert mock_requests_get.call_count == 1
    assert mock_zotero_tool_instance.invoke.call_count == 1 # Zotero is still called even if download fails
    mock_embedding.assert_not_called() # Should not embed if download fails
    assert final_state["report"] == "Final Report"

@pytest.mark.asyncio
@patch('agent.application.workflows.research_workflow.completion')
@patch('agent.application.workflows.research_workflow.arxiv_tool')
@patch('agent.application.workflows.research_workflow.unpaywall_tool')
@patch('agent.application.workflows.research_workflow.zotero_tool')
@patch('requests.get')
@patch('agent.application.workflows.research_workflow.embeddings')
async def test_full_agent_workflow_zotero_fails(mock_embedding, mock_requests_get, mock_zotero_tool_instance, mock_unpaywall_tool_instance, mock_arxiv_tool_instance, mock_litellm_completion, db_session, mocked_graph):
    """
    Tests the workflow when the Zotero tool fails.
    The agent should log the error and continue to generate the report.
    """
    mock_litellm_completion.side_effect = [
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1"], "rationale": "test"}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
    ]
    mock_arxiv_tool_instance.invoke.return_value = """Published: 2024-01-01
Title: Test Paper
Authors: Author A, Author B
Summary: This is a test abstract for paper. DOI: 10.1234/test.001"""
    mock_unpaywall_tool_instance.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
    mock_zotero_tool_instance.invoke.return_value = "Failed to add paper to Zotero: some error"
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
    mock_embedding.return_value = MagicMock(data=[MagicMock(embedding=[0.1]*1024)])

    initial_state = {"messages": [HumanMessage(content="test topic")]}
    final_state = await mocked_graph.ainvoke(initial_state)

    assert mock_zotero_tool_instance.invoke.call_count == 1
    assert final_state["report"] == "Final Report"
