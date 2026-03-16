"""
MCP Handler for Zotero Expert Server
Implements the Model Context Protocol interface for the Zotero Expert server.
"""

import json
from typing import Dict, Any, List
import logging

from .server import ZoteroExpertServer
from .config import get_zotero_config

logger = logging.getLogger(__name__)

class ZoteroExpertMCPHandler:
    """MCP Handler for Zotero Expert Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        try:
            # Server initializes its own config internally
            self.server = ZoteroExpertServer()
        except Exception as e:
            logger.error(f"Failed to initialize Zotero server: {e}")
            self.server = None
    
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
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "Zotero Expert MCP Server",
                    "version": "1.0.0"
                },
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
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            limit = params.get("limit", 50)
            start = params.get("start", 0)
            item_type = params.get("item_type")
            
            items = self.server.get_library_items(limit=limit, start=start, item_type=item_type)
            return {"result": items}
        except Exception as e:
            logger.error(f"Error in get_library_items: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get library items: {str(e)}"
                }
            }
    
    def _handle_get_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_id = params.get("item_id")
            if not item_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: item_id"
                    }
                }
            
            item = self.server.get_item(item_id)
            return {"result": item}
        except Exception as e:
            logger.error(f"Error in get_item: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get item: {str(e)}"
                }
            }
    
    def _handle_search_items(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_items request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            query = params.get("query")
            limit = params.get("limit", 50)
            
            if not query:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: query"
                    }
                }
            
            items = self.server.search_items(query, limit=limit)
            return {"result": items}
        except Exception as e:
            logger.error(f"Error in search_items: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to search items: {str(e)}"
                }
            }
    
    def _handle_get_collections(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_collections request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            collections = self.server.get_collections()
            return {"result": collections}
        except Exception as e:
            logger.error(f"Error in get_collections: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get collections: {str(e)}"
                }
            }
    
    def _handle_get_item_children(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item_children request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_id = params.get("item_id")
            if not item_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: item_id"
                    }
                }
            
            children = self.server.get_item_children(item_id)
            return {"result": children}
        except Exception as e:
            logger.error(f"Error in get_item_children: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get item children: {str(e)}"
                }
            }
    
    def _handle_create_note(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_note request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            parent_item_id = params.get("parent_item_id")
            note_content = params.get("content")
            
            if not parent_item_id or not note_content:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: parent_item_id and content"
                    }
                }
            
            note_id = self.server.create_note(parent_item_id, note_content)
            return {"result": {"note_id": note_id}}
        except Exception as e:
            logger.error(f"Error in create_note: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to create note: {str(e)}"
                }
            }
    
    def _handle_update_item(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_item request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_id = params.get("item_id")
            item_data = params.get("data", {})
            
            if not item_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: item_id"
                    }
                }
            
            success = self.server.update_item(item_id, item_data)
            return {"result": {"success": success}}
        except Exception as e:
            logger.error(f"Error in update_item: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to update item: {str(e)}"
                }
            }
    
    def _handle_get_bibliography(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_bibliography request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_ids = params.get("item_ids", [])
            style = params.get("style", "apa")
            
            bibliography = self.server.get_bibliography(item_ids, style=style)
            return {"result": bibliography}
        except Exception as e:
            logger.error(f"Error in get_bibliography: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get bibliography: {str(e)}"
                }
            }
    
    def _handle_validate_citation_keys(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validate_citation_keys request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            citation_keys = params.get("citation_keys", [])
            
            validation_result = self.server.validate_citation_keys(citation_keys)
            return {"result": validation_result}
        except Exception as e:
            logger.error(f"Error in validate_citation_keys: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to validate citation keys: {str(e)}"
                }
            }
    
    def _handle_sync_ai_notes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sync_ai_notes request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_id = params.get("item_id")
            ai_notes = params.get("ai_notes", [])
            
            if not item_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: item_id"
                    }
                }
            
            result = self.server.sync_ai_notes(item_id, ai_notes)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in sync_ai_notes: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to sync AI notes: {str(e)}"
                }
            }
    
    def _handle_generate_smart_bibliography(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generate_smart_bibliography request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            topic = params.get("topic", "")
            limit = params.get("limit", 20)
            
            bibliography = self.server.generate_smart_bibliography(topic, limit=limit)
            return {"result": bibliography}
        except Exception as e:
            logger.error(f"Error in generate_smart_bibliography: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to generate smart bibliography: {str(e)}"
                }
            }
    
    def _handle_get_item_metadata(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_item_metadata request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            item_id = params.get("item_id")
            if not item_id:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: item_id"
                    }
                }
            
            metadata = self.server.get_item_metadata(item_id)
            return {"result": metadata}
        except Exception as e:
            logger.error(f"Error in get_item_metadata: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get item metadata: {str(e)}"
                }
            }
    
    def _handle_search_advanced(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_advanced request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            query_params = params.get("query_params", {})
            
            results = self.server.search_advanced(query_params)
            return {"result": results}
        except Exception as e:
            logger.error(f"Error in search_advanced: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to perform advanced search: {str(e)}"
                }
            }
    
    def _handle_read_local_library(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_local_library request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            library_path = params.get("library_path")
            if not library_path:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: library_path"
                    }
                }
            
            library_data = self.server.read_local_library(library_path)
            return {"result": library_data}
        except Exception as e:
            logger.error(f"Error in read_local_library: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to read local library: {str(e)}"
                }
            }
    
    def _handle_get_library_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_library_statistics request."""
        try:
            if not self.server:
                return {
                    "error": {
                        "code": -32603,
                        "message": "Server not initialized"
                    }
                }
            
            stats = self.server.get_library_statistics()
            return {"result": stats}
        except Exception as e:
            logger.error(f"Error in get_library_statistics: {str(e)}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Failed to get library statistics: {str(e)}"
                }
            }

def get_handler() -> ZoteroExpertMCPHandler:
    """Get singleton instance of the handler."""
    if not hasattr(get_handler, '_instance'):
        get_handler._instance = ZoteroExpertMCPHandler()
    return get_handler._instance

def handle_mcp_request(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP request using singleton handler."""
    handler = get_handler()
    return handler.handle_request(method, params)