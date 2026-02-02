from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, ConfigDict


class SessionEvent(BaseModel):
    """Domain model representing an event in a research session timeline."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str = Field(..., description="ID of the associated research session")
    event_type: str = Field(
        ...,
        description="Type of event",
        pattern="^(search_started|paper_added|report_generated|session_completed|session_archived|error_occurred|user_intervention)$"
    )
    data: Dict[str, Any] = Field(default_factory=dict, description="Event-specific data")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        """Validate event type is one of the allowed values."""
        allowed = {
            "search_started", "paper_added", "report_generated",
            "session_completed", "session_archived", "error_occurred", "user_intervention"
        }
        if v not in allowed:
            raise ValueError(f"Event type must be one of: {', '.join(sorted(allowed))}")
        return v


class ResearchSession(BaseModel):
    """Domain model representing a research session with full historical tracking."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    topic: str = Field(..., min_length=3, max_length=200, description="Research topic")
    description: str = Field("", max_length=1000, description="Optional description of the research")
    status: str = Field(
        "active",
        pattern="^(active|completed|archived)$",
        description="Current status of the session"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships (populated by adapters, not stored directly)
    papers: List[str] = Field(
        default_factory=list,
        description="List of paper IDs associated with this session"
    )
    reports: List[str] = Field(
        default_factory=list,
        description="List of report IDs associated with this session"
    )
    events: List[SessionEvent] = Field(
        default_factory=list,
        description="Timeline of events in this session"
    )
    
    @field_validator('topic')
    @classmethod
    def validate_topic_not_empty(cls, v: str) -> str:
        """Validate topic is not empty or whitespace."""
        if not v.strip():
            raise ValueError("Topic cannot be empty or whitespace")
        return v.strip()
    
    @field_validator('status')
    @classmethod  
    def validate_status_transition(cls, v: str, info) -> str:
        """Validate status transitions (business logic)."""
        # This would be expanded with more complex business logic
        # For now, just ensure it's a valid status
        allowed = {"active", "completed", "archived"}
        if v not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")
        return v
