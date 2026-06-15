---
kind: concept
aliases:
- command dispatcher
- name-based routing
tags:
- architecture
---

# Tool Dispatch Pattern

## 概要 (Description)
A centralized routing mechanism where a single function maps tool names (e.g., 'plugins.list', 'tasks.run_plugin_async') to specific handler implementations, enabling thin gateways and dynamic extensibility.
## 关联 (Related)
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
- [[ScholarHandler]]
## Sources
- [[rpc]]
