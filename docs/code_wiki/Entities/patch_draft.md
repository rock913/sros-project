---
kind: entity
type: function
aliases: []
tags: []
---

# patch_draft

## 概要 (Description)
批量应用多个补丁来更新稿件内容。支持乐观并发控制。入参：patches (List[Dict]), file_path (str), expected_sha256 (Optional[str])；出参：Dict[str, Any] 操作结果。

## 关系 (Relations)
- (depends_on) [[乐观并发控制]] — expected_sha256 参数提供乐观并发校验
- (depends_on) [[结构化返回]] — 返回 Dict[str, Any] 而非异常

## 关联 (Related)
- [[乐观并发控制]]
- [[ManuscriptProtocol]]
- [[find_gaps]]
- [[get_outline_tree]]
- [[get_file_sha256]]
- [[insert_section]]
- [[结构化返回]]
## Sources
- [[manuscript_protocol]]
