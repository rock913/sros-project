---
kind: entity
type: class
aliases:
- external handler
tags: []
---

# ExtHandler

## 概要 (Description)
静态工具类，封装外部工具调用，目前提供web_scrape方法。入参：url (str), timeout_s (float 可选)；出参：Dict[str, Any] 包含ok (bool), error (str), url (str), title (str 可选), text (str) 等字段

## 关系 (Relations)
- (calls) [[web_scrape]] — ExtHandler 的静态方法 web_scrape 内部调用 requests.get
- (calls) [[web_scrape]] — ExtHandler 类中定义了 web_scrape 静态方法
## 关联 (Related)
- [[Deterministic external tool wrapper]]
- [[web_scrape]]
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
- [[RagHandler]]
- [[ScholarHandler]]
- [[外部工具封装]]
- [[可测试性设计]]
## Sources
- [[rpc]]
- [[handler]]
