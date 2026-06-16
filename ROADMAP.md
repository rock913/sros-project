# SROS ROADMAP

> **角色**：进度追踪与状态看板（WHEN + STATUS） | 架构/规格 → `doc/SROS_V4.0.md` | 实现规格 → `doc/PRD_SXMU_Data_Ingestion_HPC.md`
>
> **V4.0-dev** | S1–S7 + DSL-1–DSL-6 + FS-1 全部交付 | 138 tests | 2026-06-02

---

## 状态图例

| 标记 | 含义 |
|:----:|------|
| ✅ | 已交付，测试通过 |
| 🔵 | 功能稳定，Beta 打磨中 |
| 🔶 | 开发中 |
| 📋 | 提案/指南已就绪，待执行 |
| ❌ | 待开始 |

---

## 里程碑

| 版本 | 目标 | 状态 | 交付日期 |
|------|------|:----:|----------|
| **V3.0** | 写作 OS 稳定版（文稿+文献+知识图谱） | 🔵 | — |
| **V3.1–V3.5** | 数据摄入、HPC 调度、SQL 查询、Code-Wiki 契约+CI | ✅ | 2026-05-12/14 |
| **V4.0** | 全面 MCP 化 + 生态纳管 + 数据 OS | 🔶 核心已交付 | 2026-Q2 |
| **V4.1** | DevX 基础设施 + 跨项目契约验证 + Hermes 集成 | 🔶 进行中 | 2026-Q2 |
| **V4.2** | sros-sdk: AI4S DSL 科学编译器 | ✅ | 2026-Q2 |

---

## SXMU 驱动任务清单

| ID | 内容 | 状态 |
|:--:|------|:----:|
| S1–S7 | `db ingest/query` + `hpc-server` + Code-Wiki 契约/CI/Doctor/强制激活 | ✅ |
| DSL-1–DSL-6 | sros-sdk 骨架 → BrainGraphDataset → GNNTrainer → DuckDB 连接器 → DSPy 断言 → E2E | ✅ |
| FS-1 | 飞书 Webhook `POST /webhook/execute` + 字段翻译 + BackgroundTasks → GraphMRI-Lite | ✅ |
| MCP-Adapter | MCP-to-OpenAI Function Calling 协议翻译层 (DeepSeek v4 Pro 适配) | ✅ |

---

## 能力矩阵

| 模块 | 状态 | 关键能力 |
|------|:----:|---------|
| Manuscript | ✅ | gap / outline / insert / patch / refactor + SHA256 乐观并发 |
| Scholar | ✅ | federated_search / zotero_sync + OpenAlex |
| Memory | ✅ | DuckDB 知识图谱 (nodes/edges) + 全文搜索 |
| RAG | ✅ | 词法分块 DuckDB + URL 抓取 |
| Data | ✅ | BIDS/TSV/Excel 摄入 + DuckDB SQL (8表DDL) |
| HPC | ✅ | Slurm 作业管理 + OOM 自愈 + Apptainer 模板 |
| Plugin | ✅ | `.sros/plugins/` 动态发现 + 异步任务 |
| Code-Wiki | ✅ | ARC 契约 + 强制激活 + CI Sidecar + Doctor 诊断 |
| Neuro | ✅ | BIDS 结构验证、graphmri 脚本生成、fMRIPrep 批量编排 |
| CLI UX | ✅ | Rich Panel/Table/Progress — `start`/`doctor`/`db ingest` 结构化输出 |
| SDK | ✅ | BrainGraphDataset Fluent API + GNNTrainer + DuckDB 连接器 + DSPy 断言 |
| Webhook | ✅ | 飞书控制平面 `POST /webhook/execute` → GraphMRI-Lite 异步任务触发 |

---

## V4.0 交付进度

| 方向 | 说明 | 优先级 | 状态 |
|------|------|:------:|:----:|
| CLI 结构化输出 | Rich Panel/Table/Progress 升级 `sros start`/`doctor`/`db ingest` | P1 | ✅ |
| E2E 集成测试 | Gateway + MCP 全链路 smoke test | P2 | ✅ |
| `sros-neuro-server` | BIDS 验证、graphmri 脚本生成、fMRIPrep 管线编排 | P2 | ✅ |
| sros-sdk DSL | BrainGraphDataset + GNNTrainer + DuckDB 连接器 + DSPy 断言 + E2E | P1 | ✅ |
| 飞书 Webhook | `POST /webhook/execute` + 字段翻译 + BackgroundTasks → GraphMRI-Lite | P1 | ✅ |
| DevX SLAIB Git 流 | 短期分支 + PR 门禁 + 自动清理 | P1 | ✅ |
| ARC CI 契约测试 | ARC 侧 `sros-contract-test` job（SROS 侧契约已就绪） | P1 | 📋 |
| Hermes Workflows 集成 | fMRIPrep → graphmri → 统计报告长周期流水线 | P2 | 📋 |
| DevX Branch Protection | GitHub 5 仓库 main 分支写保护 + Squash & Merge | P1 | 📋 |
| DevX Systemd Bridge | 飞书桥接 systemd 服务 + Tmux 别名 | P2 | 📋 |
| TypeScript SDK | 多语言客户端 / VS Code 扩展 | P3 | ❌ |
| 分布式 DuckDB | MotherDuck / 多节点联邦查询 | P3 | ❌ |
| AgenticOps 遥测 | MCP Gateway 遥测中间件 → AgenticOps Dashboard | P2 | ❌ |

---

## 下一步行动（按优先级）

1. **DevX Branch Protection (P1)** — 按 `docs/DevX-GitHub-Branch-Protection.md` 逐仓库配置 GitHub Settings（需用户手动操作 GitHub Web UI）
2. **DevX Systemd Bridge (P2)** — 按 `docs/DevX-Systemd-Bridge-Setup.md` 配置 systemd 服务 + Tmux 别名（需用户手动操作终端）
3. **ARC CI 契约测试 (P1)** — 等待 ARC-Engine 侧执行提案
4. **Hermes H1H2 框架验证 (P1)** — 等待 Hermes-Workflows 侧执行提案
5. **AgenticOps 遥测 (P2)** — 等待 `01-Core_Infra/AgenticOps/` 仓库骨架创建后集成

---

## 风险

| 风险 | 影响 | 级别 | 缓解 |
|------|------|:----:|------|
| BIDS 格式多样性 | 解析器覆盖不足 | 中 | 先适配 SXMU 队列，再泛化 |
| HPC 网络隔离（无外网） | MCP 通信中断 | 高 | `sros-hpc-server` 部署在登录节点，走 SSH 隧道 |
| MCP 工具数量增长 | Gateway schema 膨胀 | 低 | STATIC_TOOLS 模式已验证可承载 50+ tool |
| SLAIB 分支流未强制执行 | AI 直接 push main | 高 | Branch Protection + CLAUDE.md 双重门禁 |
| sros-sdk DSL 与 GraphMRI-Lite API 不同步 | DSL 调用失败 | 中 | DSL 是封装层，CLI `--raw` JSON 契约稳定 |
| `lark-channel-bridge` 不可用 | 飞书轨道降级 | 中 | 降级为手动 `claude -p` 模式 |
