"""Human-in-the-Loop (HITL) Decision Models

Phase 3.6: HITL & Real-time Collaboration
Author: Development Team
Date: 2025-10-14
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .base import Base


class HITLDecision(Base):
    """Human-in-the-Loop Decision Record
    
    Stores user decisions made during AI research sessions
    at critical intervention points.
    """
    __tablename__ = "hitl_decisions"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to Session
    session_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Request Identification
    request_id = Column(String(255), nullable=False, unique=True, index=True)
    
    # Decision Type
    # Possible values: 'query_approval', 'paper_selection', 'report_revision'
    decision_type = Column(String(50), nullable=False, index=True)
    
    # User Prompt
    prompt = Column(Text, nullable=False)
    
    # Available Options (JSON array)
    # Example: ["approve", "reject", "modify"]
    options = Column(JSONB, nullable=False)
    
    # User's Decision
    user_decision = Column(String(255), nullable=True)
    
    # Modified Data (if user chose to modify)
    # Example: {"modified_query": "new query text", "selected_papers": [...]}
    modified_data = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    responded_at = Column(DateTime, nullable=True)
    
    # Timeout Configuration
    timeout_seconds = Column(Integer, nullable=True, default=300)  # 5 minutes default
    
    # Context Data (for display purposes)
    # Example: {"current_query": "...", "paper_count": 10}
    context = Column(JSONB, nullable=True)
    
    # Relationship
    session = relationship("Session", back_populates="hitl_decisions")
    
    def __repr__(self):
        return (
            f"<HITLDecision(id={self.id}, "
            f"session_id={self.session_id}, "
            f"type={self.decision_type}, "
            f"decision={self.user_decision})>"
        )
    
    @property
    def is_pending(self) -> bool:
        """Check if this decision is still waiting for user response"""
        return self.user_decision is None and self.responded_at is None
    
    @property
    def is_timeout(self) -> bool:
        """Check if this decision has timed out"""
        if self.is_pending and self.timeout_seconds:
            elapsed = (datetime.utcnow() - self.created_at).total_seconds()
            return elapsed > self.timeout_seconds
        return False
