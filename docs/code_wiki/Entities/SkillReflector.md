---
kind: entity
type: class
aliases: []
tags: []
---

# SkillReflector

## 概要 (Description)
Reflector that dynamically resolves tool names to actual skill implementations. Used by SROSGateway for tool calls.

## 关系 (Relations)
- (depends_on) [[SkillCallResult]] — call 方法返回 SkillCallResult 类型。
- (depends_on) [[SkillCallResult]] — call方法返回SkillCallResult实例
## 关联 (Related)
- [[SSE Transport]]
- [[Tool Registry]]
- [[Reflection Call]]
- [[Thread-Bridge Notification]]
- [[SROSGateway]]
- [[create_app]]
- [[main]]
- [[STATIC_TOOLS]]
- [[GatewayConfig]]
- [[mcp_list_tools]]
- [[dispatch_jsonrpc]]
- [[进程内RPC]]
- [[SkillCallResult]]
- [[call]]
- [[Reflection-based RPC]]
## Sources
- [[skill_reflector]]
- [[main]]
