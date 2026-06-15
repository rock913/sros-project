---
kind: entity
type: function
aliases: []
tags: []
---

# _validate_citekeys_exist

## 概要 (Description)
Private method. Queries DuckDB `citations` table for missing citekeys, raises ValueError if any are absent. Requires .sros/graph.db in workspace.

## 关系 (Relations)
- (calls) [[resolve_workspace_path]] — Calls resolve_workspace_path? No, but _validate_citekeys_exist reads environment variable and DuckDB path directly. No direct call in source.

## 关联 (Related)
- [[Workspace-relative path resolution]]
- [[Citation validation]]
- [[Figure reference indexing]]
- [[ManuscriptHandler]]
- [[resolve_workspace_path]]
- [[index_figure_references]]
- [[ManuscriptProtocol]]
## Sources
- [[handler]]
