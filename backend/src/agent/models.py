"""
SQLAlchemy models for session management and data persistence.

This module defines the database schema for:
- Research sessions
- Collected papers
- Generated reports
- Session event logs

All tables use UUID primary keys and integrate with LangGraph's checkpointer
via the thread_id foreign key relationship.
"""

from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

from sqlalchemy import (
    Column, String, Text, DateTime, Integer, ARRAY, 
    ForeignKey, Index, func, Boolean
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Session(Base):
    """
    Research session metadata.
    
    Each session represents a distinct research task and is linked to a
    LangGraph thread via thread_id.
    """
    __tablename__ = 'sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    thread_id = Column(
        UUID(as_uuid=True), 
        unique=True, 
        nullable=False,
        comment="Foreign key to LangGraph checkpoints.thread_id"
    )
    title = Column(String(500), nullable=False)
    research_topic = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True, comment="Timestamp when session completed")
    status = Column(
        String(50), 
        default='active',
        comment="Session status: active, completed, archived"
    )
    tags = Column(ARRAY(String), default=list)
    notes = Column(Text, nullable=True)
    
    # Relationships
    papers = relationship("Paper", back_populates="session", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="session", cascade="all, delete-orphan")
    events = relationship("SessionEvent", back_populates="session", cascade="all, delete-orphan")
    hitl_decisions = relationship("HITLDecision", back_populates="session", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_sessions_thread_id', 'thread_id'),
        Index('idx_sessions_status', 'status'),
        Index('idx_sessions_created_at', 'created_at'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'thread_id': str(self.thread_id),
            'title': self.title,
            'research_topic': self.research_topic,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status,
            'tags': self.tags or [],
            'notes': self.notes,
            'paper_count': len(self.papers) if hasattr(self, 'papers') else 0,
            'report_count': len(self.reports) if hasattr(self, 'reports') else 0,
        }


class Paper(Base):
    """
    Collected research paper metadata.
    
    Papers are associated with a session and stored for later reference.
    """
    __tablename__ = 'papers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(1000), nullable=False)
    authors = Column(ARRAY(String), default=list)
    abstract = Column(Text, nullable=True)
    doi = Column(String(255), nullable=True)
    arxiv_id = Column(String(50), nullable=True)
    url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    extra_metadata = Column(JSONB, default=dict, comment="Additional paper metadata")
    
    # Relationships
    session = relationship("Session", back_populates="papers")
    
    __table_args__ = (
        Index('idx_papers_session_id', 'session_id'),
        Index('idx_papers_doi', 'doi'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'session_id': str(self.session_id),
            'title': self.title,
            'authors': self.authors or [],
            'abstract': self.abstract,
            'doi': self.doi,
            'arxiv_id': self.arxiv_id,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'extra_metadata': self.extra_metadata or {},
        }


class Report(Base):
    """
    Generated research reports.
    
    Reports are versioned outputs of the research process, stored in different formats.
    """
    __tablename__ = 'reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    format = Column(String(50), default='markdown', comment="Report format: markdown, pdf, html")
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    extra_metadata = Column(JSONB, default=dict, comment="Report generation metadata")
    
    # Relationships
    session = relationship("Session", back_populates="reports")
    
    __table_args__ = (
        Index('idx_reports_session_id', 'session_id'),
        Index('idx_reports_created_at', 'created_at'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'session_id': str(self.session_id),
            'content': self.content,
            'format': self.format,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'extra_metadata': self.extra_metadata or {},
        }


class SessionEvent(Base):
    """
    Session event log for tracking research progress.
    
    Events capture key milestones like query generation, paper retrieval, etc.
    """
    __tablename__ = 'session_events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False)
    event_type = Column(
        String(100), 
        nullable=False,
        comment="Event type: query_generated, paper_retrieved, report_created, etc."
    )
    event_data = Column(JSONB, default=dict, comment="Event payload")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    session = relationship("Session", back_populates="events")
    
    __table_args__ = (
        Index('idx_events_session_id', 'session_id'),
        Index('idx_events_type', 'event_type'),
        Index('idx_events_created_at', 'created_at'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'session_id': str(self.session_id),
            'event_type': self.event_type,
            'event_data': self.event_data or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class HITLDecision(Base):
    """
    Human-in-the-Loop (HITL) Decision Record
    
    Phase 3.6: Stores user decisions made during AI research sessions
    at critical intervention points.
    """
    __tablename__ = "hitl_decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    request_id = Column(
        String(255), 
        nullable=False, 
        unique=True,
        comment="Unique identifier for this HITL request"
    )
    decision_type = Column(
        String(50), 
        nullable=False,
        comment="Type: query_approval, paper_selection, report_revision"
    )
    prompt = Column(Text, nullable=False, comment="Question/prompt shown to user")
    options = Column(JSONB, nullable=False, comment="Available options array")
    user_decision = Column(String(255), nullable=True, comment="User's chosen option")
    modified_data = Column(JSONB, nullable=True, comment="User-modified data if applicable")
    context = Column(JSONB, nullable=True, comment="Additional context for display")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    responded_at = Column(DateTime, nullable=True, comment="When user responded")
    timeout_seconds = Column(Integer, default=300, comment="Timeout in seconds (default 5 min)")
    
    # Relationships
    session = relationship("Session", back_populates="hitl_decisions")
    
    __table_args__ = (
        Index('idx_hitl_session_id', 'session_id'),
        Index('idx_hitl_request_id', 'request_id'),
        Index('idx_hitl_decision_type', 'decision_type'),
        Index('idx_hitl_created_at', 'created_at'),
    )
    
    @property
    def is_pending(self) -> bool:
        """Check if this decision is still waiting for user response"""
        return self.user_decision is None and self.responded_at is None
    
    @property
    def is_timeout(self) -> bool:
        """Check if this decision has timed out"""
        if self.is_pending and self.timeout_seconds:
            from datetime import datetime
            elapsed = (datetime.utcnow() - self.created_at).total_seconds()
            return elapsed > self.timeout_seconds
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'session_id': str(self.session_id),
            'request_id': self.request_id,
            'decision_type': self.decision_type,
            'prompt': self.prompt,
            'options': self.options or [],
            'user_decision': self.user_decision,
            'modified_data': self.modified_data,
            'context': self.context,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'timeout_seconds': self.timeout_seconds,
            'is_pending': self.is_pending,
            'is_timeout': self.is_timeout,
        }
