#!/usr/bin/env python3
"""
Manual Test Script for Co-STORM Graph Isolation Diagnosis

Purpose: Directly test the costorm_graph in isolation without WebSocket mediation.
This script identifies whether the "Unknown error" originates from Graph internal issues
or WebSocket handling problems.

USAGE:
    cd backend
    python -m pytest tests/manual_test_costorm.py -v -s
    OR
    PYTHONPATH=/app python tests/manual_test_costorm.py

EXTERNAL DEPENDENCIES:
- Requires POSTGRES_URI environment variable
- Requires database connection (assumes containers are up)
- Requires GEMINI_API_KEY for LLM calls (node execution)

WORKFLOW:
1. Import and initialize costorm_graph
2. Create test input state matching CoStormState schema
3. Execute graph.ainvoke() asynchronously
4. Print full stack trace on failure or success metrics on success
"""

import asyncio
import os
import sys
import traceback
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend/src to Python path for MPA imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # MPA hexagonal imports for isolation testing
    from agent.application.workflows.costorm_graph import get_costorm_graph
    from agent.application.nodes.costorm import CoStormState
    print("✓ Successfully imported costorm_graph and domain schemas")

except ImportError as e:
    print(f"✗ Import error during initialization: {e}")
    print("Traceback:", traceback.format_exc())
    sys.exit(1)


async def test_costorm_graph_isolation():
    """
    Execute isolated Co-STORM graph test

    Test State: Minimal but valid CoStormState for perspective generation
    Expected Flow: START -> generate_perspectives -> librarian -> analyst -> END
    Expected Output: Complete CoStormState with mindmap and perspectives
    """

    print("\n=== Co-STORM Graph Isolation Test ===")

    # Step 1: Get compiled graph
    print("Step 1: Initializing Co-STORM graph...")
    try:
        graph = get_costorm_graph()
        print(f"✓ Graph factory successful: {type(graph).__name__}")

        # Print graph structure for debugging
        print(f"  - Nodes: {list(graph.nodes.keys())}")
        # Note: CompiledStateGraph may not have .edges attribute directly

    except Exception as e:
        print(f"✗ Graph factory failed: {e}")
        print("Traceback:", traceback.format_exc())
        return False

    # Step 2: Create test input state
    print("\nStep 2: Creating test input state...")
    try:
        test_topic = "The role of quantum computing in solving complex optimization problems"

        initial_state = CoStormState(
            topic=test_topic,
            mindmap=None,  # Will be populated by generate_perspectives
            perspectives=[],  # Will be populated by generate_perspectives -> librarian flow
        )

        print(f"✓ Test state created: topic='{test_topic[:50]}...'")
        print(f"  - State type: {type(initial_state).__name__}")

    except Exception as e:
        print(f"✗ State creation failed: {e}")
        print("Traceback:", traceback.format_exc())
        return False

    # Step 3: Execute graph with full stack trace capture
    print("\nStep 3: Executing graph.ainvoke()...")
    print("⚠️  This may take several minutes due to LLM calls...")

    try:
        # Execute with proper checkpointer configuration (Operation Async-Stability fix)
        result_state = await graph.ainvoke(
            initial_state,
            config={
                "configurable": {
                    "session_id": "test_session_manual_diagnosis",
                    "thread_id": str(uuid.uuid4())  # Required by AsyncPostgresSaver - must be UUID format
                }
            }
        )

        print("✓ Graph execution completed successfully!")
        print("\nStep 4: Analyzing results...")
        print(f"  - Result type: {type(result_state).__name__}")

        # Validate result structure
        # LangGraph returns a dict, not object
        mindmap = result_state.get('mindmap')
        perspectives = result_state.get('perspectives')

        if mindmap:
            print(f"  - MindMap: ✓ Generated ({len(mindmap.nodes)} perspectives)")
            for i, node in enumerate(mindmap.nodes):
                print(f"    [{i+1}] {node.name[:40]}... ({node.id})")
        else:
            print("  - MindMap: ✗ Not generated or None")
            return False

        if perspectives:
            print(f"  - Perspectives: ✓ Generated ({len(perspectives)} items)")
        else:
            print("  - Perspectives: ✗ Not generated or empty")
            return False

        print("\n🎉 **SUCCESS**: Co-STORM graph executes without errors in isolation")
        print("   This suggests WebSocket layer is the source of 'Unknown error'")
        return True

    except Exception as e:
        print(f"✗ Graph execution failed: {e}")
        print("\n=== FULL STACK TRACE ===")
        traceback.print_exc()
        print("\n=== END STACK TRACE ===")
        print("\n📋 **DIAGNOSIS**: This confirms Graph-level issue, not WebSocket")
        print("   Next steps: Analyze AsyncPostgresSaver + connection pool conflicts")
        return False


async def main():
    """
    Main execution wrapper with error handling
    """
    print("=== Operation Async-Stability: Phase 1 Diagnosis ===")
    print("Testing Co-STORM graph in complete isolation")

    # Pre-flight checks
    required_env = ["POSTGRES_URI", "GEMINI_API_KEY"]
    missing = [k for k in required_env if not os.getenv(k)]
    if missing:
        print(f"✗ Missing required environment variables: {missing}")
        print("   Please ensure .env file is loaded or set variables directly")
        return

    print("✓ Environment check passed")
    print(f"  - Database: {os.getenv('POSTGRES_URI', 'NOT_SET')[:50]}...")

    # Execute test
    success = await test_costorm_graph_isolation()

    # Exit code for CI/CD integration
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())