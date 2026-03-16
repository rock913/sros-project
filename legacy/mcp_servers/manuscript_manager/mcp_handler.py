"""
MCP Handler for Manuscript Manager Server
Implements the Model Context Protocol interface for the Manuscript Manager server.
"""

import json
from typing import Dict, Any, List
from .server import ManuscriptManagerServer
from .config import get_manuscript_path

class ManuscriptManagerMCPHandler:
    """MCP Handler for Manuscript Manager Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        self.server = ManuscriptManagerServer(get_manuscript_path())
    
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
            elif method == "get_structure":
                return self._handle_get_structure(params)
            elif method == "detect_gaps":
                return self._handle_detect_gaps(params)
            elif method == "edit_section":
                return self._handle_edit_section(params)
            elif method == "insert_content":
                return self._handle_insert_content(params)
            elif method == "get_section_content":
                return self._handle_get_section_content(params)
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
                    "name": "Manuscript Manager MCP Server",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "structureRetrieval": True,
                    "gapDetection": True,
                    "sectionEditing": True,
                    "contentInsertion": True
                }
            }
        }
    
    def _handle_get_structure(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_structure request."""
        try:
            structure = self.server.get_structure()
            return {"result": structure}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get structure: {str(e)}"
                }
            }
    
    def _handle_detect_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle detect_gaps request."""
        try:
            gaps = self.server.detect_gaps()
            return {"result": gaps}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to detect gaps: {str(e)}"
                }
            }
    
    def _handle_edit_section(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle edit_section request."""
        try:
            section_path = params.get("section_path")
            content = params.get("content")
            mode = params.get("mode", "append")
            
            if not section_path or content is None:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: section_path and content"
                    }
                }
            
            success = self.server.edit_section(section_path, content, mode)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to edit section: {str(e)}"
                }
            }
    
    def _handle_insert_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle insert_content request."""
        try:
            section_path = params.get("section_path")
            content = params.get("content")
            citation_keys = params.get("citation_keys", [])
            
            if not section_path or content is None:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: section_path and content"
                    }
                }
            
            success = self.server.insert_content(section_path, content, citation_keys)
            return {"result": {"success": success}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to insert content: {str(e)}"
                }
            }
    
    def _handle_get_section_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_section_content request."""
        try:
            section_path = params.get("section_path")
            if not section_path:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: section_path"
                    }
                }
            
            content = self.server.get_section_content(section_path)
            return {"result": {"content": content}}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get section content: {str(e)}"
                }
            }

def get_handler() -> ManuscriptManagerMCPHandler:
    """Get singleton instance of the handler."""
    if not hasattr(get_handler, '_instance'):
        get_handler._instance = ManuscriptManagerMCPHandler()
    return get_handler._instance

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request using singleton handler."""
    handler = get_handler()
    return handler.handle_request(method, params)