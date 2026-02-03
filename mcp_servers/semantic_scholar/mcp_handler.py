"""
MCP Handler for Semantic Scholar Server
Implements the Model Context Protocol interface for the Semantic Scholar server.
"""
import json
import logging
from typing import Dict, Any, List
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Handle relative imports properly
try:
    from .server import SemanticScholarServer
    from .config import SemanticScholarConfig
except (ImportError, ValueError):
    # Fallback for direct script execution
    from server import SemanticScholarServer
    from config import SemanticScholarConfig

logger = logging.getLogger(__name__)

class SemanticScholarMCPHandler:
    """MCP Handler for Semantic Scholar Server."""
    
    def __init__(self):
        """Initialize the MCP handler."""
        self.config = SemanticScholarConfig()
        self.server = SemanticScholarServer()
        
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
            elif method == "search_papers":
                return self._handle_search_papers(params)
            elif method == "get_paper_details":
                return self._handle_get_paper_details(params)
            elif method == "get_citation_context":
                return self._handle_get_citation_context(params)
            elif method == "download_pdf":
                return self._handle_download_pdf(params)
            elif method == "search_by_author":
                return self._handle_search_by_author(params)
            elif method == "search_by_title":
                return self._handle_search_by_title(params)
            elif method == "get_paper_references":
                return self._handle_get_paper_references(params)
            elif method == "get_cache_stats":
                return self._handle_get_cache_stats(params)
            elif method == "clear_cache":
                return self._handle_clear_cache(params)
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
                    "paperSearch": True,
                    "paperDetails": True,
                    "citationContext": True,
                    "pdfDownload": True,
                    "authorSearch": True,
                    "titleSearch": True,
                    "paperReferences": True,
                    "cacheManagement": True
                }
            }
        }
        
    def _handle_search_papers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_papers request."""
        try:
            query = params.get("query", "")
            limit = params.get("limit", 10)
            fields = params.get("fields")
            
            result = self.server.search_papers(query, limit, fields)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error searching papers: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error searching papers: {str(e)}"
                }
            }
            
    def _handle_get_paper_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper_details request."""
        try:
            paper_id = params.get("paper_id", "")
            fields = params.get("fields")
            
            result = self.server.get_paper_details(paper_id, fields)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting paper details: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting paper details: {str(e)}"
                }
            }
            
    def _handle_get_citation_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_citation_context request."""
        try:
            paper_id = params.get("paper_id", "")
            limit = params.get("limit", 10)
            
            result = self.server.get_citation_context(paper_id, limit)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting citation context: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting citation context: {str(e)}"
                }
            }
            
    def _handle_download_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle download_pdf request."""
        try:
            paper_id = params.get("paper_id", "")
            output_path = params.get("output_path", f"{paper_id}.pdf")
            
            result = self.server.download_pdf(paper_id, output_path)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error downloading PDF: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error downloading PDF: {str(e)}"
                }
            }
            
    def _handle_search_by_author(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_by_author request."""
        try:
            author_name = params.get("author_name", "")
            limit = params.get("limit", 10)
            fields = params.get("fields")
            
            result = self.server.search_by_author(author_name, limit, fields)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error searching by author: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error searching by author: {str(e)}"
                }
            }
            
    def _handle_search_by_title(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_by_title request."""
        try:
            title = params.get("title", "")
            limit = params.get("limit", 10)
            fields = params.get("fields")
            
            result = self.server.search_by_title(title, limit, fields)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error searching by title: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error searching by title: {str(e)}"
                }
            }
            
    def _handle_get_paper_references(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper_references request."""
        try:
            paper_id = params.get("paper_id", "")
            limit = params.get("limit", 10)
            fields = params.get("fields")
            
            result = self.server.get_paper_references(paper_id, limit, fields)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting paper references: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting paper references: {str(e)}"
                }
            }
            
    def _handle_get_cache_stats(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_cache_stats request."""
        try:
            result = self.server.get_cache_stats()
            return {"result": result}
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error getting cache stats: {str(e)}"
                }
            }
            
    def _handle_clear_cache(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle clear_cache request."""
        try:
            result = self.server.clear_cache()
            return {"result": {"success": result}}
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Error clearing cache: {str(e)}"
                }
            }