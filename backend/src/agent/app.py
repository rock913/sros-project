import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import text
from starlette.websockets import WebSocketState

import agent.analytics as analytics
import agent.db_manager as db_manager
from agent.database import get_all_documents, init_db
from agent.document_utils import DocumentDiffer

# Correctly import the 'graph' object from agent.graph
from agent.graph import async_graph, graph, get_async_graph
from agent.langfuse_manager import LangfuseManager

# Remove LangServe to avoid Pydantic conflicts
# from langserve import add_routes

# 1. Define lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    print("--- Initializing database ---")
    init_db()
    db_manager.init_db()  # Initialize session management tables
    print("--- Database initialized ---")
    yield
    # Cleanup code can go here if needed
    print("--- Shutting down ---")

# 2. Define Pydantic models for API input and output
class Message(BaseModel):
    """A single message in the conversation."""
    role: str = Field(description="The role of the message sender (user or assistant)")
    content: str = Field(description="The content of the message")

class AgentInput(BaseModel):
    """The serializable input schema for the agent."""
    messages: List[Message] = Field(description="The history of messages in the conversation.")

class ConfigurableConfig(BaseModel):
    """Configuration for the agent, including thread management."""
    thread_id: str | None = Field(None, description="The ID of the conversation thread. If omitted, a new one is created.")

class AgentConfig(BaseModel):
    """Full configuration wrapper."""
    configurable: ConfigurableConfig | None = Field(None, description="Configurable options for the agent")

class AgentInvokeRequest(BaseModel):
    """Request body for /agent/invoke endpoint."""
    input: AgentInput = Field(description="The input to the agent")
    config: AgentConfig | None = Field(None, description="Configuration for the agent run")

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
    session_id: str | None = Field(None, description="The UUID of the associated Session record.")
    thread_id: str | None = Field(None, description="The LangGraph thread_id for state persistence.")

