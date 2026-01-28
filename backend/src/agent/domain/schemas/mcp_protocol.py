from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ResearchOp:
    """Standard Operation Types

    @TestScenarios
    - Create a new research session
    - Query session status
    - Send human input to active session
    """
    START_SESSION: str = "start_session"
    GET_STATUS: str = "get_status"
    HUMAN_INPUT: str = "human_input"


class ResearchRequest(BaseModel):
    """Incoming MCP Request Structure

    @TestScenarios
    - Start session with topic only
    - Start session with topic and custom payload
    - Query status for existing session
    """
    session_id: Optional[str] = Field(None, description="Session ID for operations requiring existing session")
    operation: str = Field(ResearchOp.START_SESSION, description="Operation type")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Operation-specific parameters")


class ResearchUpdate(BaseModel):
    """Streamed Updates to Client During Research Session

    @TestScenarios
    - Status change: initializing, processing, completed
    - Thought process: LLM reasoning steps
    - Result delivery: final output or partial results
    - Error notification: failure conditions
    """
    type: str = Field(
        ...,
        description="Update type: log, thought, mindmap_update, status_change, final_result, error",
        pattern="^(log|thought|mindmap_update|status_change|final_result|error)$"
    )
    content: str = Field(..., description="Update content/message")
    timestamp: Optional[datetime] = Field(None, description="Event timestamp (auto-filled if not provided)")
    payload: Optional[Dict[str, Any]] = Field(None, description="Structured data payload (e.g., MindMap JSON for updates)")
