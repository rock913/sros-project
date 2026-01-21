import unittest
from unittest.mock import MagicMock, patch
from fastmcp import FastMCP  # Assuming this is the FastMCP library
from agent.infrastructure.mcp.server import FastMcpServer
from agent.domain.schemas.mcp import McpTool

class TestFastMcpServer(unittest.TestCase):

    @patch('agent.infrastructure.mcp.server.FastMCP')
    def setUp(self, MockFastMCP):
        self.mock_fastmcp = MockFastMCP()
        self.server = FastMcpServer(self.mock_fastmcp)

    def test_registration_success(self):
        tool = McpTool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}},
            handler=lambda: None
        )
        self.server.register_tool(tool)
        self.mock_fastmcp.add_tool.assert_called_once_with(tool.name, tool.handler)

    def test_duplicate_registration(self):
        tool = McpTool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}},
            handler=lambda: None
        )
        self.server.register_tool(tool)
        with self.assertRaises(ValueError):
            self.server.register_tool(tool)

    def test_list_tools(self):
        tool1 = McpTool(
            name="test_tool1",
            description="A test tool",
            input_schema={"type": "object", "properties": {}},
            handler=lambda: None
        )
        tool2 = McpTool(
            name="test_tool2",
            description="Another test tool",
            input_schema={"type": "object", "properties": {}},
            handler=lambda: None
        )
        self.server.register_tool(tool1)
        self.server.register_tool(tool2)
        tools = self.server.list_tools()
        self.assertEqual(len(tools), 2)
        self.assertIn(tool1, tools)
        self.assertIn(tool2, tools)

    def test_start_server(self):
        self.server.start()
        self.mock_fastmcp.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()
