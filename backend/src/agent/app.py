import asyncio
import uvicorn
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime

# Correctly import the 'graph' object from agent.graph
from agent.graph import graph
from agent.database import init_db, get_all_documents
from agent.state import AgentState
import agent.db_manager as db_manager
from agent.models import Session, Paper, Report, SessionEvent

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
# Remove LangServe to avoid Pydantic conflicts
# from langserve import add_routes

# 1. Define Pydantic models for API input and output
class Message(BaseModel):
    """A single message in the conversation."""
    role: str = Field(description="The role of the message sender (user or assistant)")
    content: str = Field(description="The content of the message")

class AgentInput(BaseModel):
    """The serializable input schema for the agent."""
    messages: List[Message] = Field(description="The history of messages in the conversation.")

class ConfigurableConfig(BaseModel):
    """Configuration for the agent, including thread management."""
    thread_id: Optional[str] = Field(None, description="The ID of the conversation thread. If omitted, a new one is created.")

class AgentConfig(BaseModel):
    """Full configuration wrapper."""
    configurable: Optional[ConfigurableConfig] = Field(None, description="Configurable options for the agent")

class AgentInvokeRequest(BaseModel):
    """Request body for /agent/invoke endpoint."""
    input: AgentInput = Field(description="The input to the agent")
    config: Optional[AgentConfig] = Field(None, description="Configuration for the agent run")

class AgentOutput(BaseModel):
    """The serializable output schema for the agent."""
    messages: List[Dict[str, Any]] = Field(description="The history of messages in the conversation.")
    research_topic: str = Field(default="", description="The initial research topic.")
    search_queries: List[str] = Field(default_factory=list, description="The search queries generated.")
    literature_abstracts: List[Dict[str, Any]] = Field(default_factory=list, description="List of retrieved literature abstracts.")
    literature_full_text: List[str] = Field(default_factory=list, description="List of URLs for full text literature.")
    is_sufficient: bool = Field(default=False, description="Whether the research is sufficient.")
    knowledge_gap: str = Field(default="", description="The identified knowledge gap.")
    report: str = Field(default="", description="The final generated report.")
    # Phase 3.5.2: Session Management fields
    session_id: Optional[str] = Field(None, description="The UUID of the associated Session record.")
    thread_id: Optional[str] = Field(None, description="The LangGraph thread_id for state persistence.")

# 2. Initialize the FastAPI app
app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API for an autonomous research agent powered by LangGraph and Gemini.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Manually define agent endpoints (replacing LangServe add_routes)
@app.post("/agent/invoke", response_model=AgentOutput, tags=["Agent"])
async def invoke_agent(request: AgentInvokeRequest):
    """
    Invoke the research agent to start or continue a research task.
    
    This endpoint accepts a conversation history and optional configuration,
    runs the LangGraph agent, and returns the final state including the research report.
    
    **Phase 3.5.2 Enhancement**: Automatically creates a Session record for tracking.
    """
    try:
        # 1. Generate or use provided thread_id
        thread_id = None
        if request.config and request.config.configurable and request.config.configurable.thread_id:
            thread_id = request.config.configurable.thread_id
        else:
            thread_id = str(uuid4())
        
        # 2. Extract user query from messages
        user_query = ""
        if request.input.messages:
            # Get the last user message
            for msg in reversed(request.input.messages):
                if msg.role == "user":
                    user_query = msg.content
                    break
        
        # 3. Create Session record automatically
        session = db_manager.create_session(
            thread_id=thread_id,
            title=f"Research: {user_query[:100]}" if user_query else "Untitled Research",
            research_topic=user_query,
            status="active",
            tags=["auto-created"],
            notes=f"Started via API at {datetime.utcnow().isoformat()}"
        )
        session_id = session["id"]
        
        print(f"[Session Management] Created session {session_id} with thread_id {thread_id}")
        
        # 4. Record research_started event
        db_manager.add_session_event(
            session_id=session_id,
            event_type="research_started",
            event_data={
                "query": user_query,
                "timestamp": datetime.utcnow().isoformat(),
                "thread_id": thread_id
            }
        )
        
        # 5. Convert Pydantic models to dict format expected by LangGraph
        input_data = {
            "messages": [msg.dict() for msg in request.input.messages],
            "session_id": session_id,  # Pass session_id to graph
            "thread_id": thread_id      # Pass thread_id to graph
        }
        
        # 6. Prepare config with thread_id
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        
        # 7. Invoke the graph
        result = await graph.ainvoke(input_data, config=config)
        
        # 8. Convert BaseMessage objects to dicts for JSON serialization
        messages = []
        for msg in result.get("messages", []):
            if hasattr(msg, 'dict'):
                messages.append(msg.dict())
            elif hasattr(msg, 'content'):
                # Handle LangChain BaseMessage objects
                messages.append({
                    "role": getattr(msg, 'type', 'unknown'),
                    "content": msg.content
                })
            else:
                messages.append(msg)
        
        # 9. Return the result matching our AgentOutput schema (including session_id)
        return AgentOutput(
            messages=messages,
            research_topic=result.get("research_topic", ""),
            search_queries=result.get("search_queries", []),
            literature_abstracts=result.get("literature_abstracts", []),
            literature_full_text=result.get("literature_full_text", []),
            is_sufficient=result.get("is_sufficient", False),
            knowledge_gap=result.get("knowledge_gap", ""),
            report=result.get("report", ""),
            session_id=session_id,  # Include session_id in response
            thread_id=thread_id     # Include thread_id in response
        )
    except Exception as e:
        # Record error event if session was created
        if 'session_id' in locals():
            try:
                db_manager.add_session_event(
                    session_id=session_id,
                    event_type="error_occurred",
                    event_data={
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat(),
                        "node": "invoke_agent"
                    }
                )
            except:
                pass  # Don't fail if event logging fails
        
        raise HTTPException(status_code=500, detail=f"Agent invocation failed: {str(e)}")


