---
kind: entity
type: function
aliases: []
tags: []
---

# search_citations_tool

## 概要 (Description)
MCP 工具，接收 query 参数，调用 ZoteroProtocol.search_citations 搜索引用，返回 CallToolResult

## 关系 (Relations)
- (calls) [[get_zotero_service]] — 调用 get_zotero_service() 获取服务并调用 search_citations

## 关联 (Related)
- [[MCP Tool]]
- [[get_zotero_service]]
- [[create_zotero_server]]
- [[main]]
- [[add_citation_tool]]
- [[get_citation_tool]]
## Sources
- [[server]]
