---
kind: entity
type: class
aliases: []
tags: []
---

# ManuscriptProtocol

## 概要 (Description)
协议类，定义稿件操作的标准接口。包含查找待办项、获取大纲、增量写入和批量更新等方法。所有方法以文件路径和可选的预期SHA256哈希为参数，返回结构化结果。

## 关系 (Relations)
- (depends_on) [[乐观并发控制]] — insert_section 和 patch_draft 方法通过 expected_sha256 参数实现乐观并发控制
- (depends_on) [[find_gaps]] — 接口方法声明
- (depends_on) [[get_outline_tree]] — 接口方法声明
- (depends_on) [[get_file_sha256]] — 接口方法声明
- (depends_on) [[insert_section]] — 接口方法声明
- (depends_on) [[patch_draft]] — 接口方法声明
## 关联 (Related)
- [[乐观并发控制]]
- [[find_gaps]]
- [[get_outline_tree]]
- [[get_file_sha256]]
- [[insert_section]]
- [[patch_draft]]
- [[Workspace-relative path resolution]]
- [[Citation validation]]
- [[Figure reference indexing]]
- [[ManuscriptHandler]]
- [[resolve_workspace_path]]
- [[_validate_citekeys_exist]]
- [[index_figure_references]]
- [[__init__]]
- [[ScholarProtocol]]
- [[MemoryProtocol]]
- [[ZoteroProtocol]]
- [[结构化返回]]
- [[MCP Server]]
- [[get_manuscript_service]]
- [[create_manuscript_server]]
- [[main]]
- [[find_gaps_tool]]
- [[get_outline_tree_tool]]
- [[insert_section_tool]]
- [[patch_draft_tool]]
## Sources
- [[server]]
- [[__init__]]
- [[handler]]
- [[manuscript_protocol]]