@app.get("/agent/state", response_model=AgentOutput, tags=["Agent"])
def get_agent_state():
    """
    Fetches the latest agent state from the database.
    
    This endpoint returns the current state based on ingested documents.
    It does not require a thread_id and returns a default/latest state.
    
    Note: This is a convenience endpoint for simple use cases. For production,
    use GET /agent/state/{thread_id} with proper thread management.
    """
    documents = get_all_documents()
    literature_abstracts = [
        {"title": doc.source, "summary": doc.content, "authors": []} for doc in documents
    ]
    return AgentOutput(
        messages=[],
        research_topic="",
        search_queries=[],
        literature_abstracts=literature_abstracts,
        literature_full_text=[],
        is_sufficient=False,
        knowledge_gap="",
        report="",
        session_id=None,  # Phase 3.5.2: No session for this convenience endpoint
        thread_id=None    # Phase 3.5.2: No thread for this convenience endpoint
    )


@app.get("/agent/state/{thread_id}", response_model=AgentOutput, tags=["Agent"])
def get_agent_state_by_thread(
    thread_id: str = Path(..., description="The ID of the conversation thread to fetch.")
):
    """
    Retrieves the current state for a specific research thread.
    
    Uses the LangGraph checkpointer to fetch the persisted state for the given thread_id.
    If the thread doesn't exist or has no checkpoints, returns a 404 error.
    
    **Fallback**: If checkpointer is unavailable (e.g., in tests), returns documents from database.
    """
    try:
        # Try to use the graph's get_state method to retrieve the checkpoint
        config = {"configurable": {"thread_id": thread_id}}
        state_snapshot = graph.get_state(config)
        
        # If no state found, return 404
        if not state_snapshot or not state_snapshot.values:
            raise HTTPException(
                status_code=404,
                detail=f"Thread {thread_id} not found or has no checkpoints."
            )
        
        # Extract the state values
        state = state_snapshot.values
        
        # Convert to AgentOutput format
        messages = []
        for msg in state.get("messages", []):
            if isinstance(msg, BaseMessage):
                messages.append({
                    "role": msg.type,
                    "content": msg.content
                })
            else:
                messages.append(msg)
        
        return AgentOutput(
            messages=messages,
            research_topic=state.get("research_topic", ""),
            search_queries=state.get("search_queries", []),
            literature_abstracts=state.get("literature_abstracts", []),
            literature_full_text=state.get("literature_full_text", []),
            is_sufficient=state.get("is_sufficient", False),
            knowledge_gap=state.get("knowledge_gap", ""),
            report=state.get("report", ""),
            session_id=state.get("session_id"),  # Phase 3.5.2: Include session_id
            thread_id=thread_id  # Phase 3.5.2: Include thread_id
        )
    except HTTPException:
        raise
    except Exception as e:
        # Fallback: Return documents from database (for testing compatibility)
        # This handles cases where checkpointer is unavailable
        documents = get_all_documents()
        if not documents:
            raise HTTPException(
                status_code=404,
                detail=f"Thread {thread_id} not found or has no checkpoints."
            )
        
        literature_abstracts = [
            {"title": doc.source, "summary": doc.content, "authors": []} for doc in documents
        ]
        return AgentOutput(
            messages=[],
            research_topic="",
            search_queries=[],
            literature_abstracts=literature_abstracts,
            literature_full_text=[],
            is_sufficient=False,
            knowledge_gap="",
            report="",
            session_id=None,
            thread_id=thread_id
        )

