#!/usr/bin/env python3
"""
Enhanced tests for SROS Logic MCP Server.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
from server import SROSLogicServer

class TestEnhancedSROSLogicServer(unittest.TestCase):
    """Enhanced test cases for SROSLogicServer."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.server = SROSLogicServer(str(self.temp_dir))
        
        # Create a sample manuscript for testing
        self.draft_path = self.temp_dir / "draft.md"
        with open(self.draft_path, 'w') as f:
            f.write("""# Research Paper

## Abstract
This is a sample abstract.

## Introduction
This is the introduction.

## Related Work
Some related work.

## Methodology
Our approach.

## Results
Findings here.

## Conclusion
Wrapping up.

## References
No citations yet.
""")
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_enhanced_workspace_initialization(self):
        """Test enhanced workspace initialization."""
        result = self.server.init_workspace()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check that directories were created
        sros_dir = self.temp_dir / ".sros"
        configs_dir = sros_dir / "configs"
        cache_dir = sros_dir / "cache"
        logs_dir = sros_dir / "logs"
        references_dir = self.temp_dir / "references"
        
        self.assertTrue(sros_dir.exists())
        self.assertTrue(configs_dir.exists())
        self.assertTrue(cache_dir.exists())
        self.assertTrue(logs_dir.exists())
        self.assertTrue(references_dir.exists())
        
        # Check that files were created
        graph_db = sros_dir / "graph.db"
        research_log = sros_dir / "research_log.jsonl"
        config_file = sros_dir / "workspace.json"
        
        self.assertTrue(graph_db.exists())
        self.assertTrue(research_log.exists())
        self.assertTrue(config_file.exists())
        
        # Check config file content
        with open(config_file, 'r') as f:
            import json
            config = json.load(f)
            self.assertIn("version", config)
            self.assertIn("components", config)
    
    def test_enhanced_academic_gap_detection(self):
        """Test enhanced academic gap detection with quality metrics."""
        # Initialize workspace first
        self.server.init_workspace()
        
        # Test gap detection
        result = self.server.detect_academic_gaps()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check that gaps were detected
        self.assertIn("gaps", result)
        self.assertIsInstance(result["gaps"], list)
        
        # Check for quality metrics
        self.assertIn("quality_score", result)
        self.assertIn("analysis_report", result)
        self.assertIsInstance(result["quality_score"], (int, float))
        self.assertIsInstance(result["analysis_report"], dict)
        
        # Check analysis report structure
        analysis = result["analysis_report"]
        self.assertIn("structure_analysis", analysis)
        self.assertIn("content_analysis", analysis)
        self.assertIn("citation_analysis", analysis)
        self.assertIn("quality_metrics", analysis)
    
    def test_enhanced_research_coordination(self):
        """Test enhanced research coordination with task planning."""
        result = self.server.research_coordination()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check for enhanced results
        self.assertIn("results", result)
        self.assertIn("log", result)
        
        results = result["results"]
        self.assertIn("coordination_plan", results)
        self.assertIn("executed_tasks", results)
        
        # Check coordination plan
        plan = results["coordination_plan"]
        self.assertIsInstance(plan, list)
        self.assertGreater(len(plan), 0)
        
        # Check executed tasks
        tasks = results["executed_tasks"]
        self.assertIn("total_count", tasks)
        self.assertIn("success_count", tasks)
        self.assertGreaterEqual(tasks["success_count"], 0)
    
    def test_enhanced_workflow_management(self):
        """Test enhanced workflow management with progress tracking."""
        result = self.server.workflow_management()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check for enhanced results
        self.assertIn("results", result)
        self.assertIn("steps", result)
        self.assertIn("quality_score", result)
        
        # Check results structure
        results = result["results"]
        self.assertIn("gap_detection", results)
        self.assertIn("coordination", results)
        self.assertIn("summary", results)
        
        # Check summary
        summary = results["summary"]
        self.assertIn("overall_status", summary)
        self.assertIn("recommendations", summary)
        self.assertIn("next_steps", summary)
    
    def test_citation_analysis_functionality(self):
        """Test citation analysis functionality."""
        # Test the private method directly
        gaps = self.server._analyze_citations(str(self.draft_path))
        
        # Should detect missing citations
        self.assertIsInstance(gaps, list)
        self.assertGreater(len(gaps), 0)
        
        # Check gap structure
        gap = gaps[0]
        self.assertIn("type", gap)
        self.assertIn("description", gap)
        self.assertIn("section", gap)
        self.assertIn("priority", gap)
    
    def test_quality_metrics_calculation(self):
        """Test quality metrics calculation."""
        # Test the private method directly
        gaps = self.server._analyze_citations(str(self.draft_path))
        metrics = self.server._calculate_quality_metrics(str(self.draft_path), gaps)
        
        # Check metrics structure
        self.assertIn("overall_score", metrics)
        self.assertIn("structure_score", metrics)
        self.assertIn("content_score", metrics)
        self.assertIn("citation_score", metrics)
        self.assertIn("length_score", metrics)
        self.assertIn("word_count", metrics)
        self.assertIn("line_count", metrics)
        
        # Scores should be numeric
        self.assertIsInstance(metrics["overall_score"], (int, float))
        self.assertGreaterEqual(metrics["overall_score"], 0)
        self.assertLessEqual(metrics["overall_score"], 100)

if __name__ == "__main__":
    unittest.main()