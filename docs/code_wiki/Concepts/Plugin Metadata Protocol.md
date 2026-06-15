---
kind: concept
aliases:
- metadata convention
tags:
- architecture
---

# Plugin Metadata Protocol

## 概要 (Description)
Convention that plugins define SKILL_NAME, SKILL_DESCRIPTION, SKILL_INPUT_SCHEMA as module-level variables, extracted statically via AST before execution.
## 关联 (Related)
- [[Safe Plugin Loading]]
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
