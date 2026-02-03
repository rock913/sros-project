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
                    "code": -32602,
                    "message": f"Error retrieving structure: {str(e)}"
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
                    "code": -32602,
                    "message": f"Error detecting gaps: {str(e)}"
                }
            }
    
    def _handle_edit_section(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle edit_section request."""
        try:
            section_path = params["section_path"]
            content = params["content"]
            mode = params.get("mode", "append")
            
            success = self.server.edit_section(section_path, content, mode)
            return {"result": {"success": success}}
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error editing section: {str(e)}"
                }
            }
    
    def _handle_insert_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle insert_content request."""
        try:
            section_path = params["section_path"]
            content = params["content"]
            citation_keys = params.get("citation_keys", [])
            
            success = self.server.insert_content(section_path, content, citation_keys)
            return {"result": {"success": success}}
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error inserting content: {str(e)}"
                }
            }
    
    def _handle_get_section_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_section_content request."""
        try:
            section_path = params["section_path"]
            content = self.server.get_section_content(section_path)
            
            if content is not None:
                return {"result": {"content": content}}
            else:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Section not found"
                    }
                }
        except KeyError as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Missing required parameter: {str(e)}"
                }
            }
        except Exception as e:
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error retrieving section content: {str(e)}"
                }
            }
    
    def close(self):
        """Close the server connection."""
        # No cleanup needed for this server
        pass

# Global handler instance
_handler = None

def get_handler() -> ManuscriptManagerMCPHandler:
    """Get or create the global MCP handler instance."""
    global _handler
    if _handler is None:
        _handler = ManuscriptManagerMCPHandler()
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

if __name__ == "__main__":
    # Example usage
    handler = get_handler()
    print("Manuscript Manager MCP Handler initialized successfully!")