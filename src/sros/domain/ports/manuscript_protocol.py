from __future__ import annotations

from typing import Protocol, List, Dict, Any, Optional
from ..schemas import GapAnalysisResult, OutlineNode


class ManuscriptProtocol(Protocol):
    def find_gaps(self, file_path: str) -> List[GapAnalysisResult]:
        """基于规则识别待办项"""
        ...
    
    def get_outline_tree(self, file_path: str) -> OutlineNode:
        """返回 Markdown/AST 的树状结构"""
        ...

    def get_file_sha256(self, file_path: str = "draft.md") -> str:
        """Return sha256 of the current file contents."""
        ...
    
    def insert_section(
        self,
        target: str,
        content: str,
        citations: List[str],
        file_path: str = "draft.md",
        expected_sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        """带引用的增量写入（结构化返回，支持乐观并发）"""
        ...
    
    def patch_draft(
        self,
        patches: List[Dict[str, Any]],
        file_path: str = "draft.md",
        expected_sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        """批量更新稿件内容（结构化返回，支持乐观并发）"""
        ...