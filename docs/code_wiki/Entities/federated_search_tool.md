---
kind: entity
type: function
aliases: []
tags: []
---

# federated_search_tool

## 概要 (Description)
MCP tool，接收query、max_results、filters，构造SearchQuery，调用ScholarProtocol.federated_search执行联邦搜索，返回JSON结果。

## 关系 (Relations)
- (calls) [[get_scholar_service]] — 调用get_scholar_service()
- (calls) [[ScholarProtocol]] — 调用service.federated_search方法

## 关联 (Related)
- [[MCP Tool]]
- [[get_scholar_service]]
- [[create_scholar_server]]
- [[main]]
- [[brainstorm_perspectives_tool]]
- [[find_critiques_tool]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[MCP服务器模式]]
- [[懒加载服务初始化]]
## Sources
- [[server]]
