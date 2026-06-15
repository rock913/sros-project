---
kind: entity
type: function
aliases: []
tags: []
---

# _ingest_participants

## 概要 (Description)
解析 participants.tsv 并填充 subjects 表。返回插入的行数。副作用：对 subjects 表执行 INSERT OR REPLACE。
## 关联 (Related)
- [[数据摄取工作流]]
- [[DBHandler]]
- [[init_schema]]
- [[ingest]]
- [[_ingest_bids]]
- [[_ingest_clinical]]
- [[query]]
- [[_serialize_rows]]
## Sources
- [[handler]]
