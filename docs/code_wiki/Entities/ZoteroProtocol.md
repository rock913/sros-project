---
kind: entity
type: class
aliases: []
tags: []
---

# ZoteroProtocol

## 概要 (Description)
协议类，定义Zotero引文管理的基本操作接口。方法包括：add_citation(citation: Citation) -> bool，添加引用并返回成功状态；get_citation(citekey: str) -> Citation，根据citekey获取引用；search_citations(query: str) -> List[Citation]，搜索引用并返回列表
## 关联 (Related)
- [[协议接口]]
- [[Schema Migration]]
- [[ZoteroHandler]]
- [[Citation]]
- [[__init__]]
- [[add_citation]]
- [[get_citation]]
- [[search_citations]]
- [[__del__]]
- [[ManuscriptProtocol]]
- [[ScholarProtocol]]
- [[MemoryProtocol]]
- [[协议约定]]
## Sources
- [[__init__]]
- [[handler]]
- [[zotero_protocol]]
