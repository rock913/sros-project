"""
OpenAlex Provider for Federal Academic Search MCP Server
"""
import logging
from typing import Dict, Any, List, Optional
from .base import BaseProvider

logger = logging.getLogger(__name__)


class OpenAlexProvider(BaseProvider):
    """Provider for OpenAlex academic search API."""

    async def search_papers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for academic papers using OpenAlex API."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        url = f"{self.config.openalex_base_url}/works"
        params = {
            "search": query,
            "per-page": min(limit, 200),  # OpenAlex max is 200
            "select": "id,doi,title,display_name,publication_year,abstract_inverted_index,cited_by_count,best_oa_location,authorships"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET", 
                url, 
                headers=self.config.get_openalex_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_search_results(data)
            else:
                return {"error": "No response from OpenAlex API"}
                
        except Exception as e:
            logger.error(f"Error searching papers in OpenAlex: {str(e)}")
            return {"error": str(e)}

    async def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific paper from OpenAlex."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        # Handle both full URLs and IDs
        if paper_id.startswith("https://"):
            url = paper_id
        else:
            url = f"{self.config.openalex_base_url}/works/{paper_id}"
            
        params = {
            "select": "id,doi,title,display_name,publication_year,abstract_inverted_index,cited_by_count,best_oa_location,authorships,referenced_works"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_openalex_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_paper_details(data)
            else:
                return {"error": "No response from OpenAlex API"}
                
        except Exception as e:
            logger.error(f"Error getting paper details from OpenAlex: {str(e)}")
            return {"error": str(e)}

    async def get_paper_references(self, paper_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get references for a paper from OpenAlex."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        # Handle both full URLs and IDs
        if paper_id.startswith("https://"):
            url = f"{paper_id}/referenced-works"
        else:
            url = f"{self.config.openalex_base_url}/works/{paper_id}/referenced-works"
            
        params = {
            "per-page": min(limit, 200),
            "select": "id,doi,title,display_name,publication_year,cited_by_count"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_openalex_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_references(data)
            else:
                return {"error": "No response from OpenAlex API"}
                
        except Exception as e:
            logger.error(f"Error getting paper references from OpenAlex: {str(e)}")
            return {"error": str(e)}

    async def search_by_author(self, author_name: str, limit: int = 10) -> Dict[str, Any]:
        """Search for papers by author name using OpenAlex."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        # First search for the author
        author_url = f"{self.config.openalex_base_url}/authors"
        author_params = {
            "search": author_name,
            "per-page": 1  # Get the most relevant author
        }
        
        try:
            author_response = await self._make_request_with_retry(
                "GET",
                author_url,
                headers=self.config.get_openalex_headers(),
                params=author_params
            )
            
            if not author_response:
                return {"error": "No response from OpenAlex API when searching for author"}
                
            author_data = await author_response.json()
            
            if not author_data.get("results"):
                return {"error": f"No author found for name: {author_name}"}
                
            author_id = author_data["results"][0]["id"].split("/")[-1]
            
            # Now search for papers by this author
            works_url = f"{self.config.openalex_base_url}/works"
            works_params = {
                "filter": f"author.id:{author_id}",
                "per-page": min(limit, 200),
                "select": "id,doi,title,display_name,publication_year,abstract_inverted_index,cited_by_count,best_oa_location,authorships"
            }
            
            works_response = await self._make_request_with_retry(
                "GET",
                works_url,
                headers=self.config.get_openalex_headers(),
                params=works_params
            )
            
            if works_response:
                works_data = await works_response.json()
                return self._transform_search_results(works_data)
            else:
                return {"error": "No response from OpenAlex API when searching for papers"}
                
        except Exception as e:
            logger.error(f"Error searching by author in OpenAlex: {str(e)}")
            return {"error": str(e)}

    async def search_by_title(self, title: str, limit: int = 10) -> Dict[str, Any]:
        """Search for papers by title using OpenAlex."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        url = f"{self.config.openalex_base_url}/works"
        params = {
            "search": f'title:"{title}"',  # Exact title match
            "per-page": min(limit, 200),
            "select": "id,doi,title,display_name,publication_year,abstract_inverted_index,cited_by_count,best_oa_location,authorships"
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_openalex_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_search_results(data)
            else:
                return {"error": "No response from OpenAlex API"}
                
        except Exception as e:
            logger.error(f"Error searching by title in OpenAlex: {str(e)}")
            return {"error": str(e)}

    def _transform_search_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenAlex search results to unified format."""
        if "error" in data:
            return data
            
        transformed_results = []
        
        for work in data.get("results", []):
            transformed_work = self._transform_single_work(work)
            transformed_results.append(transformed_work)
            
        return {
            "results": transformed_results,
            "total": data.get("meta", {}).get("count", 0),
            "pagination": {
                "next": data.get("meta", {}).get("next_cursor"),
                "previous": data.get("meta", {}).get("previous_cursor")
            }
        }

    def _transform_paper_details(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenAlex paper details to unified format."""
        if "error" in data:
            return data
            
        return self._transform_single_work(data)

    def _transform_references(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenAlex references to unified format."""
        if "error" in data:
            return data
            
        transformed_references = []
        
        for work in data.get("results", []):
            transformed_work = {
                "paperId": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("display_name"),
                "year": work.get("publication_year"),
                "citationCount": work.get("cited_by_count")
            }
            transformed_references.append(transformed_work)
            
        return {
            "references": transformed_references,
            "total": len(transformed_references)
        }

    def _transform_single_work(self, work: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single OpenAlex work to unified format."""
        # Extract abstract from inverted index
        abstract = ""
        if work.get("abstract_inverted_index"):
            # Reconstruct abstract from inverted index
            inverted_index = work["abstract_inverted_index"]
            if isinstance(inverted_index, dict):
                # Sort by position and reconstruct
                words = []
                for word, positions in inverted_index.items():
                    for pos in positions if isinstance(positions, list) else [positions]:
                        while len(words) <= pos:
                            words.append("")
                        words[pos] = word
                abstract = " ".join(words)
        
        # Extract authors
        authors = []
        if work.get("authorships"):
            for authorship in work["authorships"]:
                if authorship.get("author", {}).get("display_name"):
                    authors.append(authorship["author"]["display_name"])
        
        return {
            "paperId": work.get("id"),
            "doi": work.get("doi"),
            "title": work.get("display_name") or work.get("title"),
            "year": work.get("publication_year"),
            "abstract": abstract,
            "citationCount": work.get("cited_by_count"),
            "authors": ", ".join(authors) if authors else None,
            "openAccessPdf": work.get("best_oa_location", {}).get("url_for_pdf") if work.get("best_oa_location") else None,
            "venue": work.get("primary_location", {}).get("source", {}).get("display_name") if work.get("primary_location", {}).get("source") else None
        }