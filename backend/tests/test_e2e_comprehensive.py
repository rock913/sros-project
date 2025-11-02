#!/usr/bin/env python3
"""
Phase 3.6 E2E Test Suite - All 3 HITL Nodes

Comprehensive E2E testing for:
1. Query Approval (approve/reject/modify)
2. Paper Selection (select_all/select_subset/reject)
3. Report Revision (approve/modify/reject)
"""

import sys
import time
from test_e2e_hitl_flow import E2EHITLTest


class ComprehensiveE2ETest:
    """Test all 3 HITL nodes with different decision paths"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def test_query_approval_approve(self):
        """Test 1: Query Approval with APPROVE decision"""
        print("\n" + "="*60)
        print("Test 1: Query Approval → APPROVE")
        print("="*60)
        
        test = E2EHITLTest()
        try:
            test.create_test_session()
            request_id = test.simulate_hitl_trigger()
            test.check_pending_hitl()
            test.user_responds(request_id, decision="approve")
            test.verify_response_recorded(request_id)
            result = test.simulate_graph_resumption()
            
            assert result.get("hitl_approved") == True
            assert result.get("hitl_pending") == False
            
            print("✅ Test 1 PASSED\n")
            self.tests_passed += 1
            self.results.append(("Query Approval (Approve)", "PASSED"))
            return True
        except Exception as e:
            print(f"❌ Test 1 FAILED: {e}\n")
            self.tests_failed += 1
            self.results.append(("Query Approval (Approve)", f"FAILED: {e}"))
            return False
        finally:
            test.cleanup()
    
    def test_query_approval_reject(self):
        """Test 2: Query Approval with REJECT decision"""
        print("\n" + "="*60)
        print("Test 2: Query Approval → REJECT")
        print("="*60)
        
        test = E2EHITLTest()
        try:
            test.create_test_session()
            request_id = test.simulate_hitl_trigger()
            test.user_responds(request_id, decision="reject")
            test.verify_response_recorded(request_id)
            
            # Simulate graph resumption with reject
            from agent.hitl_nodes import query_approval_node
            
            state = {
                "session_id": str(test.session_id),
                "research_topic": test.research_topic,
                "search_queries": ["query1", "query2"],
                "hitl_response": {
                    "decision_type": "query_approval",
                    "user_decision": "reject"
                }
            }
            config = {"configurable": {"thread_id": str(test.thread_id)}}
            result = query_approval_node(state, config)
            
            assert result.get("stop_research") == True
            assert result.get("hitl_approved") == False
            
            print("✅ Test 2 PASSED\n")
            self.tests_passed += 1
            self.results.append(("Query Approval (Reject)", "PASSED"))
            return True
        except Exception as e:
            print(f"❌ Test 2 FAILED: {e}\n")
            self.tests_failed += 1
            self.results.append(("Query Approval (Reject)", f"FAILED: {e}"))
            return False
        finally:
            test.cleanup()
    
    def test_paper_selection_select_all(self):
        """Test 3: Paper Selection with SELECT_ALL decision"""
        print("\n" + "="*60)
        print("Test 3: Paper Selection → SELECT_ALL")
        print("="*60)
        
        test = E2EHITLTest()
        try:
            test.create_test_session()
            
            # Create paper selection HITL request
            from agent.hitl_nodes import create_hitl_request
            
            papers = [{"title": f"Paper {i}", "doi": f"10.1234/{i}"} for i in range(25)]
            
            request_id = create_hitl_request(
                session_id=str(test.session_id),
                decision_type="paper_selection",
                prompt="请选择要分析的论文",
                options=["select_all", "select_subset", "reject"],
                context={"papers": papers, "total_count": 25},
                timeout_seconds=300
            )
            
            test.log(f"Paper selection request created: {request_id}", "SUCCESS")
            
            # User responds
            test.user_responds(request_id, decision="select_all")
            test.verify_response_recorded(request_id)
            
            # Simulate graph resumption
            from agent.hitl_nodes import paper_selection_node
            
            state = {
                "session_id": str(test.session_id),
                "literature_abstracts": papers,
                "hitl_response": {
                    "decision_type": "paper_selection",
                    "user_decision": "select_all"
                }
            }
            config = {"configurable": {"thread_id": str(test.thread_id)}}
            result = paper_selection_node(state, config)
            
            assert result.get("paper_selection_done") == True
            assert result.get("hitl_approved") == True
            assert len(result.get("selected_papers", [])) == 25
            
            print("✅ Test 3 PASSED\n")
            self.tests_passed += 1
            self.results.append(("Paper Selection (Select All)", "PASSED"))
            return True
        except Exception as e:
            print(f"❌ Test 3 FAILED: {e}\n")
            self.tests_failed += 1
            self.results.append(("Paper Selection (Select All)", f"FAILED: {e}"))
            return False
        finally:
            test.cleanup()
    
    def test_report_revision_approve(self):
        """Test 4: Report Revision with APPROVE decision"""
        print("\n" + "="*60)
        print("Test 4: Report Revision → APPROVE")
        print("="*60)
        
        test = E2EHITLTest()
        try:
            test.create_test_session()
            
            # Create report revision HITL request
            from agent.hitl_nodes import create_hitl_request
            
            test_report = "# Research Report\n\nThis is a test report on quantum computing."
            
            request_id = create_hitl_request(
                session_id=str(test.session_id),
                decision_type="report_revision",
                prompt="请审核研究报告",
                options=["approve", "modify", "reject"],
                context={
                    "report": test_report,
                    "word_count": len(test_report.split()),
                    "research_topic": test.research_topic
                },
                timeout_seconds=900
            )
            
            test.log(f"Report revision request created: {request_id}", "SUCCESS")
            
            # User responds
            test.user_responds(request_id, decision="approve")
            test.verify_response_recorded(request_id)
            
            # Simulate graph resumption
            from agent.hitl_nodes import report_revision_node
            
            state = {
                "session_id": str(test.session_id),
                "report": test_report,
                "research_topic": test.research_topic,
                "hitl_response": {
                    "decision_type": "report_revision",
                    "user_decision": "approve"
                }
            }
            config = {"configurable": {"thread_id": str(test.thread_id)}}
            result = report_revision_node(state, config)
            
            assert result.get("final_report") == test_report
            assert result.get("hitl_approved") == True
            
            print("✅ Test 4 PASSED\n")
            self.tests_passed += 1
            self.results.append(("Report Revision (Approve)", "PASSED"))
            return True
        except Exception as e:
            print(f"❌ Test 4 FAILED: {e}\n")
            self.tests_failed += 1
            self.results.append(("Report Revision (Approve)", f"FAILED: {e}"))
            return False
        finally:
            test.cleanup()
    
    def test_api_duplicate_response(self):
        """Test 5: API rejects duplicate responses"""
        print("\n" + "="*60)
        print("Test 5: Duplicate Response Rejection")
        print("="*60)
        
        test = E2EHITLTest()
        try:
            test.create_test_session()
            request_id = test.simulate_hitl_trigger()
            
            # First response
            test.user_responds(request_id, decision="approve")
            
            # Second response (should fail)
            import requests
            url = f"http://127.0.0.1:8000/agent/hitl/respond"
            response = requests.post(url, params={
                "request_id": request_id,
                "decision": "reject"
            })
            
            assert response.status_code == 400  # Bad request
            assert "already responded" in response.text.lower()
            
            print("✅ Test 5 PASSED\n")
            self.tests_passed += 1
            self.results.append(("Duplicate Response Rejection", "PASSED"))
            return True
        except Exception as e:
            print(f"❌ Test 5 FAILED: {e}\n")
            self.tests_failed += 1
            self.results.append(("Duplicate Response Rejection", f"FAILED: {e}"))
            return False
        finally:
            test.cleanup()
    
    def run_all_tests(self):
        """Run all E2E tests"""
        print("\n" + "="*70)
        print(" "*15 + "Phase 3.6 Comprehensive E2E Test Suite")
        print("="*70)
        
        start_time = time.time()
        
        # Run all tests
        self.test_query_approval_approve()
        self.test_query_approval_reject()
        self.test_paper_selection_select_all()
        self.test_report_revision_approve()
        self.test_api_duplicate_response()
        
        duration = time.time() - start_time
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        for test_name, result in self.results:
            status = "✅" if result == "PASSED" else "❌"
            print(f"{status} {test_name:40s} {result}")
        
        print("\n" + "-"*70)
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {total}")
        print(f"Passed:      {self.tests_passed} ({self.tests_passed/total*100:.0f}%)")
        print(f"Failed:      {self.tests_failed}")
        print(f"Duration:    {duration:.2f}s")
        print("-"*70)
        
        if self.tests_failed == 0:
            print("\n🎉🎉🎉 ALL TESTS PASSED! 🎉🎉🎉\n")
            return True
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed\n")
            return False


if __name__ == "__main__":
    suite = ComprehensiveE2ETest()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
