---
kind: entity
type: function
aliases: []
tags: []
---

# _ingest_clinical

## 概要 (Description)
解析临床 Excel 文件并填充 clinical_data 表。返回插入的行数。副作用：对 clinical_data 表执行 INSERT OR REPLACE。
## 关联 (Related)
- [[数据摄取工作流]]
- [[DBHandler]]
- [[init_schema]]
- [[ingest]]
- [[_ingest_participants]]
- [[_ingest_bids]]
- [[query]]
- [[_serialize_rows]]
## Sources
- [[handler]]
