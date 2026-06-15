---
kind: concept
aliases:
- secure load
tags:
- architecture
---

# Safe Plugin Loading

## 概要 (Description)
Plugin files are loaded from a fixed .sros/plugins directory under the workspace, with path traversal protection and metadata validation.
## 关联 (Related)
- [[Plugin Metadata Protocol]]
- [[PluginInfo]]
- [[PluginLoadError]]
- [[parse_plugin_metadata]]
- [[get_workspace_dir]]
- [[get_plugins_dir]]
- [[discover_plugins]]
- [[load_plugin]]
- [[run_plugin]]
## Sources
- [[plugin_loader]]
