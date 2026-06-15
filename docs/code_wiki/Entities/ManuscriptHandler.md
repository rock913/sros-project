---
kind: entity
type: class
aliases:
- manuscript handler
tags: []
---

# ManuscriptHandler

## 概要 (Description)
处理稿件的核心类，在 .handler 模块中定义，具体职责待查看实现。

## 关系 (Relations)
- (implements) [[ManuscriptProtocol]] — class ManuscriptHandler(ManuscriptProtocol)
- (calls) [[resolve_workspace_path]] — in index_figure_references: path = resolve_workspace_path(file_path)
## 关联 (Related)
- [[__init__]]
- [[create_manuscript_server]]
- [[Workspace-relative path resolution]]
- [[Citation validation]]
- [[Figure reference indexing]]
- [[resolve_workspace_path]]
- [[_validate_citekeys_exist]]
- [[index_figure_references]]
- [[ManuscriptProtocol]]
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Task Management]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[dispatch_tool]]
- [[discover_plugins]]
- [[run_plugin]]
- [[TasksHandler]]
- [[ExtHandler]]
- [[RagHandler]]
- [[ScholarHandler]]
- [[Workspace-Relative Path Resolution]]
## Sources
- [[rpc]]
- [[handler]]
- [[__init__]]
