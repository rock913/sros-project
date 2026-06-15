---
kind: entity
type: function
aliases: []
tags: []
---

# parse_plugin_metadata

## 概要 (Description)
Static analysis of a Python file via AST to extract SKILL_NAME, SKILL_DESCRIPTION, SKILL_INPUT_SCHEMA without executing code. Returns PluginInfo.

## 关系 (Relations)
- (produces) [[PluginInfo]] — parse_plugin_metadata returns a new PluginInfo instance.

## 关联 (Related)
- [[Plugin Metadata Protocol]]
- [[Safe Plugin Loading]]
- [[PluginInfo]]
- [[PluginLoadError]]
- [[get_workspace_dir]]
- [[get_plugins_dir]]
- [[discover_plugins]]
- [[load_plugin]]
- [[run_plugin]]
- [[Plugin Lifecycle]]
- [[Workspace Layout Convention]]
## Sources
- [[plugin_loader]]
