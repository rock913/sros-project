---
kind: entity
type: class
aliases:
- Gateway
tags: []
---

# SROSGateway

## 概要 (Description)
Main gateway class implementing MCP SSE Hub. Manages SSE sessions, tool registry (TOOLS), and routes. Starts Async pumps for notifications.

## 关系 (Relations)
- (calls) [[SkillReflector]] — self._reflector.call(tool_name, kwargs) in _make_tool
- (depends_on) [[STATIC_TOOLS]] — self._make_tool(name) for each name in STATIC_TOOLS
- (depends_on) [[GatewayConfig]] — self.config = config or GatewayConfig()
- (depends_on) [[STATIC_TOOLS]] — Uses static tool name list to construct tools dynamically
- (depends_on) [[SkillReflector]] — Depends on SkillReflector for dynamic binding

## 关联 (Related)
- [[SSE Transport]]
- [[Tool Registry]]
- [[Reflection Call]]
- [[Thread-Bridge Notification]]
- [[create_app]]
- [[main]]
- [[STATIC_TOOLS]]
- [[SkillReflector]]
- [[GatewayConfig]]
- [[mcp_list_tools]]
- [[dispatch_jsonrpc]]
- [[SSE Hub]]
- [[Thin Reflector]]
- [[SROSGateway__init__]]
- [[SROSGatewaymcp_list_tools]]
- [[SROSGatewaydispatch_jsonrpc]]
- [[SROSGatewaystart]]
## Sources
- [[main]]
