---
kind: entity
type: function
aliases: []
tags: []
---

# brainstorm_perspectives_tool

## 概要 (Description)
MCP tool，接收query字符串，调用ScholarProtocol.brainstorm_perspectives生成多维研究视角，返回JSON序列化的ResearchPerspective列表。

## 关系 (Relations)
- (calls) [[get_scholar_service]] — 调用get_scholar_service()获取service实例
- (calls) [[ScholarProtocol]] — 调用service.brainstorm_perspectives方法
- (depends_on) [[ResearchPerspective]] — 使用ResearchPerspective的dict()方法

## 关联 (Related)
- [[MCP Tool]]
- [[get_scholar_service]]
- [[create_scholar_server]]
- [[main]]
- [[find_critiques_tool]]
- [[federated_search_tool]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[MCP服务器模式]]
- [[懒加载服务初始化]]
## Sources
- [[server]]
