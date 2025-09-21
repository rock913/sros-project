from langserve import add_routes
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from agent.graph import graph
from agent.database import create_db_and_tables

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API for an autonomous research agent powered by LangGraph and Gemini.",
    version="1.0.0",
)

# 2. Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 3. Add the research agent to the app
add_routes(app, graph, path="/research_agent")


# 4. WebSocket endpoint for connection management
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time updates."""
    await websocket.accept()
    try:
        while True:
            # You can implement bi-directional communication here if needed
            await websocket.receive_text()
            await websocket.send_text("Message received")
    except WebSocketDisconnect:
        print("Client disconnected")


# 5. Add a startup event to initialize the database
@app.on_event("startup")
def on_startup():
    """Initializes the database when the application starts."""
    print("--- Initializing database ---")
    create_db_and_tables()
    print("--- Database initialized ---")