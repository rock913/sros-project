---
kind: entity
type: function
aliases: []
tags: []
---

# run_plugin

## 概要 (Description)
Imported from sros.utils.plugin_loader; executes a named plugin with given arguments and returns the result.

## 关系 (Relations)
- (calls) [[load_plugin]] — run_plugin calls load_plugin to get plugin info and module.
- (calls) [[load_plugin]] — run_plugin calls load_plugin(name, workspace_dir) to load plugin module.
- (emits) [[PluginLoadError]] — run_plugin raises PluginLoadError if plugin lacks callable run function.
## 关联 (Related)
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Task Management]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[dispatch_tool]]
- [[discover_plugins]]
- [[TasksHandler]]
- [[ManuscriptHandler]]
- [[ExtHandler]]
- [[RagHandler]]
- [[ScholarHandler]]
- [[Plugin Metadata Protocol]]
- [[Safe Plugin Loading]]
- [[PluginInfo]]
- [[PluginLoadError]]
- [[parse_plugin_metadata]]
- [[get_workspace_dir]]
- [[get_plugins_dir]]
- [[load_plugin]]
- [[Plugin Lifecycle]]
- [[Workspace Layout Convention]]
## Sources
- [[plugin_loader]]
- [[rpc]]
