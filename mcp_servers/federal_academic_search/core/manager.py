"""
Academic Search Manager for Federal Academic Search MCP Server
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from ..providers import OpenAlexProvider, UnpaywallProvider, SemanticScholarProvider
from ..transformers import ResultTransformer
from ..cache import CacheManager
from ..config import FederalAcademicSearchConfig

logger = logging.getLogger(__name__)


class AcademicSearchManager:
    """Main manager coordinating all academic search providers in federal architecture."""

    def __init__(self, config: FederalAcademicSearchConfig = None):
        """
        Initialize the academic search manager.
        
        Args:
            config: Configuration object
        """
        self.config = config or FederalAcademicSearchConfig()
        self.cache_manager = CacheManager(
            db_path=self.config.cache_db_path,
            ttl=self.config.cache_ttl
        )
        self.transformer = ResultTransformer()
        
        # Initialize providers
        self.openalex_provider = OpenAlexProvider(self.config)
        self.unpaywall_provider = UnpaywallProvider(self.config)
        self.s2_provider = SemanticScholarProvider(self.config)
        
        # Rate limiting and circuit breaker state
        self._s2_last_error_time = None
        self._s2_error_count = 0
        self._s2_circuit_open = False
        self._s2_circuit_timeout = timedelta(minutes=5)  # 5 minute timeout

    async def search_papers(self, query: str, limit: int = 10, 
                          enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for academic papers using federal architecture.
        
        Args:
            query: Search query
            limit: Maximum number of results
            enrich: Whether to enrich results with S2 and Unpaywall data
            use_cache: Whether to use cache
            
        Returns:
            Dict containing search results
        """
        cache_key = f"search:{query}:limit:{limit}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for search: {query}")
                return cached_result
        
        try:
            # Primary search with OpenAlex
            async with self.openalex_provider as openalex:
                openalex_results = await openalex.search_papers(query, limit)
            
            if "error" in openalex_results:
                return openalex_results
                
            # Early return if not enriching
            if not enrich:
                result = self.transformer.transform_search_results(openalex_results)
                if use_cache and self.config.cache_enabled:
                    self.cache_manager.set(cache_key, result)
                return result
            
            # Concurrent enrichment with Unpaywall and Semantic Scholar
            enriched_result = await self._enrich_search_results(openalex_results)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, enriched_result)
                
            return enriched_result
            
        except Exception as e:
            logger.error(f"Error in search_papers: {str(e)}")
            return {"error": str(e)}

    async def get_paper_details(self, paper_id: str, 
                              enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper.
        
        Args:
            paper_id: Paper ID or DOI
            enrich: Whether to enrich with S2 and Unpaywall data
            use_cache: Whether to use cache
            
        Returns:
            Dict containing paper details
        """
        cache_key = f"details:{paper_id}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for paper details: {paper_id}")
                return cached_result
        
        try:
            # Get base details from OpenAlex
            async with self.openalex_provider as openalex:
                openalex_detail = await openalex.get_paper_details(paper_id)
            
            if "error" in openalex_detail:
                return openalex_detail
                
            # Early return if not enriching
            if not enrich:
                result = self.transformer.transform_paper_details(openalex_detail)
                if use_cache and self.config.cache_enabled:
                    self.cache_manager.set(cache_key, result)
                return result
            
            # Concurrent enrichment
            enriched_result = await self._enrich_paper_details(paper_id, openalex_detail)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, enriched_result)
                
            return enriched_result
            
        except Exception as e:
            logger.error(f"Error in get_paper_details: {str(e)}")
            return {"error": str(e)}

    async def get_paper_references(self, paper_id: str, limit: int = 10, 
                                 use_cache: bool = True) -> Dict[str, Any]:
        """
        Get references for a paper.
        
        Args:
            paper_id: Paper ID
            limit: Maximum number of references
            use_cache: Whether to use cache
            
        Returns:
            Dict containing references
        """
        cache_key = f"references:{paper_id}:limit:{limit}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for paper references: {paper_id}")
                return cached_result
        
        try:
            # Get references from OpenAlex
            async with self.openalex_provider as openalex:
                references = await openalex.get_paper_references(paper_id, limit)
            
            if "error" in references:
                return references
                
            # Transform result
            result = self.transformer.transform_references(references)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, result)
                
            return result
            
        except Exception as e:
            logger.error(f"Error in get_paper_references: {str(e)}")
            return {"error": str(e)}

    async def get_citation_context(self, paper_id: str, limit: int = 10, 
                                 use_cache: bool = True) -> Dict[str, Any]:
        """
        Get citation contexts for a paper from Semantic Scholar.
        
        Args:
            paper_id: Paper ID
            limit: Maximum number of contexts
            use_cache: Whether to use cache
            
        Returns:
            Dict containing citation contexts
        """
        # Check if S2 circuit breaker is open
        if self._is_s2_circuit_open():
            logger.warning("Semantic Scholar circuit breaker is open, skipping citation context")
            return {"error": "Semantic Scholar service temporarily unavailable due to rate limiting"}
        
        cache_key = f"citation_context:{paper_id}:limit:{limit}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for citation context: {paper_id}")
                return cached_result
        
        try:
            # Get citation contexts from Semantic Scholar
            async with self.s2_provider as s2:
                contexts = await s2.get_citation_context(paper_id, limit)
            
            # Check for rate limiting errors
            if "error" in contexts:
                self._handle_s2_error(contexts)
                return contexts
                
            # Transform result
            result = self.transformer.transform_citation_contexts(contexts)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, result)
                
            return result
            
        except Exception as e:
            logger.error(f"Error in get_citation_context: {str(e)}")
            error_result = {"error": str(e)}
            self._handle_s2_error(error_result)
            return error_result

    async def download_pdf(self, paper_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get PDF URL for a paper using Unpaywall.
        
        Args:
            paper_id: Paper ID or DOI
            use_cache: Whether to use cache
            
        Returns:
            Dict containing PDF URL
        """
        # First get paper details to extract DOI
        paper_details = await self.get_paper_details(paper_id, enrich=False, use_cache=use_cache)
        
        if "error" in paper_details:
            return paper_details
            
        doi = paper_details.get("doi")
        if not doi:
            return {"error": "No DOI available for this paper"}
        
        cache_key = f"pdf:{doi}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for PDF URL: {doi}")
                return cached_result
        
        try:
            # Get PDF URL from Unpaywall
            async with self.unpaywall_provider as unpaywall:
                pdf_result = await unpaywall.get_pdf_url(doi)
            
            if "error" in pdf_result:
                return pdf_result
                
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, pdf_result)
                
            return pdf_result
            
        except Exception as e:
            logger.error(f"Error in download_pdf: {str(e)}")
            return {"error": str(e)}

    async def search_by_author(self, author_name: str, limit: int = 10, 
                             enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for papers by author name.
        
        Args:
            author_name: Author name
            limit: Maximum number of results
            enrich: Whether to enrich results
            use_cache: Whether to use cache
            
        Returns:
            Dict containing search results
        """
        cache_key = f"author:{author_name}:limit:{limit}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for author search: {author_name}")
                return cached_result
        
        try:
            # Search with OpenAlex
            async with self.openalex_provider as openalex:
                openalex_results = await openalex.search_by_author(author_name, limit)
            
            if "error" in openalex_results:
                return openalex_results
                
            # Early return if not enriching
            if not enrich:
                result = self.transformer.transform_search_results(openalex_results)
                if use_cache and self.config.cache_enabled:
                    self.cache_manager.set(cache_key, result)
                return result
            
            # Concurrent enrichment
            enriched_result = await self._enrich_search_results(openalex_results)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, enriched_result)
                
            return enriched_result
            
        except Exception as e:
            logger.error(f"Error in search_by_author: {str(e)}")
            return {"error": str(e)}

    async def search_by_title(self, title: str, limit: int = 10, 
                            enrich: bool = True, use_cache: bool = True) -> Dict[str, Any]:
        """
        Search for papers by title.
        
        Args:
            title: Paper title
            limit: Maximum number of results
            enrich: Whether to enrich results
            use_cache: Whether to use cache
            
        Returns:
            Dict containing search results
        """
        cache_key = f"title:{title}:limit:{limit}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for title search: {title}")
                return cached_result
        
        try:
            # Search with OpenAlex
            async with self.openalex_provider as openalex:
                openalex_results = await openalex.search_by_title(title, limit)
            
            if "error" in openalex_results:
                return openalex_results
                
            # Early return if not enriching
            if not enrich:
                result = self.transformer.transform_search_results(openalex_results)
                if use_cache and self.config.cache_enabled:
                    self.cache_manager.set(cache_key, result)
                return result
            
            # Concurrent enrichment
            enriched_result = await self._enrich_search_results(openalex_results)
            
            # Cache the result
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, enriched_result)
                
            return enriched_result
            
        except Exception as e:
            logger.error(f"Error in search_by_title: {str(e)}")
            return {"error": str(e)}

    async def get_tldr(self, paper_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get TLDR summary for a paper from Semantic Scholar.
        
        Args:
            paper_id: Paper ID
            use_cache: Whether to use cache
            
        Returns:
            Dict containing TLDR summary
        """
        # Check if S2 circuit breaker is open
        if self._is_s2_circuit_open():
            logger.warning("Semantic Scholar circuit breaker is open, skipping TLDR")
            return {"error": "Semantic Scholar service temporarily unavailable due to rate limiting"}
        
        cache_key = f"tldr:{paper_id}"
        
        # Try cache first
        if use_cache and self.config.cache_enabled:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for TLDR: {paper_id}")
                return cached_result
        
        try:
            # Get TLDR from Semantic Scholar
            async with self.s2_provider as s2:
                tldr_result = await s2.get_tldr(paper_id)
            
            # Check for rate limiting errors
            if "error" in tldr_result:
                self._handle_s2_error(tldr_result)
                return tldr_result
                
            # Cache the result (especially valuable for TLDR)
            if use_cache and self.config.cache_enabled:
                self.cache_manager.set(cache_key, tldr_result)
                
            return tldr_result
            
        except Exception as e:
            logger.error(f"Error in get_tldr: {str(e)}")
            error_result = {"error": str(e)}
            self._handle_s2_error(error_result)
            return error_result

    async def _enrich_search_results(self, openalex_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich search results with Unpaywall and Semantic Scholar data.
        
        Args:
            openalex_results: Results from OpenAlex
            
        Returns:
            Enriched results
        """
        if "error" in openalex_results:
            return openalex_results
            
        # Extract DOIs and paper IDs for batch processing
        dois = []
        paper_ids = []
        
        for result in openalex_results.get("results", []):
            if result.get("doi"):
                dois.append(result["doi"])
            if result.get("paperId"):
                paper_ids.append(result["paperId"])
        
        # Concurrent tasks for enrichment
        tasks = []
        
        # Get PDF URLs from Unpaywall
        if dois:
            unpaywall_tasks = [
                self._get_unpaywall_pdf(doi) for doi in dois[:10]  # Limit concurrent requests
            ]
            tasks.append(asyncio.gather(*unpaywall_tasks, return_exceptions=True))
        
        # Get TLDRs from Semantic Scholar
        if paper_ids and not self._is_s2_circuit_open():
            s2_tasks = [
                self._get_s2_tldr(paper_id) for paper_id in paper_ids[:10]  # Limit concurrent requests
            ]
            tasks.append(asyncio.gather(*s2_tasks, return_exceptions=True))
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True) if tasks else [[], []]
        
        # Process results
        unpaywall_results = results[0] if len(results) > 0 else []
        s2_results = results[1] if len(results) > 1 else []
        
        # Filter out exceptions
        unpaywall_results = [r for r in unpaywall_results if not isinstance(r, Exception)]
        s2_results = [r for r in s2_results if not isinstance(r, Exception)]
        
        # Transform final result
        return self.transformer.transform_search_results(
            openalex_results, 
            unpaywall_results, 
            s2_results
        )

    async def _enrich_paper_details(self, paper_id: str, openalex_detail: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich paper details with Unpaywall and Semantic Scholar data.
        
        Args:
            paper_id: Paper ID
            openalex_detail: Details from OpenAlex
            
        Returns:
            Enriched details
        """
        if "error" in openalex_detail:
            return openalex_detail
            
        # Concurrent tasks for enrichment
        tasks = []
        
        # Get PDF URL from Unpaywall
        doi = openalex_detail.get("doi")
        if doi:
            tasks.append(self._get_unpaywall_pdf(doi))
        
        # Get TLDR from Semantic Scholar (if circuit breaker is not open)
        if not self._is_s2_circuit_open():
            tasks.append(self._get_s2_tldr(paper_id))
        
        # Execute tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True) if tasks else []
        
        # Process results
        unpaywall_result = None
        s2_result = None
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue
            if doi and i == 0:  # First task is Unpaywall
                unpaywall_result = result
            else:  # Second task is S2 (or first if no DOI)
                s2_result = result
        
        # Transform final result
        return self.transformer.transform_paper_details(
            openalex_detail,
            unpaywall_result,
            s2_result
        )

    async def _get_unpaywall_pdf(self, doi: str) -> Dict[str, Any]:
        """Get PDF URL from Unpaywall."""
        try:
            async with self.unpaywall_provider as unpaywall:
                return await unpaywall.get_pdf_url(doi)
        except Exception as e:
            logger.warning(f"Failed to get PDF from Unpaywall for DOI {doi}: {str(e)}")
            return {"error": str(e)}

    async def _get_s2_tldr(self, paper_id: str) -> Dict[str, Any]:
        """Get TLDR from Semantic Scholar."""
        try:
            async with self.s2_provider as s2:
                return await s2.get_tldr(paper_id)
        except Exception as e:
            logger.warning(f"Failed to get TLDR from Semantic Scholar for paper {paper_id}: {str(e)}")
            self._handle_s2_error({"error": str(e)})
            return {"error": str(e)}

    def _is_s2_circuit_open(self) -> bool:
        """Check if Semantic Scholar circuit breaker is open."""
        if not self._s2_circuit_open:
            return False
            
        # Check if timeout has passed
        if self._s2_last_error_time:
            elapsed = datetime.now() - self._s2_last_error_time
            if elapsed > self._s2_circuit_timeout:
                logger.info("Semantic Scholar circuit breaker timeout passed, closing circuit")
                self._s2_circuit_open = False
                self._s2_error_count = 0
                return False
                
        return True

    def _handle_s2_error(self, error_result: Dict[str, Any]):
        """Handle Semantic Scholar errors and manage circuit breaker."""
        self._s2_error_count += 1
        self._s2_last_error_time = datetime.now()
        
        # Check for rate limiting
        error_msg = str(error_result.get("error", "")).lower()
        if "429" in error_msg or "rate limit" in error_msg or "too many requests" in error_msg:
            logger.warning("Semantic Scholar rate limit detected")
            self._s2_circuit_open = True
        elif self._s2_error_count >= 3:  # Open circuit after 3 consecutive errors
            logger.warning("Opening Semantic Scholar circuit breaker after 3 consecutive errors")
            self._s2_circuit_open = True

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache_manager.get_stats()

    async def clear_cache(self) -> Dict[str, Any]:
        """Clear all cache entries."""
        count = self.cache_manager.clear_all()
        return {
            "message": f"Cleared {count} cache entries",
            "entries_cleared": count
        }