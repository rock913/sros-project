#!/usr/bin/env python3
"""
Tests for SROS Logic MCP Server.
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
from server import SROSLogicServer

class TestSROSLogicServer(unittest.TestCase):
    """Test cases for SROSLogicServer."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.server = SROSLogicServer(str(self.temp_dir))
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_init_workspace(self):
        """Test workspace initialization."""
        result = self.server.init_workspace()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check that directories were created
        sros_dir = self.temp_dir / ".sros"
        references_dir = self.temp_dir / "references"
        
        self.assertTrue(sros_dir.exists())
        self.assertTrue(references_dir.exists())
        
        # Check that files were created
        graph_db = sros_dir / "graph.db"
        research_log = sros_dir / "research_log.jsonl"
        
        self.assertTrue(graph_db.exists())
        self.assertTrue(research_log.exists())
    
    def test_detect_academic_gaps(self):
        """Test academic gap detection."""
        # Initialize workspace first
        self.server.init_workspace()
        
        # Test gap detection
        result = self.server.detect_academic_gaps()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check that gaps were detected (placeholder implementation)
        self.assertIn("gaps", result)
        self.assertIsInstance(result["gaps"], list)
    
    def test_research_coordination(self):
        """Test research coordination."""
        result = self.server.research_coordination()
        
        # Check that the result is successful
        self.assertTrue(result["success"])
    
    def test_workflow_management(self):
        """Test workflow management."""
        result = self.server.workflow_management()
        
        # Check that the result is successful
        self.assertTrue(result["success"])

if __name__ == "__main__":
    unittest.main()