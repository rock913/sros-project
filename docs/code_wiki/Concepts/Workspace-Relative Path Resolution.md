---
kind: concept
aliases: []
tags:
- architecture
---

# Workspace-Relative Path Resolution

## 概要 (Description)
All file paths are resolved relative to the SROS_WORKSPACE_DIR environment variable, with strict validation to prevent directory traversal.
## 关联 (Related)
- [[ManuscriptHandler]]
- [[resolve_workspace_path]]
## Sources
- [[handler]]