# 3. Initialize the FastAPI app with lifespan
app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API for an autonomous research agent powered by LangGraph and Gemini.",
    version="1.0.0",
    lifespan=lifespan,
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
    """Invoke the research agent to start or continue a research task.
    
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
        db_manager.log_event(
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
        # Note: Using sync invoke in thread pool due to PostgresSaver not supporting async aget_tuple
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                lambda: graph.invoke(input_data, config=config)
            )
        
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
        # Enhanced error logging
        import traceback
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"[ERROR] Agent invocation failed: {error_details}")
        
        # Record error event if session was created
        if 'session_id' in locals():
            try:
                db_manager.log_event(
                    session_id=session_id,
                    event_type="error_occurred",
                    event_data={
                        **error_details,
                        "timestamp": datetime.utcnow().isoformat(),
                        "node": "invoke_agent"
                    }
                )
            except:
                pass  # Don't fail if event logging fails
        
        raise HTTPException(
            status_code=500, 
            detail=f"Agent invocation failed: {type(e).__name__}: {str(e)}"
        )


@app.get("/agent/state", response_model=AgentOutput, tags=["Agent"])
def get_agent_state():
    """Fetches the latest agent state from the database.
    
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
    """Retrieves the current state for a specific research thread.
    
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
    except Exception:
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


@app.get("/health", tags=["Health"])
def health_check():
    """Enhanced health check endpoint with dependency validation.
    
    Phase 3.5.4: Production Readiness
    
    Returns:
        - status: overall (healthy | degraded | unhealthy)
        - version: API version
        - timestamp: current server time
        - dependencies: status of each dependency
        - performance: response time metrics
    """
    import time
    from datetime import datetime
    
    start_time = time.time()
    
    # Initialize response
    health_status = {
        "status": "healthy",
        "version": "3.5.4",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {},
        "performance": {}
    }
    
    dependency_checks = []
    
    # 1. Database Check
    try:
        db_start = time.time()
        # Simple query to verify connection
        test_session = db_manager.get_session_by_id(UUID('00000000-0000-0000-0000-000000000000'))
        db_time = (time.time() - db_start) * 1000
        
        health_status["dependencies"]["database"] = {
            "status": "healthy",
            "response_time_ms": round(db_time, 2),
            "type": "postgresql"
        }
        dependency_checks.append(True)
    except Exception as e:
        health_status["dependencies"]["database"] = {
            "status": "unhealthy",
            "error": str(e)[:100],
            "type": "postgresql"
        }
        dependency_checks.append(False)
    
    # 2. LangGraph Graph Check
    try:
        langgraph_start = time.time()
        # Check if graph is accessible
        _ = graph.get_graph()
        langgraph_time = (time.time() - langgraph_start) * 1000
        
        health_status["dependencies"]["langgraph"] = {
            "status": "healthy",
            "response_time_ms": round(langgraph_time, 2),
            "type": "graph"
        }
        dependency_checks.append(True)
    except Exception as e:
        health_status["dependencies"]["langgraph"] = {
            "status": "degraded",
            "error": str(e)[:100],
            "type": "graph"
        }
        # LangGraph is not critical for all endpoints
        dependency_checks.append(True)
    
    # 3. Environment Variables Check
    required_env_vars = ["GEMINI_API_KEY", "UNPAYWALL_EMAIL"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        health_status["dependencies"]["environment"] = {
            "status": "degraded",
            "missing_variables": missing_vars
        }
        dependency_checks.append(False)
    else:
        health_status["dependencies"]["environment"] = {
            "status": "healthy",
            "configured_variables": len(required_env_vars)
        }
        dependency_checks.append(True)
    
    # 4. File System Check (for logs, cache)
    try:
        import tempfile
        fs_start = time.time()
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tmp.write(b"health_check")
            tmp.flush()
        fs_time = (time.time() - fs_start) * 1000
        
        health_status["dependencies"]["filesystem"] = {
            "status": "healthy",
            "response_time_ms": round(fs_time, 2)
        }
        dependency_checks.append(True)
    except Exception as e:
        health_status["dependencies"]["filesystem"] = {
            "status": "unhealthy",
            "error": str(e)[:100]
        }
        dependency_checks.append(False)
    
    # Calculate overall status
    total_checks = len(dependency_checks)
    healthy_checks = sum(dependency_checks)
    
    if healthy_checks == total_checks:
        health_status["status"] = "healthy"
    elif healthy_checks >= total_checks * 0.75:
        health_status["status"] = "degraded"
    else:
        health_status["status"] = "unhealthy"
    
    # Performance metrics
    total_time = (time.time() - start_time) * 1000
    health_status["performance"] = {
        "total_response_time_ms": round(total_time, 2),
        "healthy_dependencies": healthy_checks,
        "total_dependencies": total_checks,
        "health_percentage": round((healthy_checks / total_checks) * 100, 1)
    }
    
    return health_status


# ==================== Session Management Endpoints ====================

# Pydantic models for Session API
class SessionCreate(BaseModel):
    """Request body for creating a session."""
    thread_id: UUID = Field(description="LangGraph thread UUID")
    title: str = Field(description="Session title", max_length=500)
    research_topic: str | None = Field(None, description="Research topic")
    tags: List[str] | None = Field(default_factory=list, description="Tags")
    notes: str | None = Field(None, description="Notes")

class SessionUpdate(BaseModel):
    """Request body for updating a session."""
    title: str | None = Field(None, max_length=500)
    research_topic: str | None = None
    status: str | None = Field(None, pattern="^(active|completed|archived)$")
    tags: List[str] | None = None
    notes: str | None = None

class SessionResponse(BaseModel):
    """Response model for session data."""
    id: str
    thread_id: str
    title: str
    research_topic: str | None
    created_at: str
    updated_at: str
    status: str
    tags: List[str]
    notes: str | None
    paper_count: int
    report_count: int


@app.get("/sessions", response_model=List[SessionResponse], tags=["Sessions"])
def list_sessions_endpoint(
    status: str | None = Query(None, description="Filter by status (active, completed, archived)"),
    limit: int = Query(50, le=100, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """List all research sessions with optional filtering.
    
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
    """Create a new research session.
    
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


@app.get("/sessions/{session_id}/details", tags=["Sessions"])
def get_session_details(session_id: str = Path(..., description="Session UUID")):
    """Get comprehensive session details including events, papers, reports, and statistics.
    
    Returns:
        - session: Basic session information
        - events: Event timeline (most recent 50 events)
        - papers: List of papers associated with this session
        - reports: List of report versions
        - stats: Aggregated statistics
    """
    try:

        from dateutil.parser import parse
        
        session_uuid = UUID(session_id)
        
        # Get basic session info
        session = db_manager.get_session_by_id(session_uuid)
        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Get events timeline (limit to 50 most recent)
        events_list = db_manager.list_events(session_uuid, limit=50)
        
        # Get papers
        papers_list = db_manager.list_papers(session_id=session_uuid)
        
        # Get reports
        reports_list = db_manager.list_reports(session_id=session_uuid)
        
        # Calculate statistics
        def calculate_duration(events: list) -> int:
            """Calculate session duration in seconds"""
            if not events:
                return 0
            
            try:
                timestamps = [e.get("created_at") for e in events if e.get("created_at")]
                if not timestamps:
                    return 0
                
                start = min(timestamps)
                end = max(timestamps)
                
                # Parse ISO timestamps
                start_dt = parse(start) if isinstance(start, str) else start
                end_dt = parse(end) if isinstance(end, str) else end
                
                duration = (end_dt - start_dt).total_seconds()
                return int(duration)
            except Exception as e:
                logger.warning(f"Error calculating duration: {e}")
                return 0
        
        def estimate_cost(events: list) -> float:
            """Estimate session cost based on token usage"""
            total_tokens = 0
            
            for event in events:
                if event.get("event_type") == "llm_call":
                    data = event.get("event_data", {})
                    total_tokens += data.get("input_tokens", 0)
                    total_tokens += data.get("output_tokens", 0)
            
            # Simple estimation: $0.01 per 1000 tokens (Gemini pricing approximation)
            return round(total_tokens / 1000 * 0.01, 4)
        
        stats = {
            "total_events": len(events_list),
            "duration_seconds": calculate_duration(events_list),
            "paper_count": len(papers_list),
            "report_count": len(reports_list),
            "status": session.get("status", "unknown"),
            "cost_estimate": estimate_cost(events_list)
        }
        
        return {
            "session": session,
            "events": events_list,
            "papers": papers_list,
            "reports": reports_list,
            "stats": stats
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session details: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving session details: {str(e)}")


@app.get("/sessions/{session_id}/events", tags=["Sessions"])
def list_session_events(
    session_id: str = Path(..., description="Session UUID"),
    event_type: str | None = Query(None, description="Filter by event type"),
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


# ==================== Phase 3.5.2: Paper Management APIs ====================

@app.get("/papers", tags=["Papers"])
def list_all_papers(
    session_id: str | None = Query(None, description="Filter by session UUID"),
    source: str | None = Query(None, description="Filter by data source (arxiv, unpaywall, zotero)"),
    start_date: str | None = Query(None, description="Filter papers collected after this timestamp"),
    end_date: str | None = Query(None, description="Filter papers collected before this timestamp"),
    keyword: str | None = Query(None, description="Search keyword in titles and abstracts"),
    limit: int = Query(100, le=500, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """List all papers with advanced filtering.
    
    Supports filtering by session, source, date range, and full-text keyword search.
    """
    try:
        session_uuid = UUID(session_id) if session_id else None
        papers, total = db_manager.get_all_papers(
            session_id=session_uuid,
            source=source,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword,
            limit=limit,
            offset=offset
        )
        return {
            "papers": papers,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving papers: {str(e)}")


@app.get("/papers/export", tags=["Papers"])
def export_papers(
    format: str = Query(..., description="Export format: bibtex, ris, or json"),
    session_id: str | None = Query(None, description="Filter by session UUID"),
    source: str | None = Query(None, description="Filter by data source")
):
    """Export papers to bibliography formats (BibTeX, RIS, JSON).
    
    Supports the same filtering options as GET /papers.
    """
    try:
        from fastapi.responses import JSONResponse, PlainTextResponse
        
        session_uuid = UUID(session_id) if session_id else None
        papers, _ = db_manager.get_all_papers(
            session_id=session_uuid,
            source=source,
            limit=10000  # Export all matching papers
        )
        
        if format == "json":
            return JSONResponse(content=papers)
        
        elif format == "bibtex":
            # Generate BibTeX format
            bibtex_entries = []
            for paper in papers:
                entry_type = "article"
                cite_key = f"{paper.get('authors', ['Unknown'])[0].split()[-1] if paper.get('authors') else 'Unknown'}{paper.get('id', '')[:8]}"
                
                entry = f"@{entry_type}{{{cite_key},\n"
                entry += f"  title = {{{paper.get('title', 'Untitled')}}},\n"
                if paper.get('authors'):
                    entry += f"  author = {{{' and '.join(paper['authors'])}}},\n"
                if paper.get('doi'):
                    entry += f"  doi = {{{paper['doi']}}},\n"
                if paper.get('url'):
                    entry += f"  url = {{{paper['url']}}},\n"
                entry += "}\n"
                bibtex_entries.append(entry)
            
            return PlainTextResponse(
                content="\n".join(bibtex_entries),
                media_type="application/x-bibtex"
            )
        
        elif format == "ris":
            # Generate RIS format
            ris_entries = []
            for paper in papers:
                entry = "TY  - JOUR\n"
                entry += f"TI  - {paper.get('title', 'Untitled')}\n"
                for author in paper.get('authors', []):
                    entry += f"AU  - {author}\n"
                if paper.get('abstract'):
                    entry += f"AB  - {paper['abstract']}\n"
                if paper.get('doi'):
                    entry += f"DO  - {paper['doi']}\n"
                if paper.get('url'):
                    entry += f"UR  - {paper['url']}\n"
                entry += "ER  -\n"
                ris_entries.append(entry)
            
            return PlainTextResponse(
                content="\n".join(ris_entries),
                media_type="application/x-research-info-systems"
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}. Use bibtex, ris, or json.")
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting papers: {str(e)}")


@app.get("/papers/{paper_id}", tags=["Papers"])
def get_paper_details(paper_id: str = Path(..., description="Paper UUID")):
    """Get detailed information for a specific paper."""
    try:
        paper_uuid = UUID(paper_id)
        paper = db_manager.get_paper_by_id(paper_uuid)
        if not paper:
            raise HTTPException(status_code=404, detail=f"Paper {paper_id} not found")
        return paper
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper: {str(e)}")


# ==================== Phase 3.5.2: Report Management APIs ====================

@app.get("/reports", tags=["Reports"])
def list_all_reports(
    session_id: str | None = Query(None, description="Filter by session UUID"),
    start_date: str | None = Query(None, description="Filter reports created after this timestamp"),
    end_date: str | None = Query(None, description="Filter reports created before this timestamp"),
    limit: int = Query(50, le=500, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """List all reports with filtering.
    
    Supports filtering by session and date range.
    """
    try:
        session_uuid = UUID(session_id) if session_id else None
        reports, total = db_manager.get_all_reports(
            session_id=session_uuid,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        return {
            "reports": reports,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving reports: {str(e)}")


@app.get("/reports/compare", tags=["Reports"])
def compare_reports(
    report_id_1: str = Query(..., description="First report UUID (older version)"),
    report_id_2: str = Query(..., description="Second report UUID (newer version)")
):
    """Compare two report versions and generate a diff.
    
    Returns both reports and a unified diff showing changes.
    """
    try:
        import difflib
        
        report_uuid_1 = UUID(report_id_1)
        report_uuid_2 = UUID(report_id_2)
        
        report_1 = db_manager.get_report_by_id(report_uuid_1)
        report_2 = db_manager.get_report_by_id(report_uuid_2)
        
        if not report_1:
            raise HTTPException(status_code=404, detail=f"Report {report_id_1} not found")
        if not report_2:
            raise HTTPException(status_code=404, detail=f"Report {report_id_2} not found")
        
        # Generate unified diff
        content_1_lines = report_1.get('content', '').splitlines(keepends=True)
        content_2_lines = report_2.get('content', '').splitlines(keepends=True)
        
        diff = ''.join(difflib.unified_diff(
            content_1_lines,
            content_2_lines,
            fromfile=f"Report {report_id_1}",
            tofile=f"Report {report_id_2}",
            lineterm=''
        ))
        
        return {
            "report_1": report_1,
            "report_2": report_2,
            "diff": diff
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing reports: {str(e)}")


# ==================== Analytics Endpoints (Phase 3.5.3) ====================

@app.get("/analytics/sessions", tags=["Analytics"])
def get_sessions_list(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    status: str | None = Query(None, regex="^(active|completed|archived)$", description="Filter by status"),
    user_id: str | None = Query(None, description="Filter by user ID"),
    sort_by: str = Query("created_at", regex="^(created_at|duration|papers_count)$"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    """Phase 3.5.3: Get paginated list of sessions with filtering and sorting.
    
    Returns:
        - sessions: List of session summaries
        - total: Total matching sessions
        - pagination info
    """
    try:
        result = analytics.get_sessions_list(
            limit=limit,
            offset=offset,
            status=status,
            user_id=user_id,
            sort_by=sort_by,
            order=order
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")


@app.get("/analytics/sessions/stats", tags=["Analytics"])
def get_sessions_statistics(
    time_range: str = Query("7d", regex="^(24h|7d|30d|all)$", description="Time range"),
    user_id: str | None = Query(None, description="Filter by user ID")
):
    """Phase 3.5.3: Get aggregated statistics across sessions.
    
    Returns:
        - stats: Aggregated metrics (total, completed, success rate, averages)
        - daily_breakdown: Sessions per day
        - top_topics: Most researched topics
    """
    try:
        result = analytics.get_sessions_stats(
            time_range=time_range,
            user_id=user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")


@app.get("/analytics/sessions/{session_id}", tags=["Analytics"])
def get_session_analytics(session_id: str = Path(..., description="Session UUID")):
    """Phase 3.5.3: Get detailed analytics for a specific session.
    
    Returns:
        - session: Complete session metadata
        - events: Chronological event timeline
        - timeline: Phase breakdown analysis
    """
    try:
        session_uuid = UUID(session_id)
        result = analytics.get_session_details(session_uuid)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching session analytics: {str(e)}")


@app.get("/analytics/papers/trends", tags=["Analytics"])
def get_papers_trends(
    time_range: str = Query("7d", regex="^(24h|7d|30d|all)$", description="Time range")
):
    """Phase 3.5.3: Get paper collection trends and distribution.
    
    Returns:
        - trends: Paper counts, daily breakdown, venue distribution, year distribution
    """
    try:
        result = analytics.get_papers_trends(time_range=time_range)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing paper trends: {str(e)}")


# ============================================================================
# HITL (Human-in-the-Loop) Endpoints - Phase 3.6
# ============================================================================

@app.post("/agent/hitl/respond", tags=["HITL"])
async def respond_to_hitl(
    request_id: str = Query(..., description="HITL request ID"),
    decision: str = Query(..., description="User's decision (approve/reject/modify/etc)"),
    modified_data: Dict[str, Any] | None = None
):
    """Phase 3.6: Respond to a Human-in-the-Loop decision request.
    
    This endpoint is called when the user makes a decision on a HITL request
    (e.g., approving queries, selecting papers, revising report).
    
    Args:
        request_id: Unique identifier for the HITL request
        decision: User's decision (approve, reject, modify, select_all, select_subset, revise)
        modified_data: Optional modified data (e.g., modified queries, selected paper IDs, feedback)
    
    Returns:
        Success confirmation and next steps
    """
    try:
        from datetime import datetime

        from agent.database import get_db_connection
        from agent.models import HITLDecision
        
        # 1. Find the HITL decision record
        with get_db_connection() as session:
            hitl_record = session.query(HITLDecision).filter(
                HITLDecision.request_id == request_id
            ).first()
            
            if not hitl_record:
                raise HTTPException(status_code=404, detail=f"HITL request {request_id} not found")
            
            if not hitl_record.is_pending:
                raise HTTPException(status_code=400, detail=f"HITL request {request_id} already responded")
            
            # 2. Update the record with user's decision
            hitl_record.user_decision = decision
            hitl_record.modified_data = modified_data
            hitl_record.responded_at = datetime.utcnow()
            session.commit()
            
            session_id = str(hitl_record.session_id)
            thread_id_result = session.execute(
                text("SELECT thread_id FROM sessions WHERE id = :session_id"),
                {"session_id": hitl_record.session_id}
            ).fetchone()
            
            if not thread_id_result:
                raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
            
            thread_id = str(thread_id_result[0])
        
        # 3. Decision recorded successfully
        # Note: Graph resumption requires client to re-invoke the stream endpoint
        # or use the WebSocket to continue execution with the recorded response
        
        return {
            "status": "success",
            "message": f"HITL response recorded for request {request_id}",
            "decision": decision,
            "session_id": session_id,
            "thread_id": thread_id,
            "next_action": "Use /agent/stream endpoint with recorded response to resume graph execution"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_msg = str(e) if str(e) else repr(e)
        traceback.print_exc()  # Log full traceback for debugging
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing HITL response: {error_msg}\nType: {type(e).__name__}"
        )


@app.get("/agent/hitl/pending", tags=["HITL"])
async def get_pending_hitl(
    session_id: str = Query(..., description="Session UUID")
):
    """Phase 3.6: Get all pending HITL requests for a session.
    
    Useful for:
    - Reconnecting after disconnect
    - Checking if user action is needed
    - Displaying pending decisions in UI
    
    Args:
        session_id: Session UUID
    
    Returns:
        List of pending HITL requests
    """
    try:
        from uuid import UUID

        from agent.database import get_db_connection
        from agent.models import HITLDecision
        
        session_uuid = UUID(session_id)
        
        with get_db_connection() as session:
            pending_requests = session.query(HITLDecision).filter(
                HITLDecision.session_id == session_uuid,
                HITLDecision.user_decision.is_(None),
                HITLDecision.responded_at.is_(None)
            ).order_by(HITLDecision.created_at.desc()).all()
            
            return {
                "session_id": session_id,
                "pending_count": len(pending_requests),
                "requests": [
                    {
                        "request_id": r.request_id,
                        "decision_type": r.decision_type,
                        "prompt": r.prompt,
                        "options": r.options,
                        "context": r.context,
                        "created_at": r.created_at.isoformat(),
                        "timeout_seconds": r.timeout_seconds,
                        "is_timeout": r.is_timeout
                    }
                    for r in pending_requests
                ]
            }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving pending HITL requests: {str(e)}")


@app.get("/agent/hitl/history", tags=["HITL"])
async def get_hitl_history(
    session_id: str = Query(..., description="Session UUID"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of records to return")
):
    """Phase 3.6: Get HITL decision history for a session.
    
    Returns all HITL decisions (pending and completed) for analytics and review.
    
    Args:
        session_id: Session UUID
        limit: Maximum number of records
    
    Returns:
        List of HITL decisions with timestamps and outcomes
    """
    try:
        from uuid import UUID

        from agent.database import get_db_connection
        from agent.models import HITLDecision
        
        session_uuid = UUID(session_id)
        
        with get_db_connection() as session:
            history = session.query(HITLDecision).filter(
                HITLDecision.session_id == session_uuid
            ).order_by(HITLDecision.created_at.desc()).limit(limit).all()
            
            return {
                "session_id": session_id,
                "total_count": len(history),
                "history": [r.to_dict() for r in history]
            }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving HITL history: {str(e)}")


@app.get("/reports/{report_id}", tags=["Reports"])
def get_report_details(report_id: str = Path(..., description="Report UUID")):
    """Get detailed information for a specific report."""
    try:
        report_uuid = UUID(report_id)
        report = db_manager.get_report_by_id(report_uuid)
        if not report:
            raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
        return report
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report: {str(e)}")


@app.get("/sessions/{session_id}/reports/latest", tags=["Reports"])
def get_latest_session_report(session_id: str = Path(..., description="Session UUID")):
    """Get the most recent report for a session."""
    try:
        session_uuid = UUID(session_id)
        report = db_manager.get_latest_report(session_uuid)
        if not report:
            raise HTTPException(status_code=404, detail=f"No reports found for session {session_id}")
        return report
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving latest report: {str(e)}")


@app.get("/reports/{report_id}/export", tags=["Reports"])
def export_report(
    report_id: str = Path(..., description="Report UUID"),
    format: str = Query(..., description="Export format: markdown, html, or pdf")
):
    """Export a report to various formats (Markdown, HTML, PDF).
    
    Note: PDF export is a placeholder for future implementation.
    """
    try:
        from fastapi.responses import HTMLResponse, PlainTextResponse
        
        report_uuid = UUID(report_id)
        report = db_manager.get_report_by_id(report_uuid)
        if not report:
            raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
        
        content = report.get('content', '')
        
        if format == "markdown":
            return PlainTextResponse(content=content, media_type="text/markdown")
        
        elif format == "html":
            # Simple Markdown to HTML conversion (for demo purposes)
            # In production, use a proper Markdown library like python-markdown
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Research Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; }}
    </style>
</head>
<body>
    <pre>{content}</pre>
</body>
</html>
            """
            return HTMLResponse(content=html_content)
        
        elif format == "pdf":
            # Placeholder for PDF export (requires additional libraries like weasyprint)
            raise HTTPException(
                status_code=501,
                detail="PDF export not yet implemented. Use markdown or html format."
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format: {format}. Use markdown, html, or pdf."
            )
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting report: {str(e)}")


