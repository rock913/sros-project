"""
Result Transformer for Federal Academic Search MCP Server
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ResultTransformer:
    """Transform results from different providers to unified format and maintain compatibility."""

    @staticmethod
    def transform_search_results(openalex_results: Dict[str, Any], 
                               unpaywall_results: List[Dict[str, Any]] = None,
                               s2_results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Transform federated search results to unified format.
        
        Args:
            openalex_results: Results from OpenAlex provider
            unpaywall_results: Results from Unpaywall provider (optional)
            s2_results: Results from Semantic Scholar provider (optional)
            
        Returns:
            Dict containing unified search results
        """
        if "error" in openalex_results:
            return openalex_results
            
        unified_results = []
        unpaywall_map = {}
        s2_map = {}
        
        # Create maps for quick lookup
        if unpaywall_results:
            for result in unpaywall_results:
                if result.get("doi"):
                    unpaywall_map[result["doi"]] = result
                    
        if s2_results:
            for result in s2_results:
                if result.get("paperId"):
                    s2_map[result["paperId"]] = result
        
        # Transform each OpenAlex result and enrich with other sources
        for openalex_result in openalex_results.get("results", []):
            unified_result = ResultTransformer._transform_single_result(
                openalex_result, 
                unpaywall_map, 
                s2_map
            )
            unified_results.append(unified_result)
            
        return {
            "results": unified_results,
            "total": openalex_results.get("total", 0),
            "pagination": openalex_results.get("pagination", {}),
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def transform_paper_details(openalex_detail: Dict[str, Any],
                              unpaywall_result: Dict[str, Any] = None,
                              s2_detail: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Transform federated paper details to unified format.
        
        Args:
            openalex_detail: Details from OpenAlex provider
            unpaywall_result: Result from Unpaywall provider (optional)
            s2_detail: Details from Semantic Scholar provider (optional)
            
        Returns:
            Dict containing unified paper details
        """
        if "error" in openalex_detail:
            return openalex_detail
            
        # Start with OpenAlex data as base
        unified_detail = ResultTransformer._transform_openalex_paper(openalex_detail)
        
        # Enrich with Unpaywall data
        if unpaywall_result and not unified_detail.get("error"):
            unified_detail = ResultTransformer._enrich_with_unpaywall(unified_detail, unpaywall_result)
            
        # Enrich with Semantic Scholar data
        if s2_detail and not unified_detail.get("error"):
            unified_detail = ResultTransformer._enrich_with_semantic_scholar(unified_detail, s2_detail)
            
        unified_detail["timestamp"] = datetime.now().isoformat()
        return unified_detail

    @staticmethod
    def transform_references(openalex_references: Dict[str, Any],
                           s2_references: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Transform federated references to unified format.
        
        Args:
            openalex_references: References from OpenAlex provider
            s2_references: References from Semantic Scholar provider (optional)
            
        Returns:
            Dict containing unified references
        """
        if "error" in openalex_references:
            return openalex_references
            
        # Use OpenAlex references as primary source
        unified_references = openalex_references.copy()
        
        # Optionally merge with S2 references if available
        if s2_references and not s2_references.get("error"):
            # Merge logic could be implemented here if needed
            pass
            
        unified_references["timestamp"] = datetime.now().isoformat()
        return unified_references

    @staticmethod
    def transform_citation_contexts(s2_contexts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform Semantic Scholar citation contexts to unified format.
        
        Args:
            s2_contexts: Citation contexts from Semantic Scholar provider
            
        Returns:
            Dict containing unified citation contexts
        """
        if "error" in s2_contexts:
            return s2_contexts
            
        # S2 citation contexts are already in a good format, just add timestamp
        unified_contexts = s2_contexts.copy()
        unified_contexts["timestamp"] = datetime.now().isoformat()
        return unified_contexts

    @staticmethod
    def _transform_single_result(openalex_result: Dict[str, Any],
                               unpaywall_map: Dict[str, Dict[str, Any]],
                               s2_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Transform a single OpenAlex result and enrich with other sources."""
        # Start with OpenAlex data
        unified_result = ResultTransformer._transform_openalex_paper(openalex_result)
        
        # Enrich with Unpaywall data if DOI is available
        doi = unified_result.get("doi")
        if doi and doi in unpaywall_map:
            unified_result = ResultTransformer._enrich_with_unpaywall(
                unified_result, 
                unpaywall_map[doi]
            )
            
        # Enrich with Semantic Scholar data if paperId is available
        paper_id = unified_result.get("paperId")
        if paper_id and paper_id in s2_map:
            unified_result = ResultTransformer._enrich_with_semantic_scholar(
                unified_result, 
                s2_map[paper_id]
            )
            
        return unified_result

    @staticmethod
    def _transform_openalex_paper(openalex_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenAlex paper data to unified format."""
        if "error" in openalex_data:
            return openalex_data
            
        return {
            "paperId": openalex_data.get("paperId"),
            "doi": openalex_data.get("doi"),
            "title": openalex_data.get("title"),
            "abstract": openalex_data.get("abstract"),
            "year": openalex_data.get("year"),
            "citationCount": openalex_data.get("citationCount"),
            "authors": openalex_data.get("authors"),
            "openAccessPdf": openalex_data.get("openAccessPdf"),
            "venue": openalex_data.get("venue"),
            "source": "openalex"
        }

    @staticmethod
    def _enrich_with_unpaywall(base_result: Dict[str, Any], 
                              unpaywall_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich base result with Unpaywall data."""
        if "error" in unpaywall_data:
            return base_result
            
        # Only update if we have better PDF information
        if unpaywall_data.get("pdf_url") and not base_result.get("openAccessPdf"):
            base_result["openAccessPdf"] = unpaywall_data["pdf_url"]
            
        # Add OA status information
        base_result["is_oa"] = unpaywall_data.get("is_oa", False)
        base_result["oa_status"] = unpaywall_data.get("oa_status")
        
        return base_result

    @staticmethod
    def _enrich_with_semantic_scholar(base_result: Dict[str, Any], 
                                    s2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich base result with Semantic Scholar data."""
        if "error" in s2_data:
            return base_result
            
        # Add TLDR if available
        if s2_data.get("tldr") and not base_result.get("tldr"):
            base_result["tldr"] = s2_data["tldr"]
            
        # Add reference count if available
        if s2_data.get("referenceCount") and not base_result.get("referenceCount"):
            base_result["referenceCount"] = s2_data["referenceCount"]
            
        # Enhance abstract if S2 has a better one
        if s2_data.get("abstract") and not base_result.get("abstract"):
            base_result["abstract"] = s2_data["abstract"]
            
        # Add source information
        if "sources" not in base_result:
            base_result["sources"] = [base_result.get("source", "unknown")]
        if "semantic_scholar" not in base_result["sources"]:
            base_result["sources"].append("semantic_scholar")
            
        return base_result

    @staticmethod
    def ensure_s2_compatibility(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure result is compatible with original Semantic Scholar API format.
        
        Args:
            result: Unified result to make S2 compatible
            
        Returns:
            Dict in S2 compatible format
        """
        if "error" in result:
            return result
            
        # Map unified fields to S2 format
        s2_compatible = {
            "paperId": result.get("paperId"),
            "doi": result.get("doi"),
            "title": result.get("title"),
            "abstract": result.get("abstract"),
            "year": result.get("year"),
            "citationCount": result.get("citationCount"),
            "referenceCount": result.get("referenceCount"),
            "authors": result.get("authors"),
            "tldr": result.get("tldr"),
            "openAccessPdf": result.get("openAccessPdf"),
            "is_oa": result.get("is_oa"),
            "oa_status": result.get("oa_status"),
            "venue": result.get("venue")
        }
        
        # Remove None values
        s2_compatible = {k: v for k, v in s2_compatible.items() if v is not None}
        
        return s2_compatible