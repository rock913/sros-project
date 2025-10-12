"""
Database session management and CRUD operations.

Provides database connection pool and helper functions for interacting
with the session management tables.
"""

import os
from contextlib import contextmanager
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session as DBSession
from sqlalchemy.pool import NullPool

from agent.models import Base, Session, Paper, Report, SessionEvent

# Database connection URI from environment
DB_URI = os.getenv(
    "POSTGRES_URI", 
    "postgresql://postgres:postgres@langgraph-postgres:5432/postgres"
)

# Create engine with connection pooling
engine = create_engine(
    DB_URI,
    poolclass=NullPool,  # Use NullPool for serverless/Lambda environments
    echo=False,  # Set to True for SQL logging during development
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize database tables.
    
    Creates all tables defined in models.py if they don't exist.
    Safe to call multiple times (idempotent).
    """
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DB_URI}")


@contextmanager
def get_db():
    """
    Context manager for database sessions.
    
    Usage:
        with get_db() as db:
            sessions = db.query(Session).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ==================== Session CRUD Operations ====================

def create_session(
    thread_id: UUID,
    title: str,
    research_topic: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: Optional[str] = None
) -> Session:
    """
    Create a new research session.
    
    Args:
        thread_id: LangGraph thread UUID
        title: Session title
        research_topic: Initial research topic
        tags: List of tags for categorization
        notes: User notes
    
    Returns:
        Created Session object
    """
    with get_db() as db:
        session = Session(
            thread_id=thread_id,
            title=title,
            research_topic=research_topic,
            tags=tags or [],
            notes=notes
        )
        db.add(session)
        db.flush()
        db.refresh(session)
        return session


def get_session_by_id(session_id: UUID) -> Optional[Session]:
    """Get session by ID."""
    with get_db() as db:
        return db.query(Session).filter(Session.id == session_id).first()


def get_session_by_thread_id(thread_id: UUID) -> Optional[Session]:
    """Get session by LangGraph thread_id."""
    with get_db() as db:
        return db.query(Session).filter(Session.thread_id == thread_id).first()


def list_sessions(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Session]:
    """
    List sessions with optional filtering.
    
    Args:
        status: Filter by status (active, completed, archived)
        limit: Maximum number of results
        offset: Pagination offset
    
    Returns:
        List of Session objects
    """
    with get_db() as db:
        query = db.query(Session).order_by(desc(Session.created_at))
        
        if status:
            query = query.filter(Session.status == status)
        
        return query.limit(limit).offset(offset).all()


def update_session(
    session_id: UUID,
    title: Optional[str] = None,
    research_topic: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: Optional[str] = None
) -> Optional[Session]:
    """
    Update session fields.
    
    Only provided fields are updated. Returns None if session not found.
    """
    with get_db() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            return None
        
        if title is not None:
            session.title = title
        if research_topic is not None:
            session.research_topic = research_topic
        if status is not None:
            session.status = status
        if tags is not None:
            session.tags = tags
        if notes is not None:
            session.notes = notes
        
        db.flush()
        db.refresh(session)
        return session


def delete_session(session_id: UUID) -> bool:
    """
    Delete a session and all associated data (cascade).
    
    Returns:
        True if deleted, False if not found
    """
    with get_db() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            return False
        
        db.delete(session)
        return True


# ==================== Paper CRUD Operations ====================

def add_paper(
    session_id: UUID,
    title: str,
    authors: Optional[List[str]] = None,
    abstract: Optional[str] = None,
    doi: Optional[str] = None,
    arxiv_id: Optional[str] = None,
    url: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Paper:
    """Add a paper to a session."""
    with get_db() as db:
        paper = Paper(
            session_id=session_id,
            title=title,
            authors=authors or [],
            abstract=abstract,
            doi=doi,
            arxiv_id=arxiv_id,
            url=url,
            metadata=metadata or {}
        )
        db.add(paper)
        db.flush()
        db.refresh(paper)
        return paper


def list_papers(session_id: UUID) -> List[Paper]:
    """Get all papers for a session."""
    with get_db() as db:
        return db.query(Paper).filter(Paper.session_id == session_id).all()


# ==================== Report CRUD Operations ====================

def create_report(
    session_id: UUID,
    content: str,
    format: str = "markdown",
    version: int = 1,
    metadata: Optional[Dict[str, Any]] = None
) -> Report:
    """Create a report for a session."""
    with get_db() as db:
        report = Report(
            session_id=session_id,
            content=content,
            format=format,
            version=version,
            metadata=metadata or {}
        )
        db.add(report)
        db.flush()
        db.refresh(report)
        return report


def list_reports(session_id: UUID) -> List[Report]:
    """Get all reports for a session."""
    with get_db() as db:
        return db.query(Report).filter(Report.session_id == session_id).order_by(desc(Report.created_at)).all()


# ==================== Event Logging ====================

def log_event(
    session_id: UUID,
    event_type: str,
    event_data: Optional[Dict[str, Any]] = None
) -> SessionEvent:
    """Log an event for a session."""
    with get_db() as db:
        event = SessionEvent(
            session_id=session_id,
            event_type=event_type,
            event_data=event_data or {}
        )
        db.add(event)
        db.flush()
        db.refresh(event)
        return event


def list_events(
    session_id: UUID,
    event_type: Optional[str] = None,
    limit: int = 100
) -> List[SessionEvent]:
    """Get events for a session, optionally filtered by type."""
    with get_db() as db:
        query = db.query(SessionEvent).filter(SessionEvent.session_id == session_id).order_by(desc(SessionEvent.created_at))
        
        if event_type:
            query = query.filter(SessionEvent.event_type == event_type)
        
        return query.limit(limit).all()
