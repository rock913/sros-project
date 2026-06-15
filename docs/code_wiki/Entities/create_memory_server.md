---
kind: entity
type: function
aliases: []
tags: []
---

# create_memory_server

## 概要 (Description)
创建内存MCP服务器的工厂函数，具体实现在.server模块

## 关系 (Relations)
- (calls) [[get_memory_service]] — 在store_knowledge_tool、query_knowledge_tool、get_citation_map_tool内部调用get_memory_service()
- (calls) [[get_memory_service]] — 工具函数内部调用get_memory_service()获取服务实例
## 关联 (Related)
- [[__init__]]
- [[MemoryHandler]]
- [[MCP服务器]]
- [[工具注册模式]]
- [[get_memory_service]]
- [[main]]
- [[store_knowledge_tool]]
- [[query_knowledge_tool]]
- [[get_citation_map_tool]]
- [[模型上下文协议MCP服务器]]
- [[MemoryProtocol]]
- [[KnowledgeEdge]]
## Sources
- [[server]]
- [[__init__]]
