---
kind: entity
type: function
aliases:
- 查询
tags: []
---

# RagHandlerquery

## 概要 (Description)
执行查询：接收query和top_k参数，从DuckDB中读取所有块，基于词法匹配（查询词与块文本中的词）计算分数，按分数降序返回top_k个RagChunk。
## 关联 (Related)
- [[External RAG Services]]
- [[RagChunk]]
- [[RagHandler]]
- [[RagHandlerbuild]]
- [[_iter_files]]
- [[_chunk_text]]
- [[_workspace_root]]
- [[_resolve_ws_path]]
## Sources
- [[handler]]
