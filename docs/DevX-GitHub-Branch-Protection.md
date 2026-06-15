# DevX-GitHub-Branch-Protection — 手动配置指南

> 目标：对 AI4S 生态 5 个仓库的 `main` 分支启用写保护 + PR 门禁 + Squash & Merge
> 阻塞原因：GitHub Branch Protection 规则只能通过 Web UI 或 API 手动配置，无法由 AI Agent 自动化
> 预计耗时：15 分钟

## 受影响的 5 个仓库

| # | 仓库 | 角色 |
|---|------|------|
| 1 | `AI4S_Workspace/01-Core_Infra/SROS` | L1 科研操作系统 |
| 2 | `AI4S_Workspace/01-Core_Infra/ARC-Engine` | L2 知识引擎 |
| 3 | `AI4S_Workspace/01-Core_Infra/GraphMRI-Lite` | L0 神经影像引擎 |
| 4 | `AI4S_Workspace/02-Agent_Orchestration/Hermes-Workflows` | L3 编排层 |
| 5 | `AI4S_Workspace/03-Science_Projects/Project_SXMU_MDD_Twin` | 科学项目 |

> **注意**：如果上述仓库托管在 GitHub Organization 下且使用免费计划，部分功能可能需要升级到 GitHub Team 或 Enterprise。请先确认 Organization 的计划等级。

## 逐仓库配置步骤（GitHub Web UI）

对每个仓库，按以下步骤操作：

### Step 1 — 进入 Branch Protection 页面

1. 浏览器打开目标仓库（例如 `https://github.com/<owner>/<repo>`）
2. 顶部导航栏点击 **Settings**
3. 左侧边栏点击 **Branches**（在 "Code and automation" 分组下）
4. 在 "Branch protection rules" 区域，点击 **Add branch protection rule**

### Step 2 — 配置规则

在 "Branch name pattern" 输入框中填入：`main`

然后按以下清单逐项勾选：

#### 必须勾选（P0 — 安全红线）

| 设置项 | 值 | 说明 |
|--------|-----|------|
| **Require a pull request before merging** | ✅ 勾选 | 禁止直接 push main |
| └ Require approvals | `1` | 至少 1 位人类主理人审批 |
| └ Dismiss stale pull request approvals when new commits are pushed | ✅ 勾选 | 新 commit 后重置审批 |
| └ Require approval of the most recent reviewable push | ✅ 勾选 | 必须审批最新版本 |
| **Require status checks to pass before merging** | ✅ 勾选 | CI 绿条后才能合并 |
| └ Require branches to be up to date before merging | ✅ 勾选 | 分支必须基于最新 main |
| **Do not allow bypassing the above settings** | ✅ 勾选 | 管理员也必须遵守（含此复选框时请确认） |

> **关于 "Do not allow bypassing"**：GitHub Free 计划的个人仓库可能不显示此选项。如果缺失，请确保至少 "Require a pull request before merging" + "Require approvals ≥ 1" 两项已启用。

#### 推荐勾选（P1 — 质量门禁）

| 设置项 | 值 | 说明 |
|--------|-----|------|
| **Require conversation resolution before merging** | ✅ 勾选 | 所有评论必须 resolve |
| **Allow merge commits** | ❌ | 关闭 |
| **Allow squash merging** | ✅ | 仅允许 Squash & Merge |
| **Allow rebase merging** | ❌ | 关闭 |

> **Squash & Merge 的理由**：SLAIB 分支流中每个 PR 对应一个短期 AI 分支，Squash 将多轮"提交-修复"压缩为一条干净 commit，保持 main 线性历史。

#### 可选（P2 — 按仓库实际情况）

| 设置项 | 值 | 说明 |
|--------|-----|------|
| **Require signed commits** | 建议 ❌ | GitHub Free 不支持，忽略 |
| **Require linear history** | 建议 ❌ | Squash merge 已保证线性，不需要额外限制 |
| **Lock branch** | ❌ | 不要勾选——这会阻止所有 push，包括通过 PR |

### Step 3 — 保存并验证

1. 点击页面底部绿色 **Create** 或 **Save changes** 按钮
2. 回到仓库主页，做一次烟雾测试：

```bash
# 尝试直接 push main（应该被拒绝）
echo "test" > /tmp/test_protection.txt
git add /tmp/test_protection.txt  # 不会生效，仅示意
# 预期结果：remote: error: GH006: ... protected branch ...

# 正确流程：通过 feat/fix 分支 + PR
git checkout -b feat/test-protection
echo "test" >> README.md
git add README.md && git commit -m "test: verify branch protection"
git push origin feat/test-protection
# → 创建 PR → 观察是否需要审批 → 确认 Squash & Merge 可用
```

## 状态检查（Status Check）的具体配置

如果在 Step 2 中启用了 "Require status checks"，需要指定具体的 CI job 名称：

| 仓库 | 建议的 Status Check 名称 | 说明 |
|------|------------------------|------|
| SROS | `pytest` / `make test` | 如果已配置 GitHub Actions CI |
| ARC-Engine | `pytest` / `make test` | 同上 |
| GraphMRI-Lite | `pytest` / `make test` | 同上 |
| Hermes-Workflows | `pytest` / `make test` | 同上 |
| Project_SXMU_MDD_Twin | — | 科研项目，可暂不要求 CI |

> **如果仓库尚未配置 GitHub Actions**：建议先用 `gh pr create --fill` 发起一个测试 PR，观察是否有 CI job 出现在 status check 列表中。如果没有 CI，暂时**取消勾选** "Require status checks"，否则所有 PR 都会卡住无法合并。

## 5 仓库配置 Checklist

完成后逐项打勾：

- [ ] SROS — `main` 分支保护已启用（PR + 1 approval + Squash & Merge）
- [ ] ARC-Engine — `main` 分支保护已启用（PR + 1 approval + Squash & Merge）
- [ ] GraphMRI-Lite — `main` 分支保护已启用（PR + 1 approval + Squash & Merge）
- [ ] Hermes-Workflows — `main` 分支保护已启用（PR + 1 approval + Squash & Merge）
- [ ] Project_SXMU_MDD_Twin — `main` 分支保护已启用（PR + 1 approval + Squash & Merge）
- [ ] 烟雾测试：直接 push main 被拒绝
- [ ] 烟雾测试：通过 feat 分支 + PR 可正常合并

## 替代方案：GitHub CLI 配置

如果你更习惯使用命令行，也可以用 `gh api` 配置（需要 GitHub Token 有 admin:repo 权限）：

```bash
OWNER="your-org-or-user"
REPO="SROS"

gh api repos/$OWNER/$REPO/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_last_push_approval": true
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": false
}
EOF
```

> **注意**：`enforce_admins: true` 要求管理员也遵守 PR 规则（即 "Do not allow bypassing"）。GitHub Free 计划的个人仓库可能在 API 返回 422 错误，此时请改用 Web UI 方式并跳过此字段。

## 配置完成后

更新 `ROADMAP.md` 中第 78 行：

```markdown
| DevX Branch Protection | GitHub 5 仓库 main 分支写保护 + Squash & Merge | P1 | ✅ |
```
