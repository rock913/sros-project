from __future__ import annotations

from typing import Protocol, List, Dict, Any
from pydantic import BaseModel

class Citation(BaseModel):
    citekey: str
    title: str
    authors: List[str]
    year: int
    journal: str
    url: str
    bibtex: str

class ZoteroProtocol(Protocol):
    def add_citation(self, citation: Citation) -> bool:
        """添加引用到数据库"""
        ...
    
    def get_citation(self, citekey: str) -> Citation:
        """根据 citekey 获取引用信息"""
        ...
    
    def search_citations(self, query: str) -> List[Citation]:
        """搜索引用"""
        ...