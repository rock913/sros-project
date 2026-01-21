"""Module for adapting arXiv search results to domain objects."""

from typing import List

import arxiv

from agent.domain.ports.paper_searcher import PaperSearcher
from agent.domain.schemas.paper import OpenAccessInfo, Paper


class ArxivAdapter(PaperSearcher):
    """Adapter for searching papers on arXiv.org using the 'arxiv' python package."""
    
    def search(self, query: str, max_results: int = 5) -> List[Paper]:
        """Search arXiv for papers and convert them to domain objects."""
        # Construct client (default settings)
        client = arxiv.Client()
        
        # Build search object
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        try:
            # Execute search
            # Note: client.results returns a generator
            for result in client.results(search):
                paper = self._to_domain(result)
                results.append(paper)
        except Exception as e:
            # Wrap or log errors as needed
            raise RuntimeError(f"Arxiv search failed: {str(e)}") from e
            
        return results

    def _to_domain(self, r: arxiv.Result) -> Paper:
        """Convert arxiv.Result to domain Paper."""
        # Handle cases where DOI might be None
        doi: str | None = r.doi if r.doi else None
        
        # Arxiv papers are generally "Open Access" in terms of visibility, 
        # but technically Green OA. We mark them as OA with URL.
        oa_info = OpenAccessInfo(
            is_oa=True,
            oa_status="green",
            oa_url=r.pdf_url
        )
        
        # Format authors
        authors = [a.name for a in r.authors]
        
        return Paper(
            doi=doi,
            title=r.title,
            authors=authors,
            publication_date=r.published.date(),
            publisher="arXiv",
            oa_info=oa_info,
            abstract=r.summary  # Map summary to abstract
        )
