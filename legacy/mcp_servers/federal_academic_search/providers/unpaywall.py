"""
Unpaywall Provider for Federal Academic Search MCP Server
"""
import logging
from typing import Dict, Any, Optional
from .base import BaseProvider

logger = logging.getLogger(__name__)


class UnpaywallProvider(BaseProvider):
    """Provider for Unpaywall PDF retrieval API."""

    async def get_pdf_url(self, doi: str) -> Dict[str, Any]:
        """Get PDF URL for a paper using Unpaywall API."""
        if not self.session:
            raise RuntimeError("Provider not initialized. Use async context manager.")
            
        if not doi:
            return {"error": "DOI is required"}
            
        # Clean DOI if it's a full URL
        if doi.startswith("http"):
            doi = doi.split("/")[-1]
            
        url = f"{self.config.unpaywall_base_url}/{doi}"
        params = {
            "email": self.config.unpaywall_email
        }
        
        try:
            response = await self._make_request_with_retry(
                "GET",
                url,
                headers=self.config.get_unpaywall_headers(),
                params=params
            )
            
            if response:
                data = await response.json()
                return self._transform_pdf_result(data)
            else:
                return {"error": "No response from Unpaywall API"}
                
        except Exception as e:
            logger.error(f"Error getting PDF URL from Unpaywall: {str(e)}")
            return {"error": str(e)}

    def _transform_pdf_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Unpaywall result to unified format."""
        if "error" in data:
            return data
            
        # Look for the best OA location
        best_oa_location = data.get("best_oa_location")
        if best_oa_location and best_oa_location.get("url_for_pdf"):
            return {
                "pdf_url": best_oa_location["url_for_pdf"],
                "is_oa": data.get("is_oa", False),
                "oa_status": data.get("oa_status"),
                "license": best_oa_location.get("license")
            }
        
        # Check other locations
        oa_locations = data.get("oa_locations", [])
        for location in oa_locations:
            if location.get("url_for_pdf"):
                return {
                    "pdf_url": location["url_for_pdf"],
                    "is_oa": data.get("is_oa", False),
                    "oa_status": data.get("oa_status"),
                    "license": location.get("license")
                }
        
        # No PDF found
        return {
            "pdf_url": None,
            "is_oa": data.get("is_oa", False),
            "oa_status": data.get("oa_status"),
            "license": None
        }

    async def search_papers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Stub method for paper search (Unpaywall only provides PDF URLs)."""
        return {"error": "Unpaywall provider only supports PDF URL retrieval, not paper search"}

    async def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """Stub method for paper details (Unpaywall only provides PDF URLs)."""
        return {"error": "Unpaywall provider only supports PDF URL retrieval, not paper details"}