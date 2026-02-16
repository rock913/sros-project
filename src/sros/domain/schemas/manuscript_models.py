from __future__ import annotations

from typing import List
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
    children: List['OutlineNode'] = []

# Pydantic v2 note: Recursive models need to be rebuilt after module loading
OutlineNode.model_rebuild()