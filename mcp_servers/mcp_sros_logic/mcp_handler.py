"""
MCP Handler for SROS Logic Server
Implements the Model Context Protocol interface for the SROS Logic server.
"""

import json
from typing import Dict, Any, List
from .server import SROSLogicServer

class SROSLogicMCPHandler:
    """MCP Handler for SROS Logic Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        self.server = SROSLogicServer()
    
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
            elif method == "coordinate_research":
                return self._handle_coordinate_research(params)
            elif method == "manage_workflow":
                return self._handle_manage_workflow(params)
            elif method == "get_current_state":
                return self._handle_get_current_state(params)
            elif method == "update_progress":
                return self._handle_update_progress(params)
            elif method == "generate_report":
                return self._handle_generate_report(params)
            elif method == "set_research_goals":
                return self._handle_set_research_goals(params)
            elif method == "get_research_goals":
                return self._handle_get_research_goals(params)
            elif method == "analyze_literature_gaps":
                return self._handle_analyze_literature_gaps(params)
            elif method == "suggest_next_steps":
                return self._handle_suggest_next_steps(params)
            elif method == "track_dependencies":
                return self._handle_track_dependencies(params)
            elif method == "validate_hypotheses":
                return self._handle_validate_hypotheses(params)
            elif method == "optimize_workflow":
                return self._handle_optimize_workflow(params)
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
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "SROS Logic MCP Server",
                    "version": "1.0.0"
                },
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
            config = params.get("config", {})
            success = self.server.init_workspace(config)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to initialize workspace: {str(e)}"
                }
            }
    
    def _handle_detect_academic_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle detect_academic_gaps request."""
        try:
            topic = params.get("topic", "")
            scope = params.get("scope", "broad")
            
            gaps = self.server.detect_academic_gaps(topic, scope)
            return {"result": gaps}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to detect academic gaps: {str(e)}"
                }
            }
    
    def _handle_coordinate_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle coordinate_research request."""
        try:
            tasks = params.get("tasks", [])
            resources = params.get("resources", {})
            
            coordination_plan = self.server.coordinate_research(tasks, resources)
            return {"result": coordination_plan}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to coordinate research: {str(e)}"
                }
            }
    
    def _handle_manage_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle manage_workflow request."""
        try:
            workflow_config = params.get("config", {})
            workflow_state = self.server.manage_workflow(workflow_config)
            return {"result": workflow_state}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to manage workflow: {str(e)}"
                }
            }
    
    def _handle_get_current_state(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_current_state request."""
        try:
            state = self.server.get_current_state()
            return {"result": state}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get current state: {str(e)}"
                }
            }
    
    def _handle_update_progress(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_progress request."""
        try:
            progress_data = params.get("progress", {})
            success = self.server.update_progress(progress_data)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to update progress: {str(e)}"
                }
            }
    
    def _handle_generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate_report request."""
        try:
            report_type = params.get("type", "summary")
            options = params.get("options", {})
            
            report = self.server.generate_report(report_type, options)
            return {"result": report}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to generate report: {str(e)}"
                }
            }
    
    def _handle_set_research_goals(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle set_research_goals request."""
        try:
            goals = params.get("goals", [])
            success = self.server.set_research_goals(goals)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to set research goals: {str(e)}"
                }
            }
    
    def _handle_get_research_goals(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_research_goals request."""
        try:
            goals = self.server.get_research_goals()
            return {"result": goals}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get research goals: {str(e)}"
                }
            }
    
    def _handle_analyze_literature_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analyze_literature_gaps request."""
        try:
            literature_data = params.get("literature", {})
            gaps_analysis = self.server.analyze_literature_gaps(literature_data)
            return {"result": gaps_analysis}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to analyze literature gaps: {str(e)}"
                }
            }
    
    def _handle_suggest_next_steps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle suggest_next_steps request."""
        try:
            current_state = params.get("current_state", {})
            next_steps = self.server.suggest_next_steps(current_state)
            return {"result": next_steps}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to suggest next steps: {str(e)}"
                }
            }
    
    def _handle_track_dependencies(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle track_dependencies request."""
        try:
            tasks = params.get("tasks", [])
            dependencies = self.server.track_dependencies(tasks)
            return {"result": dependencies}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to track dependencies: {str(e)}"
                }
            }
    
    def _handle_validate_hypotheses(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validate_hypotheses request."""
        try:
            hypotheses = params.get("hypotheses", [])
            validation_results = self.server.validate_hypotheses(hypotheses)
            return {"result": validation_results}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to validate hypotheses: {str(e)}"
                }
            }
    
    def _handle_optimize_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle optimize_workflow request."""
        try:
            current_workflow = params.get("workflow", {})
            optimized_workflow = self.server.optimize_workflow(current_workflow)
            return {"result": optimized_workflow}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to optimize workflow: {str(e)}"
                }
            }

def get_handler() -> SROSLogicMCPHandler:
    """Get singleton instance of the handler."""
    if not hasattr(get_handler, '_instance'):
        get_handler._instance = SROSLogicMCPHandler()
    return get_handler._instance

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request using singleton handler."""
    handler = get_handler()
    return handler.handle_request(method, params)