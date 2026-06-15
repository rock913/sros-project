---
kind: entity
type: function
aliases: []
tags: []
---

# add_citation

## 概要 (Description)
插入或替换一条引用记录。入参：Citation 对象；出参：布尔值表示成功与否。副作用：对 citations 表执行 INSERT OR REPLACE。

## 关系 (Relations)
- (calls) [[ZoteroHandler]] — self.conn.execute in add_citation

## 关联 (Related)
- [[Schema Migration]]
- [[ZoteroHandler]]
- [[ZoteroProtocol]]
- [[Citation]]
- [[__init__]]
- [[get_citation]]
- [[search_citations]]
- [[__del__]]
- [[持久化存储]]
## Sources
- [[handler]]
