---
kind: entity
type: function
aliases: []
tags: []
---

# search_citations

## 概要 (Description)
根据关键词对 title、journal、citekey 进行模糊搜索，按年份降序。入参：字符串查询词；出参：Citation 列表。副作用：仅读取数据。

## 关系 (Relations)
- (calls) [[ZoteroHandler]] — self.conn.execute in search_citations

## 关联 (Related)
- [[Schema Migration]]
- [[ZoteroHandler]]
- [[ZoteroProtocol]]
- [[Citation]]
- [[__init__]]
- [[add_citation]]
- [[get_citation]]
- [[__del__]]
- [[持久化存储]]
## Sources
- [[handler]]
