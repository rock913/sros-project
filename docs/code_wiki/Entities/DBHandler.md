---
kind: entity
type: class
aliases:
- 数据库处理器
tags: []
---

# DBHandler

## 概要 (Description)
日志数据库处理器，负责将日志记录写入数据库。

## 关系 (Relations)
- (calls) [[init_schema]] — ingest 方法中调用 self.init_schema(schema_path)
- (calls) [[_ingest_participants]] — ingest 方法中调用 self._ingest_participants(parts_path)
- (calls) [[_ingest_bids]] — ingest 方法中调用 self._ingest_bids(bids_path, ...)
- (calls) [[_ingest_clinical]] — ingest 方法中调用 self._ingest_clinical(clinical_path)

## 关联 (Related)
- [[__init__]]
- [[Data Ingestion Pipeline]]
- [[close]]
- [[init_schema]]
- [[ingest]]
- [[query]]
- [[数据摄取工作流]]
- [[_ingest_participants]]
- [[_ingest_bids]]
- [[_ingest_clinical]]
- [[_serialize_rows]]
## Sources
- [[handler]]
- [[__init__]]