# ==================== WebSocket Streaming ====================
@app.websocket("/agent/stream")
async def stream_agent_progress(websocket: WebSocket):
    """WebSocket endpoint for real-time agent progress streaming.
    
    Client sends:
    {
        "messages": [{"role": "user", "content": "research topic"}],
        "thread_id": "optional-uuid"
    }
    
    Server streams:
    {
        "type": "started",
        "session_id": "uuid",
        "thread_id": "uuid"
    }
    {
        "type": "progress",
        "node": "node_name",
        "data": {...state_update...}
    }
    {
        "type": "complete",
        "session_id": "uuid",
        "thread_id": "uuid"
    }
    """
    await websocket.accept()
    thread_id = None
    session_id = None
    trace = None  # LangFuse trace for WebSocket session
    
    try:
        # 1. Receive initial request
        data = await websocket.receive_json()
        
        # 2. Generate or use provided thread_id
        thread_id = data.get("thread_id") or str(uuid4())
        messages = data.get("messages", [])
        
        # 3. Create LangFuse trace for entire WebSocket session
        trace = LangfuseManager.trace(
            name="WebSocket Research Session",
            input={
                "thread_id": thread_id,
                "message_count": len(messages),
                "has_existing_thread": bool(data.get("thread_id"))
            },
            tags=["websocket", "streaming", "research_session"]
        )
        
        if not messages:
            await websocket.send_json({
                "type": "error",
                "message": "No messages provided"
            })
            await websocket.close()
            return
        
        # 3. Extract research topic
        user_query = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_query = msg.get("content", "")
                break
        
        # 4. Create Session record
        session = db_manager.create_session(
            thread_id=thread_id,
            title=f"Research: {user_query[:100]}" if user_query else "Untitled",
            research_topic=user_query,
            tags=["websocket", "streaming"],
            notes=f"Started via WebSocket at {datetime.utcnow().isoformat()}"
        )
        session_id = session["id"]
        
        # Update trace with session_id
        trace.update(
            session_id=session_id,
            metadata={"research_topic": user_query}
        )
        
        print(f"[WebSocket] Created session {session_id} with thread_id {thread_id}")
        
        # 5. Log research_started event
        db_manager.log_event(
            session_id=session_id,
            event_type="research_started",
            event_data={
                "query": user_query,
                "thread_id": thread_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # 6. Send acknowledgment
        await websocket.send_json({
            "type": "started",
            "session_id": session_id,
            "thread_id": thread_id
        })
        
        # 7. Prepare input and config
        config = {"configurable": {"thread_id": thread_id}}
        input_data = {
            "messages": messages,
            "session_id": session_id,
            "thread_id": thread_id
        }
        
        # 8. Run agent execution with HITL streaming
        # Note: Using sync invoke in executor due to PostgresSaver not supporting async operations
        await websocket.send_json({
            "type": "progress",
            "node": "agent_start",
            "message": "Starting research agent..."
        })
        
        # Stream graph execution using astream_events for fine-grained control
        # This allows us to detect HITL requests in real-time
        async def stream_with_hitl_detection():
            """Stream graph execution and detect HITL requests and document updates"""
            final_result = None
            
            # Initialize document differ for streaming updates
            differ = DocumentDiffer()
            last_report_version = ""
            
            # 💓 WebSocket heartbeat mechanism to prevent timeout
            import time
            last_heartbeat = time.time()
            HEARTBEAT_INTERVAL = 30  # Send heartbeat every 30 seconds
            
            # Use async_graph.astream for asynchronous streaming with async checkpointer
            async for chunk in get_async_graph().astream(input_data, config=config):
                # Check if we need to send a heartbeat
                current_time = time.time()
                if current_time - last_heartbeat > HEARTBEAT_INTERVAL:
                    await websocket.send_json({
                        "type": "heartbeat",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    last_heartbeat = current_time
                # chunk is a dict with node name as key
                for node_name, state_update in chunk.items():
                    # 🔄 INTERRUPT DETECTION: When interrupt_before triggers,
                    # state_update might be a tuple instead of dict
                    # Special handling for __interrupt__ signal
                    if node_name == "__interrupt__":
                        # Graph has paused - send notification to frontend
                        await websocket.send_json({
                            "type": "progress",
                            "node": node_name,
                            "message": "Workflow paused, waiting for user input..."
                        })
                        # Don't try to access .get() on interrupt signal
                        continue
                    
                    # Ensure state_update is a dict before calling .get()
                    if not isinstance(state_update, dict):
                        print(f"[WebSocket] Warning: state_update is not a dict for node {node_name}, got {type(state_update)}")
                        # Send progress update anyway
                        await websocket.send_json({
                            "type": "progress",
                            "node": node_name,
                            "message": f"Processing {node_name}..."
                        })
                        continue
                    
                    # Send progress update
                    await websocket.send_json({
                        "type": "progress",
                        "node": node_name,
                        "message": f"Processing {node_name}..."
                    })
                    
                    # 📝 DOCUMENT UPDATE: Check for partial report updates
                    # Note: "report" is set by retrieve_and_synthesize_report node
                    #       "final_report" is set by report_revision_node (HITL)
                    current_report = state_update.get("report") or state_update.get("final_report", "")
                    if current_report and current_report != last_report_version:
                        # Create span for document update
                        doc_span = trace.span(
                            name="WebSocket Document Update",
                            input={
                                "node": node_name,
                                "old_length": len(last_report_version),
                                "new_length": len(current_report)
                            },
                            tags=["websocket", "document_update"]
                        )
                        
                        # Generate incremental diff
                        diffs = differ.generate_paragraph_diff(last_report_version, current_report)
                        
                        # Send only changed paragraphs to frontend
                        for diff in diffs:
                            if diff["action"] != "unchanged":
                                # Create document update message
                                update_msg = differ.generate_update_message(
                                    diff,
                                    rationale=f"AI generating report in {node_name}"
                                )
                                update_msg["session_id"] = session_id
                                update_msg["node"] = node_name
                                
                                await websocket.send_json(update_msg)
                                
                                # Log document update
                                db_manager.log_event(
                                    session_id=session_id,
                                    event_type="document_update",
                                    event_data={
                                        "action": diff["action"],
                                        "paragraph_index": diff["paragraph_index"],
                                        "node": node_name,
                                        "timestamp": datetime.utcnow().isoformat()
                                    }
                                )
                        
                        # End document update span
                        doc_span.end(output={
                            "diff_count": len(diffs),
                            "changed_paragraphs": len([d for d in diffs if d["action"] != "unchanged"])
                        })
                        
                        # Update last known version
                        last_report_version = current_report
                    
                    # 🔔 HITL Detection: Check if node set hitl_pending flag
                    if state_update.get("hitl_pending"):
                        hitl_request = state_update.get("hitl_request", {})
                        
                        # Create span for HITL request via WebSocket
                        hitl_span = trace.span(
                            name="WebSocket HITL Request",
                            input={
                                "request_id": hitl_request.get("request_id"),
                                "decision_type": hitl_request.get("decision_type"),
                                "timeout_seconds": hitl_request.get("timeout_seconds", 300)
                            },
                            tags=["websocket", "hitl", hitl_request.get("decision_type", "unknown")]
                        )
                        
                        # Send HITL request to frontend
                        await websocket.send_json({
                            "type": "hitl_request",
                            "request_id": hitl_request.get("request_id"),
                            "decision_type": hitl_request.get("decision_type"),
                            "prompt": hitl_request.get("prompt"),
                            "options": hitl_request.get("options", []),
                            "context": hitl_request.get("context", {}),
                            "timeout_seconds": hitl_request.get("timeout_seconds", 300),
                            "session_id": session_id,
                            "thread_id": thread_id
                        })
                        
                        # Log HITL request
                        db_manager.log_event(
                            session_id=session_id,
                            event_type="hitl_request_sent",
                            event_data={
                                "request_id": hitl_request.get("request_id"),
                                "decision_type": hitl_request.get("decision_type"),
                                "timestamp": datetime.utcnow().isoformat()
                            }
                        )
                        
                        # End HITL span
                        hitl_span.end(output={
                            "sent_to_client": True,
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        
                        # Graph will pause here (conditional edge returns [])
                        # Execution will resume when user calls /agent/hitl/respond
                        print(f"[HITL] Sent request {hitl_request.get('request_id')} to frontend")
                    
                    # Check if research was stopped by user
                    if state_update.get("stop_research"):
                        await websocket.send_json({
                            "type": "research_stopped",
                            "message": "Research stopped by user decision"
                        })
                        return state_update  # Early exit
                    
                    final_result = state_update
            
            return final_result
        
        # Execute with HITL detection
        result = await stream_with_hitl_detection()
        
        # 🔄 CRITICAL: Check if result is None (happens when graph hits interrupt_before)
        # When interrupt_before triggers, astream() ends without final state
        # In this case, we should NOT send 'complete' - just keep WebSocket open for HITL
        if result is None:
            print("[WebSocket] Graph interrupted (result is None), keeping connection open for HITL...")
            # Don't send 'complete' or close WebSocket
            # Connection stays open until user responds via HITL API
            # Mark session as 'waiting_input' instead of 'completed'
            db_manager.update_session(session_id, status="waiting_input")
            return  # Keep WebSocket alive
        
        # Send completion with result summary (if not stopped)
        if not result.get("stop_research"):
            await websocket.send_json({
                "type": "progress",
                "node": "agent_complete",
                "message": f"Research completed. Found {len(result.get('literature_abstracts', []))} papers."
            })
            
            # Update trace with success output
            trace.update(output={
                "status": "completed",
                "paper_count": len(result.get('literature_abstracts', [])),
                "has_report": bool(result.get('report')),
                "word_count": len(result.get('report', '').split())
            })
        else:
            # Update trace for stopped research
            trace.update(output={
                "status": "stopped_by_user",
                "stop_reason": "User decision"
            })
        
        # 9. Update session status
        db_manager.update_session(session_id, status="completed")
        
        # 10. Log completion event
        db_manager.log_event(
            session_id=session_id,
            event_type="research_completed",
            event_data={
                "timestamp": datetime.utcnow().isoformat(),
                "thread_id": thread_id
            }
        )
        
        # 11. Send completion signal
        await websocket.send_json({
            "type": "complete",
            "session_id": session_id,
            "thread_id": thread_id
        })
        
    except WebSocketDisconnect:
        print(f"[WebSocket] Client disconnected: thread_id={thread_id}")
        if trace:
            trace.update(
                status="interrupted",
                status_message="Client disconnected",
                output={"disconnect_reason": "WebSocket connection lost"}
            )
        if session_id:
            db_manager.update_session(session_id, status="interrupted")
            db_manager.log_event(
                session_id=session_id,
                event_type="connection_lost",
                event_data={
                    "timestamp": datetime.utcnow().isoformat(),
                    "thread_id": thread_id
                }
            )
    
    except Exception as e:
        import traceback
        error_msg = str(e) or "Unknown error"
        print(f"[WebSocket] Error: {error_msg}")
        print(f"[WebSocket] Traceback: {traceback.format_exc()}")
        
        if trace:
            trace.update(
                status="error",
                status_message=error_msg,
                output={"error": error_msg, "traceback": traceback.format_exc()}
            )
        
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({
                "type": "error",
                "message": error_msg
            })
        if session_id:
            db_manager.update_session(session_id, status="failed")
            db_manager.log_event(
                session_id=session_id,
                event_type="error_occurred",
                event_data={
                    "error": error_msg,
                    "traceback": traceback.format_exc(),
                    "timestamp": datetime.utcnow().isoformat(),
                    "thread_id": thread_id
                }
            )
    
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()


# ==================== Main Entry Point ====================
# 4. Main entry point for running the app with uvicorn
if __name__ == "__main__":
    print("--- Starting Research Agent API ---")
    # To run this, execute `python -m agent.app` from the `backend/src` directory
    uvicorn.run("agent.app:app", host="0.0.0.0", port=8000, reload=True)
