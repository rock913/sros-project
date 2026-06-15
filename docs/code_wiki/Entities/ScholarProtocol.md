---
kind: entity
type: class
aliases:
- 学术协议
tags: []
---

# ScholarProtocol

## 概要 (Description)
学术研究协议接口，包含三个抽象方法：brainstorm_perspectives(查询字符串→研究视角列表)、find_critiques(论文ID→质疑文献列表)、federated_search(搜索查询→结果列表)

## 关系 (Relations)
- (manages) [[brainstorm_perspectives]] — 定义为协议的方法
- (manages) [[find_critiques]] — 定义为协议的方法
- (manages) [[federated_search]] — 定义为协议的方法
- (depends_on) [[ResearchPerspective]] — brainstorm_perspectives方法返回List[ResearchPerspective]
- (depends_on) [[SearchQuery]] — federated_search方法接受SearchQuery参数
## 关联 (Related)
- [[研究协议模式]]
- [[brainstorm_perspectives]]
- [[find_critiques]]
- [[federated_search]]
- [[后端切换策略]]
- [[联邦搜索]]
- [[ScholarHandler]]
- [[ResearchPerspective]]
- [[SearchQuery]]
- [[OpenAlexBackend]]
- [[MCP Tool]]
- [[get_scholar_service]]
- [[create_scholar_server]]
- [[main]]
- [[brainstorm_perspectives_tool]]
- [[find_critiques_tool]]
- [[federated_search_tool]]
- [[__init__]]
- [[ManuscriptProtocol]]
- [[MemoryProtocol]]
- [[ZoteroProtocol]]
- [[Scholarly Research Protocol]]
## Sources
- [[__init__]]
- [[server]]
- [[handler]]
- [[scholar_protocol]]
