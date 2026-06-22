> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-MCP-OpenAI-Adapter.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：MCP-to-OpenAI Adapter — DeepSeek v4 Pro 协议适配层

> 目标主 PRD：`01-Core_Infra/SROS/docs/PRD.md`
> 提案日期：2026-06-15
> 驱动来源：`meta-docs/strategy/upgrade-notes/0615-DeepSeek v4 Pro 架构适配与非对称成本优势指南.md`

## 动机 (Why)

主控模型已确立为 DeepSeek v4 Pro。DeepSeek 的 API 完全兼容 OpenAI 格式（`tools` 和 `tool_choice` 字段），但 SROS 的 MCP Gateway 按 Anthropic MCP 标准输出 JSON-RPC 格式的工具列表。两者之间存在协议断层：

- **MCP 输出**：`jsonrpc: "2.0", method: "tools/list"` → `[{name, description, inputSchema}]`
- **DeepSeek 期望**：OpenAI Function Calling 格式 → `[{type: "function", function: {name, description, parameters}}]`

如果不加适配层，Hermes 或飞书桥接进程在调用 DeepSeek 时将无法正确传递 SROS 工具列表。当前系统对 Claude 系模型有隐性耦合——MCP 是 Anthropic 发起的标准，Claude SDK 原生支持。切换到 DeepSeek 后这条链路会断裂。

**核心洞察**：SROS Gateway 的 MCP 实现保持不变（保持对外的先进性和标准化），只需在中间件层增加一个轻量级的 Python 翻译脚本。

## 提议内容

### Task 1: MCP-to-OpenAI Adapter (2d)

**新增文件** (`src/sros/gateway/mcp_openai_adapter.py`)：

```python
"""
MCP-to-OpenAI Function Calling Adapter
将 SROS MCP JSON-RPC 工具列表翻译为 OpenAI/DeepSeek tools 参数格式
"""

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
    """MCP inputSchema → OpenAI parameters (JSON Schema 子集)"""
    params = {
        "type": schema.get("type", "object"),
        "properties": schema.get("properties", {}),
    }
    if "required" in schema:
        params["required"] = schema["required"]
    return params


def openai_tool_call_to_mcp(tool_call: dict) -> dict:
    """OpenAI tool_call 响应 → MCP tools/call 请求参数"""
    return {
        "method": "tools/call",
        "params": {
            "name": tool_call["function"]["name"],
            "arguments": _parse_arguments(tool_call["function"].get("arguments", "{}")),
        }
    }


def _parse_arguments(args):
    """安全解析 JSON string arguments"""
    import json
    if isinstance(args, str):
        return json.loads(args)
    return args


def build_deepseek_request(
    model: str = "deepseek-v4-pro",
    messages: list[dict] = None,
    mcp_tools: list[dict] = None,
    system_prompt: str = "",
    stream: bool = False,
) -> dict:
    """构建完整的 DeepSeek API 请求体"""
    body = {
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
```

### Task 2: Gateway 适配端点 (1d)

**扩展** (`src/sros/gateway/main.py`)：

新增 `/api/v1/mcp/openai-tools` 端点，直接返回 OpenAI 兼容格式的工具列表：

```python
@gw_app.get("/api/v1/mcp/openai-tools")
async def list_tools_openai():
    """返回 OpenAI Function Calling 格式的工具列表 (供 DeepSeek 消费)"""
    from sros.gateway.mcp_openai_adapter import mcp_tools_to_openai
    from sros.skills.rpc import list_all_tools
    
    mcp_tools = await list_all_tools()
    return {"tools": mcp_tools_to_openai(mcp_tools)}
```

新增 `/api/v1/mcp/call-openai` 端点，接收 OpenAI tool_call 格式并转换为 MCP 调用：

```python
@gw_app.post("/api/v1/mcp/call-openai")
async def call_tool_openai(request: dict):
    """接收 OpenAI tool_call 格式，内部转换为 MCP tools/call"""
    from sros.gateway.mcp_openai_adapter import openai_tool_call_to_mcp
    from sros.skills.rpc import dispatch_tool
    
    mcp_params = openai_tool_call_to_mcp(request)
    result = await dispatch_tool(
        tool_name=mcp_params["params"]["name"],
        arguments=mcp_params["params"]["arguments"]
    )
    return result
```

### Task 3: 测试 + CLI 验证 (0.5d)

```python
# tests/unit/test_mcp_openai_adapter.py
def test_mcp_tools_to_openai_basic():
    mcp_tools = [
        {"name": "sros_db_query", "description": "Execute SQL query", 
         "inputSchema": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}}
    ]
    result = mcp_tools_to_openai(mcp_tools)
    assert result[0]["type"] == "function"
    assert result[0]["function"]["name"] == "sros_db_query"
    assert result[0]["function"]["parameters"]["required"] == ["sql"]

def test_openai_tool_call_to_mcp():
    tool_call = {"function": {"name": "sros_db_query", "arguments": '{"sql": "SELECT 1"}'}}
    result = openai_tool_call_to_mcp(tool_call)
    assert result["method"] == "tools/call"
    assert result["params"]["name"] == "sros_db_query"
    assert result["params"]["arguments"] == {"sql": "SELECT 1"}

def test_roundtrip():
    """MCP tools → OpenAI → MCP call 无损往返"""
    mcp_tools = [
        {"name": "test_tool", "description": "Test", 
         "inputSchema": {"type": "object", "properties": {"x": {"type": "integer"}}}}
    ]
    openai_tools = mcp_tools_to_openai(mcp_tools)
    # 模拟 DeepSeek 返回的 tool_call
    mock_response = {"function": {"name": "test_tool", "arguments": '{"x": 42}'}}
    mcp_call = openai_tool_call_to_mcp(mock_response)
    assert mcp_call["params"]["name"] == "test_tool"
    assert mcp_call["params"]["arguments"] == {"x": 42}
```

## 验收标准

- [ ] `src/sros/gateway/mcp_openai_adapter.py` 存在，含 `mcp_tools_to_openai()` + `openai_tool_call_to_mcp()` + `build_deepseek_request()`
- [ ] `/api/v1/mcp/openai-tools` 端点返回 OpenAI Function Calling 兼容格式
- [ ] `/api/v1/mcp/call-openai` 端点接收 OpenAI tool_call 并正确分发到 MCP handler
- [ ] ≥ 3 个 adapter 单元测试 green（含往返测试）
- [ ] SROS ROADMAP.md 新增 MCP-Adapter 任务并标记 ✅
- [ ] 主 PRD (`docs/PRD.md`) 新增"MCP-to-OpenAI Adapter"章节，描述协议翻译层

## 参考实现

- SROS MCP Gateway 实现：`src/sros/gateway/main.py` — FastAPI + JSON-RPC
- SROS 工具分发器：`src/sros/skills/rpc.py` — `dispatch_tool()` 和 `list_all_tools()`
- 现有 MCP 工具列表：SROS ROADMAP 已记录 7+ MCP tools (db_query, hpc_submit, etc.)
- 策略文档：`meta-docs/strategy/upgrade-notes/0615-DeepSeek v4 Pro 架构适配与非对称成本优势指南.md` — §2.1 MCP 协议翻译层
