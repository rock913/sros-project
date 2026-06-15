---
kind: entity
type: class
aliases:
- config
tags: []
---

# GatewayConfig

## 概要 (Description)
网关配置类，包含端口（port）、主机（host）、SSE端点（sse_endpoint）、MCP服务器列表（mcp_servers）和工作区目录（workspace_dir）等配置项。初始化时从环境变量读取覆盖值，若未设置则使用类默认值。
## 关联 (Related)
- [[环境变量覆盖]]
- [[SSE Transport]]
- [[Tool Registry]]
- [[Reflection Call]]
- [[Thread-Bridge Notification]]
- [[SROSGateway]]
- [[create_app]]
- [[main]]
- [[STATIC_TOOLS]]
- [[SkillReflector]]
- [[mcp_list_tools]]
- [[dispatch_jsonrpc]]
- [[config]]
## Sources
- [[main]]
- [[config]]
