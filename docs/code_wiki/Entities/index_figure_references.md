---
kind: entity
type: function
aliases: []
tags: []
---

# index_figure_references

## 概要 (Description)
Parses a Markdown file for image links (e.g., ![alt](figures/foo.png)), creates draft_section nodes for each heading, Figure nodes for each figure, and REFERENCED_IN edges. Returns a dict with ok/error status and list of referenced figures.

## 关系 (Relations)
- (calls) [[resolve_workspace_path]] — path = resolve_workspace_path(file_path)

## 关联 (Related)
- [[Workspace-relative path resolution]]
- [[Citation validation]]
- [[Figure reference indexing]]
- [[ManuscriptHandler]]
- [[resolve_workspace_path]]
- [[_validate_citekeys_exist]]
- [[ManuscriptProtocol]]
## Sources
- [[handler]]
