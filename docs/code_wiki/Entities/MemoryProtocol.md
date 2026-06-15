---
kind: entity
type: class
aliases: []
tags: []
---

# MemoryProtocol

## 概要 (Description)
一个typing.Protocol，定义了知识图谱接口。方法包括：store_knowledge(nodes: List[Dict], edges: List[KnowledgeEdge]) -> bool，用于存储知识节点和关系；query_knowledge(query: str, limit: int=10) -> List[Dict]，用于查询知识图谱；get_citation_map(section_id: str) -> List[KnowledgeEdge]，用于获取特定章节的引用关系图。

## 关系 (Relations)
- (depends_on) [[KnowledgeEdge]] — store_knowledge和get_citation_map的方法签名中使用了KnowledgeEdge类型。
- (depends_on) [[KnowledgeEdge]] — store_knowledge和get_citation_map方法使用KnowledgeEdge类型
## 关联 (Related)
- [[内存协议契约]]
- [[KnowledgeEdge]]
- [[__init__]]
- [[ManuscriptProtocol]]
- [[ScholarProtocol]]
- [[ZoteroProtocol]]
- [[知识图谱存储协议]]
- [[store_knowledge]]
- [[query_knowledge]]
- [[get_citation_map]]
- [[DuckDB持久化]]
- [[知识图谱模式]]
- [[MemoryHandler]]
- [[模型上下文协议MCP服务器]]
- [[get_memory_service]]
- [[create_memory_server]]
- [[main]]
- [[store_knowledge_tool]]
- [[query_knowledge_tool]]
- [[get_citation_map_tool]]
## Sources
- [[server]]
- [[handler]]
- [[__init__]]
- [[memory_protocol]]
