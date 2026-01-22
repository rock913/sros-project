from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.mcp.fastapi_adapter import FastAPIMcpServerAdapter


def test_registration_of_tools():
    app = FastAPI()
    adapter = FastAPIMcpServerAdapter(app)
    tool = McpTool(
        name="fetch-paper",
        description="Fetch a paper by its ID",
        input_schema={"paper_id": {"type": "string"}},
        handler=lambda paper_id: f"Fetching paper {paper_id}"
    )
    adapter.register_tool(tool)
    assert len(adapter.list_tools()) == 1


def test_duplicate_tool_registration():
    app = FastAPI()
    adapter = FastAPIMcpServerAdapter(app)
    tool = McpTool(
        name="fetch-paper",
        description="Fetch a paper by its ID",
        input_schema={"paper_id": {"type": "string"}},
        handler=lambda paper_id: f"Fetching paper {paper_id}"
    )
    adapter.register_tool(tool)
    with pytest.raises(ValueError):
        adapter.register_tool(tool)


def test_listing_registered_tools():
    app = FastAPI()
    adapter = FastAPIMcpServerAdapter(app)
    tool1 = McpTool(
        name="fetch-paper",
        description="Fetch a paper by its ID",
        input_schema={"paper_id": {"type": "string"}},
        handler=lambda paper_id: f"Fetching paper {paper_id}"
    )
    tool2 = McpTool(
        name="search-papers",
        description="Search for papers by keyword",
        input_schema={"keyword": {"type": "string"}},
        handler=lambda keyword: f"Searching for papers with keyword {keyword}"
    )
    adapter.register_tool(tool1)
    adapter.register_tool(tool2)
    tools = adapter.list_tools()
    assert len(tools) == 2
    assert tools[0].name == "fetch-paper"
    assert tools[1].name == "search-papers"


@patch("agent.infrastructure.mcp.fastapi_adapter.uvicorn.run")
def test_tool_execution_via_server(mock_run):
    app = FastAPI()
    client = TestClient(app)
    adapter = FastAPIMcpServerAdapter(app)
    tool = McpTool(
        name="fetch-paper",
        description="Fetch a paper by its ID",
        input_schema={"paper_id": {"type": "string"}},
        handler=lambda paper_id: f"Fetching paper {paper_id}"
    )
    adapter.register_tool(tool)
    response = client.post("/execute/fetch-paper", json={"paper_id": "123"})
    assert response.status_code == 200
    assert response.json() == "Fetching paper 123"


@patch("agent.infrastructure.mcp.fastapi_adapter.uvicorn.run")
def test_server_lifecycle(mock_run):
    app = FastAPI()
    adapter = FastAPIMcpServerAdapter(app)
    with patch.object(adapter, "start") as mock_start:
        adapter.start()
        mock_start.assert_called_once()
