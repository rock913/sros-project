---
kind: entity
type: function
aliases: []
tags: []
---

# load_plugin

## 概要 (Description)
Loads a named plugin by dynamic import from plugins directory, validates SKILL_NAME, extracts metadata from module attributes (with JSON schema fallback), returns (PluginInfo, module). Side-effect: module execution.

## 关系 (Relations)
- (calls) [[get_plugins_dir]] — load_plugin calls get_plugins_dir to determine plugin path.
- (calls) [[get_plugins_dir]] — load_plugin calls get_plugins_dir(workspace_dir) to resolve plugin path.
- (emits) [[PluginLoadError]] — load_plugin raises PluginLoadError on invalid path, missing plugin, or bad SKILL_NAME.
## 关联 (Related)
- [[Plugin Metadata Protocol]]
- [[Safe Plugin Loading]]
- [[PluginInfo]]
- [[PluginLoadError]]
- [[parse_plugin_metadata]]
- [[get_workspace_dir]]
- [[get_plugins_dir]]
- [[discover_plugins]]
- [[run_plugin]]
- [[Plugin Lifecycle]]
- [[Workspace Layout Convention]]
## Sources
- [[plugin_loader]]
