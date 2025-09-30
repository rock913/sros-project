from typing import List, TypedDict, Any, Annotated
import operator
from langgraph.graph import add_messages

class AgentState(TypedDict):
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