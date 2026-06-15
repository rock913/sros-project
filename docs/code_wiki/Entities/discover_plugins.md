---
kind: entity
type: function
aliases: []
tags: []
---

# discover_plugins

## 概要 (Description)
Imported from sros.utils.plugin_loader; returns a list of discovered plugin metadata objects (name, display_name, description, path, input_schema).

## 关系 (Relations)
- (calls) [[get_plugins_dir]] — discover_plugins calls get_plugins_dir to obtain the plugins directory.
- (calls) [[parse_plugin_metadata]] — For each plugin file, discover_plugins calls parse_plugin_metadata.
- (calls) [[get_plugins_dir]] — discover_plugins calls get_plugins_dir(workspace_dir) to locate plugins directory.
- (calls) [[parse_plugin_metadata]] — discover_plugins calls parse_plugin_metadata(path) for each .py file.
## 关联 (Related)
- [[Tool Dispatch Pattern]]
- [[Plugin System]]
- [[Task Management]]
- [[Manuscript Service]]
- [[External RAG Services]]
- [[dispatch_tool]]
- [[run_plugin]]
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
