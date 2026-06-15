---
kind: entity
type: function
aliases: []
tags: []
---

# build

## 概要 (Description)
Scans provided source files/directories (only .md, .txt, .bib) and embedded URLs, chunks text via paragraph splitting, inserts chunks into DuckDB with deduplication. Returns {ok, db_path, scanned_files, inserted, chunk_count}.
## 关联 (Related)
- [[Token Matching Retrieval]]
- [[Workspace-Relative Path Validation]]
- [[RagChunk]]
- [[RagHandler]]
- [[query]]
- [[RagHandler_ensure_schema]]
- [[RagHandler_iter_files]]
- [[RagHandler_chunk_text]]
## Sources
- [[handler]]
