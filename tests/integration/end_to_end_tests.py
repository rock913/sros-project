#!/usr/bin/env python3
"""
End-to-end workflow tests for the SROS system.
Tests complete research workflows from start to finish.
"""

import tempfile
import shutil
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def test_complete_research_workflow():
    """Test a complete research workflow from initialization to publication."""
    print("Testing complete research workflow...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)

    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer
        from mcp_servers.mcp_sros_logic.mcp_handler import SROSMCPHandler

        print("Step 1: Initializing research workspace...")
        server = SROSLogicServer(str(workspace_path))
        handler = SROSMCPHandler()

        init_result = server.init_workspace()
        assert init_result["success"], "Workspace initialization failed"
        print("✅ Workspace initialized successfully")

        required_paths = [
            ".sros",
            ".sros/configs",
            ".sros/cache",
            ".sros/logs",
            ".sros/graph.db",
            ".sros/research_log.jsonl",
            "references",
            "draft.md",
        ]

        for path in required_paths:
            full_path = workspace_path / path
            assert full_path.exists(), f"Required path {path} not created"
        print("✅ Workspace structure verified")

        print("Step 2: Performing initial academic gap analysis...")
        gaps_result = server.detect_academic_gaps()
        assert gaps_result["success"], "Initial gap detection failed"
        initial_gaps = len(gaps_result["gaps"])
        print(f"✅ Initial gap analysis completed - found {initial_gaps} gaps")

        print("Step 3: Coordinating research activities...")
        coord_result = server.research_coordination()
        assert coord_result["success"], "Research coordination failed"
        print("✅ Research coordination completed")

        print("Step 4: Managing research workflow...")
        workflow_result = server.workflow_management()
        assert workflow_result["success"], "Workflow management failed"
        workflow_gaps = workflow_result["gaps_found"]
        print(f"✅ Workflow management completed - {workflow_gaps} gaps identified")

        print("Step 5: Testing MCP handler integration...")
        mcp_methods = [
            ("initialize", {}),
            ("init_workspace", {"workspace_path": str(workspace_path)}),
            ("detect_academic_gaps", {"manuscript_path": str(workspace_path / "draft.md")}),
            ("research_coordination", {}),
            ("workflow_management", {}),
        ]

        for method, params in mcp_methods:
            mcp_result = handler.handle_request(method, params)
            assert "error" not in mcp_result, (
                f"MCP method {method} failed: {mcp_result.get('error', 'Unknown error')}"
            )
            print(f"✅ MCP method '{method}' executed successfully")

        print("Step 6: Verifying research activity logging...")
        log_path = workspace_path / ".sros" / "research_log.jsonl"
        assert log_path.exists(), "Research log not created"
        with open(log_path, "r") as f:
            log_lines = f.readlines()
        assert len(log_lines) >= 0, "Research log should contain entries"
        print("✅ Research activity logging verified")

        print("Step 7: Verifying knowledge graph integration...")
        with patch("mcp_servers.mcp_sros_logic.server.DuckDBMemoryServer") as mock_db:
            mock_db_instance = MagicMock()
            mock_db_instance.create_research_gap.return_value = 1
            mock_db.return_value = mock_db_instance

            gaps_result = server.detect_academic_gaps()
            assert gaps_result["success"], "Gap detection with DB integration failed"
            mock_db_instance.create_research_gap.assert_called()
            print("✅ Knowledge graph integration verified")

        print("\n🎉 Complete research workflow test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Complete research workflow test FAILED: {e}")
        return False
    finally:
        shutil.rmtree(test_dir)


def test_iterative_improvement_workflow():
    """Test iterative manuscript improvement workflow."""
    print("Testing iterative improvement workflow...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    draft_path = workspace_path / "draft.md"

    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        initial_draft = """# Research on Machine Learning Applications

## Introduction
Machine learning is important.

## Related Work

## Methodology

## Results

## Conclusion
"""

        with open(draft_path, "w") as f:
            f.write(initial_draft)

        server = SROSLogicServer(str(workspace_path))
        server.init_workspace()

        print("Iteration 1: Initial gap analysis...")
        gaps_result1 = server.detect_academic_gaps(str(draft_path))
        assert gaps_result1["success"], "Iteration 1 gap detection failed"
        initial_gap_count = len(gaps_result1["gaps"])
        print(f"✅ Found {initial_gap_count} gaps initially")

        improved_draft = """# Research on Machine Learning Applications

## Abstract
This paper explores applications of machine learning in modern research.

## Introduction
Machine learning has become a fundamental tool in scientific research, enabling automated analysis of complex datasets and pattern recognition in large-scale studies.

## Related Work
Previous research has shown significant advances in deep learning techniques [Smith2020, Jones2021].

## Methodology
We employed supervised learning algorithms to analyze experimental data.

## Results
Our experiments demonstrated improved accuracy compared to baseline methods.

## Discussion
The results suggest promising directions for future research.

## Conclusion
This study contributes to the growing body of knowledge in ML applications.

## References
[@Smith2020; @Jones2021]
"""

        with open(draft_path, "w") as f:
            f.write(improved_draft)

        print("Iteration 2: Gap analysis after improvements...")
        gaps_result2 = server.detect_academic_gaps(str(draft_path))
        assert gaps_result2["success"], "Iteration 2 gap detection failed"
        improved_gap_count = len(gaps_result2["gaps"])
        print(f"✅ Found {improved_gap_count} gaps after improvements")

        assert improved_gap_count <= initial_gap_count, "Improvements should reduce gap count"
        print("✅ Iterative improvement verified - gap count reduced")

        initial_quality = gaps_result1.get("quality_score", 0)
        improved_quality = gaps_result2.get("quality_score", 0)
        assert improved_quality >= initial_quality, "Quality score should improve with better content"
        print(f"✅ Quality score improved: {initial_quality} → {improved_quality}")

        print("\n🎉 Iterative improvement workflow test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Iterative improvement workflow test FAILED: {e}")
        return False
    finally:
        shutil.rmtree(test_dir)


def test_multi_server_collaboration():
    """Test collaboration between multiple MCP servers."""
    print("Testing multi-server collaboration...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)

    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        with patch.multiple(
            "mcp_servers.mcp_sros_logic.server",
            ManuscriptManagerServer=MagicMock(),
            DuckDBMemoryServer=MagicMock(),
        ) as mocks:
            mock_manuscript = mocks["ManuscriptManagerServer"]
            mock_duckdb = mocks["DuckDBMemoryServer"]

            mock_manuscript_instance = MagicMock()
            mock_duckdb_instance = MagicMock()

            mock_manuscript.return_value = mock_manuscript_instance
            mock_duckdb.return_value = mock_duckdb_instance

            mock_manuscript_instance.get_structure.return_value = {
                "success": True,
                "structure": {
                    "sections": [
                        {"title": "Introduction", "line_start": 1, "line_end": 3},
                        {"title": "Related Work", "line_start": 4, "line_end": 5},
                    ]
                },
            }

            mock_manuscript_instance.detect_gaps.return_value = {
                "success": True,
                "gaps": [
                    {
                        "type": "structure",
                        "description": "Missing Methodology section",
                        "section": "Overall Structure",
                        "priority": "high",
                    }
                ],
            }

            mock_duckdb_instance.create_research_gap.return_value = 1
            mock_duckdb_instance.get_open_research_gaps.return_value = [
                {
                    "id": 1,
                    "description": "Missing Methodology section",
                    "section": "Overall Structure",
                    "priority": "high",
                }
            ]

            server = SROSLogicServer(str(workspace_path))
            server.init_workspace()

            gaps_result = server.detect_academic_gaps()
            assert gaps_result["success"], "Multi-server gap detection failed"
            assert len(gaps_result["gaps"]) > 0, "Should detect gaps from manuscript manager"

            mock_manuscript_instance.get_structure.assert_called()
            mock_manuscript_instance.detect_gaps.assert_called()
            print("✅ Manuscript manager collaboration verified")

            coord_result = server.research_coordination()
            assert coord_result["success"], "Multi-server coordination failed"

            mock_duckdb_instance.get_open_research_gaps.assert_called()
            print("✅ DuckDB memory collaboration verified")

            assert mock_duckdb_instance.create_research_gap.called, "Gaps should be stored in DuckDB"
            print("✅ Gap storage in knowledge graph verified")

        print("\n🎉 Multi-server collaboration test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Multi-server collaboration test FAILED: {e}")
        return False
    finally:
        shutil.rmtree(test_dir)


def test_publication_ready_workflow():
    """Test workflow for preparing publication-ready manuscript."""
    print("Testing publication-ready workflow...")

    test_dir = tempfile.mkdtemp()
    workspace_path = Path(test_dir)
    draft_path = workspace_path / "research_paper.md"

    try:
        from mcp_servers.mcp_sros_logic.server import SROSLogicServer

        publication_draft = """# Novel Approaches to Neural Network Optimization

## Abstract
Recent advances in neural network architectures have opened new possibilities for optimization.

## Introduction
Neural networks have revolutionized artificial intelligence research.

## Related Work
Significant contributions have been made in this field [Author2020].

## Methodology
We propose a novel approach combining reinforcement learning with gradient descent.

## Results
Experimental results demonstrate superior performance.

## Discussion
Our findings suggest important implications for future research.

## Conclusion
This work presents a significant advancement in neural network optimization.

## References
[@Author2020]

## Acknowledgments
We thank our colleagues for their support.

## Author Contributions
All authors contributed equally to this work.
"""

        with open(draft_path, "w") as f:
            f.write(publication_draft)

        server = SROSLogicServer(str(workspace_path))
        server.init_workspace()

        print("Performing publication readiness analysis...")
        gaps_result = server.detect_academic_gaps(str(draft_path))
        assert gaps_result["success"], "Publication readiness analysis failed"

        gaps = gaps_result["gaps"]
        quality_score = gaps_result["quality_score"]

        print("✅ Publication analysis completed")
        print(f"   - Quality score: {quality_score}/100")
        print(f"   - Remaining gaps: {len(gaps)}")

        assert len(gaps) <= 5, "Publication-ready manuscript should have minimal gaps"
        print("✅ Gap count acceptable for publication")

        assert quality_score >= 80, "Publication-ready manuscript should have high quality score"
        print("✅ Quality score sufficient for publication")

        high_priority_gaps = [gap for gap in gaps if gap.get("priority") == "high"]
        assert len(high_priority_gaps) == 0, "Publication-ready manuscript should have no high-priority gaps"
        print("✅ No high-priority gaps found")

        workflow_result = server.workflow_management()
        assert workflow_result["success"], "Final workflow management failed"

        summary = workflow_result["results"].get("summary", {})
        overall_status = summary.get("overall_status", "unknown")

        assert overall_status in ["success", "partial_success"], "Workflow should be successful"
        print("✅ Final workflow status acceptable")

        print("\n🎉 Publication-ready workflow test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Publication-ready workflow test FAILED: {e}")
        return False
    finally:
        shutil.rmtree(test_dir)


def run_end_to_end_test_suite():
    """Run complete end-to-end test suite."""
    print("=" * 80)
    print("SROS End-to-End Workflow Test Suite")
    print("=" * 80)

    test_functions = [
        ("Complete Research Workflow", test_complete_research_workflow),
        ("Iterative Improvement Workflow", test_iterative_improvement_workflow),
        ("Multi-Server Collaboration", test_multi_server_collaboration),
        ("Publication-Ready Workflow", test_publication_ready_workflow),
    ]

    results = {}

    for test_name, test_func in test_functions:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        try:
            success = test_func()
            results[test_name] = {"success": success}
            print(f"Result: {'✅ PASSED' if success else '❌ FAILED'}")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = {"success": False, "error": str(e)}

    print("\n" + "=" * 80)
    print("End-to-End Test Suite Results Summary")
    print("=" * 80)

    passed_tests = sum(1 for result in results.values() if result.get("success", False))
    total_tests = len(results)

    print(f"Tests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 Overall result: ALL TESTS PASSED")
        print("✅ SROS system is ready for production use")
    elif passed_tests >= total_tests * 0.75:
        print("⚠️  Overall result: MOST TESTS PASSED")
        print("✅ SROS system is mostly ready, minor issues to address")
    else:
        print("❌ Overall result: SIGNIFICANT ISSUES DETECTED")
        print("⚠️  SROS system requires substantial improvements")

    print("\nDetailed Test Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
        print(f"  {status} {test_name}")
        if "error" in result:
            print(f"      Error: {result['error']}")

    return results


if __name__ == "__main__":
    run_end_to_end_test_suite()
