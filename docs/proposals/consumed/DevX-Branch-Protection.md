# DevX PRD 更新提案：GitHub 仓库 Branch Protection + Squash and Merge 配置

> 目标：5 个 GitHub 仓库的 Settings 配置
> 提案日期：2026-06-02（刷新自 2026-05-26 原版）
> 驱动来源：Phase 7 (DevX 混合架构基础设施升级) — PRD §6C.5 SLAIB Git 流
>
> ⚡ **Quick Start**：本提案为 GitHub Settings UI 操作清单，无需子项目会话执行。请用户按以下 checklist 逐仓库配置。

## 动机 (Why)

当前所有子项目仓库只有 `main` 分支，没有写保护。AI Agent 在任何子项目会话中都可以直接执行 `git push origin main`，存在以下风险：

1. **AI 幻觉直接污染生产代码** — 无 PR 审查门禁，错误代码直接进入 main
2. **多 AI 进程并发冲突** — 多个子项目会话同时 push main 引发灾难级合并冲突
3. **提交历史污染** — AI 琐碎的 "update file"、"fix typo" 会铺满 main 的 commit log
4. **无人类审批环节** — 用户对代码变更无感知，直到出问题才发现

## 目标仓库清单

| # | 仓库 | GitHub URL | 当前保护状态 |
|---|------|-----------|:-----------:|
| 1 | SROS | `github.com/rock913/sros-project` | ❌ 未保护 |
| 2 | ARC-Engine | `github.com/rock913/ARC-Engine` | ❌ 未保护 |
| 3 | GraphMRI-Lite | `github.com/AutoBrainLab/GraphMRI-Lite` | ⚠️ Squash Merge 已生效，BP 需 Pro |
| 4 | Hermes-Workflows | `github.com/rock913/Hermes-Workflows` | ❌ 未保护 |
| 5 | SXMU_MDD_Twin | `github.com/AutoBrainLab/Project_SXMU_MDD_Twin` | ❌ 未保护 |

> **注意**：GraphMRI-Lite 的 GitHub URL 需用户确认。当前推测为 `github.com/rock913/GraphMRI-Lite`。

## 操作步骤（逐仓库执行）

### Step 1：进入仓库 Settings → Branches

在浏览器中打开 `https://github.com/<owner>/<repo>/settings/branches`

### Step 2：添加 Branch Protection Rule

1. 点击 **"Add branch protection rule"**
2. **Branch name pattern** 填入：`main`
3. 勾选以下选项：

```
☑ Require a pull request before merging
  ☑ Require approvals (1)                          # 至少 1 人审批
  ☐ Dismiss stale pull request approvals          # 可选
  ☐ Require review from Code Owners               # 可选

☐ Require status checks to pass before merging    # 等 CI 就绪后再开启
☐ Require conversation resolution before merging  # 可选

☐ Require signed commits                          # 可选
☐ Require linear history                          # 可选
☐ Include administrators                          # 建议勾选：管理员也受保护
```

4. 点击 **"Create"** 或 **"Save changes"**

### Step 3：配置 Pull Request 合并策略

在仓库 Settings → General → Pull Requests 区域：

```
☑ Allow squash merging
  Default commit message: "Default to PR title"
☑ Allow rebase merging (可选)
☑ Automatically delete head branches             # ⭐ 关键：PR 合并后自动删分支
```

### Step 4：验证

在本地克隆的仓库中尝试直接 push main：

```bash
git checkout main
echo "test" >> test.txt && git add test.txt && git commit -m "test direct push"
git push origin main
# 预期：被拒绝！错误信息类似：
# remote: error: GH006: Protected branch update failed
```

然后验证 SLAIB 完整流程：
```bash
git checkout -b feat/test-branch-protection
echo "test" >> test.txt && git add test.txt && git commit -m "test slaib flow"
git push origin feat/test-branch-protection
# 在 GitHub Web UI 创建 PR → Squash and Merge → 验证分支自动删除
git checkout main && git pull origin main
git branch -d feat/test-branch-protection  # 清理本地分支
```

## 验收标准

- [ ] 5 个仓库的 main 分支均开启 Branch Protection（Require PR before merging）
- [ ] 5 个仓库均开启 Squash and Merge + Automatically delete head branches
- [ ] 验证：`git push origin main` 在至少 1 个仓库被拒绝
- [ ] 验证：SLAIB 完整流程（feat/xxx → PR → Squash & Merge → 自动删分支）在至少 1 个仓库通过
- [ ] GraphMRI-Lite 的 GitHub 仓库 URL 已确认并完成配置
