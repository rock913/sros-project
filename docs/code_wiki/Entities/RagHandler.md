---
kind: entity
type: class
aliases:
- RAG handler
- RAG处理器
tags: []
---

# RagHandler

## 概要 (Description)
Main RAG handler providing build() and query() methods. Manages DuckDB persistence for document chunks. Side effects: creates DuckDB database file at <workspace>/.sros/graph.db, reads files from workspace, performs web scraping via ExtHandler.

## 关系 (Relations)
- (implements) [[Token Matching Retrieval]] — query() uses token overlap scoring as retrieval algorithm
- (depends_on) [[RagChunk]] — query方法中创建RagChunk对象列表。
- (calls) [[_workspace_root]] — _iter_files和_db_path中调用_workspace_root()。
## 关联 (Related)
- [[Token Matching Retrieval]]
- [[Workspace-Relative Path Validation]]
- [[RagChunk]]
- [[build]]
- [[query]]
- [[RagHandler_ensure_schema]]
- [[RagHandler_iter_files]]
- [[RagHandler_chunk_text]]
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
- [[ScholarHandler]]
- [[RagHandlerbuild]]
- [[RagHandlerquery]]
- [[_iter_files]]
- [[_chunk_text]]
- [[_workspace_root]]
- [[_resolve_ws_path]]
## Sources
- [[rpc]]
- [[handler]]
