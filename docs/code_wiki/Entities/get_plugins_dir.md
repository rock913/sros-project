---
kind: entity
type: function
aliases: []
tags: []
---

# get_plugins_dir

## 概要 (Description)
Returns Path to .sros/plugins folder under workspace directory. Side-effect: calls get_workspace_dir if workspace_dir not provided.

## 关系 (Relations)
- (calls) [[get_workspace_dir]] — When workspace_dir is not provided, get_plugins_dir calls get_workspace_dir().
- (calls) [[get_workspace_dir]] — get_plugins_dir calls get_workspace_dir() if workspace_dir is None.
## 关联 (Related)
- [[Plugin Metadata Protocol]]
- [[Safe Plugin Loading]]
- [[PluginInfo]]
- [[PluginLoadError]]
- [[parse_plugin_metadata]]
- [[get_workspace_dir]]
- [[discover_plugins]]
- [[load_plugin]]
- [[run_plugin]]
- [[Plugin Lifecycle]]
- [[Workspace Layout Convention]]
## Sources
- [[plugin_loader]]
