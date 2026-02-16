from __future__ import annotations

from typing import List
from pydantic import BaseModel


class Citation(BaseModel):
    citekey: str
    title: str
    authors: List[str]
    year: int
    journal: str
    url: str
    bibtex: str