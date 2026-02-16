from __future__ import annotations

from typing import Protocol, List, Dict, Any
from ..schemas import Citation


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