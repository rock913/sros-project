"""This module contains unit tests for the SimpleMcpServer class."""

from unittest.mock import patch

import pytest

from agent.domain.schemas.mcp import McpTool
from agent.infrastructure.mcp.simple_mcp_server import SimpleMcpServer


class TestSimpleMcpServer:
    """Test suite for the SimpleMcpServer class."""

    @pytest.fixture
    def mcp_tool(self):
        """Fixture to create a sample McpTool instance.

        Returns:
            McpTool: A sample McpTool instance.
        """
        return McpTool(
            name="fetch-paper",
            description="Fetch a research paper",
            input_schema={"paper_id": {"type": "string"}},
            handler=lambda paper_id: f"Fetching paper with ID: {paper_id}"
        )

    @pytest.fixture
    def simple_mcp_server(self):
        """Fixture to create a SimpleMcpServer instance.

        Returns:
            SimpleMcpServer: An instance of SimpleMcpServer.
        """
        return SimpleMcpServer()

    def test_register_tool_success(self, simple_mcp_server, mcp_tool):
        """Test that a tool can be successfully registered.

        Args:
            simple_mcp_server: An instance of SimpleMcpServer.
            mcp_tool: A sample McpTool instance.
        """
        simple_mcp_server.register_tool(mcp_tool)
        assert mcp_tool in simple_mcp_server.list_tools()

    def test_register_tool_duplicate(self, simple_mcp_server, mcp_tool):
        """Test that registering a duplicate tool raises a ValueError.

        Args:
            simple_mcp_server: An instance of SimpleMcpServer.
            mcp_tool: A sample McpTool instance.
        """
        simple_mcp_server.register_tool(mcp_tool)
        with pytest.raises(ValueError):
            simple_mcp_server.register_tool(mcp_tool)

    def test_list_tools(self, simple_mcp_server, mcp_tool):
        """Test that the list_tools method returns the correct list of tools.

        Args:
            simple_mcp_server: An instance of SimpleMcpServer.
            mcp_tool: A sample McpTool instance.
        """
        simple_mcp_server.register_tool(mcp_tool)
        tools = simple_mcp_server.list_tools()
        assert len(tools) == 1
        assert tools[0] == mcp_tool

    @patch("mcp.server.Server")
    def test_start_server(self, MockServer, simple_mcp_server):
        """Test that the start method calls the underlying server's start method.

        Args:
            MockServer: A mock instance of the MCP server.
            simple_mcp_server: An instance of SimpleMcpServer.
        """
        simple_mcp_server.start()
        MockServer.assert_called_once()
