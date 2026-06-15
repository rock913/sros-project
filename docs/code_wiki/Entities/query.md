---
kind: entity
type: function
aliases: []
tags: []
---

# query

## 概要 (Description)
(Not shown in code but listed in AST HINTS) Executes SQL query against DuckDB. Expected to take SQL string and return rows.

## 关系 (Relations)
- (calls) [[_serialize_rows]] — query 方法中调用 _serialize_rows

## 关联 (Related)
- [[Data Ingestion Pipeline]]
- [[DBHandler]]
- [[__init__]]
- [[close]]
- [[init_schema]]
- [[ingest]]
- [[Token Matching Retrieval]]
- [[Workspace-Relative Path Validation]]
- [[RagChunk]]
- [[RagHandler]]
- [[build]]
- [[RagHandler_ensure_schema]]
- [[RagHandler_iter_files]]
- [[RagHandler_chunk_text]]
- [[数据摄取工作流]]
- [[_ingest_participants]]
- [[_ingest_bids]]
- [[_ingest_clinical]]
- [[_serialize_rows]]
## Sources
- [[handler]]
