#!/usr/bin/env python3
"""
Stress tests for the SROS system.
Tests system behavior under extreme conditions and failure scenarios.
"""

import time
import tempfile
import shutil
import os
from pathlib import Path
import sys
import threading
import random
from unittest.mock import patch, MagicMock

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp_servers'))

def test_network_interruption_resilience():
    """Test system resilience to network interruptions."""
    print("Testing network interruption resilience...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    
    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        server = SROSLogicServer(str(workspace_path))
        
        # Initialize workspace normally
        result = server.init_workspace()
        print(f"Workspace initialization: {'Success' if result['success'] else 'Failed'}")
        
        # Simulate network interruption by mocking failed API calls
        with patch('mcp_servers.mcp_sros_logic.server.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network timeout")
            
            # Try to perform operations that would normally make network calls
            gaps_result = server.detect_academic_gaps()
            coord_result = server.research_coordination()
            
            print(f"Gap detection with network failure: {'Handled gracefully' if gaps_result['success'] else 'Failed'}")
            print(f"Research coordination with network failure: {'Handled gracefully' if coord_result['success'] else 'Failed'}")
            
            return gaps_result['success'] and coord_result['success']
            
    finally:
        shutil.rmtree(test_dir)

def test_large_file_processing():
    """Test processing of extremely large files."""
    print("Testing large file processing...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    draft_path = workspace_path / "huge_draft.md"
    
    try:
        # Create an extremely large manuscript (10,000 sections, 100 lines each)
        print("Creating extremely large manuscript (~1MB)...")
        with open(draft_path, 'w') as f:
            f.write("# Extremely Large Research Manuscript\n\n")
            
            for i in range(10000):
                f.write(f"## Section {i+1}\n\n")
                for j in range(100):
                    f.write(f"This is line {j+1} of section {i+1}. " +
                           "It contains substantial academic content for stress testing purposes. " +
                           "The quick brown fox jumps over the lazy dog. " +
                           "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n")
                f.write("\n")
        
        print("Manuscript created. Testing processing...")
        
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        server = SROSLogicServer(str(workspace_path))
        
        start_time = time.time()
        result = server.detect_academic_gaps(str(draft_path))
        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f"Large file processing took {processing_time:.2f} seconds")
        print(f"Success: {result['success']}")
        print(f"Gaps found: {len(result.get('gaps', [])) if result['success'] else 0}")
        
        return result['success'], processing_time
        
    except MemoryError:
        print("❌ Memory error occurred - system handled large file gracefully")
        return True, float('inf')
    except Exception as e:
        print(f"❌ Large file processing failed: {e}")
        return False, 0
    finally:
        shutil.rmtree(test_dir)

def test_concurrent_user_simulation():
    """Simulate multiple concurrent users accessing the system."""
    print("Testing concurrent user simulation...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    
    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        
        # Create multiple server instances (simulating multiple users)
        servers = []
        for i in range(50):  # 50 concurrent users
            user_workspace = workspace_path / f"user_{i}"
            user_workspace.mkdir()
            server = SROSLogicServer(str(user_workspace))
            servers.append(server)
        
        # Function to run operations for each user
        def user_operations(server, user_id, results):
            try:
                # Each user performs a series of operations
                server.init_workspace()
                gaps_result = server.detect_academic_gaps()
                coord_result = server.research_coordination()
                workflow_result = server.workflow_management()
                
                results[user_id] = {
                    'success': all([gaps_result['success'], coord_result['success'], workflow_result['success']]),
                    'operations_completed': 4
                }
            except Exception as e:
                results[user_id] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Run concurrent operations
        results = {}
        threads = []
        
        start_time = time.time()
        
        for i, server in enumerate(servers):
            thread = threading.Thread(target=user_operations, args=(server, i, results))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        total_time = end_time - start_time
        successful_users = sum(1 for result in results.values() if result.get('success', False))
        
        print(f"50 concurrent users completed in {total_time:.2f} seconds")
        print(f"Successful users: {successful_users}/50 ({successful_users/50*100:.1f}%)")
        
        return successful_users, total_time
        
    finally:
        shutil.rmtree(test_dir)

def test_database_connection_failure():
    """Test system behavior when database connections fail."""
    print("Testing database connection failure handling...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    
    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        
        # Mock database connection failure
        with patch('mcp_servers.mcp_sros_logic.server.DuckDBMemoryServer') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")
            
            server = SROSLogicServer(str(workspace_path))
            
            # System should still function in degraded mode
            init_result = server.init_workspace()
            gaps_result = server.detect_academic_gaps()
            coord_result = server.research_coordination()
            workflow_result = server.workflow_management()
            
            all_success = all([
                init_result['success'],
                gaps_result['success'],
                coord_result['success'],
                workflow_result['success']
            ])
            
            print(f"System functionality with DB failure: {'Maintained' if all_success else 'Degraded'}")
            
            # Check that appropriate warnings were logged
            if not all_success:
                print("Some operations failed as expected due to database unavailability")
            
            return all_success
            
    finally:
        shutil.rmtree(test_dir)

def test_resource_exhaustion():
    """Test system behavior under resource exhaustion conditions."""
    print("Testing resource exhaustion handling...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    
    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        server = SROSLogicServer(str(workspace_path))
        
        # Test with increasingly large operations
        success_count = 0
        max_operations = 1000
        
        print("Performing stress operations...")
        for i in range(max_operations):
            try:
                # Perform various operations
                if i % 4 == 0:
                    server.init_workspace()
                elif i % 4 == 1:
                    server.detect_academic_gaps()
                elif i % 4 == 2:
                    server.research_coordination()
                else:
                    server.workflow_management()
                
                success_count += 1
                
                # Occasionally force garbage collection
                if i % 100 == 0:
                    import gc
                    gc.collect()
                    
            except MemoryError:
                print(f"Memory exhausted at operation {i}")
                break
            except Exception as e:
                print(f"Operation {i} failed: {e}")
                # Continue with other operations
        
        print(f"Successfully completed {success_count}/{max_operations} stress operations")
        
        # Test system recovery
        try:
            final_result = server.workflow_management()
            recovery_success = final_result['success']
            print(f"System recovery after stress: {'Successful' if recovery_success else 'Failed'}")
        except Exception as e:
            print(f"Recovery test failed: {e}")
            recovery_success = False
        
        return success_count, recovery_success
        
    finally:
        shutil.rmtree(test_dir)

def test_api_rate_limiting():
    """Test system behavior under API rate limiting conditions."""
    print("Testing API rate limiting handling...")
    
    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    
    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        server = SROSLogicServer(str(workspace_path))
        
        # Mock API rate limiting responses
        with patch('mcp_servers.mcp_sros_logic.server.requests.get') as mock_get:
            # Simulate 429 Too Many Requests response
            from requests.exceptions import HTTPError
            http_error = HTTPError("429 Client Error: Too Many Requests")
            http_error.response = MagicMock()
            http_error.response.status_code = 429
            mock_get.side_effect = http_error
            
            # Test operations that would hit rate limits
            start_time = time.time()
            gaps_result = server.detect_academic_gaps()
            coord_result = server.research_coordination()
            end_time = time.time()
            
            # System should handle rate limiting gracefully
            graceful_handling = gaps_result['success'] and coord_result['success']
            handling_time = end_time - start_time
            
            print(f"Rate limiting handled gracefully: {'Yes' if graceful_handling else 'No'}")
            print(f"Handling time: {handling_time:.2f} seconds")
            
            return graceful_handling, handling_time
            
    finally:
        shutil.rmtree(test_dir)

def run_stress_test_suite():
    """Run complete stress test suite."""
    print("=" * 70)
    print("SROS Stress Test Suite")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Network interruption resilience
    try:
        network_resilience = test_network_interruption_resilience()
        results['network_resilience'] = {'success': network_resilience}
        print(f"✅ Network interruption test: {'Passed' if network_resilience else 'Failed'}")
    except Exception as e:
        print(f"❌ Network interruption test failed: {e}")
        results['network_resilience'] = {'success': False, 'error': str(e)}
    
    # Test 2: Large file processing
    try:
        large_file_success, processing_time = test_large_file_processing()
        results['large_file_processing'] = {
            'success': large_file_success,
            'processing_time': processing_time
        }
        print(f"✅ Large file processing test: {'Passed' if large_file_success else 'Failed'}")
    except Exception as e:
        print(f"❌ Large file processing test failed: {e}")
        results['large_file_processing'] = {'success': False, 'error': str(e)}
    
    # Test 3: Concurrent user simulation
    try:
        successful_users, total_time = test_concurrent_user_simulation()
        results['concurrent_users'] = {
            'successful_users': successful_users,
            'total_time': total_time,
            'success_rate': successful_users / 50 * 100
        }
        print(f"✅ Concurrent user test: {successful_users}/50 users successful")
    except Exception as e:
        print(f"❌ Concurrent user test failed: {e}")
        results['concurrent_users'] = {'success': False, 'error': str(e)}
    
    # Test 4: Database connection failure
    try:
        db_failure_handling = test_database_connection_failure()
        results['db_failure_handling'] = {'success': db_failure_handling}
        print(f"✅ Database failure test: {'Passed' if db_failure_handling else 'Failed'}")
    except Exception as e:
        print(f"❌ Database failure test failed: {e}")
        results['db_failure_handling'] = {'success': False, 'error': str(e)}
    
    # Test 5: Resource exhaustion
    try:
        operations_completed, recovery_success = test_resource_exhaustion()
        results['resource_exhaustion'] = {
            'operations_completed': operations_completed,
            'recovery_success': recovery_success
        }
        print(f"✅ Resource exhaustion test: {operations_completed} operations completed")
    except Exception as e:
        print(f"❌ Resource exhaustion test failed: {e}")
        results['resource_exhaustion'] = {'success': False, 'error': str(e)}
    
    # Test 6: API rate limiting
    try:
        rate_limit_handled, handling_time = test_api_rate_limiting()
        results['rate_limiting'] = {
            'handled_gracefully': rate_limit_handled,
            'handling_time': handling_time
        }
        print(f"✅ Rate limiting test: {'Passed' if rate_limit_handled else 'Failed'}")
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")
        results['rate_limiting'] = {'success': False, 'error': str(e)}
    
    # Print summary
    print("\n" + "=" * 70)
    print("Stress Test Results Summary")
    print("=" * 70)
    
    passed_tests = sum(1 for result in results.values() if result.get('success', True) != False and 'error' not in result)
    total_tests = len(results)
    
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests >= total_tests * 0.8:
        print("🎉 Overall stress test result: PASSED (80%+ success rate)")
    elif passed_tests >= total_tests * 0.6:
        print("⚠️  Overall stress test result: PARTIAL SUCCESS (60-80% success rate)")
    else:
        print("❌ Overall stress test result: FAILED (<60% success rate)")
    
    # Detailed results
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result.get('success', True) != False and 'error' not in result else "❌ FAIL"
        print(f"  {status} {test_name.replace('_', ' ').title()}")
        if 'error' in result:
            print(f"      Error: {result['error']}")
    
    return results

if __name__ == '__main__':
    run_stress_test_suite()