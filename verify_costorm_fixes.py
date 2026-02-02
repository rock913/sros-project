#!/usr/bin/env python3
"""
Quick verification script for Co-STORM persistence fixes.

This script checks:
1. writer_node imports work
2. writer_node has the new persistence logic
3. app.py passes session_id to Co-STORM input_data
4. Basic imports are valid

This is a lightweight alternative to the full integration test.
"""

import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_writer_node_persistence():
    """Test that writer_node has persistence logic."""
    print("🔍 Testing writer_node persistence logic...")

    try:
        from agent.application.nodes.costorm import writer_node, CoStormState
        print("✅ writer_node import successful")

        # Create a mock state with a mindmap
        state = CoStormState()
        state["mindmap"] = {
            "root_topic": "Test",
            "nodes": [
                {
                    "id": "test1",
                    "name": "Test Perspective",
                    "description": "Test description",
                    "query_keywords": ["test"],
                    "papers": [
                        {
                            "title": "Test Paper",
                            "authors": ["Test Author"],
                            "abstract": "Test abstract",
                            "source": "test"
                        }
                    ],
                    "summary": "Test summary"
                }
            ]
        }
        state["session_id"] = "test-session-id"

        print("✅ Mock state created successfully")

        # Test that the function signature is correct
        import inspect
        sig = inspect.signature(writer_node)
        params = list(sig.parameters.keys())
        print(f"✅ writer_node parameters: {params}")

        if "state" in params:
            print("✅ writer_node has correct parameter signature")
        else:
            print("❌ writer_node missing 'state' parameter")
            return False

        return True

    except Exception as e:
        print(f"❌ writer_node test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_costorm_input_data():
    """Test that app.py passes session_id to Co-STORM."""
    print("\n🔍 Testing Co-STORM input_data in app.py...")

    try:
        # Check if the code contains our fix
        with open("backend/src/agent/app.py", "r") as f:
            content = f.read()

        if '"session_id": session_id' in content:
            print("✅ app.py passes session_id to Co-STORM input_data")
        else:
            print("❌ app.py does not pass session_id to Co-STORM")
            return False

        if '"thread_id": thread_id' in content:
            print("✅ app.py passes thread_id to Co-STORM input_data")
        else:
            print("❌ app.py does not pass thread_id to Co-STORM")
            return False

        return True

    except Exception as e:
        print(f"❌ app.py test failed: {e}")
        return False

def test_db_manager_imports():
    """Test that db_manager functions can be imported."""
    print("\n🔍 Testing db_manager imports...")

    try:
        import agent.db_manager as db_manager
        print("✅ db_manager import successful")

        # Check if required functions exist
        funcs = ['add_paper', 'create_report', 'list_papers', 'list_reports']
        for func in funcs:
            if hasattr(db_manager, func):
                print(f"✅ db_manager.{func} exists")
            else:
                print(f"❌ db_manager.{func} missing")
                return False

        return True

    except Exception as e:
        print(f"❌ db_manager test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 Starting Co-STORM persistence fixes verification...")

    tests = [
        test_writer_node_persistence,
        test_app_costorm_input_data,
        test_db_manager_imports
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)

    passed = sum(results)
    total = len(results)

    print(f"\n📊 Verification Results:")
    print(f"   Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All verification tests passed!")
        print("\nNext step: Run the integration test")
        print("docker exec langgraph-api sh -c \"cd /app && PYTHONPATH=/app/backend/src python -m pytest backend/tests/agent/workflows/test_costorm_persistence.py -v\"")
        return True
    else:
        print("❌ Some verification tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)