from typing import List, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    research_topic: str
    search_queries: List[str]
    # The results of the search queries
    literature_abstracts: List[str]
    # The full text of the literature
    literature_full_text: List[str]
    is_sufficient: bool
    knowledge_gap: str
    report: str
    research_loop_count: int