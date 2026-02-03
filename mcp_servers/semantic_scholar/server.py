"""
Semantic Scholar MCP Server Implementation
"""
import requests
import logging
import time
import random
from typing import Dict, List, Any, Optional
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Handle relative imports properly
try:
    from .config import SemanticScholarConfig
    from .cache import CacheManager
except (ImportError, ValueError):
    # Fallback for direct script execution
    from config import SemanticScholarConfig
    from cache import CacheManager

logger = logging.getLogger(__name__)

class SemanticScholarServer:
    """Main server class for Semantic Scholar MCP integration."""
    
    def __init__(self):
        self.config = SemanticScholarConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        self.cache = CacheManager(self.config)
        
    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # Add rate limiting delay
                if attempt > 0:
                    delay = self.config.rate_limit_delay * (2 ** (attempt - 1))  # Exponential backoff
                    delay += random.uniform(0, 0.1)  # Add jitter
                    time.sleep(delay)
                
                response = self.session.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    logger.warning(f"Rate limited on attempt {attempt + 1}")
                    if attempt < self.config.max_retries:
                        continue
                    else:
                        response.raise_for_status()
                elif response.status_code >= 500:
                    logger.warning(f"Server error {response.status_code} on attempt {attempt + 1}")
                    if attempt < self.config.max_retries:
                        continue
                    else:
                        response.raise_for_status()
                else:
                    response.raise_for_status()
                    
                return response
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                logger.warning(f"Request failed on attempt {attempt + 1}: {str(e)}")
                if attempt >= self.config.max_retries:
                    raise e
                    
        raise last_exception
    
    def search_papers(self, query: str, limit: int = 10, fields: List[str] = None) -> Dict[str, Any]:
        """Search for academic papers."""
        if fields is None:
            fields = ["title", "authors", "year", "abstract"]
            
        url = f"{self.config.base_url}/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": ",".join(fields)
        }
        
        # Check cache first
        cached_result = self.cache.get(url, params)
        if cached_result is not None:
            logger.info("Returning cached result for paper search")
            return cached_result
            
        try:
            response = self._make_request_with_retry("GET", url, params=params, timeout=self.config.timeout)
            result = response.json()
            
            # Cache the result
            self.cache.set(url, params, result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching papers: {str(e)}")
            return {"error": str(e)}
            
    def get_paper_details(self, paper_id: str, fields: List[str] = None) -> Dict[str, Any]:
        """Get detailed information about a specific paper."""
        if fields is None:
            fields = ["title", "authors", "year", "abstract", "citationCount", "references", "openAccessPdf"]
            
        url = f"{self.config.base_url}/paper/{paper_id}"
        params = {
            "fields": ",".join(fields)
        }
        
        # Check cache first
        cached_result = self.cache.get(url, params)
        if cached_result is not None:
            logger.info("Returning cached result for paper details")
            return cached_result
            
        try:
            response = self._make_request_with_retry("GET", url, params=params, timeout=self.config.timeout)
            result = response.json()
            
            # Cache the result
            self.cache.set(url, params, result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting paper details: {str(e)}")
            return {"error": str(e)}
            
    def get_citation_context(self, paper_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get citation contexts for a paper."""
        url = f"{self.config.base_url}/paper/{paper_id}/citations"
        params = {
            "limit": limit
        }
        
        # Check cache first
        cached_result = self.cache.get(url, params)
        if cached_result is not None:
            logger.info("Returning cached result for citation context")
            return cached_result
            
        try:
            response = self._make_request_with_retry("GET", url, params=params, timeout=self.config.timeout)
            result = response.json()
            
            # Cache the result
            self.cache.set(url, params, result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting citation context: {str(e)}")
            return {"error": str(e)}
            
    def download_pdf(self, paper_id: str, output_path: str) -> Dict[str, Any]:
        """Download PDF for a paper."""
        # First get paper details to find PDF URL
        paper_details = self.get_paper_details(paper_id, ["openAccessPdf"])
        if "error" in paper_details:
            return paper_details
            
        pdf_url = paper_details.get("openAccessPdf", {}).get("url")
        if not pdf_url:
            return {"error": "No open access PDF available for this paper"}
            
        try:
            response = self._make_request_with_retry("GET", pdf_url, timeout=self.config.timeout)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            return {"success": True, "path": output_path, "size": len(response.content)}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading PDF: {str(e)}")
            return {"error": str(e)}
        except IOError as e:
            logger.error(f"Error saving PDF: {str(e)}")
            return {"error": str(e)}
            
    def search_by_author(self, author_name: str, limit: int = 10, fields: List[str] = None) -> Dict[str, Any]:
        """Search for papers by author name."""
        if fields is None:
            fields = ["title", "authors", "year", "abstract"]
            
        url = f"{self.config.base_url}/author/search"
        params = {
            "query": author_name,
            "limit": limit,
            "fields": ",".join(fields)
        }
        
        # Check cache first
        cached_result = self.cache.get(url, params)
        if cached_result is not None:
            logger.info("Returning cached result for author search")
            return cached_result
            
        try:
            response = self._make_request_with_retry("GET", url, params=params, timeout=self.config.timeout)
            result = response.json()
            
            # Cache the result
            self.cache.set(url, params, result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching by author: {str(e)}")
            return {"error": str(e)}
            
    def search_by_title(self, title: str, limit: int = 10, fields: List[str] = None) -> Dict[str, Any]:
        """Search for papers by title."""
        if fields is None:
            fields = ["title", "authors", "year", "abstract"]
            
        # Use general search with exact title match
        query = f'"{title}"'  # Quote for exact match
        return self.search_papers(query, limit, fields)
            
    def get_paper_references(self, paper_id: str, limit: int = 10, fields: List[str] = None) -> Dict[str, Any]:
        """Get references for a paper."""
        if fields is None:
            fields = ["title", "authors", "year"]
            
        url = f"{self.config.base_url}/paper/{paper_id}/references"
        params = {
            "limit": limit,
            "fields": ",".join(fields)
        }
        
        # Check cache first
        cached_result = self.cache.get(url, params)
        if cached_result is not None:
            logger.info("Returning cached result for paper references")
            return cached_result
            
        try:
            response = self._make_request_with_retry("GET", url, params=params, timeout=self.config.timeout)
            result = response.json()
            
            # Cache the result
            self.cache.set(url, params, result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting paper references: {str(e)}")
            return {"error": str(e)}
            
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()
        
    def clear_cache(self) -> bool:
        """Clear all cached data."""
        return self.cache.clear()