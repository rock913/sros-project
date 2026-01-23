from typing import Protocol, List, Optional
from datetime import datetime
from uuid import UUID

from agent.domain.schemas.session import ResearchSession, SessionEvent
from agent.domain.schemas.report import Report, ReportVersion
from agent.domain.schemas.paper import Paper


class SessionManager(Protocol):
    """Protocol for managing research sessions with full historical tracking.
    
    This acts as a Port in the Hexagonal Architecture, decoupling the
    application from specific database implementations (Postgres, SQLite, in-memory).
    
    @TestScenarios
    def test_create_session_with_valid_data():
        # Test session creation returns ResearchSession with UUID
        session = implementation.create_session(
            topic="Quantum Computing",
            description="Research on quantum algorithms"
        )
        assert isinstance(session, ResearchSession)
        assert session.id is not None
        assert session.status == "active"
        
    @TestScenarios  
    def test_create_session_duplicate_topic_handling():
        # Test duplicate topic handling (should allow duplicates with timestamps)
        session1 = implementation.create_session(topic="Test")
        session2 = implementation.create_session(topic="Test")
        assert session1.id != session2.id
        assert session1.created_at != session2.created_at
        
    @TestScenarios
    def test_database_connection_failure():
        # Test graceful handling of database connection failures
        with mock.patch('sqlalchemy.create_engine', side_effect=Exception("DB down")):
            with pytest.raises(ConnectionError):
                implementation.create_session(topic="Test")
                
    @TestScenarios
    def test_get_session_by_id():
        # Test retrieving an existing session
        created = implementation.create_session(topic="Test")
        retrieved = implementation.get_session(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.topic == "Test"
        
    @TestScenarios
    def test_get_nonexistent_session():
        # Test retrieving a non-existent session returns None
        retrieved = implementation.get_session("non-existent-uuid")
        assert retrieved is None
        
    @TestScenarios
    def test_list_sessions_pagination():
        # Test listing sessions with pagination
        for i in range(5):
            implementation.create_session(topic=f"Test{i}")
        sessions = implementation.list_sessions(limit=3, offset=0)
        assert len(sessions) == 3
        sessions2 = implementation.list_sessions(limit=3, offset=3)
        assert len(sessions2) == 2
    """

    def create_session(self, topic: str, description: str = "") -> ResearchSession:
        """Create a new research session.

        Args:
            topic (str): The research topic (3-200 characters).
            description (str): Optional description of the research (max 1000 characters).

        Returns:
            ResearchSession: The created session with generated ID and timestamps.

        Raises:
            ValueError: If topic is empty or invalid.
            ConnectionError: If the database is unreachable.
        """
        ...

    def get_session(self, session_id: str) -> Optional[ResearchSession]:
        """Retrieve a session by ID.

        Args:
            session_id (str): The UUID of the session.

        Returns:
            Optional[ResearchSession]: The session if found, None otherwise.

        Raises:
            ConnectionError: If the database is unreachable.
        """
        ...

    def list_sessions(self, limit: int = 100, offset: int = 0) -> List[ResearchSession]:
        """List research sessions with pagination.

        Args:
            limit (int): Maximum number of sessions to return (default 100).
            offset (int): Number of sessions to skip (default 0).

        Returns:
            List[ResearchSession]: List of sessions ordered by creation date (newest first).

        Raises:
            ConnectionError: If the database is unreachable.
        """
        ...

    def add_session_event(self, session_id: str, event_type: str, data: dict) -> SessionEvent:
        """Add an event to session timeline.

        Args:
            session_id (str): The UUID of the session.
            event_type (str): Type of event (e.g., "search_started", "paper_added", "report_generated").
            data (dict): Event-specific data (must be JSON-serializable).

        Returns:
            SessionEvent: The created event with timestamp.

        Raises:
            ValueError: If session_id does not exist or event_type is invalid.
            ConnectionError: If the database is unreachable.
        """
        ...

    def update_session_status(self, session_id: str, status: str) -> ResearchSession:
        """Update the status of a research session.

        Args:
            session_id (str): The UUID of the session.
            status (str): New status ("active", "completed", "archived").

        Returns:
            ResearchSession: The updated session.

        Raises:
            ValueError: If session_id does not exist or status is invalid.
            ConnectionError: If the database is unreachable.
        """
        ...

    def add_paper_to_session(self, session_id: str, paper: Paper) -> None:
        """Associate a paper with a research session.

        Args:
            session_id (str): The UUID of the session.
            paper (Paper): The paper domain model.

        Raises:
            ValueError: If session_id does not exist.
            ConnectionError: If the database is unreachable.
        """
        ...

    def add_report_to_session(self, session_id: str, report: Report) -> None:
        """Associate a report with a research session.

        Args:
            session_id (str): The UUID of the session.
            report (Report): The report domain model.

        Raises:
            ValueError: If session_id does not exist.
            ConnectionError: If the database is unreachable.
        """
        ...

    def get_session_papers(self, session_id: str) -> List[Paper]:
        """Get all papers associated with a session.

        Args:
            session_id (str): The UUID of the session.

        Returns:
            List[Paper]: List of papers associated with the session.

        Raises:
            ValueError: If session_id does not exist.
            ConnectionError: If the database is unreachable.
        """
        ...

    def get_session_reports(self, session_id: str) -> List[Report]:
        """Get all reports associated with a session.

        Args:
            session_id (str): The UUID of the session.

        Returns:
            List[Report]: List of reports associated with the session.

        Raises:
            ValueError: If session_id does not exist.
            ConnectionError: If the database is unreachable.
        """
        ...
