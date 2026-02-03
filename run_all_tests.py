#!/usr/bin/env python3
"""
Test runner for SROS system - executes all test suites in order.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_test_suite(suite_name, script_path):
    """Run a test suite and return results."""
    print(f"\n{'='*60}")
    print(f"Running {suite_name}")
    print(f"{'='*60}")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, script_path],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True,
                              timeout=300)  # 5 minute timeout
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {suite_name} completed successfully")
            return True
        else:
            print(f"❌ {suite_name} failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {suite_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ {suite_name} failed with exception: {e}")
        return False

def main():
    """Run all test suites in order."""
    print("SROS Comprehensive Test Suite Runner")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define test suites in order of execution
    test_suites = [
        ("Unit Tests", "mcp_servers/mcp_sros_logic/tests.py"),
        ("Enhanced Unit Tests", "mcp_servers/mcp_sros_logic/tests_enhanced.py"),
        ("Integration Tests", "mcp_servers/mcp_sros_logic/integration_tests.py"),
        ("Zotero Expert Comprehensive Tests", "mcp_servers/zotero_expert/comprehensive_test.py"),
        ("Performance Tests", "performance_tests.py"),
        ("Stress Tests", "stress_tests.py"),
        ("End-to-End Tests", "end_to_end_tests.py")
    ]
    
    # Track results
    results = []
    
    # Run each test suite
    for suite_name, script_path in test_suites:
        if os.path.exists(script_path):
            success = run_test_suite(suite_name, script_path)
            results.append((suite_name, success))
        else:
            print(f"⚠️  Skipping {suite_name} - script not found: {script_path}")
            results.append((suite_name, False))
    
    # Print final summary
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Test suites completed: {passed}/{total}")
    
    for suite_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {suite_name}")
    
    # Overall result
    if passed == total:
        print("\n🎉 ALL TEST SUITES PASSED")
        print("🚀 SROS system is ready for deployment!")
        return 0
    elif passed >= total * 0.8:
        print(f"\n⚠️  MOST TESTS PASSED ({passed}/{total})")
        print("✅ System is mostly ready, some minor issues to address")
        return 1
    else:
        print(f"\n❌ SIGNIFICANT TEST FAILURES ({passed}/{total})")
        print("⚠️  System requires substantial improvements before deployment")
        return 2

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)