from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

class DecisionCard(BaseModel):
    """
    Schema for a UI Card presented to the user for Human-in-the-Loop decision making.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: Literal["selection", "confirmation", "input", "info"] = Field(..., description="Type of interaction")
    title: str = Field(..., description="Card title")
    content: str = Field(..., description="Markdown content or description")
    options: List[Dict[str, Any]] = Field(default_factory=list, description="List of options (e.g., papers to select)")
    multi_select: bool = Field(False, description="Whether multiple options can be selected")
    timeout_seconds: Optional[int] = Field(None, description="Auto-dismiss or default action timeout")
    
class HitlEvent(BaseModel):
    """Event sent from Frontend back to Backend"""
    card_id: str
    action: str # "submit", "dismiss", "timeout"
    payload: Dict[str, Any] # e.g., {"selected_ids": ["1", "2"]}
