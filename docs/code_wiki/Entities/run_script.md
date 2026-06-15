---
kind: entity
type: function
aliases: []
tags: []
---

# run_script

## 概要 (Description)
在子进程中执行 Python 脚本，检测新生成/修改的图形文件，使用 MemoryHandler 注册节点和边到知识图谱。入参：script_path(str)、dataset_paths(List[str] 可选)。出参：Dict 包含 ok 布尔值及执行详情（脚本路径、标准输出、标准错误、数据集列表、图形列表）。副作用：写入文件系统（创建 figures 目录）、调用 MemoryHandler.store_knowledge。

## 关系 (Relations)
- (calls) [[preview_csv]] — 未在代码中发现直接调用，但可能被外部调用。如果考虑关系则此条可删除。实际代码中 run_script 不调用 preview_csv。
- (calls) [[MemoryHandler]] — run_script 方法中实例化 MemoryHandler 并调用 store_knowledge
- (calls) [[KnowledgeEdge]] — 创建 KnowledgeEdge 实例作为 edges 列表元素

## 关联 (Related)
- [[Knowledge Graph Registry]]
- [[Execution Sandbox]]
- [[DataHandler]]
- [[preview_csv]]
- [[MemoryHandler]]
- [[KnowledgeEdge]]
- [[Knowledge Graph Integration]]
- [[Secure Script Execution]]
## Sources
- [[handler]]
