from __future__ import annotations

from typing import Protocol, List, Dict, Any
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

class ScholarProtocol(Protocol):
    def brainstorm_perspectives(self, query: str) -> List[ResearchPerspective]:
        """Co-STORM 核心，生成多维研究视角"""
        ...
    
    def find_critiques(self, paper_id: str) -> List[Dict[str, Any]]:
        """CiTO 逻辑，寻找反驳/质疑类文献"""
        ...
    
    def federated_search(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """联邦搜索多个学术数据库"""
        ...