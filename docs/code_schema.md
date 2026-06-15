# SROS Code Schema — ARC Code-Wiki 编译器专用 Schema

> 继承自 ARC Engine `code_schema.md` v1 基础提取规则；
> 本文件定义 SROS 项目特有的实体/概念/关系提取约定。

## SROS 特有概念

- **Workspace Contract**：`data/raw` → `data/processed` → `figures/` 的数据流约定
- **Skill-First Pattern**：所有能力通过 `sros-skill` CLI 暴露，Gateway 只做薄层反射
- **Thin Gateway**：MCP Gateway 不含业务逻辑，仅做协议路由（`dispatch_tool()` → handler）
- **Provenance Chain**：DuckDB 异构图谱节点（Script/Figure/Dataset/Section）与边（GENERATES/ANALYZES/REFERENCED_IN）
- **Plugin Contract**：`.sros/plugins/<id>.py` → `SKILL_NAME/SKILL_DESCRIPTION/SKILL_INPUT_SCHEMA` → `def run(args)`
- **Data Ingestion Pipeline**：BIDS 目录 + TSV + Excel → DuckDB 8 表 DDL schema
- **HPC Job Lifecycle**：sbatch/squeue/scancel 包装 + OOM 自愈重试策略

## 提取规则

### Entities (实体)

提取代码中的主要 Class、高频调用的公共 Function、关键 Module。必须说明：

- **入参/出参特征**：函数签名、关键参数类型
- **核心职责**：这个实体在系统中的角色
- **副作用**：是否修改全局状态、读写文件、网络调用

### Concepts (概念)

如果代码涉及跨模块的交互（如：事件总线、缓存策略、并发控制、契约约定），将其抽象为概念。概念描述的是“模式”而非具体实现。

### Relations (关系)

描述实体之间的有向关系：
- `depends_on`：导入/依赖
- `implements`：实现接口/抽象类
- `extends`：继承
- `calls`：函数调用
- `emits`：事件/信号发出
- `manages`：生命周期管理

### Synthesis (架构更新)

简述这次代码的加入/修改，对整体架构有什么影响？有没有引入新的第三方依赖？

## 硬性约束

- 每篇代码提取核心概念 ≤ 5 个
- 每篇代码提取关键实体 ≤ 8 个
- 关系 ≤ 12 条，且只在本次抽取到的概念/实体之间连边
- 忽略测试文件、临时脚本的边缘细节
- 忽略 import 语句的机械依赖，只记录有架构意义的依赖关系

## 输出格式

强制输出为 JSON 格式，不要任何额外解释：

```json
{
  "summary": "一句话总结这个文件在架构中的角色",
  "concepts": [
    {
      "name": "概念名",
      "description": "这个模式/约定的说明",
      "tags": ["architecture", "cross-cutting"],
      "aliases": ["别名"]
    }
  ],
  "entities": [
    {
      "name": "ClassName 或 function_name",
      "type": "class 或 function 或 module",
      "description": "核心职责与入参/出参特征",
      "aliases": ["别名"]
    }
  ],
  "relations": [
    {
      "source": "源实体/概念",
      "target": "目标实体/概念",
      "type": "depends_on 或 implements 或 extends 或 calls 或 emits 或 manages",
      "evidence": "代码中的具体证据（如类继承行、关键调用）"
    }
  ]
}
```