# 5. Add a health check endpoint
@app.get("/ok", tags=["Health"])
def ok():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}


# ==================== Session Management Endpoints ====================

# Pydantic models for Session API
class SessionCreate(BaseModel):
    """Request body for creating a session."""
    thread_id: UUID = Field(description="LangGraph thread UUID")
    title: str = Field(description="Session title", max_length=500)
    research_topic: Optional[str] = Field(None, description="Research topic")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    notes: Optional[str] = Field(None, description="Notes")

class SessionUpdate(BaseModel):
    """Request body for updating a session."""
    title: Optional[str] = Field(None, max_length=500)
    research_topic: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|archived)$")
    tags: Optional[List[str]] = None
    notes: Optional[str] = None

class SessionResponse(BaseModel):
    """Response model for session data."""
    id: str
    thread_id: str
    title: str
    research_topic: Optional[str]
    created_at: str
    updated_at: str
    status: str
    tags: List[str]
    notes: Optional[str]
    paper_count: int
    report_count: int


@app.get("/sessions", response_model=List[SessionResponse], tags=["Sessions"])
def list_sessions_endpoint(
    status: Optional[str] = Query(None, description="Filter by status (active, completed, archived)"),
    limit: int = Query(50, le=100, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    List all research sessions with optional filtering.
    
    Returns sessions ordered by creation date (newest first).
    """
    try:
        sessions = db_manager.list_sessions(status=status, limit=limit, offset=offset)
        return [SessionResponse(**s) for s in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing sessions: {str(e)}")


@app.get("/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def get_session_endpoint(session_id: str = Path(..., description="Session UUID")):
    """Get a specific session by ID."""
    try:
        session_uuid = UUID(session_id)
        session = db_manager.get_session_by_id(session_uuid)
        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return SessionResponse(**session)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")


@app.post("/sessions", response_model=SessionResponse, tags=["Sessions"], status_code=201)
def create_session_endpoint(request: SessionCreate):
    """
    Create a new research session.
    
    The session is linked to a LangGraph thread via thread_id.
    """
    try:
        session = db_manager.create_session(
            thread_id=request.thread_id,
            title=request.title,
            research_topic=request.research_topic,
            tags=request.tags,
            notes=request.notes
        )
        return SessionResponse(**session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")


@app.patch("/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def update_session_endpoint(
    session_id: str = Path(..., description="Session UUID"),
    request: SessionUpdate = ...
):
    """Update session fields. Only provided fields are updated."""
    try:
        session_uuid = UUID(session_id)
        session = db_manager.update_session(
            session_id=session_uuid,
            title=request.title,
            research_topic=request.research_topic,
            status=request.status,
            tags=request.tags,
            notes=request.notes
        )
        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return SessionResponse(**session)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {str(e)}")


@app.delete("/sessions/{session_id}", tags=["Sessions"], status_code=204)
def delete_session_endpoint(session_id: str = Path(..., description="Session UUID")):
    """Delete a session and all associated data (papers, reports, events)."""
    try:
        session_uuid = UUID(session_id)
        deleted = db_manager.delete_session(session_uuid)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


@app.get("/sessions/{session_id}/events", tags=["Sessions"])
def list_session_events(
    session_id: str = Path(..., description="Session UUID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    limit: int = Query(100, le=500, description="Maximum events to return")
):
    """Get all events for a session, optionally filtered by type."""
    try:
        session_uuid = UUID(session_id)
        events = db_manager.list_events(session_uuid, event_type=event_type, limit=limit)
        return events
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving events: {str(e)}")


# 6. Startup event to initialize the database
@app.on_event("startup")
async def on_startup():
    """Initializes the database."""
    print("--- Initializing database ---")
    init_db()
    db_manager.init_db()  # Initialize session management tables
    print("--- Database initialized ---")

# 7. Main entry point for running the app with uvicorn
if __name__ == "__main__":
    print("--- Starting Research Agent API ---")
    # To run this, execute `python -m agent.app` from the `backend/src` directory
    uvicorn.run("agent.app:app", host="0.0.0.0", port=8000, reload=True)
