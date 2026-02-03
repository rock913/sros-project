"""
MCP Handler for Zotero Expert Server
Implements the Model Context Protocol interface for the Zotero Expert server.
"""
import json
import logging
from typing import Dict, Any, List
import sys
import os

# Handle relative imports properly
try:
    from .server import ZoteroExpertServer
    from .config import ZoteroExpertConfig
except (ImportError, ValueError):
    # Fallback for direct script execution
    from server import ZoteroExpertServer
    from config import ZoteroExpertConfig

logger = logging.getLogger(__name__)

class ZoteroExpertMCPHandler:
    """MCP Handler for Zotero Expert Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        self.config = ZoteroExpertConfig()
        self.server = ZoteroExpertServer()
        
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
            elif method == "get_library_items":
                return self._handle_get_library_items(params)
            elif method == "get_item":
                return self._handle_get_item(params)
            elif method == "search_items":
                return self._handle_search_items(params)
            elif method == "get_collections":
                return self._handle_get_collections(params)
            elif method == "get_item_children":
                return self._handle_get_item_children(params)
            elif method == "create_note":
                return self._handle_create_note(params)
            elif method == "update_item":
                return self._handle_update_item(params)
            elif method == "get_bibliography":
                return self._handle_get_bibliography(params)
            elif method == "validate_citation_keys":
                return self._handle_validate_citation_keys(params)
            elif method == "sync_ai_notes":
                return self._handle_sync_ai_notes(params)
            elif method == "generate_smart_bibliography":
                return self._handle_generate_smart_bibliography(params)
            elif method == "get_item_metadata":
                return self._handle_get_item_metadata(params)
            elif method == "search_advanced":
                return self._handle_search_advanced(params)
            elif method == "read_local_library":
                return self._handle_read_local_library(params)
            elif method == "get_library_statistics":
                return self._handle_get_library_statistics(params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            logger.error(f"Error handling request {method}: {str(e)}")
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
                    "libraryAccess": True,
                    "itemSearch": True,
                    "collectionManagement": True,
                    "noteCreation": True,
                    "bibliographyGeneration": True
                }
            }
        }
        
    def _handle_get_library_items(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_library_items request."""
        try:
            limit = params.get("limit", 100)
            start = params.get("start", 0)
            
            result = self.server.get_library_items(limit, start)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting library items: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting library items: {str(e)}"
                }
            }
            
    def _handle_get_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item request."""
        try:
            item_key = params.get("item_key", "")
            if not item_key:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_key parameter is required"
                    }
                }
                
            result = self.server.get_item(item_key)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting item: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting item: {str(e)}"
                }
            }
            
    def _handle_search_items(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_items request."""
        try:
            query = params.get("query", "")
            limit = params.get("limit", 50)
            
            result = self.server.search_items(query, limit)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error searching items: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error searching items: {str(e)}"
                }
            }
            
    def _handle_get_collections(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_collections request."""
        try:
            result = self.server.get_collections()
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting collections: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting collections: {str(e)}"
                }
            }
            
    def _handle_get_item_children(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item_children request."""
        try:
            item_key = params.get("item_key", "")
            if not item_key:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_key parameter is required"
                    }
                }
                
            result = self.server.get_item_children(item_key)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting item children: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting item children: {str(e)}"
                }
            }
            
    def _handle_create_note(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_note request."""
        try:
            parent_item_key = params.get("parent_item_key", "")
            note_content = params.get("note_content", "")
            
            if not parent_item_key or not note_content:
                return {
                    "error": {
                        "code": -32602,
                        "message": "parent_item_key and note_content parameters are required"
                    }
                }
                
            result = self.server.create_note(parent_item_key, note_content)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error creating note: {str(e)}"
                }
            }
            
    def _handle_update_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_item request."""
        try:
            item_key = params.get("item_key", "")
            item_data = params.get("item_data", {})
            
            if not item_key or not item_data:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_key and item_data parameters are required"
                    }
                }
                
            result = self.server.update_item(item_key, item_data)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error updating item: {str(e)}"
                }
            }
            
    def _handle_get_bibliography(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_bibliography request."""
        try:
            item_keys = params.get("item_keys", [])
            style = params.get("style", "apa")
            
            if not item_keys:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_keys parameter is required"
                    }
                }
                
            result = self.server.get_bibliography(item_keys, style)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error generating bibliography: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error generating bibliography: {str(e)}"
                }
            }
    
    def _handle_validate_citation_keys(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validate_citation_keys request."""
        try:
            items = params.get("items", [])
            
            result = self.server.validate_citation_keys(items)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error validating citation keys: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error validating citation keys: {str(e)}"
                }
            }
    
    def _handle_sync_ai_notes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sync_ai_notes request."""
        try:
            item_key = params.get("item_key", "")
            ai_notes = params.get("ai_notes", [])
            
            if not item_key:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_key parameter is required"
                    }
                }
                
            result = self.server.sync_ai_notes(item_key, ai_notes)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error syncing AI notes: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error syncing AI notes: {str(e)}"
                }
            }
    
    def _handle_generate_smart_bibliography(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate_smart_bibliography request."""
        try:
            item_keys = params.get("item_keys", [])
            style = params.get("style", "apa")
            format_options = params.get("format_options", {})
            
            if not item_keys:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_keys parameter is required"
                    }
                }
                
            result = self.server.generate_smart_bibliography(item_keys, style, format_options)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error generating smart bibliography: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error generating smart bibliography: {str(e)}"
                }
            }
    
    def _handle_get_item_metadata(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item_metadata request."""
        try:
            item_key = params.get("item_key", "")
            
            if not item_key:
                return {
                    "error": {
                        "code": -32602,
                        "message": "item_key parameter is required"
                    }
                }
                
            result = self.server.get_item_metadata(item_key)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting item metadata: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting item metadata: {str(e)}"
                }
            }
    
    def _handle_search_advanced(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_advanced request."""
        try:
            query = params.get("query", "")
            item_type = params.get("item_type")
            collection_key = params.get("collection_key")
            limit = params.get("limit", 50)
            
            if not query:
                return {
                    "error": {
                        "code": -32602,
                        "message": "query parameter is required"
                    }
                }
                
            result = self.server.search_advanced(query, item_type, collection_key, limit)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in advanced search: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error in advanced search: {str(e)}"
                }
            }
    
    def _handle_read_local_library(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_local_library request."""
        try:
            limit = params.get("limit", 100)
            start = params.get("start", 0)
            
            result = self.server.read_local_library(limit, start)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error reading local library: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error reading local library: {str(e)}"
                }
            }
    
    def _handle_get_library_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_library_statistics request."""
        try:
            result = self.server.get_library_statistics()
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting library statistics: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting library statistics: {str(e)}"
                }
            }