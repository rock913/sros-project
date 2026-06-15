---
kind: entity
type: function
aliases: []
tags: []
---

# get_citation

## 概要 (Description)
根据 citekey 查询单条引用。入参：字符串 citekey；出参：Citation 对象，未找到时抛出 ValueError。副作用：仅读取数据。

## 关系 (Relations)
- (calls) [[ZoteroHandler]] — self.conn.execute in get_citation

## 关联 (Related)
- [[Schema Migration]]
- [[ZoteroHandler]]
- [[ZoteroProtocol]]
- [[Citation]]
- [[__init__]]
- [[add_citation]]
- [[search_citations]]
- [[__del__]]
- [[持久化存储]]
## Sources
- [[handler]]
