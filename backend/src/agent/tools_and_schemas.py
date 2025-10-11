import os
from typing import List
from pydantic import BaseModel, Field
from langchain_community.tools import ArxivQueryRun, PubmedQueryRun
# from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain.tools import tool
from unpywall import Unpywall
from pyzotero import zotero
from dotenv import load_dotenv

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

# Tools
arxiv_tool = ArxivQueryRun()
pubmed_tool = PubmedQueryRun()
# semantic_scholar_tool = SemanticScholarQueryRun()

@tool
def unpaywall_tool(doi: str) -> str:
    """Searches Unpywall for a given DOI to find open-access versions of a research paper."""
    try:
        paper = Unpywall.doi(dois=[doi])
        if not paper.empty and paper['is_oa'].iloc[0]:
            oa_status = paper['oa_status'].iloc[0]
            best_oa_url = paper['best_oa_location.url'].iloc[0]
            return f"Open access version found! Status: {oa_status}. URL: {best_oa_url}"
        else:
            return "No open access version found for this DOI."
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def zotero_tool(paper_info: dict) -> str:
    """Adds a paper to a Zotero library."""
    try:
        zot = zotero.Zotero(os.getenv("ZOTERO_LIBRARY_ID"), os.getenv("ZOTERO_LIBRARY_TYPE"), os.getenv("ZOTERO_API_KEY"))
        # Create a new item
        template = zot.item_template('journalArticle')
        template['title'] = paper_info.get("title", "")
        template['creators'] = paper_info.get("authors", [])
        template['abstractNote'] = paper_info.get("abstract", "")
        template['publicationTitle'] = paper_info.get("publication", "")
        template['volume'] = paper_info.get("volume", "")
        template['issue'] = paper_info.get("issue", "")
        template['pages'] = paper_info.get("pages", "")
        template['date'] = paper_info.get("date", "")
        template['DOI'] = paper_info.get("doi", "")
        
        resp = zot.create_items([template])
        if resp['success']:
            return f"Successfully added paper '{template['title']}' to Zotero."
        else:
            return f"Failed to add paper to Zotero: {resp}"
    except Exception as e:
        return f"An error occurred: {e}"