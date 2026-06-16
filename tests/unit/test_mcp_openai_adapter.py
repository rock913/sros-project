"""Tests for MCP-to-OpenAI Function Calling Adapter"""

import pytest
from sros.gateway.mcp_openai_adapter import (
    mcp_tools_to_openai,
    openai_tool_call_to_mcp,
    build_deepseek_request,
)


class TestMcpToolsToOpenAI:
    def test_basic_conversion(self):
        mcp_tools = [
            {
                "name": "sros_db_query",
                "description": "Execute SQL query",
                "inputSchema": {
                    "type": "object",
                    "properties": {"sql": {"type": "string"}},
                    "required": ["sql"],
                },
            }
        ]
        result = mcp_tools_to_openai(mcp_tools)
        assert len(result) == 1
        assert result[0]["type"] == "function"
        assert result[0]["function"]["name"] == "sros_db_query"
        assert result[0]["function"]["description"] == "Execute SQL query"
        assert result[0]["function"]["parameters"]["required"] == ["sql"]
        assert result[0]["function"]["parameters"]["properties"]["sql"]["type"] == "string"

    def test_multiple_tools(self):
        mcp_tools = [
            {"name": "tool_a", "description": "Tool A", "inputSchema": {}},
            {"name": "tool_b", "description": "Tool B", "inputSchema": {}},
        ]
        result = mcp_tools_to_openai(mcp_tools)
        assert len(result) == 2
        assert result[0]["function"]["name"] == "tool_a"
        assert result[1]["function"]["name"] == "tool_b"

    def test_no_required_params(self):
        mcp_tools = [
            {
                "name": "simple_tool",
                "description": "No required params",
                "inputSchema": {
                    "type": "object",
                    "properties": {"opt": {"type": "integer"}},
                },
            }
        ]
        result = mcp_tools_to_openai(mcp_tools)
        assert "required" not in result[0]["function"]["parameters"]


class TestOpenAIToolCallToMcp:
    def test_string_arguments(self):
        tool_call = {"function": {"name": "sros_db_query", "arguments": '{"sql": "SELECT 1"}'}}
        result = openai_tool_call_to_mcp(tool_call)
        assert result["method"] == "tools/call"
        assert result["params"]["name"] == "sros_db_query"
        assert result["params"]["arguments"] == {"sql": "SELECT 1"}

    def test_dict_arguments(self):
        tool_call = {"function": {"name": "test_tool", "arguments": {"x": 42}}}
        result = openai_tool_call_to_mcp(tool_call)
        assert result["params"]["arguments"] == {"x": 42}

    def test_flat_structure(self):
        """Test tool_call without nested 'function' key"""
        tool_call = {"name": "flat_tool", "arguments": '{"y": 1}'}
        result = openai_tool_call_to_mcp(tool_call)
        assert result["params"]["name"] == "flat_tool"


class TestBuildDeepSeekRequest:
    def test_basic_request(self):
        body = build_deepseek_request(
            model="deepseek-v4-pro",
            messages=[{"role": "user", "content": "Hello"}],
            system_prompt="You are helpful.",
        )
        assert body["model"] == "deepseek-v4-pro"
        assert body["stream"] is False
        assert body["messages"][0]["role"] == "system"
        assert body["messages"][1]["role"] == "user"
        assert "tools" not in body  # no mcp_tools provided

    def test_with_tools(self):
        mcp_tools = [
            {
                "name": "sros_db_query",
                "description": "Execute SQL",
                "inputSchema": {
                    "type": "object",
                    "properties": {"sql": {"type": "string"}},
                },
            }
        ]
        body = build_deepseek_request(mcp_tools=mcp_tools)
        assert "tools" in body
        assert body["tool_choice"] == "auto"
        assert body["tools"][0]["type"] == "function"

    def test_stream_mode(self):
        body = build_deepseek_request(stream=True)
        assert body["stream"] is True


class TestRoundtrip:
    """MCP tools → OpenAI → MCP call 无损往返"""

    def test_roundtrip(self):
        mcp_tools = [
            {
                "name": "test_tool",
                "description": "Test",
                "inputSchema": {
                    "type": "object",
                    "properties": {"x": {"type": "integer"}},
                },
            }
        ]
        openai_tools = mcp_tools_to_openai(mcp_tools)
        # 模拟 DeepSeek 返回的 tool_call
        mock_response = {"function": {"name": "test_tool", "arguments": '{"x": 42}'}}
        mcp_call = openai_tool_call_to_mcp(mock_response)
        assert mcp_call["params"]["name"] == "test_tool"
        assert mcp_call["params"]["arguments"] == {"x": 42}
