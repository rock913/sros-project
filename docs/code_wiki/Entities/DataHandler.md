---
kind: entity
type: class
aliases: []
tags: []
---

# DataHandler

## 概要 (Description)
提供数据预览和脚本执行能力。入参：file_path(str) 或 script_path(str)、dataset_paths(List[str] 可选)。出参：Dictionary 包含 ok 标志、错误信息或执行结果。副作用：运行外部脚本、写入文件系统（创建 figures 目录）、调用 MemoryHandler.store_knowledge 修改知识图谱。

## 关系 (Relations)
- (depends_on) [[MemoryHandler]] — 在 run_script 方法中实例化 MemoryHandler 并调用 store_knowledge
- (depends_on) [[KnowledgeEdge]] — 在 run_script 方法中导入并创建 KnowledgeEdge 实例
- (implements) [[Knowledge Graph Registry]] — run_script 方法通过 MemoryHandler 实现知识图谱注册功能
- (implements) [[Execution Sandbox]] — run_script 方法使用 subprocess.run 并在隔离环境中执行脚本

## 关联 (Related)
- [[Knowledge Graph Registry]]
- [[Execution Sandbox]]
- [[preview_csv]]
- [[run_script]]
- [[MemoryHandler]]
- [[KnowledgeEdge]]
- [[Knowledge Graph Integration]]
- [[Secure Script Execution]]
## Sources
- [[handler]]
