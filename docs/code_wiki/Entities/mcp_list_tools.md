---
kind: entity
type: function
aliases:
- list tools
tags: []
---

# mcp_list_tools

## 概要 (Description)
Returns MCP tool definitions with precise inputSchema. Refreshes tool registry, then builds and returns a list of tool objects.

## 关系 (Relations)
- (calls) [[SROSGateway]] — Method of SROSGateway that uses self.TOOLS and self._refresh_tools()

## 关联 (Related)
- [[SSE Transport]]
- [[Tool Registry]]
- [[Reflection Call]]
- [[Thread-Bridge Notification]]
- [[SROSGateway]]
- [[create_app]]
- [[main]]
- [[STATIC_TOOLS]]
- [[SkillReflector]]
- [[GatewayConfig]]
- [[dispatch_jsonrpc]]
## Sources
- [[main]]
