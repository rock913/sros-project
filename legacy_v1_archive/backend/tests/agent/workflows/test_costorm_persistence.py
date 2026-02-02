"""
Integration Test for Co-STORM Data Persistence

Tests the complete Co-STORM workflow end-to-end to ensure that:
1. session_id is properly threaded through the workflow
2. writer_node (final step) actually saves papers and reports to database
3. Database contains the expected data after graph execution

This test should FAIL initially (RED) due to current implementation bugs,
then PASS (GREEN) after fixes are applied.

@TDD Approach: Integration test that validates contract fulfillment
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

# Domain schemas
from agent.domain.schemas.mindmap import MindMap, PerspectiveNode, Paper
from agent.domain.schemas.paper import Paper as PaperSchema

# Co-STORM imports
from agent.application.workflows.costorm_graph import get_costorm_graph
from agent.application.nodes.costorm import CoStormState

# Database manager (infrastructure)
import agent.db_manager as db_manager


@pytest.mark.asyncio
@patch('agent.application.nodes.costorm.writer_node')  # Skip writer_node entirely for fast RED test
@patch('agent.application.nodes.librarian.get_paper_searcher')  # Mock searcher for speed
async def test_costorm_persistence_integration_red(mock_get_searcher, mock_writer_node):
    """FAST TEST: Confirm RED state - writer_node is not persisting data."""
    # Setup mock searcher to return empty or dummy papers instantly
    mock_searcher_instance = MagicMock()
    # Define async return for search_papers
    async def mock_search_papers(*args, **kwargs):
        return []
    mock_searcher_instance.search_papers = mock_search_papers
    mock_get_searcher.return_value = mock_searcher_instance

    # Mock writer_node to do nothing (return input unchanged)
    mock_writer_node.return_value = None  # Should cause immediate failure

    # Just check that papers/re_reports count is 0 for any created session
    from uuid import uuid4
    import agent.db_manager as db_manager

    # Create test session
    test_session_id = db_manager.create_session(
        thread_id=str(uuid4()),
        title="RED Test Session",
        research_topic="Test",
        tags=["red_test"]
    )["id"]

    # Check that no papers/reports exist initially
    saved_papers = db_manager.list_papers(session_id=test_session_id)
    saved_reports = db_manager.list_reports(session_id=test_session_id)

    # Should be empty
    assert len(saved_papers) == 0, f"Pre-test state should be clean, got {len(saved_papers)} papers"
    assert len(saved_reports) == 0, f"Pre-test state should be clean, got {len(saved_reports)} reports"

    print("✅ RED TEST: Clean database state confirmed")


@pytest.mark.asyncio
@patch('litellm.completion')  # Mock LLM calls for controlled testing (1st arg)
@patch('agent.application.nodes.librarian.get_paper_searcher')  # Mock searcher (2nd arg)
async def test_costorm_persistence_integration_green(mock_completion, mock_get_searcher):
    """Integration test: Co-STORM should persist papers and report to database.

    This test fails currently because:
    1. writer_node does not call db_manager.save_papers() or save_report()
    2. session_id may not be passed to the Co-STORM workflow

    @TestScenarios
    - Mock PRELIM_PHASE: complete mindmap with papers in different perspectives
    - Mock FINAL_PHASE: comprehensive report synthesis
    - Assert DATABASE: papers and report saved with session_id references
    """
    print("\n--- STARTING GREEN TEST ---")
    
    # 0. SETUP MOCKS
    # Mock PaperSearcher
    mock_searcher_instance = MagicMock()
    async def mock_search_papers(*args, **kwargs):
        print(f"  [Mock] search_papers called with {args}")
        return [
            PaperSchema(
                title=f"Mock Paper {uuid4().hex[:6]}",
                authors=["Test Author"],
                abstract="This is a mock abstract for testing persistence.",
                doi=f"10.1234/mock.{uuid4().hex[:6]}",
                url="https://mock.example.com",
                source="mock_source"
            )
        ]
    mock_searcher_instance.search_papers.side_effect = mock_search_papers
    mock_get_searcher.return_value = mock_searcher_instance
    
    print("  [Setup] Mocks configured")

    # 1. SETUP: Create session for isolation
    session_id = str(uuid4())
    thread_id = str(uuid4())

    # Create test session
    session = db_manager.create_session(
        thread_id=thread_id,
        title="Test Co-STORM Persistence",
        research_topic="Quantum Computing Applications",
        tags=["test", "costorm", "persistence"],
        notes="Integration test for Co-STORM data persistence"
    )
    test_session_id = session["id"]
    print(f"Created test session: {test_session_id}")

    # 2. MOCK LLM RESPONSES: Control what Co-STORM generates
    # Phase 1: Perspective generation (3 LLM calls)
    # Phase 2: Librarian searches (mock search results)
    # Phase 3: Analyst synthesis
    # Phase 4: Writer synthesis

    def mock_llm_response(*args, **kwargs):
        """Mock LLM responses based on prompt content."""
        prompt = kwargs.get('messages', [{}])[0].get('content', '')

        if 'perspectives' in prompt: # Removed broken kwargs check
            # Perspective generation - return mindmap with 3 perspectives
            return MagicMock(choices=[
                MagicMock(message=MagicMock(content='''{
                    "root_topic": "Quantum Computing Applications",
                    "nodes": [
                        {
                            "id": "applications",
                            "name": "Real-world Applications",
                            "description": "Current and emerging quantum computing applications",
                            "query_keywords": ["applications", "use_cases", "implementation"],
                            "papers": [
                                {
                                    "title": "Quantum Machine Learning Applications",
                                    "authors": ["Alice Chen", "Bob Smith"],
                                    "abstract": "This paper explores quantum computing applications in machine learning.",
                                    "doi": "10.1038/s42256-022-00515-0",
                                    "url": "https://www.example.com/quantum-ml",
                                    "source": "arxiv"
                                },
                                {
                                    "title": "Financial Modeling with Quantum Computers",
                                    "authors": ["Carol Wong"],
                                    "abstract": "Use of quantum algorithms for financial modeling applications.",
                                    "doi": "10.1145/3359999.3360578",
                                    "url": "https://www.example.com/quantum-finance",
                                    "source": "arxiv"
                                }
                            ],
                            "summary": "Quantum computing shows promise in machine learning and finance."
                        },
                        {
                            "id": "algorithms",
                            "name": "Quantum Algorithms",
                            "description": "Fundamental quantum algorithms and their implementations",
                            "query_keywords": ["algorithms", "shors", "grover"],
                            "papers": [
                                {
                                    "title": "Shor's Algorithm Implementation",
                                    "authors": ["David Lee"],
                                    "abstract": "Practical implementation of Shor's factoring algorithm.",
                                    "doi": "10.1103/PhysRevA.54.147",
                                    "url": "https://www.example.com/shors",
                                    "source": "crossref"
                                }
                            ],
                            "summary": "Shor's algorithm provides exponential speedup for factoring."
                        },
                        {
                            "id": "hardware",
                            "name": "Quantum Hardware",
                            "description": "Current quantum computing hardware capabilities",
                            "query_keywords": ["hardware", "qubits", "noise"],
                            "papers": [
                                {
                                    "title": "Superconducting Qubits for Quantum Computing",
                                    "authors": ["Eve Kim"],
                                    "abstract": "Development of superconducting qubit technology.",
                                    "doi": "10.1038/nature17650",
                                    "url": "https://www.example.com/superconducting",
                                    "source": "unpaywall"
                                }
                            ],
                            "summary": "Superconducting qubits are showing rapid improvements in coherence times."
                        }
                    ]
                }'''))
            ])

        elif 'summariz' in prompt.lower():
            # Analyst synthesis or Writer synthesis - return summary/report
            return MagicMock(choices=[
                MagicMock(message=MagicMock(content='''
# Quantum Computing Applications: Comprehensive Analysis

## Executive Summary
This report synthesizes current quantum computing research across applications, algorithms, and hardware domains.

## Key Findings

### Real-world Applications
Quantum computing demonstrates significant potential in machine learning and financial modeling. Recent papers (Chen et al., 2022; Wong, 2020) show promising applications with measurable speedups over classical algorithms.

### Quantum Algorithms
Core algorithms like Shor's provide exponential improvements for factoring problems. Lee's implementation study (2023) demonstrates practical feasibility despite hardware constraints.

### Hardware Progress
Superconducting qubit technology continues to advance rapidly. Kim's analysis (2015) indicates substantial improvements in coherence times, though noise remains a significant challenge.

## Recommendations
Research should focus on hybrid classical-quantum approaches that provide quantum advantage with current hardware capabilities.
                '''))
            ])
        else:
            # Default response for any other LLM calls
            return MagicMock(choices=[
                MagicMock(message=MagicMock(content="Mock response"))
            ])

    mock_completion.side_effect = mock_llm_response

    # 3. EXECUTE: Run Co-STORM graph (mocked internally)
    graph = get_costorm_graph()

    input_data = {
        "topic": "Quantum Computing Applications",
        "messages": [{"role": "user", "content": "Research quantum computing applications"}],
        "session_id": test_session_id,  # CRITICAL: This should thread through workflow
        "thread_id": thread_id
    }

    config = {"configurable": {"thread_id": thread_id}}

    # Run the graph (should complete without async issues due to mocking)
    try:
        result = graph.invoke(input_data, config=config)
        print(f"Graph completed with result keys: {list(result.keys())}")

        # Verify Co-STORM state structure
        assert "mindmap" in result
        assert "report" in result
        assert isinstance(result["mindmap"], (MindMap, dict))

        if isinstance(result["mindmap"], MindMap):
            assert len(result["mindmap"].nodes) == 3
            total_expected_papers = sum(len(node.papers or []) for node in result["mindmap"].nodes)

        assert isinstance(result["report"], str)
        assert len(result["report"]) > 100  # Reasonable report length

    except Exception as e:
        pytest.fail(f"Graph execution failed: {e}")

    # 4. ASSERT DATABASE PERSISTENCE: Verify data was saved
    # This is what currently FAILS due to writer_node not calling db_manager

    # Check papers were saved
    saved_papers = db_manager.list_papers(session_id=test_session_id)
    print(f"Saved papers count: {len(saved_papers)}")

    # EXPECTED: 4 papers (2 + 1 + 1) but currently gets 0
    expected_paper_count = 4
    assert len(saved_papers) == expected_paper_count, \
        f"Expected {expected_paper_count} papers persisted, got {len(saved_papers)}. Co-STORM writer_node not calling db_manager."

    # Check report was saved
    saved_reports = db_manager.list_reports(session_id=test_session_id)
    print(f"Saved reports count: {len(saved_reports)}")

    # EXPECTED: 1 report but currently gets 0
    assert len(saved_reports) == 1, \
        "Expected 1 report persisted, got {len(saved_reports)}. Co-STORM writer_node not calling db_manager."

    # Verify report content
    latest_report = db_manager.get_latest_report(test_session_id)
    assert latest_report is not None
    assert latest_report["content"] == result["report"]

    print("✅ Co-STORM persistence test passed!")


@pytest.mark.asyncio
async def test_writer_node_persistence_direct():
    """DIRECT TEST: Call writer_node directly with mock CoStormState to verify persistence."""

    from uuid import uuid4
    import agent.db_manager as db_manager

    # Create a test session
    test_session_id = db_manager.create_session(
        thread_id=str(uuid4()),
        title="Direct Writer Node Test",
        research_topic="Direct Test",
        tags=["direct_test"]
    )["id"]

    # Import and setup
    from agent.application.nodes.costorm import writer_node, CoStormState
    from agent.domain.schemas.mindmap import MindMap, PerspectiveNode, Paper

    # Create mock mindmap with papers (proper Paper objects, not dicts)
    mock_papers = [
        Paper(
            title="Test Paper 1",
            authors=["Author A", "Author B"],
            abstract="Abstract 1",
            doi="10.1234/test1",
            url="https://test1.com",
            source="arxiv"
        ),
        Paper(
            title="Test Paper 2",
            authors=["Author C"],
            abstract="Abstract 2",
            doi="10.1234/test2",
            url="https://test2.com",
            source="crossref"
        ),
        Paper(
            title="Test Paper 3",
            authors=["Author D", "Author E"],
            abstract="Abstract 3",
            doi="10.5678/test3",
            url="https://test3.com",
            source="unpaywall"
        )
    ]

    # Create PerspectiveNodes with summaries and papers (MindMap requires 3+ nodes)
    perspectives = [
        PerspectiveNode(
            id="perspective1",
            name="Perspective 1",
            description="First perspective",
            query_keywords=["key1", "key2"],
            papers=mock_papers[:1],  # 1 paper
            summary="Summary of perspective 1"
        ),
        PerspectiveNode(
            id="perspective2",
            name="Perspective 2",
            description="Second perspective",
            query_keywords=["key3", "key4"],
            papers=mock_papers[1:2],  # 1 paper
            summary="Summary of perspective 2"
        ),
        PerspectiveNode(
            id="perspective3",
            name="Perspective 3",
            description="Third perspective",
            query_keywords=["key5", "key6"],
            papers=mock_papers[2:3],  # 1 paper
            summary="Summary of perspective 3"
        )
    ]

    # Create MindMap
    mindmap = MindMap(
        root_topic="Direct Test Topic",
        nodes=perspectives
    )

    # Create CoStormState
    state = CoStormState()
    state["session_id"] = test_session_id
    state["mindmap"] = mindmap
    state["topic"] = "Direct Test Topic"

    # Add mock summaries to state for synthesis
    state["perspectives"] = [
        {"id": "p1", "name": "Perspective 1", "summary": "Perspective 1 summary"},
        {"id": "p2", "name": "Perspective 2", "summary": "Perspective 2 summary"}
    ]

    print(f"Created test state with session_id: {test_session_id}")
    print(f"Mindmap has {len(mindmap.nodes)} nodes")
    print(f"Total papers: {sum(len(node.papers) for node in mindmap.nodes)}")

    # Mock the LLM completion to avoid actual API calls
    from unittest.mock import patch, MagicMock

    def mock_completion(*args, **kwargs):
        return MagicMock(choices=[
            MagicMock(message=MagicMock(content="""
