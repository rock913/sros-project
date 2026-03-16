"""Shared Pydantic models for SROS MCP servers."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ManuscriptHeader(BaseModel):
    """Represents a header in a manuscript."""
    level: int
    title: str
    line_number: int
    path: str


class ManuscriptSection(BaseModel):
    """Represents a section in a manuscript."""
    start_line: int
    content: str


class ManuscriptStructure(BaseModel):
    """Represents the structure of a manuscript."""
    file: str
    headers: List[ManuscriptHeader]
    sections: Dict[str, ManuscriptSection]


class ResearchGap(BaseModel):
    """Represents a research gap detected in a manuscript."""
    id: Optional[int] = None
    section: str
    description: str
    priority: int = 1
    status: str = "open"
    line_number: Optional[int] = None
    type: str = "explicit"  # "explicit" or "implicit"


class Paper(BaseModel):
    """Represents a research paper."""
    id: Optional[int] = None
    title: str
    authors: Optional[str] = None
    year: Optional[int] = None
    venue: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    citation_key: Optional[str] = None


class Citation(BaseModel):
    """Represents a citation between papers."""
    id: Optional[int] = None
    citing_paper_id: int
    cited_paper_id: int
    citation_context: Optional[str] = None
    created_at: Optional[str] = None


class Relationship(BaseModel):
    """Represents a CiTO relationship between papers."""
    id: Optional[int] = None
    subject_paper_id: int
    object_paper_id: int
    relationship_type: str
    confidence_score: Optional[float] = None
    evidence: Optional[str] = None
    created_at: Optional[str] = None


class ResearchGapRecord(BaseModel):
    """Represents a research gap record in the knowledge base."""
    id: Optional[int] = None
    manuscript_section: str
    gap_description: str
    priority: int
    status: str = "open"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SearchResult(BaseModel):
    """Represents a search result from an academic database."""
    id: str
    title: str
    authors: List[str]
    year: Optional[int] = None
    venue: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    score: Optional[float] = None
    citation_count: Optional[int] = None


class BibliographyEntry(BaseModel):
    """Represents a bibliography entry."""
    citation_key: str
    formatted_entry: str
    paper_id: Optional[str] = None


class WorkspaceConfig(BaseModel):
    """Configuration for an SROS workspace."""
    workspace_path: str
    draft_file: str = "draft.md"
    graph_db_path: str = ".sros/graph.db"
    research_log_path: str = ".sros/research_log.jsonl"