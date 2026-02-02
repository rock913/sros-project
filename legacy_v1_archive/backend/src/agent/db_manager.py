"""Database session management and CRUD operations.

Provides database connection pool and helper functions for interacting
with the session management tables.
"""

import os
from contextlib import contextmanager
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from agent.models import Base, Paper, Report, Session, SessionEvent

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
    """Initialize database tables.
    
    Creates all tables defined in models.py if they don't exist.
    Safe to call multiple times (idempotent).
    """
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DB_URI}")


@contextmanager
def get_db():
    """Context manager for database sessions.
    
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
    research_topic: str | None = None,
    status: str = "pending",  # Added missing parameter
    tags: List[str] | None = None,
    notes: str | None = None
) -> Dict[str, Any]:
    """Create a new research session.
    
    Args:
        thread_id: LangGraph thread UUID
        title: Session title
        research_topic: Initial research topic
        status: Session status (pending, active, completed, failed)
        tags: List of tags for categorization
        notes: User notes
    
    Returns:
        Created Session dict
    """
    with get_db() as db:
        session = Session(
            thread_id=thread_id,
            title=title,
            research_topic=research_topic,
            status=status,  # Added missing field
            tags=tags or [],
            notes=notes
        )
        db.add(session)
        db.flush()
        db.refresh(session)
        return session.to_dict()


def get_session_by_id(session_id: UUID) -> Dict[str, Any] | None:
    """Get session by ID."""
    with get_db() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        return session.to_dict() if session else None


def get_session_by_thread_id(thread_id: UUID) -> Dict[str, Any] | None:
    """Get session by LangGraph thread_id."""
    with get_db() as db:
        session = db.query(Session).filter(Session.thread_id == thread_id).first()
        return session.to_dict() if session else None


def list_sessions(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """List sessions with optional filtering.
    
    Args:
        status: Filter by status (active, completed, archived)
        limit: Maximum number of results
        offset: Pagination offset
    
    Returns:
        List of Session dicts
    """
    with get_db() as db:
        query = db.query(Session).order_by(desc(Session.created_at))
        
        if status:
            query = query.filter(Session.status == status)
        
        sessions = query.limit(limit).offset(offset).all()
        return [s.to_dict() for s in sessions]


def update_session(
    session_id: UUID,
    title: str | None = None,
    research_topic: str | None = None,
    status: str | None = None,
    tags: List[str] | None = None,
    notes: str | None = None
) -> Dict[str, Any] | None:
    """Update session fields.
    
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
        return session.to_dict()


