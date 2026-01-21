"""
Phase 3.6 HITL Nodes Unit Tests

Tests for query_approval_node, paper_selection_node, and report_revision_node
"""

import uuid
from datetime import datetime

import pytest

from agent.database import get_db_connection
from agent.hitl_nodes import (
    paper_selection_node,
    query_approval_node,
    report_revision_node,
)
from agent.models import Session
from agent.state import AgentState

# Test UUID (valid format)
TEST_SESSION_ID = str(uuid.uuid4())
TEST_THREAD_ID = uuid.uuid4()


def setup_test_session():
    """Create a test session in the database"""
    with get_db_connection() as db:
        # Check if session already exists
        existing = db.query(Session).filter_by(id=uuid.UUID(TEST_SESSION_ID)).first()
        if not existing:
            test_session = Session(
                id=uuid.UUID(TEST_SESSION_ID),
                thread_id=TEST_THREAD_ID,
                title="Test Session for HITL Unit Tests",
                research_topic="Quantum Computing",
                status="active",
                created_at=datetime.utcnow()
            )
            db.add(test_session)
            db.commit()
            print(f"✅ Created test session: {TEST_SESSION_ID}")
        else:
            print(f"✅ Test session already exists: {TEST_SESSION_ID}")


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Pytest fixture to setup test database before all tests in this module"""
    setup_test_session()
    yield
    # Cleanup after all tests (optional)
    # with get_db_connection() as db:
    #     db.query(Session).filter_by(id=uuid.UUID(TEST_SESSION_ID)).delete()
    #     db.commit()


class TestQueryApprovalNode:
    """Test query_approval_node function"""
    
    def test_first_call_creates_hitl_request(self):
        """Test that first call creates HITL request and sets hitl_pending"""
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "search_queries": ["quantum computing applications", "quantum algorithms"],
            "research_topic": "Quantum Computing"
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = query_approval_node(state, config)
        
        assert result.get("hitl_pending") == True, "Should set hitl_pending=True"
        assert result.get("hitl_request") is not None, "Should create hitl_request"
        assert result["hitl_request"]["type"] == "query_approval"  # Note: uses 'type' not 'decision_type'
        assert "request_id" in result["hitl_request"]
        
        print("✅ Test 1.1a: Query approval creates HITL request")
    
    def test_approve_decision(self):
        """Test that approve decision sets hitl_approved=True"""
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "hitl_response": {
                "decision_type": "query_approval",
                "user_decision": "approve"
            }
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = query_approval_node(state, config)
        
        assert result.get("hitl_pending") == False, "Should clear hitl_pending"
        assert result.get("hitl_approved") == True, "Should set hitl_approved=True"
        assert result.get("hitl_response") is None, "Should clear hitl_response"
        
        print("✅ Test 1.1b: Query approval processes approve decision")
    
    def test_reject_decision(self):
        """Test that reject decision sets stop_research=True"""
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "hitl_response": {
                "decision_type": "query_approval",
                "user_decision": "reject"
            }
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = query_approval_node(state, config)
        
        assert result.get("stop_research") == True, "Should set stop_research=True"
        assert result.get("hitl_pending") == False, "Should clear hitl_pending"
        
        print("✅ Test 1.1c: Query approval processes reject decision")


class TestPaperSelectionNode:
    """Test paper_selection_node function"""
    
    def test_skip_when_few_papers(self):
        """Test that HITL is skipped when papers <= 20"""
        state: AgentState = {
            "literature_abstracts": [{"title": f"Paper {i}"} for i in range(10)]
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = paper_selection_node(state, config)
        
        assert result.get("paper_selection_done") == True, "Should skip HITL"
        assert result.get("hitl_pending") != True, "Should not set hitl_pending"
        
        print("✅ Test 1.2a: Paper selection skips HITL for few papers")
    
    def test_trigger_when_many_papers(self):
        """Test that HITL is triggered when papers > 20"""
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "literature_abstracts": [{"title": f"Paper {i}", "doi": f"10.1234/{i}"} for i in range(30)]
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = paper_selection_node(state, config)
        
        assert result.get("hitl_pending") == True, "Should trigger HITL"
        assert result.get("hitl_request") is not None, "Should create hitl_request"
        assert result["hitl_request"]["type"] == "paper_selection"
        
        print("✅ Test 1.2b: Paper selection triggers HITL for many papers")
    
    def test_select_all_decision(self):
        """Test that select_all returns all papers"""
        papers = [{"title": f"Paper {i}"} for i in range(30)]
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "literature_abstracts": papers,
            "hitl_response": {
                "decision_type": "paper_selection",
                "user_decision": "select_all"
            }
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = paper_selection_node(state, config)
        
        assert result.get("selected_papers") == papers, "Should return all papers"
        assert result.get("paper_selection_done") == True
        assert result.get("hitl_approved") == True
        
        print("✅ Test 1.2c: Paper selection processes select_all decision")


class TestReportRevisionNode:
    """Test report_revision_node function"""
    
    def test_creates_hitl_request(self):
        """Test that report revision creates HITL request"""
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "report": "# Test Report\n\nThis is a test report.",
            "research_topic": "Test Topic"
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = report_revision_node(state, config)
        
        assert result.get("hitl_pending") == True
        assert result.get("hitl_request") is not None
        assert result["hitl_request"]["type"] == "report_revision"
        
        print("✅ Test 1.3a: Report revision creates HITL request")
    
    def test_approve_decision(self):
        """Test that approve decision returns final_report"""
        report = "# Test Report\n\nContent..."
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "report": report,
            "hitl_response": {
                "decision_type": "report_revision",
                "user_decision": "approve"
            }
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = report_revision_node(state, config)
        
        assert result.get("final_report") == report, "Should return report as final"
        assert result.get("hitl_pending") == False
        assert result.get("hitl_approved") == True
        
        print("✅ Test 1.3b: Report revision processes approve decision")
    
    def test_modify_decision(self):
        """Test that modify decision appends feedback"""
        original_report = "# Test Report\n\nContent..."
        feedback = "Please add more details about methodology"
        
        state: AgentState = {
            "session_id": TEST_SESSION_ID,
            "report": original_report,
            "hitl_response": {
                "decision_type": "report_revision",
                "user_decision": "modify",
                "modified_data": {
                    "feedback": feedback
                }
            }
        }
        config = {"configurable": {"thread_id": "test_thread"}}
        
        result = report_revision_node(state, config)
        
        assert feedback in result.get("final_report", ""), "Should include feedback"
        assert result.get("hitl_pending") == False
        assert result.get("hitl_approved") == True
        
        print("✅ Test 1.3c: Report revision processes modify decision with feedback")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3.6 HITL Nodes Unit Tests")
    print("=" * 60)
    print()
    
    # Setup: Create test session in database
    setup_test_session()
    print()
    
    # Run Query Approval tests
    print("\n📋 Testing Query Approval Node...")
    test_qa = TestQueryApprovalNode()
    test_qa.test_first_call_creates_hitl_request()
    test_qa.test_approve_decision()
    test_qa.test_reject_decision()
    
    # Run Paper Selection tests
    print("\n📋 Testing Paper Selection Node...")
    test_ps = TestPaperSelectionNode()
    test_ps.test_skip_when_few_papers()
    test_ps.test_trigger_when_many_papers()
    test_ps.test_select_all_decision()
    
    # Run Report Revision tests
    print("\n📋 Testing Report Revision Node...")
    test_rr = TestReportRevisionNode()
    test_rr.test_creates_hitl_request()
    test_rr.test_approve_decision()
    test_rr.test_modify_decision()
    
    print("\n" + "=" * 60)
    print("✅✅✅ All Unit Tests Passed! ✅✅✅")
    print("=" * 60)
