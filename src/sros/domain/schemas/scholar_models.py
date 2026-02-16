from __future__ import annotations

from typing import List, Dict, Any
from pydantic import BaseModel


class ResearchPerspective(BaseModel):
    id: str
    title: str
    description: str
    relevance_score: float
    supporting_evidence: List[str]


class SearchQuery(BaseModel):
    query: str
    max_results: int = 10
    filters: Dict[str, Any] = {}