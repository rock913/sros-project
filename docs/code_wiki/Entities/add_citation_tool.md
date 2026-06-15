---
kind: entity
type: function
aliases: []
tags: []
---

# add_citation_tool

## 概要 (Description)
MCP 工具，接收 citekey、title、authors、year、journal、url、bibtex 参数，调用 ZoteroProtocol.add_citation 添加引用，返回 CallToolResult

## 关系 (Relations)
- (calls) [[get_zotero_service]] — 调用 get_zotero_service() 获取服务并调用 add_citation

## 关联 (Related)
- [[MCP Tool]]
- [[get_zotero_service]]
- [[create_zotero_server]]
- [[main]]
- [[get_citation_tool]]
- [[search_citations_tool]]
## Sources
- [[server]]
