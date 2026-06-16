"""
MCP-to-OpenAI Function Calling Adapter
将 SROS MCP JSON-RPC 工具列表翻译为 OpenAI/DeepSeek tools 参数格式

Proposal: meta-docs/proposals/pending/SROS-MCP-OpenAI-Adapter.md
"""

import json
from typing import Any


def mcp_tools_to_openai(mcp_tools: list[dict]) -> list[dict]:
    """MCP tools/list 响应 → OpenAI tools 参数"""
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": _convert_input_schema(tool.get("inputSchema", {})),
            }
        })
    return openai_tools


def _convert_input_schema(schema: dict) -> dict:
    """MCP inputSchema → OpenAI parameters (JSON Schema subset)"""
    params: dict[str, Any] = {
        "type": schema.get("type", "object"),
        "properties": schema.get("properties", {}),
    }
    if "required" in schema:
        params["required"] = schema["required"]
    return params


def openai_tool_call_to_mcp(tool_call: dict) -> dict:
    """OpenAI tool_call 响应 → MCP tools/call 请求参数"""
    function_info = tool_call.get("function", tool_call)
    return {
        "method": "tools/call",
        "params": {
            "name": function_info["name"],
            "arguments": _parse_arguments(function_info.get("arguments", "{}")),
        }
    }


def _parse_arguments(args: Any) -> Any:
    """安全解析 JSON string arguments"""
    if isinstance(args, str):
        return json.loads(args)
    return args


def build_deepseek_request(
    model: str = "deepseek-v4-pro",
    messages: list[dict] | None = None,
    mcp_tools: list[dict] | None = None,
    system_prompt: str = "",
    stream: bool = False,
) -> dict:
    """构建完整的 DeepSeek API 请求体"""
    body: dict[str, Any] = {
        "model": model,
        "messages": [],
        "stream": stream,
    }

    if system_prompt:
        body["messages"].append({"role": "system", "content": system_prompt})

    if messages:
        body["messages"].extend(messages)

    if mcp_tools:
        body["tools"] = mcp_tools_to_openai(mcp_tools)
        body["tool_choice"] = "auto"

    return body
