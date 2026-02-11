from __future__ import annotations

from typing import Protocol, List, Dict, Any
from pydantic import BaseModel

class KnowledgeEdge(BaseModel):
    source: str
    target: str
    relationship: str  # "CITES", "REFERENCES", "RELATED_TO", "CONTRADICTS"
    confidence: float

class MemoryProtocol(Protocol):
    def store_knowledge(self, nodes: List[Dict[str, Any]], edges: List[KnowledgeEdge]) -> bool:
        """存储知识节点和关系"""
        ...
    
    def query_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """查询知识图谱"""
        ...
    
    def get_citation_map(self, section_id: str) -> List[KnowledgeEdge]:
        """获取特定章节的引用关系图"""
        ...