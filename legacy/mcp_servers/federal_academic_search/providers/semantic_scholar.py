"""
Semantic Scholar Provider for Federal Academic Search MCP Server
"""
import logging
from typing import Dict, Any, Optional
from .base import BaseProvider

logger = logging.getLogger(__name__)


class SemanticScholarProvider(BaseProvider):
    """Provider for Semantic Scholar API enrichment services."""

    async def get_tldr(self, paper_id: str) -> Dict[str, Any]:
        """Get TLDR summary for a paper using Semantic Scholar API."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        # Handle both full URLs and IDs
        if paper_id.startswith("http"):
            # Extract paper ID from URL
            paper_id = paper_id.split("/")[-1]
            
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
        params = {
            "fields": "tldr"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_s2_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_tldr_result(data)
            else:
                return {"error": "No response from Semantic Scholar API"}
                
        except Exception as e:
            logger.error(f"Error getting TLDR from Semantic Scholar: {str(e)}")
            return {"error": str(e)}

    async def get_citation_context(self, paper_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get citation contexts for a paper using Semantic Scholar API."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        # Handle both full URLs and IDs
        if paper_id.startswith("http"):
            # Extract paper ID from URL
            paper_id = paper_id.split("/")[-1]
            
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
        params = {
            "limit": min(limit, 100),  # S2 max is 100
            "fields": "contexts,citingPaper.title,citingPaper.abstract,citingPaper.year,citingPaper.authors"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_s2_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_citation_contexts(data)
            else:
                return {"error": "No response from Semantic Scholar API"}
                
        except Exception as e:
            logger.error(f"Error getting citation contexts from Semantic Scholar: {str(e)}")
            return {"error": str(e)}

    async def get_paper_details(self, paper_id: str, fields: list = None) -> Dict[str, Any]:
        """Get detailed information about a paper from Semantic Scholar."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        if fields is None:
            fields = ["title", "abstract", "year", "authors", "citationCount", "referenceCount", "tldr"]
            
        # Handle both full URLs and IDs
        if paper_id.startswith("http"):
            # Extract paper ID from URL
            paper_id = paper_id.split("/")[-1]
            
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
        params = {
            "fields": ",".join(fields)
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_s2_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_paper_details(data)
            else:
                return {"error": "No response from Semantic Scholar API"}
                
        except Exception as e:
            logger.error(f"Error getting paper details from Semantic Scholar: {str(e)}")
            return {"error": str(e)}

    async def search_papers(self, query: str, limit: int = 10, fields: list = None) -> Dict[str, Any]:
        """Search for papers using Semantic Scholar API."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        if fields is None:
            fields = ["paperId", "title", "abstract", "year", "authors", "citationCount", "tldr"]
            
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": min(limit, 100),  # S2 max is 100
            "fields": ",".join(fields)
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_s2_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_search_results(data)
            else:
                return {"error": "No response from Semantic Scholar API"}
                
        except Exception as e:
            logger.error(f"Error searching papers in Semantic Scholar: {str(e)}")
            return {"error": str(e)}

    def _transform_tldr_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Semantic Scholar TLDR result to unified format."""
        if "error" in data:
            return data
            
        tldr_data = data.get("tldr", {})
        if tldr_data and isinstance(tldr_data, dict):
            return {
                "tldr": tldr_data.get("text", ""),
                "paperId": data.get("paperId")
            }
        elif tldr_data and isinstance(tldr_data, str):
            return {
                "tldr": tldr_data,
                "paperId": data.get("paperId")
            }
        else:
            return {
                "tldr": None,
                "paperId": data.get("paperId")
            }

    def _transform_citation_contexts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Semantic Scholar citation contexts to unified format."""
        if "error" in data:
            return data
            
        transformed_contexts = []
        
        for citation in data.get("data", []):
            citing_paper = citation.get("citingPaper", {})
            contexts = citation.get("contexts", [])
            
            if contexts and citing_paper:
                transformed_context = {
                    "citingPaperId": citing_paper.get("paperId"),
                    "citingPaperTitle": citing_paper.get("title"),
                    "citingPaperYear": citing_paper.get("year"),
                    "contexts": contexts,
                    "citingPaperAuthors": [author.get("name") for author in citing_paper.get("authors", [])]
                }
                transformed_contexts.append(transformed_context)
                
        return {
            "contexts": transformed_contexts,
            "total": len(transformed_contexts)
        }

    def _transform_paper_details(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Semantic Scholar paper details to unified format."""
        if "error" in data:
            return data
            
        authors = []
        if data.get("authors"):
            for author in data["authors"]:
                if isinstance(author, dict):
                    authors.append(author.get("name", ""))
                else:
                    authors.append(str(author))
                    
        return {
            "paperId": data.get("paperId"),
            "doi": data.get("doi"),
            "title": data.get("title"),
            "abstract": data.get("abstract"),
            "year": data.get("year"),
            "citationCount": data.get("citationCount"),
            "referenceCount": data.get("referenceCount"),
            "authors": ", ".join(authors) if authors else None,
            "tldr": data.get("tldr", {}).get("text") if isinstance(data.get("tldr"), dict) else data.get("tldr")
        }

    def _transform_search_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Semantic Scholar search results to unified format."""
        if "error" in data:
            return data
            
        transformed_results = []
        
        for paper in data.get("data", []):
            transformed_paper = self._transform_paper_details(paper)
            transformed_results.append(transformed_paper)
            
        return {
            "results": transformed_results,
            "total": data.get("total", 0),
            "offset": data.get("offset", 0),
            "next": data.get("next", 0) if data.get("next", 0) < data.get("total", 0) else None
        }