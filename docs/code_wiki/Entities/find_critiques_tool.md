---
kind: entity
type: function
aliases: []
tags: []
---

# find_critiques_tool

## 概要 (Description)
MCP tool，接收paper_id字符串，调用ScholarProtocol.find_critiques查找反驳/质疑文献，返回JSON结果。

## 关系 (Relations)
- (calls) [[get_scholar_service]] — 调用get_scholar_service()
- (calls) [[ScholarProtocol]] — 调用service.find_critiques方法

## 关联 (Related)
- [[MCP Tool]]
- [[get_scholar_service]]
- [[create_scholar_server]]
- [[main]]
- [[brainstorm_perspectives_tool]]
- [[federated_search_tool]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[MCP服务器模式]]
- [[懒加载服务初始化]]
## Sources
- [[server]]
