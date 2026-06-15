---
kind: entity
type: function
aliases:
- tool dispatcher
tags: []
---

# dispatch_tool

## 概要 (Description)
Main dispatcher that routes a tool name (string) and arguments (dict) to the appropriate server handler. Returns the handler's result. Performs validation of required arguments and imports handlers lazily.

## 关系 (Relations)
- (calls) [[discover_plugins]] — dispatch_tool imports and calls discover_plugins() for 'plugins.list'.
- (calls) [[run_plugin]] — dispatch_tool imports and calls run_plugin() for 'plugins.run' and 'plugin.*' tools.
- (calls) [[TasksHandler]] — dispatch_tool creates TasksHandler() for 'tasks.*' tools.
- (calls) [[ManuscriptHandler]] — dispatch_tool creates ManuscriptHandler() for 'manuscript.*' tools.
- (calls) [[ExtHandler]] — dispatch_tool calls ExtHandler.web_scrape(url, timeout_s) for 'ext.web_scrape'/'ext.web-scrape'.
- (calls) [[RagHandler]] — dispatch_tool creates RagHandler() for 'rag.*' tools.
- (calls) [[ScholarHandler]] — dispatch_tool creates ScholarHandler() and calls federated_search() for 'scholar.*' tools.

## 关联 (Related)
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Task Management]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[discover_plugins]]
- [[run_plugin]]
- [[TasksHandler]]
- [[ManuscriptHandler]]
- [[ExtHandler]]
- [[RagHandler]]
- [[ScholarHandler]]
## Sources
- [[rpc]]
