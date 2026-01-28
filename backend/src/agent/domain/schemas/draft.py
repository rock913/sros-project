from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class DraftContext(BaseModel):
    """
    Context of the research draft for gap analysis.

    Represents the current state of a research manuscript that needs gap analysis.
    """
    content: str = Field(..., description="Full Markdown draft text")
    cursor_position: Optional[tuple[int, int]] = Field(None, description="Optional (line, col) for focus analysis")


class EvidenceGap(BaseModel):
    """
    Represents a gap in evidence found in the research draft.

    This is the core output of the gap analysis process, identifying missing
    supporting evidence that should be filled via Co-STORM retrieval.
    """
    id: UUID = Field(default_factory=uuid4)
    context_snippet: str = Field(..., max_length=500, description="Surrounding text for precise location")
    missing_information: str = Field(..., description="What evidence is missing (e.g., 'Missing empirical data on Transformer latency')")
    search_queries: List[str] = Field(..., min_items=1, description="Targeted search queries for Co-STORM")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Gap severity confidence (0-1)")

    def __init__(self, **data):
        # Ensure required fields are set on construction
        if 'search_queries' in data and not data['search_queries']:
            raise ValueError("search_queries cannot be empty")
        super().__init__(**data)

    @property
    def is_high_confidence(self) -> bool:
        """Returns True if this gap has high confidence and should be addressed."""
        return self.confidence >= 0.7


class DraftImprovement(BaseModel):
    """
    Represents an AI-suggested improvement to fill a gap in the draft.

    Contains the patch text with citations that should replace or augment
    the original content.
    """
    gap_id: UUID
    original_snippet: str = Field(..., description="The original text that had the gap")
    suggested_insertion: str = Field(..., description="Patch text with citations like [@Smith2023]")
    citations: List[str] = Field(default_factory=list, description="List of citation keys used in the patch")
    rationale: str = Field(..., description="Why this improvement was suggested")

    @property
    def has_citations(self) -> bool:
        """Returns True if this improvement includes scholarly citations."""
        return len(self.citations) > 0