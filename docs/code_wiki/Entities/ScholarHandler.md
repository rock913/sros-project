---
kind: entity
type: class
aliases:
- scholar handler
tags: []
---

# ScholarHandler

## 概要 (Description)
核心处理器类，负责学术搜索相关逻辑，导入自 .handler 模块。

## 关系 (Relations)
- (implements) [[ScholarProtocol]] — class ScholarHandler(ScholarProtocol)
- (depends_on) [[OpenAlexBackend]] — self._openalex = OpenAlexBackend() 当 backend == 'openalex'
- (depends_on) [[ResearchPerspective]] — brainstorm_perspectives 返回 List[ResearchPerspective]
- (depends_on) [[SearchQuery]] — federated_search 入参为 SearchQuery

## 关联 (Related)
- [[__init__]]
- [[create_scholar_server]]
- [[后端切换策略]]
- [[联邦搜索]]
- [[ScholarProtocol]]
- [[ResearchPerspective]]
- [[SearchQuery]]
- [[OpenAlexBackend]]
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Task Management]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[dispatch_tool]]
- [[discover_plugins]]
- [[run_plugin]]
- [[TasksHandler]]
- [[ManuscriptHandler]]
- [[ExtHandler]]
- [[RagHandler]]
- [[后端选择与回退策略]]
- [[brainstorm_perspectives]]
- [[find_critiques]]
- [[federated_search]]
## Sources
- [[rpc]]
- [[handler]]
- [[__init__]]
