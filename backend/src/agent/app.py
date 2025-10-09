import asyncio
import uvicorn
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Correctly import the 'graph' object from agent.graph
from agent.graph import graph
from agent.database import init_db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

# 1. Define Pydantic models for API input and output
class AgentInput(BaseModel):
    """The serializable input schema for the agent."""
    messages: List[Dict[str, Any]] = Field(description="The history of messages in the conversation.")

class AgentOutput(BaseModel):
    """The serializable output schema for the agent."""
    messages: List[Dict[str, Any]] = Field(description="The history of messages in the conversation.")
    research_topic: str = Field(description="The initial research topic.")
    search_queries: List[str] = Field(description="The search queries generated.")
    literature_abstracts: List[Dict[str, Any]] = Field(description="List of retrieved literature abstracts.")
    literature_full_text: List[str] = Field(description="List of URLs for full text literature.")
    is_sufficient: bool = Field(description="Whether the research is sufficient.")
    knowledge_gap: str = Field(description="The identified knowledge gap.")
    report: str = Field(description="The final generated report.")

# 2. Initialize the FastAPI app
app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API for an autonomous research agent powered by LangGraph and Gemini.",
    version="1.0.0",
)

# 3. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Add the compiled graph to the app, using the explicit input and output schemas
add_routes(
    app, 
    graph.with_types(input_type=AgentInput, output_type=AgentOutput), 
    path="/agent"
)

# 5. Startup event to initialize the database
@app.on_event("startup")
async def on_startup():
    """Initializes the database."""
    print("--- Initializing database ---")
    init_db()
    print("--- Database initialized ---")

# 6. Add a health check endpoint
@app.get("/ok")
def ok():
    """Health check endpoint."""
    return {"status": "ok"}

# 7. Main entry point for running the app with uvicorn
if __name__ == "__main__":
    print("--- Starting Research Agent API ---")
    # To run this, execute `python -m agent.app` from the `backend/src` directory
    uvicorn.run("agent.app:app", host="0.0.0.0", port=8000, reload=True)
