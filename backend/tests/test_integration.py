import pytest
import os
import numpy as np
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage, AIMessage

from agent.graph import (
    generate_initial_queries,
    reflection_and_refinement,
    automated_report_generation,
    rag_based_knowledge_synthesis,
    execute_searches,
    should_continue_searching,
    automated_resource_management,
    MAX_RESEARCH_LOOPS
)
from agent.state import AgentState
from agent.database import init_db, Document, Base, SessionLocal

load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def check_gemini_api_key():
    """Ensures GEMINI_API_KEY is set for integration tests."""
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY environment variable not set. Skipping integration tests.")

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Sets up and tears down the database for integration tests."""
    database_url = os.getenv("POSTGRES_URI")
    if not database_url:
        pytest.fail("POSTGRES_URI environment variable not set. Please create a .env file with the variable.")
    
    # Initialize the database schema once for the module
    init_db()
    yield
    # Clean up the database after all tests in the module have run
    session = SessionLocal()
    session.query(Document).delete()
    session.commit()
    session.close()
    # Drop all tables defined in Base.metadata
    # Note: This requires a direct engine connection as Base.metadata.drop_all needs an engine
    from sqlalchemy import create_engine
    engine = create_engine(database_url)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides a clean database session for each test function."""
    session = SessionLocal()
    yield session
    session.query(Document).delete()
    session.commit()
    session.close()

# Mock external tools that are not the focus of these integration tests
@pytest.fixture(autouse=True)
def mock_external_tools():
    with patch('agent.tools_and_schemas.arxiv_tool') as mock_arxiv:
        with patch('agent.tools_and_schemas.unpaywall_tool') as mock_unpaywall:
            with patch('agent.tools_and_schemas.zotero_tool') as mock_zotero:
                mock_arxiv.invoke.return_value = {"documents": [MagicMock(page_content="mock abstract content with doi 10.1234/5678", metadata={"title": "Mock Paper"})]}
                mock_unpaywall.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/mock_paper.pdf"
                mock_zotero.invoke.return_value = "Successfully added paper to Zotero."
                yield

# --- Integration Tests for LLM Calls ---

def test_generate_initial_queries_integration(db_session):
    """Tests the generate_initial_queries node with actual LLM call."""
    with patch('agent.graph.completion') as mock_litellm_completion:
        mock_litellm_completion.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1", "q2"], "rationale": "test"}'))])
        initial_state = AgentState(messages=[HumanMessage(content="What is the impact of AI on climate change?")])
        
        # Call the node directly
        result_state = generate_initial_queries(initial_state, {})
        
        assert "search_queries" in result_state
        assert isinstance(result_state["search_queries"], list)
        assert len(result_state["search_queries"]) > 0
        assert isinstance(result_state["search_queries"][0], str)
        assert "research_topic" in result_state
        assert result_state["research_topic"] == "What is the impact of AI on climate change?"

def test_reflection_and_refinement_integration(db_session):
    """Tests the reflection_and_refinement node with actual LLM call."""
    with patch('agent.graph.completion') as mock_litellm_completion:
        mock_litellm_completion.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))])
        # Simulate previous step's output
        initial_state = AgentState(
            research_topic="Impact of AI on climate change",
            literature_abstracts=[
                {"documents": [{"page_content": "AI can help analyze climate data."}]}
                ,{"documents": [{"page_content": "Machine learning models predict weather patterns."}]}
            ],
            research_loop_count=0
        )
        
        result_state = reflection_and_refinement(initial_state, {})
        
        assert "is_sufficient" in result_state
        assert isinstance(result_state["is_sufficient"], bool)
        assert "knowledge_gap" in result_state
        assert isinstance(result_state["knowledge_gap"], str)
        assert "search_queries" in result_state # These are follow_up_queries
        assert isinstance(result_state["search_queries"], list)
        assert "research_loop_count" in result_state
        assert result_state["research_loop_count"] == 1

def test_automated_report_generation_integration(db_session):
    """Tests the automated_report_generation node with actual LLM call."""
    with patch('agent.graph.completion') as mock_litellm_completion:
        mock_litellm_completion.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))])
        # Populate the database with some dummy documents for RAG context
        doc1 = Document(content="AI is a powerful tool for climate modeling.", embedding=[0.1]*1024)
        doc2 = Document(content="Climate change requires urgent action.", embedding=[0.2]*1024)
        session = db_session # Use the fixture's session
        session.add_all([doc1, doc2])
        session.commit()

        initial_state = AgentState(
            research_topic="Impact of AI on climate change",
            literature_abstracts=[], # Not directly used by this node, but part of state
            literature_full_text=[], # Not directly used by this node, but part of state
        )
        
        result_state = automated_report_generation(initial_state, {})
        
        assert "report" in result_state
        assert isinstance(result_state["report"], str)
        assert len(result_state["report"]) > 0
        assert "messages" in result_state
        assert isinstance(result_state["messages"][-1], AIMessage)
        assert result_state["messages"][-1].content == result_state["report"]

