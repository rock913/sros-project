---
kind: entity
type: function
aliases:
- sros-gateway
tags: []
---

# app

## 概要 (Description)
CLI 主入口，由 cli 模块暴露的 app 实例提供命令行交互功能。

## 关系 (Relations)
- (calls) [[init]] — Typer command decorator @app.command() on init()
- (calls) [[start]] — Typer command decorator @app.command() on start()
- (calls) [[stop]] — Typer command decorator @app.command() on stop()
- (calls) [[restart]] — Typer command decorator @app.command() on restart()
- (calls) [[doctor]] — Typer command decorator @app.command() on doctor()
- (calls) [[status]] — Typer command decorator @app.command() on status()

## 关联 (Related)
- [[Expose main components]]
- [[__init__py]]
- [[Workspace Initialization]]
- [[Gateway Lifecycle Management]]
- [[MCP Server Integration]]
- [[Environment Configuration]]
- [[validate_workspace_dir]]
- [[init]]
- [[start]]
- [[doctor]]
- [[status]]
- [[stop]]
- [[restart]]
- [[CLI Routing]]
- [[Output Formatting]]
- [[manuscript_find_gaps]]
- [[manuscript_outline]]
- [[manuscript_get_outline_tree_compat]]
- [[manuscript_sha256]]
- [[manuscript_get_file_sha256_compat]]
- [[manuscript_index_figures]]
- [[manuscript_insert]]
- [[Gateway Process Lifecycle]]
- [[__main__]]
- [[main]]
## Sources
- [[__main__]]
- [[cli]]
- [[__init__]]
