# DevX PRD 更新提案：全局行为准则与 Git 规范 (SLAIB) — 剩余目标

> 目标主 PRD：Hermes-Workflows `CLAUDE.md`（新建）+ SXMU_MDD_Twin `CLAUDE.md`（追加）
> 提案日期：2026-06-02（刷新自 2026-05-26 原版）
> 驱动来源：Phase 7 (DevX 混合架构基础设施升级) — `meta-docs/strategy/DevX_Hybrid_Architecture_v2.md`
>
> ⚡ **Quick Start**：在目标子项目目录中打开 Claude Code，复制以下内容作为第一条消息：
> "执行 meta-docs/proposals/pending/DevX-CLAUDE.md-Rules.md 中的提案。将 DevX 6 条规则追加到本项目的 CLAUDE.md 文件末尾（如文件不存在则先创建）。
>  完成后更新自身 ROADMAP.md (DevX SLAIB→✅) + 主 PRD（Hermes: README.md / SXMU: README.md），并回复 done。"

## 动机 (Why)

当前所有子项目的 `CLAUDE.md` 均只关注项目自身的架构和开发规范，缺乏跨项目通用的 DevX 行为准则。这导致：

1. AI Agent 可能在不同环境（交互式 Tmux / 非交互式飞书桥接）中使用阻塞性命令 (`vim`, `nano`)，在飞书桥接中会导致会话卡死
2. Auto Mode 下 AI 仍频繁向用户索要权限确认，拖慢碎片化开发节奏
3. 无跨项目隔离红线 — AI 可能误操作 `cd ../` 进入其他子项目目录
4. Git 流程不一致 — 各项目缺乏统一的 SLAIB (Short-Lived AI Branches) 规范
5. PR 门禁缺失 — AI 可能直接 push 到 main 分支

## 交付状态（2026-06-02 刷新）

| # | 子项目 | CLAUDE.md 路径 | DevX 规则 |
|---|--------|---------------|:---------:|
| 1 | SROS | `01-Core_Infra/SROS/CLAUDE.md` | ✅ 已交付 |
| 2 | ARC-Engine | `01-Core_Infra/ARC-Engine/CLAUDE.md` | ✅ 已交付 |
| 3 | GraphMRI-Lite | `01-Core_Infra/GraphMRI-Lite/CLAUDE.md` | ✅ 已交付 |
| 4 | **Hermes-Workflows** | `02-Agent_Orchestration/Hermes-Workflows/CLAUDE.md` | **❌ 文件不存在，需新建** |
| 5 | **SXMU_MDD_Twin** | `03-Science_Projects/Project_SXMU_MDD_Twin/CLAUDE.md` | **❌ 文件存在但无 DevX 规则** |

> 原版（2026-05-26）要求 5 个目标。现 3/5 已完成，本提案缩小范围为剩余 2 个。

## 提议追加内容

在剩余 2 个子项目的 `CLAUDE.md` 中追加统一的 **DevX 全局行为准则与 Git 规范** 章节：

```markdown
## ⚠️ DevX 全局行为准则与 Git 规范

> 来源：Meta Phase 7 DevX 混合架构基础设施升级
> 本规范适用于交互式终端 (Tmux) 和非交互式飞书桥接两种运行环境。

1. **环境认知**：你可能运行在交互式终端 (Tmux) 或非交互式的飞书桥接中。严禁使用阻塞性交互命令 (`vim`, `nano`, `less`)。读取文件请用 `cat` 或 `head`。

2. **静默优先**：当前环境已开启 Auto Mode。对于确定性的依赖安装、Linter 执行、文件覆盖，请直接执行，遇到询问默认加 `-y`，尽量减少向用户索要权限。

3. **隔离红线**：当前所有项目运行在同一 Linux 账户下。**绝对禁止**通过 `cd ../` 访问或修改当前项目根目录以外的任何文件。所有操作必须在当前仓库目录内完成。

4. **Git 短期分支流 (SLAIB)**：
   - `main` 分支已被写保护，无法直接 push。
   - 任何修改前，必须执行 `git checkout -b <type>/<desc>`（例如 `feat/add-login`, `fix/oom-error`, `refactor/scheduler`）。
   - 修改完成后推送分支到远程。

5. **PR 门禁**：
   - 推送分支后，使用 GitHub CLI (`gh pr create --fill`) 发起 Pull Request。
   - 等待人类主理人在 GitHub 上审批并 Squash and Merge。
   - **严禁**尝试绕过 PR 机制直接 push main。

6. **自动清理**：
   - PR 被 Squash and Merge 后，远程分支会自动删除。
   - 本地执行 `git fetch --prune` 清理已删除的远程分支引用。
   - 本地分支可手动删除：`git branch -d <type>/<desc>`。
```

### 放置规则

- **Hermes-Workflows**：CLAUDE.md 不存在，需新建。内容从 DevX 6 条规则开始，后续可追加 Hermes 专有架构约定。
- **SXMU_MDD_Twin**：追加在现有"核心原则"章节之后，"日常工作流"章节之前。

## 验收标准

- [ ] Hermes-Workflows 存在 `CLAUDE.md` 文件，包含 DevX 6 条规则
- [ ] SXMU_MDD_Twin `CLAUDE.md` 包含 DevX 6 条规则
- [ ] 两个文件的规则内容一致，无个性化修改
- [ ] （SROS/ARC/GraphMRI-Lite 已在之前会话中交付，无需重复操作）
