---
kind: entity
type: function
aliases: []
tags: []
---

# _ingest_bids

## 概要 (Description)
遍历 BIDS 目录树并填充 mri_scans 表。返回插入的记录数。副作用：对 mri_scans 表执行 INSERT OR REPLACE。
## 关联 (Related)
- [[数据摄取工作流]]
- [[DBHandler]]
- [[init_schema]]
- [[ingest]]
- [[_ingest_participants]]
- [[_ingest_clinical]]
- [[query]]
- [[_serialize_rows]]
## Sources
- [[handler]]
