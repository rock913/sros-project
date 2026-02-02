import os
from typing import List

from dotenv import load_dotenv

# from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain.tools import tool
from langchain_community.tools import PubmedQueryRun
from pydantic import BaseModel, Field

from agent.domain.schemas.paper import Paper
from agent.infrastructure.tools.unpaywall_adapter import UnpaywallAdapter
from agent.infrastructure.tools.zotero_adapter import ZoteroAdapter

load_dotenv()

# Unpaywall configuration

class SearchQueryList(BaseModel):
    query: List[str] = Field(
        description="A list of search queries to be used for web research."
    )
    rationale: str = Field(
        description="A brief explanation of why these queries are relevant to the research topic."
    )


class Reflection(BaseModel):
    is_sufficient: bool = Field(
        description="Whether the provided summaries are sufficient to answer the user's question."
    )
    knowledge_gap: str = Field(
        description="A description of what information is missing or needs clarification."
    )
    follow_up_queries: List[str] = Field(
        description="A list of follow-up queries to address the knowledge gap."
    )

class ResearchResult(BaseModel):
    summary: str = Field(
        description="A summary of the research findings, including citations."
    )
    sources: List[str] = Field(
        description="A list of sources used for the research."
    )

@tool
def unpaywall_tool(doi: str) -> str:
    """Searches Unpywall for a given DOI to find open-access versions of a research paper."""
    try:
        adapter = UnpaywallAdapter()
        paper = adapter.fetch_by_doi(doi)
        
        if paper and paper.oa_info and paper.oa_info.is_oa:
            return f"Open access version found! Status: {paper.oa_info.oa_status}. URL: {paper.oa_info.oa_url}"
        else:
            return "No open access version found for this DOI."
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def zotero_tool(paper_info: dict) -> str:
    """Adds a paper to a Zotero library."""
    try:
        # Convert legacy dict to Domain Entity (Paper)
        # Note: Handling partial data gracefully
        import datetime
        
        # Parse date if possible
        pub_date = None
        date_str = paper_info.get("date", "")
        if date_str:
            try:
                # Simple attempt, can be expanded
                pub_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        paper = Paper(
            doi=paper_info.get("doi", "00.0000/no-doi"), # Fallback if missing, though schema requires it
            title=paper_info.get("title"),
            authors=paper_info.get("authors", []),
            publication_date=pub_date,
            publisher=paper_info.get("publication"),
            abstract=paper_info.get("abstract") # Note: Abstract not strictly in Paper schema yet, but Adapter handles it via inspection if we added it.
            # Ideally we update Paper schema to include abstract if Zotero needs it.
        )
        
        # Use simple attribute assignment for abstract if not in __init__ but supported dynamically or modify Schema later.
        # For now, let's assume Basic Paper details.
        
        adapter = ZoteroAdapter()
        item_key = adapter.save_paper(paper)
        return f"Successfully added paper '{paper.title}' to Zotero. Item Key: {item_key}"

    except Exception as e:
        return f"Failed to add paper to Zotero: {str(e)}"

@tool
def arxiv_tool(query: str) -> str:
    """Searches arXiv for papers based on a query."""
    # Note: Used to be ArxivQueryRun() directly.
    # Now we wrap our robust ArxivAdapter.
    from agent.infrastructure.tools.arxiv_adapter import ArxivAdapter
    
    try:
        adapter = ArxivAdapter()
        # Default behavior of ArxivQueryRun was roughly 3-5 results returned as text
        papers = adapter.search(query, max_results=3)
        
        # Format the output to match what LangChain tools typically return (string text)
        # or closer to what parse_scientific_papers expects.
        results = []
        for p in papers:
            # Reconstruct the string format that the 'parse_scientific_papers' utility expects
            # Default ArxivQueryRun output format: 
            # "Published: <date>\nTitle: <title>\nAuthors: <author1, ...>\nSummary: <summary>"
            
            # Handling None values safely
            pub_date = p.publication_date.isoformat() if p.publication_date else "Unknown"
            title = p.title or "Unknown Title"
            authors = ", ".join(p.authors)
            summary = p.abstract or "No abstract available"
            
            entry = f"Published: {pub_date}\nTitle: {title}\nAuthors: {authors}\nSummary: {summary}"
            results.append(entry)
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Error executing arxiv search: {e}"

# Tools
# arxiv_tool = ArxivQueryRun() # Deprecated: Replacing with our Hexagonal wrapper above
pubmed_tool = PubmedQueryRun()
# semantic_scholar_tool = SemanticScholarQueryRun()
