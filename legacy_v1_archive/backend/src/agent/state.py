import operator
from typing import Annotated, Any, Dict, List, TypedDict

from langgraph.graph import add_messages


class AgentState(TypedDict, total=False):
    # Required fields
    messages: Annotated[list, add_messages]
    research_topic: str
    search_queries: List[str]
    # The results of the search queries
    literature_abstracts: Annotated[List[Any], operator.add]
    # The full text of the literature
    literature_full_text: List[str]
    # Papers queued (DOI + URL) for ingestion after resource management step
    papers_for_ingestion: List[dict]
    is_sufficient: bool
    knowledge_gap: str
    research_loop_count: int
    report: str
    # Session management fields (Phase 3.5.2) - Optional
    session_id: str  # UUID of the Session record in database
    thread_id: str   # LangGraph thread_id for checkpointer integration
    
    # HITL (Human-in-the-Loop) fields (Phase 3.6) - Optional
    hitl_pending: bool | None  # True when waiting for user response
    hitl_request: Dict[str, Any] | None  # Current HITL request data
    hitl_response: Dict[str, Any] | None  # User's response data
    hitl_approved: bool | None  # Quick flag for approval status
    paper_selection_done: bool | None  # Prevent repeated paper selection
    selected_papers: List[dict] | None  # User-selected papers
    final_report: str | None  # Final report after revisions
    stop_research: bool | None  # Flag to stop research (user rejected)