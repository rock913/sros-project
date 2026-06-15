---
kind: entity
type: function
aliases: []
tags: []
---

# insert_section_tool

## 概要 (Description)
MCP tool: receives target, content, citations, file_path, expected_sha256; calls service.insert_section; returns JSON result dict.

## 关系 (Relations)
- (calls) [[ManuscriptProtocol]] — Calls service.insert_section(...).

## 关联 (Related)
- [[MCP Server]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[main]]
- [[ManuscriptProtocol]]
- [[find_gaps_tool]]
- [[get_outline_tree_tool]]
- [[patch_draft_tool]]
## Sources
- [[server]]