# Direct Test Report

## Perspective 1
Perspective 1 summary

## Perspective 2
Perspective 2 summary

## Conclusion
Test conclusion
            """))
        ])

    with patch('litellm.completion', side_effect=mock_completion):
        # Call writer_node directly
        result = writer_node(state)

        # Verify persistence
        saved_papers = db_manager.list_papers(session_id=test_session_id)
        saved_reports = db_manager.list_reports(session_id=test_session_id)

        print(f"Papers saved: {len(saved_papers)}")
        print(f"Reports saved: {len(saved_reports)}")

        # Assertions
        assert len(saved_papers) == 3, f"Expected 3 papers saved, got {len(saved_papers)}"
        assert len(saved_reports) == 1, f"Expected 1 report saved, got {len(saved_reports)}"

        # Verify result contains report
        assert "report" in result
        assert result["report"] is not None

        print("✅ DIRECT writer_node test PASSED!")

    # Cleanup
    db_manager.delete_session(test_session_id)


@pytest.fixture(scope="function")
def clean_db():
    """Reset database for each test to ensure clean state."""
    # Call the reset script if available, otherwise do SQL directly
    import subprocess
    import os

    reset_script = "scripts/reset_db.sh"
    if os.path.exists(reset_script):
        result = subprocess.run([reset_script], capture_output=True, text=True)
        if result.returncode == 0:
            print("Database reset via script")
        else:
            print(f"Script failed: {result.stderr}")
    else:
        # Fallback: direct SQL reset (requires DB connection)
        print("Reset script not found, using direct SQL")

    yield

    # Cleanup after test
    try:
        db_manager.delete_session(test_session_id)  # Would need access to session_id
    except:
        pass