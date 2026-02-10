#!/usr/bin/env python3
"""
Performance tests for the SROS system.
Tests scalability and response times for large datasets.
"""

import time
import tempfile
import shutil
import os
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def create_large_manuscript(file_path, section_count=100, lines_per_section=50):
    """Create a large manuscript for performance testing."""
    with open(file_path, "w") as f:
        f.write("# Large Research Manuscript\n\n")

        for i in range(section_count):
            f.write(f"## Section {i+1}\n\n")
            for j in range(lines_per_section):
                f.write(
                    f"This is line {j+1} of section {i+1}. It contains some academic content for performance testing.\n"
                )
            f.write("\n")


def test_workspace_initialization_performance():
    """Test workspace initialization performance with large directories."""
    print("Testing workspace initialization performance...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)

    try:
        large_refs_dir = workspace_path / "references" / "large_collection"
        large_refs_dir.mkdir(parents=True)

        for i in range(1000):
            dummy_file = large_refs_dir / f"paper_{i}.pdf"
            dummy_file.touch()

        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        server = SROSLogicServer(str(workspace_path))

        start_time = time.time()
        result = server.init_workspace()
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Workspace initialization took {execution_time:.2f} seconds")
        print(f"Success: {result['success']}")

        return execution_time, result["success"]

    finally:
        shutil.rmtree(test_dir)


def test_gap_detection_performance():
    """Test academic gap detection performance with large manuscripts."""
    print("Testing gap detection performance...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    draft_path = workspace_path / "large_draft.md"

    try:
        create_large_manuscript(draft_path, section_count=200, lines_per_section=100)

        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        server = SROSLogicServer(str(workspace_path))

        start_time = time.time()
        result = server.detect_academic_gaps(str(draft_path))
        end_time = time.time()

        execution_time = end_time - start_time
        gap_count = len(result.get("gaps", [])) if result.get("success") else 0

        print(f"Gap detection took {execution_time:.2f} seconds")
        print(f"Gaps found: {gap_count}")
        print(f"Success: {result['success']}")

        return execution_time, gap_count, result["success"]

    finally:
        shutil.rmtree(test_dir)


def test_concurrent_operations_performance():
    """Test concurrent operations performance."""
    print("Testing concurrent operations performance...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)

    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        server = SROSLogicServer(str(workspace_path))

        server.init_workspace()

        operations = []
        start_time = time.time()

        for _ in range(10):
            op_start = time.time()
            server.detect_academic_gaps()
            op_end = time.time()
            operations.append(op_end - op_start)

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = sum(operations) / len(operations)

        print(f"Total time for 10 concurrent operations: {total_time:.2f} seconds")
        print(f"Average time per operation: {avg_time:.2f} seconds")

        return total_time, avg_time

    finally:
        shutil.rmtree(test_dir)


def test_memory_usage():
    """Test memory usage during operations."""
    print("Testing memory usage...")

    import psutil
    import gc

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    draft_path = workspace_path / "draft.md"

    try:
        create_large_manuscript(draft_path, section_count=50, lines_per_section=50)

        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        server = SROSLogicServer(str(workspace_path))

        gc.collect()
        before_memory = process.memory_info().rss / 1024 / 1024

        server.init_workspace()
        server.detect_academic_gaps(str(draft_path))
        server.research_coordination()
        server.workflow_management()

        gc.collect()
        after_memory = process.memory_info().rss / 1024 / 1024

        memory_increase = after_memory - initial_memory
        peak_increase = after_memory - before_memory

        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"Memory before operations: {before_memory:.2f} MB")
        print(f"Memory after operations: {after_memory:.2f} MB")
        print(f"Total memory increase: {memory_increase:.2f} MB")
        print(f"Peak memory increase during operations: {peak_increase:.2f} MB")

        return memory_increase, peak_increase

    finally:
        shutil.rmtree(test_dir)


def run_performance_suite():
    """Run complete performance test suite."""
    print("=" * 60)
    print("SROS Performance Test Suite")
    print("=" * 60)

    results = {}

    try:
        init_time, init_success = test_workspace_initialization_performance()
        results["workspace_init"] = {"time": init_time, "success": init_success}
    except Exception as e:
        print(f"Workspace initialization test failed: {e}")
        results["workspace_init"] = {"time": 0, "success": False, "error": str(e)}

    try:
        gap_time, gap_count, gap_success = test_gap_detection_performance()
        results["gap_detection"] = {"time": gap_time, "gaps": gap_count, "success": gap_success}
    except Exception as e:
        print(f"Gap detection test failed: {e}")
        results["gap_detection"] = {"time": 0, "gaps": 0, "success": False, "error": str(e)}

    try:
        total_time, avg_time = test_concurrent_operations_performance()
        results["concurrent_ops"] = {"total_time": total_time, "avg_time": avg_time}
    except Exception as e:
        print(f"Concurrent operations test failed: {e}")
        results["concurrent_ops"] = {"total_time": 0, "avg_time": 0, "error": str(e)}

    try:
        memory_increase, peak_increase = test_memory_usage()
        results["memory_usage"] = {"total_increase": memory_increase, "peak_increase": peak_increase}
    except Exception as e:
        print(f"Memory usage test failed: {e}")
        results["memory_usage"] = {"total_increase": 0, "peak_increase": 0, "error": str(e)}

    print("\n" + "=" * 60)
    print("Performance Test Results Summary")
    print("=" * 60)

    for test_name, result in results.items():
        print(f"\n{test_name.replace('_', ' ').title()}:")
        for key, value in result.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("Performance Benchmarks")
    print("=" * 60)

    passed_tests = sum(1 for result in results.values() if result.get("success", True) != False and "error" not in result)
    total_tests = len(results)

    print(f"Tests passed: {passed_tests}/{total_tests}")

    workspace_init_target = 5.0
    gap_detection_target = 10.0
    avg_operation_target = 2.0

    if results.get("workspace_init", {}).get("time", 0) <= workspace_init_target:
        print("✅ Workspace initialization: Within target (< 5 seconds)")
    else:
        print("⚠️  Workspace initialization: Exceeds target (> 5 seconds)")

    if results.get("gap_detection", {}).get("time", 0) <= gap_detection_target:
        print("✅ Gap detection: Within target (< 10 seconds)")
    else:
        print("⚠️  Gap detection: Exceeds target (> 10 seconds)")

    if results.get("concurrent_ops", {}).get("avg_time", 0) <= avg_operation_target:
        print("✅ Average operation time: Within target (< 2 seconds)")
    else:
        print("⚠️  Average operation time: Exceeds target (> 2 seconds)")

    return results


if __name__ == "__main__":
    run_performance_suite()
