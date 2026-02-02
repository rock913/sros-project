from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from agent.domain.ports.session_manager import SessionManager
from agent.domain.schemas.paper import Paper
from agent.domain.schemas.session import ResearchSession, SessionEvent

Base = declarative_base()

class SessionTable(Base):
    __tablename__ = 'sessions'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    topic = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(Enum('active', 'completed', 'archived', name='session_status'), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SessionEventTable(Base):
    __tablename__ = 'session_events'
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    session_id = Column(PGUUID(as_uuid=True), ForeignKey('sessions.id'), nullable=False)
    event_type = Column(Enum('search_started', 'paper_added', 'report_generated', 'session_completed', 'session_archived', 'error_occurred', 'user_intervention', name='event_type'), nullable=False)
    data = Column(JSONB)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Association tables for future paper/report linking (not used yet)
class SessionPaperAssoc(Base):
    __tablename__ = 'session_paper_assoc'
    session_id = Column(PGUUID(as_uuid=True), ForeignKey('sessions.id'), primary_key=True)
    paper_doi = Column(String, primary_key=True)  # Paper uses DOI as identifier

class SessionReportAssoc(Base):
    __tablename__ = 'session_report_assoc'
    session_id = Column(PGUUID(as_uuid=True), ForeignKey('sessions.id'), primary_key=True)
    report_id = Column(PGUUID(as_uuid=True), primary_key=True)

class PostgresSessionAdapter(SessionManager):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def _get_session(self):
        return self.Session()

    def create_session(self, topic: str, description: str = "") -> ResearchSession:
        with self._get_session() as session:
            try:
                new_session = SessionTable(id=uuid4(), topic=topic, description=description)
                session.add(new_session)
                session.commit()
                # Convert UUID to string for Pydantic
                session_data = new_session.__dict__.copy()
                session_data['id'] = str(session_data['id'])
                return ResearchSession.model_validate(session_data)
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def get_session(self, session_id: str) -> ResearchSession | None:
        with self._get_session() as session:
            try:
                db_session = session.query(SessionTable).filter_by(id=session_id).first()
                if db_session:
                    return ResearchSession.model_validate(db_session.__dict__)
                return None
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def list_sessions(self, limit: int = 100, offset: int = 0) -> List[ResearchSession]:
        with self._get_session() as session:
            try:
                sessions = session.query(SessionTable).order_by(SessionTable.created_at.desc()).limit(limit).offset(offset).all()
                return [ResearchSession.model_validate(s.__dict__) for s in sessions]
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def add_session_event(self, session_id: str, event_type: str, data: dict) -> SessionEvent:
        with self._get_session() as session:
            try:
                new_event = SessionEventTable(id=uuid4(), session_id=session_id, event_type=event_type, data=data)
                session.add(new_event)
                session.commit()
                return SessionEvent.model_validate(new_event.__dict__)
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def update_session_status(self, session_id: str, status: str) -> ResearchSession:
        with self._get_session() as session:
            try:
                db_session = session.query(SessionTable).filter_by(id=session_id).first()
                if not db_session:
                    raise ValueError(f"Session with ID {session_id} does not exist.")
                db_session.status = status
                session.commit()
                return ResearchSession.model_validate(db_session.__dict__)
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def add_paper_to_session(self, session_id: str, paper: Paper) -> None:
        # TODO: Implement paper association logic. For now, this maintains only session state.
        # Paper objects are managed by separate PaperAdapter, we just store association by DOI.
        # This would create an entry in SessionPaperAssoc table with paper.doi and session_id
        with self._get_session() as session:
            try:
                # Just check session exists, don't create paper association yet
                db_session = session.query(SessionTable).filter_by(id=session_id).first()
                if not db_session:
                    raise ValueError(f"Session with ID {session_id} does not exist.")
                # TODO: session.execute(insert(SessionPaperAssoc).values(session_id=session_id, paper_doi=paper.doi))
            except SQLAlchemyError as e:
                session.rollback()
                raise ConnectionError(f"Database connection error: {e}")

    def add_report_to_session(self, session_id: str, report: any) -> None:
        # TODO: Implement report association logic. Report schema needs to be created.
        # For now, this maintains only session state.
        pass

    def get_session_papers(self, session_id: str) -> List[Paper]:
        # TODO: Integrate with PaperAdapter to fetch papers by their IDs.
        # For now, return empty list (session CRUD is complete).
        return []

    def get_session_reports(self, session_id: str) -> List[any]:
        # TODO: Implement report retrieval. Report schema needs to be created.
        # For now, return empty list (session CRUD is complete).
        return []