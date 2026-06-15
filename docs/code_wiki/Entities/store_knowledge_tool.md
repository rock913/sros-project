---
kind: entity
type: function
aliases: []
tags: []
---

# store_knowledge_tool

## 概要 (Description)
MCP工具：接收节点列表（nodes: List[Dict]）和边列表（edges: List[Dict]），转换为KnowledgeEdge对象后调用MemoryProtocol.store_knowledge存储，返回包含成功状态和计数的JSON

## 关系 (Relations)
- (depends_on) [[KnowledgeEdge]] — 使用KnowledgeEdge将字典转换为对象
- (depends_on) [[MemoryProtocol]] — 调用service.store_knowledge方法

## 关联 (Related)
- [[MCP服务器]]
- [[工具注册模式]]
- [[get_memory_service]]
- [[create_memory_server]]
- [[main]]
- [[query_knowledge_tool]]
- [[get_citation_map_tool]]
- [[模型上下文协议MCP服务器]]
- [[MemoryProtocol]]
- [[KnowledgeEdge]]
## Sources
- [[server]]