def delete_session(session_id: UUID) -> bool:
    """Delete a session and all associated data (cascade).
    
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
    authors: List[str] | None = None,
    abstract: str | None = None,
    doi: str | None = None,
    arxiv_id: str | None = None,
    url: str | None = None,
    extra_metadata: Dict[str, Any] | None = None
) -> Dict[str, Any]:
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
            extra_metadata=extra_metadata or {}
        )
        db.add(paper)
        db.flush()
        db.refresh(paper)
        return paper.to_dict()


def list_papers(session_id: UUID) -> List[Dict[str, Any]]:
    """Get all papers for a session."""
    with get_db() as db:
        papers = db.query(Paper).filter(Paper.session_id == session_id).all()
        return [p.to_dict() for p in papers]


def get_all_papers(
    session_id: UUID | None = None,
    source: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    keyword: str | None = None,
    limit: int = 100,
    offset: int = 0
) -> tuple[List[Dict[str, Any]], int]:
    """Get all papers with advanced filtering.
    
    Args:
        session_id: Filter by session UUID
        source: Filter by data source (extracted from extra_metadata)
        start_date: Filter papers collected after this timestamp
        end_date: Filter papers collected before this timestamp
        keyword: Full-text search in titles and abstracts
        limit: Maximum number of results
        offset: Pagination offset
    
    Returns:
        Tuple of (list of Paper dicts, total count)
    """
    with get_db() as db:
        query = db.query(Paper).order_by(desc(Paper.created_at))
        
        # Apply filters
        if session_id:
            query = query.filter(Paper.session_id == session_id)
        
        if source:
            # Source is stored in extra_metadata
            query = query.filter(Paper.extra_metadata['source'].astext == source)
        
        if start_date:
            query = query.filter(Paper.created_at >= start_date)
        
        if end_date:
            query = query.filter(Paper.created_at <= end_date)
        
        if keyword:
            # Full-text search in title and abstract
            from sqlalchemy import func, or_
            search_term = f"%{keyword}%"
            query = query.filter(
                or_(
                    func.lower(Paper.title).like(func.lower(search_term)),
                    func.lower(Paper.abstract).like(func.lower(search_term))
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        papers = query.limit(limit).offset(offset).all()
        
        return [p.to_dict() for p in papers], total


def get_paper_by_id(paper_id: UUID) -> Dict[str, Any] | None:
    """Get a specific paper by ID."""
    with get_db() as db:
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        return paper.to_dict() if paper else None


# ==================== Report CRUD Operations ====================

def create_report(
    session_id: UUID,
    content: str,
    format: str = "markdown",
    version: int = 1,
    extra_metadata: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """Create a report for a session."""
    with get_db() as db:
        report = Report(
            session_id=session_id,
            content=content,
            format=format,
            version=version,
            extra_metadata=extra_metadata or {}
        )
        db.add(report)
        db.flush()
        db.refresh(report)
        return report.to_dict()


def list_reports(session_id: UUID) -> List[Dict[str, Any]]:
    """Get all reports for a session."""
    with get_db() as db:
        reports = db.query(Report).filter(Report.session_id == session_id).order_by(desc(Report.created_at)).all()
        return [r.to_dict() for r in reports]


def get_all_reports(
    session_id: UUID | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 50,
    offset: int = 0
) -> tuple[List[Dict[str, Any]], int]:
    """Get all reports with filtering.
    
    Args:
        session_id: Filter by session UUID
        start_date: Filter reports created after this timestamp
        end_date: Filter reports created before this timestamp
        limit: Maximum number of results
        offset: Pagination offset
    
    Returns:
        Tuple of (list of Report dicts, total count)
    """
    with get_db() as db:
        query = db.query(Report).order_by(desc(Report.created_at))
        
        # Apply filters
        if session_id:
            query = query.filter(Report.session_id == session_id)
        
        if start_date:
            query = query.filter(Report.created_at >= start_date)
        
        if end_date:
            query = query.filter(Report.created_at <= end_date)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        reports = query.limit(limit).offset(offset).all()
        
        return [r.to_dict() for r in reports], total


def get_report_by_id(report_id: UUID) -> Dict[str, Any] | None:
    """Get a specific report by ID."""
    with get_db() as db:
        report = db.query(Report).filter(Report.id == report_id).first()
        return report.to_dict() if report else None


def get_latest_report(session_id: UUID) -> Dict[str, Any] | None:
    """Get the most recent report for a session."""
    with get_db() as db:
        report = (
            db.query(Report)
            .filter(Report.session_id == session_id)
            .order_by(desc(Report.created_at))
            .first()
        )
        return report.to_dict() if report else None


# ==================== Event Logging ====================

def log_event(
    session_id: UUID,
    event_type: str,
    event_data: Dict[str, Any] | None = None
) -> Dict[str, Any]:
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
        return event.to_dict()


def list_events(
    session_id: UUID,
    event_type: str | None = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Get events for a session, optionally filtered by type."""
    with get_db() as db:
        query = db.query(SessionEvent).filter(SessionEvent.session_id == session_id).order_by(desc(SessionEvent.created_at))
        
        if event_type:
            query = query.filter(SessionEvent.event_type == event_type)
        
        events = query.limit(limit).all()
        return [e.to_dict() for e in events]
