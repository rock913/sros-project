"""
Main Server for Federal Academic Search MCP Server
"""
import asyncio
import logging
from typing import Dict, Any, Optional
import os

from .mcp_handler import FederalAcademicSearchMCPHandler
from .config import FederalAcademicSearchConfig

logger = logging.getLogger(__name__)


class FederalAcademicSearchServer:
    """Main server class for Federal Academic Search MCP integration."""

    def __init__(self):
        """Initialize the server."""
        self.config = FederalAcademicSearchConfig()
        self.handler = FederalAcademicSearchMCPHandler()
        self._initialized = False
        
        # Validate configuration
        try:
            self.config.validate()
            logger.info("Configuration validated successfully")
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            raise

    def _make_request_with_retry(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make request with retry logic (kept for compatibility with existing server interface).
        
        Args:
            method: Method name
            params: Method parameters
            
        Returns:
            Response dictionary
        """
        try:
            return self.handler.handle_request(method, params)
        except Exception as e:
            logger.error(f"Error making request {method}: {str(e)}")
            return {"error": {"code": -32603, "message": str(e)}}

    def search_papers(self, query: str, limit: int = 10, enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for academic papers.
        
        Args:
            query: Search query
            limit: Maximum number of results (default: 10)
            enrich: Whether to enrich results with S2 and Unpaywall data (default: True)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing search results
        """
        params = {
            "query": query,
            "limit": limit,
            "enrich": enrich,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("search_papers", params)

    def get_paper_details(self, paper_id: str, enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper.
        
        Args:
            paper_id: Paper ID or DOI
            enrich: Whether to enrich with S2 and Unpaywall data (default: True)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing paper details
        """
        params = {
            "paper_id": paper_id,
            "enrich": enrich,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("get_paper_details", params)

    def get_citation_context(self, paper_id: str, limit: int = 10, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get citation contexts for a paper from Semantic Scholar.
        
        Args:
            paper_id: Paper ID
            limit: Maximum number of contexts (default: 10)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing citation contexts
        """
        params = {
            "paper_id": paper_id,
            "limit": limit,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("get_citation_context", params)

    def download_pdf(self, paper_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get PDF URL for a paper using Unpaywall.
        
        Args:
            paper_id: Paper ID or DOI
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing PDF URL
        """
        params = {
            "paper_id": paper_id,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("download_pdf", params)

    def search_by_author(self, author_name: str, limit: int = 10, enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for papers by author name.
        
        Args:
            author_name: Author name
            limit: Maximum number of results (default: 10)
            enrich: Whether to enrich results (default: True)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing search results
        """
        params = {
            "author_name": author_name,
            "limit": limit,
            "enrich": enrich,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("search_by_author", params)

    def search_by_title(self, title: str, limit: int = 10, enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for papers by title.
        
        Args:
            title: Paper title
            limit: Maximum number of results (default: 10)
            enrich: Whether to enrich results (default: True)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing search results
        """
        params = {
            "title": title,
            "limit": limit,
            "enrich": enrich,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("search_by_title", params)

    def get_paper_references(self, paper_id: str, limit: int = 10, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get references for a paper.
        
        Args:
            paper_id: Paper ID
            limit: Maximum number of references (default: 10)
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing references
        """
        params = {
            "paper_id": paper_id,
            "limit": limit,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("get_paper_references", params)

    def get_tldr(self, paper_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get TLDR summary for a paper from Semantic Scholar.
        
        Args:
            paper_id: Paper ID
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dict containing TLDR summary
        """
        params = {
            "paper_id": paper_id,
            "use_cache": use_cache
        }
        return self._make_request_with_retry("get_tldr", params)

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict containing cache statistics
        """
        return self._make_request_with_retry("get_cache_stats", {})

    def clear_cache(self) -> Dict[str, Any]:
        """
        Clear all cache entries.
        
        Returns:
            Dict containing result message
        """
        return self._make_request_with_retry("clear_cache", {})

    def initialize(self) -> Dict[str, Any]:
        """
        Initialize the server.
        
        Returns:
            Dict containing initialization result
        """
        result = self._make_request_with_retry("initialize", {})
        if "error" not in result:
            self._initialized = True
        return result

    def is_initialized(self) -> bool:
        """
        Check if server is initialized.
        
        Returns:
            Boolean indicating initialization status
        """
        return self._initialized


# Convenience functions for direct usage
def create_server() -> FederalAcademicSearchServer:
    """Create and return a new server instance."""
    return FederalAcademicSearchServer()


def main():
    """Main entry point for the server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        server = FederalAcademicSearchServer()
        logger.info("Federal Academic Search Server created successfully")
        
        # Initialize server
        init_result = server.initialize()
        if "error" in init_result:
            logger.error(f"Failed to initialize server: {init_result['error']}")
            return 1
            
        logger.info("Server initialized successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to create server: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())