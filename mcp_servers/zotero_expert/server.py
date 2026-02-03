"""
Zotero Expert MCP Server Implementation
"""
import requests
import logging
from typing import Dict, List, Any, Optional
import sys
import os
from pyzotero import zotero

# Handle relative imports properly
try:
    from .config import ZoteroExpertConfig
except (ImportError, ValueError):
    # Fallback for direct script execution
    from config import ZoteroExpertConfig

logger = logging.getLogger(__name__)

class ZoteroExpertServer:
    """Main server class for Zotero Expert MCP integration."""
    
    def __init__(self):
        self.config = ZoteroExpertConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        
        # Initialize pyzotero client if configuration is valid
        if self.config.validate():
            try:
                self.zotero_client = zotero.Zotero(
                    self.config.library_id,
                    self.config.library_type,
                    self.config.api_key
                )
            except Exception as e:
                logger.warning(f"Failed to initialize pyzotero client: {str(e)}")
                self.zotero_client = None
        else:
            self.zotero_client = None
        
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling."""
        try:
            response = self.session.request(method, url, timeout=self.config.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            raise e
    
    def get_library_items(self, limit: int = 100, start: int = 0) -> Dict[str, Any]:
        """Get items from the Zotero library."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        params = {
            "limit": limit,
            "start": start
        }
        
        try:
            response = self._make_request("GET", url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting library items: {str(e)}")
            return {"error": str(e)}
    
    def get_item(self, item_key: str) -> Dict[str, Any]:
        """Get a specific item from the library."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items/{item_key}"
        
        try:
            response = self._make_request("GET", url)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting item {item_key}: {str(e)}")
            return {"error": str(e)}
    
    def search_items(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search for items in the library."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        params = {
            "q": query,
            "limit": limit
        }
        
        try:
            response = self._make_request("GET", url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching items: {str(e)}")
            return {"error": str(e)}
    
    def get_collections(self) -> Dict[str, Any]:
        """Get all collections in the library."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/collections"
        
        try:
            response = self._make_request("GET", url)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting collections: {str(e)}")
            return {"error": str(e)}
    
    def get_item_children(self, item_key: str) -> Dict[str, Any]:
        """Get child items (notes, attachments) of a parent item."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items/{item_key}/children"
        
        try:
            response = self._make_request("GET", url)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting item children for {item_key}: {str(e)}")
            return {"error": str(e)}
    
    def create_note(self, parent_item_key: str, note_content: str) -> Dict[str, Any]:
        """Create a note attached to a parent item."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        
        # Prepare note data
        note_data = {
            "itemType": "note",
            "parentItem": parent_item_key,
            "note": note_content
        }
        
        try:
            response = self._make_request("POST", url, json=note_data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating note for item {parent_item_key}: {str(e)}")
            return {"error": str(e)}
    
    def update_item(self, item_key: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing item."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items/{item_key}"
        
        try:
            response = self._make_request("PATCH", url, json=item_data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating item {item_key}: {str(e)}")
            return {"error": str(e)}
    
    def get_bibliography(self, item_keys: List[str], style: str = "apa") -> Dict[str, Any]:
        """Generate bibliography for specified items."""
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        params = {
            "format": "bib",
            "style": style
        }
        
        # Include item keys in request
        data = {
            "items": [{"key": key} for key in item_keys]
        }
        
        try:
            response = self._make_request("POST", url, params=params, json=data)
            return {"bibliography": response.text}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating bibliography: {str(e)}")
            return {"error": str(e)}
    
    def validate_citation_keys(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate citation keys for consistency across the library.
        
        Args:
            items: List of item dictionaries to validate
            
        Returns:
            Dictionary with validation results and conflicts
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        citation_keys = {}
        conflicts = []
        
        for item in items:
            key = item.get('key')
            citation_key = item.get('data', {}).get('citationKey') or item.get('data', {}).get('key')
            
            if citation_key:
                if citation_key in citation_keys:
                    conflicts.append({
                        "citation_key": citation_key,
                        "conflicting_items": [citation_keys[citation_key], key]
                    })
                else:
                    citation_keys[citation_key] = key
        
        return {
            "valid": len(conflicts) == 0,
            "conflicts": conflicts,
            "total_items": len(items),
            "unique_citation_keys": len(citation_keys)
        }
    
    def sync_ai_notes(self, item_key: str, ai_notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronize AI-generated notes with Zotero items.
        
        Args:
            item_key: The key of the parent item
            ai_notes: List of AI-generated notes to sync
            
        Returns:
            Dictionary with sync results
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        synced_notes = []
        errors = []
        
        for note_data in ai_notes:
            try:
                # Create or update note
                note_content = note_data.get('content', '')
                note_title = note_data.get('title', 'AI Generated Note')
                
                # Prepare note data with title
                full_note_content = f"<h1>{note_title}</h1><p>{note_content}</p>"
                
                result = self.create_note(item_key, full_note_content)
                if "error" not in result:
                    synced_notes.append({
                        "title": note_title,
                        "status": "synced",
                        "zotero_note_id": result.get("key") if isinstance(result, dict) else None
                    })
                else:
                    errors.append({
                        "title": note_title,
                        "error": result.get("error", "Unknown error")
                    })
            except Exception as e:
                errors.append({
                    "title": note_data.get('title', 'Untitled'),
                    "error": str(e)
                })
        
        return {
            "synced": len(synced_notes),
            "errors": len(errors),
            "notes": synced_notes,
            "error_details": errors
        }
    
    def generate_smart_bibliography(self, item_keys: List[str], style: str = "apa",
                                     format_options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a smart bibliography with customizable formatting options.
        
        Args:
            item_keys: List of item keys to include
            style: Citation style (apa, mla, chicago, etc.)
            format_options: Additional formatting options
            
        Returns:
            Dictionary with bibliography and metadata
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        if format_options is None:
            format_options = {}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        params = {
            "format": "bib",
            "style": style
        }
        
        # Add format options to params
        for key, value in format_options.items():
            params[key] = value
        
        # Include item keys in request
        data = {
            "items": [{"key": key} for key in item_keys]
        }
        
        try:
            response = self._make_request("POST", url, params=params, json=data)
            return {
                "bibliography": response.text,
                "style": style,
                "item_count": len(item_keys),
                "format_options": format_options
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating smart bibliography: {str(e)}")
            return {"error": str(e)}
    
    def get_item_metadata(self, item_key: str) -> Dict[str, Any]:
        """
        Get comprehensive metadata for an item including citations and relations.
        
        Args:
            item_key: The key of the item to retrieve
            
        Returns:
            Dictionary with item metadata
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        try:
            # Get main item
            item_result = self.get_item(item_key)
            if "error" in item_result:
                return item_result
                
            # Get citations
            citations_url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items/{item_key}/collections"
            citations_response = self._make_request("GET", citations_url)
            citations = citations_response.json()
            
            # Get children (notes, attachments)
            children_result = self.get_item_children(item_key)
            if "error" in children_result:
                children = []
            else:
                children = children_result
            
            return {
                "item": item_result,
                "citations": citations,
                "children": children,
                "metadata_complete": True
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting item metadata: {str(e)}")
            return {"error": str(e)}
    
    def search_advanced(self, query: str, item_type: str = None,
                         collection_key: str = None, limit: int = 50) -> Dict[str, Any]:
        """
        Advanced search with multiple filters.
        
        Args:
            query: Search query
            item_type: Filter by item type (journalArticle, book, etc.)
            collection_key: Filter by collection
            limit: Maximum number of results
            
        Returns:
            Dictionary with search results
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        url = f"{self.config.base_url}/{self.config.library_type}s/{self.config.library_id}/items"
        params = {
            "q": query,
            "limit": limit
        }
        
        # Add filters
        if item_type:
            params["itemType"] = item_type
        if collection_key:
            params["collection"] = collection_key
        
        try:
            response = self._make_request("GET", url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in advanced search: {str(e)}")
            return {"error": str(e)}
    
    def read_local_library(self, limit: int = 100, start: int = 0) -> Dict[str, Any]:
        """
        Read from local Zotero library using pyzotero client.
        
        Args:
            limit: Maximum number of items to retrieve
            start: Starting position for pagination
            
        Returns:
            Dictionary with library items or error
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        if not self.zotero_client:
            return {"error": "Zotero client not initialized"}
            
        try:
            # Set pagination
            self.zotero_client.add_parameters(limit=limit, start=start)
            
            # Get items from library
            items = self.zotero_client.items()
            
            return {
                "items": items,
                "count": len(items),
                "limit": limit,
                "start": start
            }
        except Exception as e:
            logger.error(f"Error reading local library: {str(e)}")
            return {"error": str(e)}
    
    def get_library_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the local Zotero library.
        
        Returns:
            Dictionary with library statistics
        """
        if not self.config.validate():
            return {"error": "Invalid configuration: Library ID and API key required"}
            
        if not self.zotero_client:
            return {"error": "Zotero client not initialized"}
            
        try:
            # Get library metadata
            items = self.zotero_client.items()
            collections = self.zotero_client.collections()
            
            # Count item types
            item_types = {}
            for item in items:
                item_type = item.get('data', {}).get('itemType', 'unknown')
                item_types[item_type] = item_types.get(item_type, 0) + 1
            
            return {
                "total_items": len(items),
                "total_collections": len(collections),
                "item_types": item_types,
                "last_updated": self.zotero_client.last_modified_version
            }
        except Exception as e:
            logger.error(f"Error getting library statistics: {str(e)}")
            return {"error": str(e)}