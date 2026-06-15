---
kind: entity
type: function
aliases:
- 构建索引
tags: []
---

# RagHandlerbuild

## 概要 (Description)
构建RAG索引：接收sources参数（文件或目录列表），扫描匹配的文件（.md/.txt/.bib），提取文本中的URL并抓取内容，将文本分块后插入DuckDB。返回统计信息（扫描文件数、插入块数等）。

## 关系 (Relations)
- (calls) [[_resolve_ws_path]] — build方法中调用_resolve_ws_path(src)。

## 关联 (Related)
- [[External RAG Services]]
- [[RagChunk]]
- [[RagHandler]]
- [[RagHandlerquery]]
- [[_iter_files]]
- [[_chunk_text]]
- [[_workspace_root]]
- [[_resolve_ws_path]]
## Sources
- [[handler]]
