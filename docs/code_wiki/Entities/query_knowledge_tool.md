---
kind: entity
type: function
aliases: []
tags: []
---

# query_knowledge_tool

## 概要 (Description)
MCP工具：接收查询字符串（query: str）和可选限制数（limit: int=10），调用MemoryProtocol.query_knowledge返回结果JSON

## 关系 (Relations)
- (depends_on) [[MemoryProtocol]] — 调用service.query_knowledge方法

## 关联 (Related)
- [[MCP服务器]]
- [[工具注册模式]]
- [[get_memory_service]]
- [[create_memory_server]]
- [[main]]
- [[store_knowledge_tool]]
- [[get_citation_map_tool]]
- [[模型上下文协议MCP服务器]]
- [[MemoryProtocol]]
- [[KnowledgeEdge]]
## Sources
- [[server]]
