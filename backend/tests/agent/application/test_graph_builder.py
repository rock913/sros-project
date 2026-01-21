import pytest
from unittest.mock import MagicMock, patch
from agent.application.graph_builder import build_graph, AppConfig
from agent.infrastructure.tools.scholar_adapter import get_scholar_tool
from agent.infrastructure.tools.unpaywall_adapter import get_unpaywall_tool
from agent.infrastructure.mcp.server import FastMcpServer

def test_build_graph_registers_tools():
    # Arrange
    config = AppConfig()
    mcp_server_mock = MagicMock(spec=FastMcpServer)
    scholar_tool_mock = MagicMock()
    unpaywall_tool_mock = MagicMock()

    with patch('agent.application.graph_builder.FastMcpServer', return_value=mcp_server_mock), \
         patch('agent.application.graph_builder.get_scholar_tool', return_value=scholar_tool_mock), \
         patch('agent.application.graph_builder.get_unpaywall_tool', return_value=unpaywall_tool_mock):
        
        # Act
        graph = build_graph(config)

        # Assert
        mcp_server_mock.register_tool.assert_any_call(scholar_tool_mock)
        mcp_server_mock.register_tool.assert_any_call(unpaywall_tool_mock)
        assert mcp_server_mock.register_tool.call_count == 2
