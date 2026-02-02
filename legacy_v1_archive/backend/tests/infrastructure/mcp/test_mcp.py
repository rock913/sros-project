import pytest
from fastapi.testclient import TestClient
from agent.infrastructure.mcp.fastapi_adapter import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, MCP!"}

# Add more tests as needed
