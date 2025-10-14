from typing import List, TypedDict, Any, Annotated, Optional, Dict
import operator
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
    hitl_pending: Optional[bool]  # True when waiting for user response
    hitl_request: Optional[Dict[str, Any]]  # Current HITL request data
    hitl_response: Optional[Dict[str, Any]]  # User's response data
    hitl_approved: Optional[bool]  # Quick flag for approval status
    paper_selection_done: Optional[bool]  # Prevent repeated paper selection
    selected_papers: Optional[List[dict]]  # User-selected papers
    final_report: Optional[str]  # Final report after revisions
    stop_research: Optional[bool]  # Flag to stop research (user rejected)