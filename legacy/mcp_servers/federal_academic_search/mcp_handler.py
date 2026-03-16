"""
MCP Handler for Federal Academic Search Server
"""
import json
import logging
from typing import Dict, Any, List
import asyncio

from .core import AcademicSearchManager
from .config import FederalAcademicSearchConfig

logger = logging.getLogger(__name__)

class FederalAcademicSearchMCPHandler:
    """MCP Handler for Federal Academic Search Server."""

    def __init__(self):
        """Initialize the MCP handler."""
        self.config = FederalAcademicSearchConfig()
        self.search_manager = AcademicSearchManager(self.config)
        self._initialized = False

    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP requests.
        
        Args:
            method: Method name
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
            elif method == "get_tldr":
                return self._handle_get_tldr(params)
            elif method == "get_cache_stats":
                return self._handle_get_cache_stats(params)
            elif method == "clear_cache":
                return self._handle_clear_cache(params)
            elif method == "tools/list":
                return self._handle_list_tools(params)
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

    def _handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request."""
        return {
            "result": {
                "tools": [
                    {
                        "name": "search_papers",
                        "description": "Search for academic papers using OpenAlex (primary), Unpaywall (PDFs), and Semantic Scholar (enrichment).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"},
                                "limit": {"type": "integer", "description": "Max results (default 10)", "default": 10},
                                "enrich": {"type": "boolean", "description": "Enrich with S2 data", "default": True}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_paper_details",
                        "description": "Get detailed metadata for a specific paper.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "paper_id": {"type": "string", "description": "OpenAlex ID (W...) or DOI"}
                            },
                            "required": ["paper_id"]
                        }
                    },
                    {
                        "name": "download_pdf",
                        "description": "Try to download PDF for a paper.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "paper_id": {"type": "string", "description": "Paper ID"},
                                "save_path": {"type": "string", "description": "Directory to save PDF"}
                            },
                            "required": ["paper_id"]
                        }
                    }
                ]
            }
        }

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        self._initialized = True
        return {
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "Federal Academic Search MCP Server",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "search_papers": {},
                    "get_paper_details": {},
                    "get_citation_context": {},
                    "download_pdf": {},
                    "search_by_author": {},
                    "search_by_title": {},
                    "get_paper_references": {},
                    "get_tldr": {},
                    "get_cache_stats": {},
                    "clear_cache": {}
                }
            }
        }

    def _handle_search_papers(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_papers request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            query = params.get("query", "")
            limit = params.get("limit", 10)
            # Handle backward compatibility - if fields parameter is provided, don't enrich by default
            fields = params.get("fields")
            enrich = params.get("enrich", True) if fields is None else params.get("enrich", False)
            use_cache = params.get("use_cache", True)
            
            if not query:
                return {"error": {"code": -32602, "message": "Missing required parameter: query"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.search_papers(query, limit, enrich, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in search_papers: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_get_paper_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper_details request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            paper_id = params.get("paper_id", "")
            # Handle backward compatibility - if fields parameter is provided, don't enrich by default
            fields = params.get("fields")
            enrich = params.get("enrich", True) if fields is None else params.get("enrich", False)
            use_cache = params.get("use_cache", True)
            
            if not paper_id:
                return {"error": {"code": -32602, "message": "Missing required parameter: paper_id"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.get_paper_details(paper_id, enrich, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in get_paper_details: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_get_citation_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_citation_context request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            paper_id = params.get("paper_id", "")
            limit = params.get("limit", 10)
            use_cache = params.get("use_cache", True)
            
            if not paper_id:
                return {"error": {"code": -32602, "message": "Missing required parameter: paper_id"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.get_citation_context(paper_id, limit, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in get_citation_context: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_download_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle download_pdf request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            paper_id = params.get("paper_id", "")
            use_cache = params.get("use_cache", True)
            
            if not paper_id:
                return {"error": {"code": -32602, "message": "Missing required parameter: paper_id"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.download_pdf(paper_id, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in download_pdf: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_search_by_author(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_by_author request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            author_name = params.get("author_name", "")
            limit = params.get("limit", 10)
            # Handle backward compatibility - if fields parameter is provided, don't enrich by default
            fields = params.get("fields")
            enrich = params.get("enrich", True) if fields is None else params.get("enrich", False)
            use_cache = params.get("use_cache", True)
            
            if not author_name:
                return {"error": {"code": -32602, "message": "Missing required parameter: author_name"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.search_by_author(author_name, limit, enrich, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in search_by_author: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_search_by_title(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_by_title request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            title = params.get("title", "")
            limit = params.get("limit", 10)
            # Handle backward compatibility - if fields parameter is provided, don't enrich by default
            fields = params.get("fields")
            enrich = params.get("enrich", True) if fields is None else params.get("enrich", False)
            use_cache = params.get("use_cache", True)
            
            if not title:
                return {"error": {"code": -32602, "message": "Missing required parameter: title"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.search_by_title(title, limit, enrich, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in search_by_title: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_get_paper_references(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_paper_references request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            paper_id = params.get("paper_id", "")
            limit = params.get("limit", 10)
            # Handle backward compatibility - if fields parameter is provided, don't enrich by default
            fields = params.get("fields")
            enrich = params.get("enrich", True) if fields is None else params.get("enrich", False)
            use_cache = params.get("use_cache", True)
            
            if not paper_id:
                return {"error": {"code": -32602, "message": "Missing required parameter: paper_id"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.get_paper_references(paper_id, limit, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in get_paper_references: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_get_tldr(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_tldr request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            paper_id = params.get("paper_id", "")
            use_cache = params.get("use_cache", True)
            
            if not paper_id:
                return {"error": {"code": -32602, "message": "Missing required parameter: paper_id"}}
            
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.get_tldr(paper_id, use_cache)
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in get_tldr: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_get_cache_stats(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_cache_stats request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            stats = self.search_manager.get_cache_stats()
            return {"result": stats}
        except Exception as e:
            logger.error(f"Error in get_cache_stats: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def _handle_clear_cache(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle clear_cache request."""
        if not self._initialized:
            return {"error": {"code": -32002, "message": "Server not initialized"}}
            
        try:
            # Run async method in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.search_manager.clear_cache()
            )
            loop.close()
            
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in clear_cache: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}