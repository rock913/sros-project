#!/usr/bin/env python3
"""
Integration tests for the SROS Logic Server.
Tests cross-server communication and end-to-end workflows.
"""

import unittest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directories to path for imports
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock the imports before importing the server
from unittest.mock import patch, MagicMock

# Mock the imports at the module level where SROSLogicServer tries to import them
with patch.dict('sys.modules', {
    'mcp_servers': MagicMock(),
    'mcp_servers.manuscript_manager': MagicMock(),
    'mcp_servers.manuscript_manager.server': MagicMock(),
    'mcp_servers.duckdb_memory': MagicMock(),
    'mcp_servers.duckdb_memory.server': MagicMock(),
}):
    from mcp_servers.mcp_sros_logic.server import SROSLogicServer
    from mcp_servers.mcp_sros_logic.mcp_handler import SROSLogicMCPHandler

class TestSROSIntegration(unittest.TestCase):
    """Integration tests for SROS Logic Server with other MCP servers."""

    def setUp(self):
        """Set up test environment with temporary workspace."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir)
        
        # Create test draft.md
        self.draft_path = self.workspace_path / "draft.md"
        with open(self.draft_path, 'w') as f:
            f.write("""# Research Draft

## Abstract

## Introduction
This is a test introduction with some citations [@smith2020].

## Related Work

## Methodology

## Results

## Conclusion

