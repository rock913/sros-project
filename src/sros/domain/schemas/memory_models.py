from __future__ import annotations

from typing import List, Dict, Any
from pydantic import BaseModel


class KnowledgeEdge(BaseModel):
    source: str
    target: str
    relationship: str  # "CITES", "REFERENCES", "RELATED_TO", "CONTRADICTS"
    confidence: float