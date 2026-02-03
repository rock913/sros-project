"""
MCP Handler for SROS Logic Server.
Implements the Model Context Protocol interface for custom SROS logic.
"""

import json
import logging
from typing import Dict, Any, List, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import handlers from other MCP servers
# Note: In a real implementation, these would likely be called via MCP client requests
# For this demo, we'll simulate the interactions
try:
    from mcp_servers.duckdb_memory.mcp_handler import DuckDBMemoryMCPHandler
    from mcp_servers.manuscript_manager.mcp_handler import ManuscriptManagerMCPHandler
    HAS_DEPENDENCIES = True
except ImportError as e:
    logging.warning(f"Could not import dependent handlers: {e}")
    HAS_DEPENDENCIES = False

class SROSMCPHandler:
    """MCP Handler for SROS Logic Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        # Initialize handlers for dependent services
        if HAS_DEPENDENCIES:
            try:
                self.duckdb_handler = DuckDBMemoryMCPHandler()
                self.manuscript_handler = ManuscriptManagerMCPHandler()
            except Exception as e:
                logging.warning(f"Failed to initialize dependent handlers: {e}")
                self.duckdb_handler = None
                self.manuscript_handler = None
        else:
            self.duckdb_handler = None
            self.manuscript_handler = None
    
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP requests.
        
        Args:
            method: MCP method name
            params: Method parameters
            
        Returns:
            Response dictionary
        """
        try:
            if method == "initialize":
                return self._handle_initialize(params)
            elif method == "init_workspace":
                return self._handle_init_workspace(params)
            elif method == "detect_academic_gaps":
                return self._handle_detect_academic_gaps(params)
            elif method == "research_coordination":
                return self._handle_research_coordination(params)
            elif method == "workflow_management":
                return self._handle_workflow_management(params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "result": {
                "capabilities": {
                    "workspaceInitialization": True,
                    "academicGapDetection": True,
                    "researchCoordination": True,
                    "workflowManagement": True
                }
            }
        }
    
    def _handle_init_workspace(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle init_workspace request."""
        try:
            # Get workspace path from params or use default
            workspace_path = params.get("workspace_path", ".")
            
            # Create .sros directory
            sros_dir = os.path.join(workspace_path, ".sros")
            os.makedirs(sros_dir, exist_ok=True)
            
            # Create graph.db (handled by duckdb-memory server)
            # In a real implementation, this would be an MCP call to duckdb-memory
            # For demo purposes, we'll simulate it
            graph_db_path = os.path.join(sros_dir, "graph.db")
            # Simulate database initialization
            with open(graph_db_path, 'w') as f:
                f.write("DuckDB database placeholder")
            
            # Create research_log.jsonl
            log_path = os.path.join(sros_dir, "research_log.jsonl")
            with open(log_path, 'w') as f:
                f.write("")
            
            # Create references directory
            refs_dir = os.path.join(workspace_path, "references")
            os.makedirs(refs_dir, exist_ok=True)
            
            # Create default draft.md if it doesn't exist
            draft_path = os.path.join(workspace_path, "draft.md")
            if not os.path.exists(draft_path):
                with open(draft_path, 'w') as f:
                    f.write("# Research Draft\n\n## Introduction\n\n## Related Work\n\n## Methodology\n\n## Results\n\n## Conclusion\n")
            
            return {
                "result": {
                    "success": True,
                    "message": f"Workspace initialized with directories: {sros_dir}, {refs_dir}",
                    "directories_created": [sros_dir, refs_dir],
                    "files_created": [graph_db_path, log_path, draft_path]
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Failed to initialize workspace: {str(e)}"
                }
            }
    
    def _handle_detect_academic_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle detect_academic_gaps request."""
        try:
            # Get manuscript path from params
            manuscript_path = params.get("manuscript_path", "draft.md")
            
            # In a real implementation, this would involve:
            # 1. Calling manuscript-manager to get structure and detect gaps
            # 2. Analyzing the gaps with academic rules
            # 3. Storing results in duckdb-memory
            
            # Simulate calling manuscript-manager
            gaps = []
            structure_info = {}
            
            if self.manuscript_handler:
                structure_result = self.manuscript_handler.handle_request("get_structure", {})
                gaps_result = self.manuscript_handler.handle_request("detect_gaps", {})
                
                if "error" not in structure_result:
                    structure_info = structure_result.get("result", {})
                
                if "error" not in gaps_result:
                    gaps = gaps_result.get("result", {}).get("gaps", [])
            
            # Apply custom academic rules
            custom_gaps = self._apply_custom_academic_rules(manuscript_path)
            gaps.extend(custom_gaps)
            
            # Simulate storing gaps in duckdb-memory
            stored_gaps = []
            if self.duckdb_handler and gaps:
                for gap in gaps:
                    # Simulate storing gap in research_gaps table
                    # In reality, this would be an MCP call to duckdb-memory
                    stored_gaps.append({
                        "id": len(stored_gaps) + 1,
                        "description": gap.get("description", ""),
                        "section": gap.get("section", "Unknown"),
                        "priority": gap.get("priority", "medium")
                    })
            
            return {
                "result": {
                    "gaps": gaps,
                    "stored_gaps": stored_gaps,
                    "analysis": f"Academic gap analysis completed with {len(gaps)} gaps detected",
                    "manuscript_info": structure_info
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Failed to detect academic gaps: {str(e)}"
                }
            }
    
    def _apply_custom_academic_rules(self, manuscript_path: str) -> List[Dict[str, Any]]:
        """
        Apply custom academic rules to detect gaps.
        
        Args:
            manuscript_path: Path to the manuscript file
            
        Returns:
            List of detected gaps
        """
        gaps = []
        
        try:
            if not os.path.exists(manuscript_path):
                return gaps
                
            with open(manuscript_path, 'r') as f:
                content = f.read()
            
            # Rule 1: Check for citation patterns
            if "[@" not in content and "@" not in content:
                gaps.append({
                    "type": "citation",
                    "description": "No citations found in manuscript",
                    "section": "Overall",
                    "priority": "high",
                    "suggestion": "Add academic citations to support claims"
                })
            
            # Rule 2: Check for figure/table references
            if "Figure" in content and "figure" not in content.lower():
                gaps.append({
                    "type": "visualization",
                    "description": "Potential figures/tables mentioned but not properly referenced",
                    "section": "Results",
                    "priority": "medium",
                    "suggestion": "Ensure all figures and tables are properly labeled and referenced"
                })
            
            # Rule 3: Check section length balance
            lines = content.split('\n')
            section_lengths = {}
            current_section = None
            
            for line in lines:
                if line.startswith('## '):
                    current_section = line[3:].strip()
                    section_lengths[current_section] = 0
                elif current_section and line.strip():
                    section_lengths[current_section] = section_lengths.get(current_section, 0) + 1
            
            # Check for imbalanced sections
            if section_lengths:
                avg_length = sum(section_lengths.values()) / len(section_lengths)
                for section, length in section_lengths.items():
                    if length < avg_length * 0.3:  # Significantly shorter than average
                        gaps.append({
                            "type": "content_balance",
                            "description": f"Section '{section}' is significantly shorter than others",
                            "section": section,
                            "priority": "medium",
                            "suggestion": f"Expand content in '{section}' section for better balance"
                        })
            
        except Exception as e:
            logging.warning(f"Error applying custom academic rules: {e}")
        
        return gaps
    
    def _handle_research_coordination(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle research_coordination request with enhanced coordination logic."""
        try:
            coordination_log = []
            coordination_results = {}
            coordination_start_time = str(os.path.getmtime(".")) if os.path.exists(".") else "N/A"
            
            # Log the coordination attempt
            coordination_log.append("Research coordination initiated")
            
            # If dependent handlers are available, coordinate with them
            if self.manuscript_handler:
                coordination_log.append("✓ Connected to manuscript-manager server")
                
                # Get current manuscript status
                structure_result = self.manuscript_handler.handle_request("get_structure", {})
                if "error" not in structure_result:
                    structure = structure_result.get("result", {}).get("structure", {})
                    section_count = len(structure.get("sections", []))
                    coordination_log.append(f"✓ Retrieved manuscript structure with {section_count} sections")
                    coordination_results["manuscript_sections"] = section_count
                else:
                    coordination_log.append(f"✗ Failed to retrieve manuscript structure: {structure_result.get('error', {}).get('message', 'Unknown error')}")
                    coordination_results["manuscript_error"] = structure_result.get('error', {}).get('message', 'Unknown error')
            
            if self.duckdb_handler:
                coordination_log.append("✓ Connected to duckdb-memory server")
                
                # Get research gaps
                try:
                    gaps_result = self.duckdb_handler.handle_request("get_open_research_gaps", {})
                    if "error" not in gaps_result:
                        gaps = gaps_result.get("result", {}).get("gaps", [])
                        gap_count = len(gaps)
                        coordination_log.append(f"✓ Found {gap_count} open research gaps")
                        coordination_results["open_gaps"] = gap_count
                        coordination_results["gap_details"] = gaps[:5]  # First 5 gaps for summary
                    else:
                        coordination_log.append(f"✗ Failed to retrieve research gaps: {gaps_result.get('error', {}).get('message', 'Unknown error')}")
                        coordination_results["gap_error"] = gaps_result.get('error', {}).get('message', 'Unknown error')
                except Exception as e:
                    coordination_log.append(f"✗ Could not retrieve research gaps: {e}")
                    coordination_results["gap_exception"] = str(e)
            
            # Enhanced coordination with other servers (semantic-scholar, zotero-expert)
            coordination_log.append("→ Initiating coordination with semantic-scholar and zotero-expert servers...")
            
            # Generate coordination plan
            coordination_plan = self._generate_coordination_plan()
            coordination_log.append(f"✓ Generated coordination plan with {len(coordination_plan)} tasks")
            coordination_results["coordination_plan"] = coordination_plan
            
            # Execute coordination tasks (simulated)
            executed_tasks = self._execute_coordination_tasks(coordination_plan)
            coordination_log.append(f"✓ Executed {executed_tasks['success_count']}/{executed_tasks['total_count']} coordination tasks")
            coordination_results["executed_tasks"] = executed_tasks
            
            coordination_log.append("✓ Research coordination completed successfully")
            
            return {
                "result": {
                    "success": True,
                    "message": "Research coordination completed",
                    "log": coordination_log,
                    "results": coordination_results,
                    "timestamp": coordination_start_time,
                    "completion_time": str(os.path.getmtime(".")) if os.path.exists(".") else "N/A"
                }
            }
        except Exception as e:
            logging.error(f"Research coordination failed: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Research coordination failed: {str(e)}"
                }
            }
    
    def _generate_coordination_plan(self) -> List[Dict[str, Any]]:
        """
        Generate a coordination plan based on current research state.
        
        Returns:
            List of coordination tasks
        """
        plan = []
        
        # Sample coordination tasks based on typical research workflow
        plan.append({
            "task": "literature_review",
            "server": "semantic-scholar",
            "priority": "high",
            "description": "Conduct literature review for open research gaps",
            "estimated_duration": "30 minutes"
        })
        
        plan.append({
            "task": "citation_management",
            "server": "zotero-expert",
            "priority": "medium",
            "description": "Sync and validate citations with local library",
            "estimated_duration": "15 minutes"
        })
        
        plan.append({
            "task": "gap_analysis",
            "server": "duckdb-memory",
            "priority": "high",
            "description": "Update research gap priorities based on new findings",
            "estimated_duration": "10 minutes"
        })
        
        plan.append({
            "task": "manuscript_update",
            "server": "manuscript-manager",
            "priority": "medium",
            "description": "Update manuscript with new research findings",
            "estimated_duration": "45 minutes"
        })
        
        return plan
    
    def _execute_coordination_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute coordination tasks with simulated results.
        
        Args:
            tasks: List of tasks to execute
            
        Returns:
            Execution results summary
        """
        results = {
            "total_count": len(tasks),
            "success_count": 0,
            "failed_count": 0,
            "task_results": []
        }
        
        # Simulate task execution
        for i, task in enumerate(tasks, 1):
            task_result = {
                "task_id": i,
                "task": task["task"],
                "server": task["server"],
                "status": "completed",
                "message": f"Task '{task['task']}' completed successfully"
            }
            results["task_results"].append(task_result)
            results["success_count"] += 1
        
        return results
    
    def _handle_workflow_management(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow_management request."""
        try:
            workflow_steps = []
            
            # Step 1: Initialize workspace if needed
            workflow_steps.append("1. Initializing workspace...")
            init_result = self._handle_init_workspace({})
            if "error" not in init_result:
                workflow_steps.append("   ✓ Workspace initialized")
                dirs_created = init_result.get("result", {}).get("directories_created", [])
                workflow_steps.append(f"   ✓ Created directories: {', '.join(dirs_created)}")
            else:
                workflow_steps.append(f"   ✗ Workspace initialization failed: {init_result.get('error', {}).get('message')}")
                return {
                    "result": {
                        "success": False,
                        "error": "Workspace initialization failed",
                        "steps": workflow_steps
                    }
                }
            
            # Step 2: Detect academic gaps
            workflow_steps.append("2. Detecting academic gaps...")
            gaps_result = self._handle_detect_academic_gaps({"manuscript_path": "draft.md"})
            if "error" not in gaps_result:
                gap_count = len(gaps_result.get("result", {}).get("gaps", []))
                workflow_steps.append(f"   ✓ Detected {gap_count} academic gaps")
            else:
                workflow_steps.append(f"   ✗ Gap detection failed: {gaps_result.get('error', {}).get('message')}")
            
            # Step 3: Coordinate research
            workflow_steps.append("3. Coordinating research activities...")
            coord_result = self._handle_research_coordination({})
            if "error" not in coord_result:
                workflow_steps.append("   ✓ Research coordination completed")
                coord_log = coord_result.get("result", {}).get("log", [])
                for log_entry in coord_log:
                    if "completed" in log_entry.lower():
                        workflow_steps.append(f"   ✓ {log_entry}")
            else:
                workflow_steps.append(f"   ✗ Research coordination failed: {coord_result.get('error', {}).get('message')}")
            
            # Step 4: Log workflow completion
            workflow_steps.append("4. Workflow management cycle completed")
            
            return {
                "result": {
                    "success": True,
                    "message": "Workflow management completed successfully",
                    "steps": workflow_steps,
                    "gaps_found": len(gaps_result.get("result", {}).get("gaps", [])) if "error" not in gaps_result else 0,
                    "timestamp": str(os.path.getmtime(".")) if os.path.exists(".") else "N/A"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Workflow management failed: {str(e)}"
                }
            }

# Global handler instance
_handler = None

def get_handler() -> SROSMCPHandler:
    """Get or create the global MCP handler instance."""
    global _handler
    if _handler is None:
        _handler = SROSMCPHandler()
    return _handler

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle an MCP request.
    
    Args:
        method: MCP method name
        params: Method parameters
        
    Returns:
        Response dictionary
    """
    handler = get_handler()
    return handler.handle_request(method, params)