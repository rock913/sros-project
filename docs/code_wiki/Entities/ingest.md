---
kind: entity
type: function
aliases:
- 摄取入口
tags: []
---

# ingest

## 概要 (Description)
Main entry point for ingestion: accepts source_dir, bids_dir, participants, clinical, schema_path. Returns dict with counts per table or error. Side effects: database writes.

## 关系 (Relations)
- (calls) [[init_schema]] — ingest calls self.init_schema(schema_path) at the start.
- (calls) [[init_schema]] — ingest 方法内调用 init_schema
- (calls) [[_ingest_participants]] — ingest 方法内调用 _ingest_participants
- (calls) [[_ingest_bids]] — ingest 方法内调用 _ingest_bids
- (calls) [[_ingest_clinical]] — ingest 方法内调用 _ingest_clinical
## 关联 (Related)
- [[Data Ingestion Pipeline]]
- [[DBHandler]]
- [[__init__]]
- [[close]]
- [[init_schema]]
- [[query]]
- [[数据摄取工作流]]
- [[_ingest_participants]]
- [[_ingest_bids]]
- [[_ingest_clinical]]
- [[_serialize_rows]]
## Sources
- [[handler]]