## References
""")

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    @patch('mcp_servers.manuscript_manager.server.ManuscriptManagerServer')
    @patch('mcp_servers.duckdb_memory.server.DuckDBMemoryServer')
    def test_cross_server_workspace_initialization(self, mock_duckdb, mock_manuscript):
        """Test workspace initialization with cross-server communication."""
        # Mock server instances
        mock_duckdb_instance = MagicMock()
        mock_manuscript_instance = MagicMock()
        mock_duckdb.return_value = mock_duckdb_instance
        mock_manuscript.return_value = mock_manuscript_instance
        
        # Create server instance
        server = SROSLogicServer(str(self.workspace_path))
        
        # Test workspace initialization
        result = server.init_workspace()
        
        # Verify success
        self.assertTrue(result["success"])
        self.assertIn("Workspace initialized successfully", result["message"])
        
        # Verify directory creation
        self.assertTrue((self.workspace_path / ".sros").exists())
        self.assertTrue((self.workspace_path / ".sros" / "configs").exists())
        self.assertTrue((self.workspace_path / ".sros" / "cache").exists())
        self.assertTrue((self.workspace_path / ".sros" / "logs").exists())
        self.assertTrue((self.workspace_path / "references").exists())
        
        # Verify file creation
        self.assertTrue((self.workspace_path / "draft.md").exists())
        self.assertTrue((self.workspace_path / ".sros" / "graph.db").exists())
        self.assertTrue((self.workspace_path / ".sros" / "research_log.jsonl").exists())
        
        # Verify dependent servers were called
        mock_duckdb.assert_called_once_with(str(self.workspace_path / ".sros" / "graph.db"))
        mock_manuscript.assert_called_once_with(str(self.workspace_path / "draft.md"))

    @patch('mcp_servers.manuscript_manager.server.ManuscriptManagerServer')
    @patch('mcp_servers.duckdb_memory.server.DuckDBMemoryServer')
    def test_academic_gap_detection_integration(self, mock_duckdb, mock_manuscript):
        """Test academic gap detection with cross-server integration."""
        # Mock server instances
        mock_duckdb_instance = MagicMock()
        mock_manuscript_instance = MagicMock()
        mock_duckdb.return_value = mock_duckdb_instance
        mock_manuscript.return_value = mock_manuscript_instance
        
        # Mock manuscript manager responses
        mock_manuscript_instance.get_structure.return_value = {
            "success": True,
            "structure": {
                "sections": [
                    {"title": "Introduction", "line_start": 3, "line_end": 5},
                    {"title": "Related Work", "line_start": 6, "line_end": 7},
                    {"title": "Methodology", "line_start": 8, "line_end": 9}
                ]
            }
        }
        
        mock_manuscript_instance.detect_gaps.return_value = {
            "success": True,
            "gaps": [
                {
                    "type": "structure",
                    "description": "Missing Results section",
                    "section": "Overall Structure",
                    "priority": "high",
                    "suggestion": "Add Results section"
                }
            ]
        }
        
        # Mock DuckDB memory responses
        mock_duckdb_instance.create_research_gap.return_value = 1
        
        # Create server instance
        server = SROSLogicServer(str(self.workspace_path))
        
        # Test gap detection
        result = server.detect_academic_gaps(str(self.draft_path))
        
        # Verify success
        self.assertTrue(result["success"])
        self.assertGreater(len(result["gaps"]), 0)
        
        # Verify manuscript manager was called
        mock_manuscript_instance.get_structure.assert_called_once()
        mock_manuscript_instance.detect_gaps.assert_called_once()
        
        # Verify DuckDB memory was called to store gaps
        mock_duckdb_instance.create_research_gap.assert_called()

    @patch('mcp_servers.manuscript_manager.server.ManuscriptManagerServer')
    @patch('mcp_servers.duckdb_memory.server.DuckDBMemoryServer')
    def test_research_coordination_integration(self, mock_duckdb, mock_manuscript):
        """Test research coordination with cross-server communication."""
        # Mock server instances
        mock_duckdb_instance = MagicMock()
        mock_manuscript_instance = MagicMock()
        mock_duckdb.return_value = mock_duckdb_instance
        mock_manuscript.return_value = mock_manuscript_instance
        
        # Mock responses
        mock_manuscript_instance.get_structure.return_value = {
            "success": True,
            "structure": {
                "sections": [
                    {"title": "Introduction", "line_start": 3, "line_end": 5}
                ]
            }
        }
        
        mock_duckdb_instance.get_open_research_gaps.return_value = [
            {
                "id": 1,
                "description": "Missing Results section",
                "section": "Overall Structure",
                "priority": "high"
            }
        ]
        
        # Create server instance
        server = SROSLogicServer(str(self.workspace_path))
        
        # Test research coordination
        result = server.research_coordination()
        
        # Verify success
        self.assertTrue(result["success"])
        self.assertIn("Research coordination completed", result["message"])
        self.assertIn("log", result)
        self.assertIn("results", result)
        
        # Verify dependent servers were called
        mock_manuscript_instance.get_structure.assert_called_once()
        mock_duckdb_instance.get_open_research_gaps.assert_called_once()

    @patch('mcp_servers.manuscript_manager.server.ManuscriptManagerServer')
    @patch('mcp_servers.duckdb_memory.server.DuckDBMemoryServer')
    def test_workflow_management_integration(self, mock_duckdb, mock_manuscript):
        """Test complete workflow management with cross-server integration."""
        # Mock server instances
        mock_duckdb_instance = MagicMock()
        mock_manuscript_instance = MagicMock()
        mock_duckdb.return_value = mock_duckdb_instance
        mock_manuscript.return_value = mock_manuscript_instance
        
        # Mock responses for all steps
        mock_duckdb_instance.create_research_gap.return_value = 1
        mock_manuscript_instance.get_structure.return_value = {
            "success": True,
            "structure": {
                "sections": [
                    {"title": "Introduction", "line_start": 3, "line_end": 5}
                ]
            }
        }
        mock_manuscript_instance.detect_gaps.return_value = {
            "success": True,
            "gaps": [
                {
                    "type": "structure",
                    "description": "Missing Results section",
                    "section": "Overall Structure",
                    "priority": "high"
                }
            ]
        }
        mock_duckdb_instance.get_open_research_gaps.return_value = [
            {
                "id": 1,
                "description": "Missing Results section",
                "section": "Overall Structure",
                "priority": "high"
            }
        ]
        
        # Create server instance
        server = SROSLogicServer(str(self.workspace_path))
        
        # Test workflow management
        result = server.workflow_management()
        
        # Verify success
        self.assertTrue(result["success"])
        self.assertIn("Workflow management completed successfully", result["message"])
        self.assertIn("steps", result)
        self.assertIn("results", result)
        self.assertGreater(result["gaps_found"], 0)
        
        # Verify all steps were executed
        steps = result["steps"]
        self.assertTrue(any("Initializing workspace" in step for step in steps))
        self.assertTrue(any("Detecting academic gaps" in step for step in steps))
        self.assertTrue(any("Coordinating research activities" in step for step in steps))

    def test_mcp_handler_integration(self):
        """Test MCP handler with cross-server communication."""
        # Create handler instance
        handler = SROSLogicMCPHandler()
        
        # Test initialize method
        init_result = handler.handle_request("initialize", {})
        self.assertIn("result", init_result)
        self.assertIn("capabilities", init_result["result"])
        
        # Test init_workspace method
        workspace_result = handler.handle_request("init_workspace", {
            "workspace_path": str(self.workspace_path)
        })
        self.assertIn("result", workspace_result)
        self.assertTrue(workspace_result["result"]["success"])
        
        # Test detect_academic_gaps method
        gaps_result = handler.handle_request("detect_academic_gaps", {
            "manuscript_path": str(self.draft_path)
        })
        self.assertIn("result", gaps_result)
        self.assertIn("gaps", gaps_result["result"])
        
        # Test research_coordination method
        coord_result = handler.handle_request("research_coordination", {})
        self.assertIn("result", coord_result)
        self.assertTrue(coord_result["result"]["success"])
        
        # Test workflow_management method
        workflow_result = handler.handle_request("workflow_management", {})
        self.assertIn("result", workflow_result)
        self.assertTrue(workflow_result["result"]["success"])

    @patch('mcp_servers.manuscript_manager.server.ManuscriptManagerServer')
    @patch('mcp_servers.duckdb_memory.server.DuckDBMemoryServer')
    def test_error_handling_in_cross_server_communication(self, mock_duckdb, mock_manuscript):
        """Test error handling when dependent servers fail."""
        # Mock server instances that raise exceptions
        mock_duckdb.side_effect = Exception("DuckDB connection failed")
        mock_manuscript.side_effect = Exception("Manuscript manager failed")
        
        # Create server instance
        server = SROSLogicServer(str(self.workspace_path))
        
        # Test that server still functions despite dependency failures
        # Workspace initialization should still work (fallback mode)
        result = server.init_workspace()
        self.assertTrue(result["success"])
        
        # Gap detection should still work with custom rules
        gaps_result = server.detect_academic_gaps(str(self.draft_path))
        self.assertTrue(gaps_result["success"])
        
        # Research coordination should handle errors gracefully
        coord_result = server.research_coordination()
        self.assertTrue(coord_result["success"])  # Should succeed with warnings

if __name__ == '__main__':
    unittest.main()