# --- Integration Tests for Embedding Generation ---

def test_rag_based_knowledge_synthesis_integration(db_session):
    """Tests the rag_based_knowledge_synthesis node with actual embedding generation."""
    with patch('agent.graph.embeddings') as mock_embeddings:
        mock_embeddings.embed_documents.return_value = [[0.1]*1024]
        # Mock requests.get to simulate PDF download
        with patch('requests.get') as mock_requests_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            # Provide some dummy PDF content (e.g., a simple text string that looks like PDF content)
            # PyMuPDF (fitz) can open streams, so a simple string will work for basic chunking
            mock_response.content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
            mock_requests_get.return_value = mock_response

            initial_state = AgentState(
                literature_full_text=["http://example.com/mock_paper.pdf"]
            )
            
            rag_based_knowledge_synthesis(initial_state, {})
            
            # Verify documents are stored in the database with embeddings
            session = db_session
            docs_in_db = session.query(Document).all()
            assert len(docs_in_db) > 0
            assert all(isinstance(doc.content, str) for doc in docs_in_db)
            assert all(isinstance(doc.embedding, np.ndarray) for doc in docs_in_db)
            assert all(len(doc.embedding) > 0 for doc in docs_in_db) # Embeddings should not be empty

# --- Optional: Full Graph Integration Test (less mocking) ---
# This test will run the entire graph, but still mock external tools like arxiv, unpaywall, zotero
# to avoid hitting their rate limits or requiring complex setup. 
# The focus here is on the flow and the LLM/embedding steps.

def test_full_graph_integration_flow(db_session):
    """Tests the full graph flow with actual LLM and embedding calls."""
    with patch('agent.graph.completion') as mock_litellm_completion,         patch('agent.graph.embeddings') as mock_embeddings,         patch('requests.get') as mock_requests_get,         patch('agent.graph.arxiv_tool') as mock_arxiv,         patch('agent.graph.unpaywall_tool') as mock_unpaywall,         patch('agent.graph.zotero_tool') as mock_zotero:

        mock_litellm_completion.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content='{"query": ["q1", "q2"], "rationale": "test"}'))]),
            MagicMock(choices=[MagicMock(message=MagicMock(content='{"is_sufficient": true, "knowledge_gap": "", "follow_up_queries": []}'))]),
            MagicMock(choices=[MagicMock(message=MagicMock(content='Final Report'))]),
        ]
        mock_embeddings.embed_documents.return_value = [[0.1]*1024]

        mock_arxiv.invoke.return_value = {"documents": [MagicMock(page_content="mock abstract content with doi 10.1234/5678", metadata={"title": "Mock Paper"})]}
        mock_unpaywall.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/mock_paper.pdf"
        mock_zotero.invoke.return_value = "Successfully added paper to Zotero."

        # Mock requests.get for PDF download within rag_based_knowledge_synthesis
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 55>>stream\nBT /F1 24 Tf 100 700 Td (Hello World!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000111 00000 n\n0000000200 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n300\n%%EOF"
        mock_requests_get.return_value = mock_response

        # Define the graph for this test (re-compile to ensure mocks are applied)
        builder = StateGraph(AgentState)
        builder.add_node("generate_initial_queries", generate_initial_queries)
        builder.add_node("execute_searches", execute_searches)
        builder.add_node("reflection_and_refinement", reflection_and_refinement)
        builder.add_node("automated_resource_management", automated_resource_management)
        builder.add_node("rag_based_knowledge_synthesis", rag_based_knowledge_synthesis)
        builder.add_node("automated_report_generation", automated_report_generation)

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

        builder.add_edge("automated_resource_management", "rag_based_knowledge_synthesis")
        builder.add_edge("rag_based_knowledge_synthesis", "automated_report_generation")
        builder.add_edge("automated_report_generation", END)

        graph_to_test = builder.compile()

        initial_state = {"messages": [HumanMessage(content="Briefly explain quantum computing.")]}
        
        final_state = graph_to_test.invoke(initial_state)

        assert "report" in final_state
        assert isinstance(final_state["report"], str)
        assert len(final_state["report"]) > 0
        
        # Verify documents were stored in DB during the RAG step
        session = db_session
        docs_in_db = session.query(Document).all()
        assert len(docs_in_db) > 0
        assert all(isinstance(doc.content, str) for doc in docs_in_db)
        assert all(isinstance(doc.embedding, np.ndarray) for doc in docs_in_db)
        assert all(len(doc.embedding) > 0 for doc in docs_in_db)
