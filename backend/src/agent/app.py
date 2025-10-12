import asyncio
import uvicorn
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Correctly import the 'graph' object from agent.graph
from agent.graph import graph
from agent.database import init_db, get_all_documents
from agent.state import AgentState

from fastapi import FastAPI, HTTPException, Path
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
    """
    try:
        # Convert Pydantic models to dict format expected by LangGraph
        input_data = {
            "messages": [msg.dict() for msg in request.input.messages]
        }
        
        # Prepare config with thread_id if provided
        config = {}
        if request.config and request.config.configurable and request.config.configurable.thread_id:
            config = {
                "configurable": {
                    "thread_id": request.config.configurable.thread_id
                }
            }
        
        # Invoke the graph
        result = await graph.ainvoke(input_data, config=config)
        
        # Convert BaseMessage objects to dicts for JSON serialization
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
        
        # Return the result matching our AgentOutput schema
        return AgentOutput(
            messages=messages,
            research_topic=result.get("research_topic", ""),
            search_queries=result.get("search_queries", []),
            literature_abstracts=result.get("literature_abstracts", []),
            literature_full_text=result.get("literature_full_text", []),
            is_sufficient=result.get("is_sufficient", False),
            knowledge_gap=result.get("knowledge_gap", ""),
            report=result.get("report", "")
        )
    except Exception as e:
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
    )


@app.get("/agent/state/{thread_id}", response_model=AgentOutput, tags=["Agent"])
def get_agent_state_by_thread(
    thread_id: str = Path(..., description="The ID of the conversation thread to fetch.")
):
    """
    Retrieves the current state for a specific research thread.
    
    Note: This implementation currently returns the same data as /agent/state
    since the graph is compiled without a checkpointer. To fully support
    thread-specific state persistence, the graph needs to be compiled with
    a checkpointer (e.g., SqliteSaver or PostgresSaver).
    
    TODO: Implement actual thread-based state retrieval when checkpointer is added.
    """
    # TODO: Implement actual thread-based state retrieval when checkpointer is added
    # For now, return the latest state from the database
    documents = get_all_documents()
    literature_abstracts = [
        {"title": doc.source, "summary": doc.content, "authors": []} for doc in documents
    ]
    
    # If no documents found, return 404
    if not literature_abstracts:
        raise HTTPException(
            status_code=404, 
            detail=f"Thread {thread_id} not found or has no data."
        )
    
    return AgentOutput(
        messages=[],
        research_topic="",
        search_queries=[],
        literature_abstracts=literature_abstracts,
        literature_full_text=[],
        is_sufficient=False,
        knowledge_gap="",
        report="",
    )

# 5. Add a health check endpoint
@app.get("/ok", tags=["Health"])
def ok():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok"}

# 6. Startup event to initialize the database
@app.on_event("startup")
async def on_startup():
    """Initializes the database."""
    print("--- Initializing database ---")
    init_db()
    print("--- Database initialized ---")

# 7. Main entry point for running the app with uvicorn
if __name__ == "__main__":
    print("--- Starting Research Agent API ---")
    # To run this, execute `python -m agent.app` from the `backend/src` directory
    uvicorn.run("agent.app:app", host="0.0.0.0", port=8000, reload=True)
