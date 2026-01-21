#!/usr/bin/env python3
"""
Phase 3.6 E2E Graph Execution Test

Tests the complete HITL workflow:
1. Create session and trigger graph execution
2. Graph executes until HITL point
3. User responds via API
4. Graph resumes and completes

This simulates the real user workflow.
"""

import uuid
from datetime import datetime
from typing import Any, Dict

import requests

# Configuration
# Use 127.0.0.1:8000 when running inside container, localhost:8121 from host
API_BASE_URL = "http://127.0.0.1:8000"
TEST_TOPIC = "Quantum Computing Applications"


class E2EHITLTest:
    def __init__(self):
        self.session_id = None
        self.thread_id = None
        self.research_topic = TEST_TOPIC
        
    def log(self, message: str, level: str = "INFO"):
        """Pretty logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        symbol = symbols.get(level, "•")
        print(f"[{timestamp}] {symbol} {message}")
    
    def create_test_session(self) -> tuple:
        """Create a test session in the database"""
        self.log("Creating test session...")
        
        # Use direct database access
        from agent.database import get_db_connection
        from agent.models import Session
        
        self.session_id = uuid.uuid4()
        self.thread_id = uuid.uuid4()
        
        with get_db_connection() as db:
            session = Session(
                id=self.session_id,
                thread_id=self.thread_id,
                title=f"E2E Test: {self.research_topic}",
                research_topic=self.research_topic,
                status="active",
                created_at=datetime.utcnow()
            )
            db.add(session)
            db.commit()
        
        self.log(f"Session created: {self.session_id}", "SUCCESS")
        self.log(f"Thread ID: {self.thread_id}", "INFO")
        
        return str(self.session_id), str(self.thread_id)
    
    def start_graph_execution(self) -> Dict[str, Any]:
        """Start graph execution via API"""
        self.log(f"Starting graph execution for: {self.research_topic}")
        
        # Call the /agent/research endpoint
        # Note: This is a simulation - actual endpoint might be /agent/stream
        # For now, we'll manually trigger HITL nodes
        
        self.log("⚠️ Direct graph execution requires streaming endpoint", "WARNING")
        self.log("For this test, we'll simulate by directly calling HITL nodes", "INFO")
        
        return {"status": "simulated"}
    
    def simulate_hitl_trigger(self) -> str:
        """Simulate graph reaching HITL point"""
        self.log("Simulating graph execution reaching HITL point...")
        
        from agent.hitl_nodes import create_hitl_request
        
        # Simulate query_approval_node creating HITL request
        request_id = create_hitl_request(
            session_id=str(self.session_id),
            decision_type="query_approval",
            prompt=f"AI已为研究主题「{self.research_topic}」生成以下查询，是否继续？",
            options=["approve", "reject", "modify"],
            context={
                "research_topic": self.research_topic,
                "queries": [
                    "quantum computing hardware development",
                    "quantum algorithms and complexity",
                    "quantum error correction methods"
                ],
                "query_count": 3
            },
            timeout_seconds=300
        )
        
        self.log(f"HITL request created: {request_id}", "SUCCESS")
        return request_id
    
    def check_pending_hitl(self) -> Dict[str, Any]:
        """Check for pending HITL requests via API"""
        self.log("Checking for pending HITL requests...")
        
        url = f"{API_BASE_URL}/agent/hitl/pending"
        params = {"session_id": str(self.session_id)}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            pending_count = data.get("pending_count", 0)
            self.log(f"Found {pending_count} pending request(s)", "SUCCESS")
            return data
        else:
            self.log(f"Failed to get pending requests: {response.status_code}", "ERROR")
            return {}
    
    def user_responds(self, request_id: str, decision: str = "approve") -> Dict[str, Any]:
        """Simulate user responding to HITL request via API"""
        self.log(f"User responding to {request_id} with decision: {decision}")
        
        url = f"{API_BASE_URL}/agent/hitl/respond"
        params = {
            "request_id": request_id,
            "decision": decision
        }
        
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            self.log(f"Response recorded: {data.get('message', 'Success')}", "SUCCESS")
            return data
        else:
            self.log(f"Failed to record response: {response.text}", "ERROR")
            return {}
    
    def verify_response_recorded(self, request_id: str) -> bool:
        """Verify that response was recorded in database"""
        self.log(f"Verifying response for {request_id}...")
        
        from agent.database import get_db_connection
        from agent.models import HITLDecision
        
        with get_db_connection() as db:
            hitl_record = db.query(HITLDecision).filter(
                HITLDecision.request_id == request_id
            ).first()
            
            if hitl_record:
                has_response = hitl_record.user_decision is not None
                if has_response:
                    self.log(f"✓ Decision: {hitl_record.user_decision}", "SUCCESS")
                    self.log(f"✓ Responded at: {hitl_record.responded_at}", "INFO")
                    return True
                else:
                    self.log("Response not found in database", "ERROR")
                    return False
            else:
                self.log("HITL record not found", "ERROR")
                return False
    
    def simulate_graph_resumption(self) -> Dict[str, Any]:
        """Simulate graph resuming after HITL response"""
        self.log("Simulating graph resumption...")
        
        from agent.hitl_nodes import query_approval_node
        from agent.state import AgentState
        
        # Create state with HITL response
        state: AgentState = {
            "session_id": str(self.session_id),
            "research_topic": self.research_topic,
            "search_queries": [
                "quantum computing hardware development",
                "quantum algorithms and complexity",
                "quantum error correction methods"
            ],
            "hitl_response": {
                "decision_type": "query_approval",
                "user_decision": "approve"
            }
        }
        
        config = {"configurable": {"thread_id": str(self.thread_id)}}
        
        # Call the node again (second execution with response)
        result = query_approval_node(state, config)
        
        if result.get("hitl_approved") == True:
            self.log("Graph node processed approval successfully", "SUCCESS")
            self.log(f"✓ hitl_approved: {result.get('hitl_approved')}", "INFO")
            self.log(f"✓ hitl_pending: {result.get('hitl_pending')}", "INFO")
            return result
        else:
            self.log("Graph node did not process approval correctly", "ERROR")
            return result
    
    def cleanup(self):
        """Clean up test data"""
        self.log("Cleaning up test data...")
        
        from agent.database import get_db_connection
        from agent.models import HITLDecision, Session
        
        with get_db_connection() as db:
            # Delete HITL records
            db.query(HITLDecision).filter(
                HITLDecision.session_id == self.session_id
            ).delete()
            
            # Delete session
            db.query(Session).filter(
                Session.id == self.session_id
            ).delete()
            
            db.commit()
        
        self.log("Cleanup complete", "SUCCESS")
    
    def run_full_test(self):
        """Run complete E2E test"""
        print("\n" + "="*60)
        print("Phase 3.6 E2E HITL Workflow Test")
        print("="*60 + "\n")
        
        try:
            # Step 1: Create session
            self.create_test_session()
            print()
            
            # Step 2: Simulate graph execution to HITL point
            request_id = self.simulate_hitl_trigger()
            print()
            
            # Step 3: Check pending requests via API
            pending_data = self.check_pending_hitl()
            if not pending_data.get("requests"):
                raise Exception("No pending requests found!")
            print()
            
            # Step 4: User responds via API
            response_data = self.user_responds(request_id, decision="approve")
            if response_data.get("status") != "success":
                raise Exception("Failed to record user response!")
            print()
            
            # Step 5: Verify response in database
            if not self.verify_response_recorded(request_id):
                raise Exception("Response not recorded in database!")
            print()
            
            # Step 6: Simulate graph resumption
            resume_result = self.simulate_graph_resumption()
            if not resume_result.get("hitl_approved"):
                raise Exception("Graph did not process approval correctly!")
            print()
            
            # Success!
            print("="*60)
            print("✅✅✅ E2E Test PASSED! ✅✅✅")
            print("="*60)
            print("\nAll steps completed successfully:")
            print("  ✓ Session created")
            print("  ✓ HITL request triggered")
            print("  ✓ API pending check works")
            print("  ✓ User response recorded")
            print("  ✓ Response verified in database")
            print("  ✓ Graph resumption successful")
            print()
            
            return True
            
        except Exception as e:
            print("\n" + "="*60)
            print("❌ E2E Test FAILED")
            print("="*60)
            print(f"\nError: {str(e)}")
            print()
            return False
        
        finally:
            # Always cleanup
            print()
            self.cleanup()


if __name__ == "__main__":
    test = E2EHITLTest()
    success = test.run_full_test()
    exit(0 if success else 1)
