from __future__ import annotations

from typing import Protocol, List, Dict, Any
from pydantic import BaseModel

class GapAnalysisResult(BaseModel):
    section: str
    type: str  # "Evidence Needed", "Elaboration Needed", "Citation Needed"
    confidence: float
    suggestions: List[str]

class OutlineNode(BaseModel):
    id: str
    title: str
    level: int
    content: str
    children: List['OutlineNode']

# Pydantic v2 注意：递归模型需要在模块加载后执行 `OutlineNode.model_rebuild()`
# 或使用 `from __future__ import annotations`（本示例已包含）。

class ManuscriptProtocol(Protocol):
    def find_gaps(self, file_path: str) -> List[GapAnalysisResult]:
        """基于规则识别待办项"""
        ...
    
    def get_outline_tree(self, file_path: str) -> OutlineNode:
        """返回 Markdown/AST 的树状结构"""
        ...
    
    def insert_section(self, target: str, content: str, citations: List[str]) -> bool:
        """带引用的增量写入"""
        ...
    
    def patch_draft(self, patches: List[Dict[str, Any]]) -> bool:
        """批量更新稿件内容"""
        ...