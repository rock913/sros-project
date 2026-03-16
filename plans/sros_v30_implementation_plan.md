# SROS V3.0 Implementation Plan (Golden Thread + TDD)

目标：以 [doc/SROS_V3.0.md](../doc/SROS_V3.0.md) 为单一事实来源，按“黄金主线”垂直切片推进；每一条切片都可端到端演示、可自动化验收。

## Guiding Principles

- **IDE-as-UI**：不做传统 Web GUI；以 VS Code 文件树 + Markdown 预览 + Terminal 作为“可视化界面”。
- **Skill-first**：把能力做成可组合的 CLI 技能（`sros-skill`），默认人类可读，`--raw` 输出机器可读 JSON。
- **Gateway is thin**：MCP Gateway 只做 CLI 反射代理，不含业务逻辑。
- **Workspace is truth**：所有状态落在工作区文件与 `.sros/graph.db`，不依赖隐式内存。
- **TDD**：先写验收测试（unit/integration），再写实现；每个切片都落入测试与文档。

## Milestones

### V3.0-Alpha (3 weeks)

**Definition of Done**

- `sros-skill` 可在本地完成最小闭环：
  - `gap -> search (mock) -> insert -> update draft.md`
- 统一输出协议：
  - 默认 rich/人类友好
  - `--raw` 输出 JSON（stderr 只输出错误）
- MCP Gateway 可将 `tools/call` 反射为 `sros-skill ... --raw`，并返回 JSON

**Acceptance Tests (must pass)**

- `tests/unit/test_skills_cli_*`：`--raw` 必须是可解析 JSON
- `tests/integration/test_gateway_reflects_skill_*`：`tools/list` 与 `tools/call` 路由到对应 skill

### V3.0-Beta (1–2 months)

- Workspace 扩展：`data/raw`, `data/processed`, `figures`, `scripts`
- 数据闭环：`preview csv -> run script -> register figure -> insert into draft`
- DuckDB 异构图谱：Section/Dataset/Script/Figure 节点与 GENERATES/ANALYZES 边

### V3.0-GA (long-term)

- 插件系统：`.sros/plugins/` 动态加载 skill
- packs：neuro/bio/viz 等官方扩展包

## Golden Thread (Vertical Slices)

Slice 0 (Bootstrapping)

- `sros init` 生成 V3 workspace 结构与 Agent 引导配置（`.clauderc`, `openclaw.yaml`, `.roo/mcp.json`）
- 测试：生成的目录与配置必须可用、路径安全必须生效

Slice 1 (Write loop)

- `sros-skill manuscript.find-gaps`（读）
- `sros-skill scholar.search`（mock，读）
- `sros-skill manuscript.insert`（写，带乐观锁 expected_sha256）

Slice 2 (Data loop)

- `sros-skill data.preview`（CSV 摘要）
- `sros-skill data.run-script`（执行脚本产物落地 figures/）
- `sros-skill manuscript.insert-figure`（写入 Markdown 图片引用）

## Test Strategy

- **Unit**：纯函数/路径解析/输出格式/JSON schema
- **Integration**：子进程启动 gateway、真实读写 workspace、duckdb 持久化
- **End-to-end**：复用现有 verify 脚本 + 新增 v3 验收脚本

## Repo Cleanup Policy

- `doc/` 只保留当前有效文档，其余移动到 `doc/archive/`。
- 旧实现保留在代码历史中，但 V3 分支优先做破坏性重构（不为历史客户端保兼容）。
