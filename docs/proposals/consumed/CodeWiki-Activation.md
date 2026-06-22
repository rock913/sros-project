> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-CodeWiki-Activation.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：Code-Wiki 强制激活

> 目标主 PRD：`01-Core_Infra/SROS/doc/SROS_V4.0.md`
> 提案日期：2026-05-13
> 驱动来源：总 PRD Section 12.3 — Code-Wiki 强制激活方案
> 状态：已交付 (2026-05-14 整合至 SROS_V4.0.md §1.3 + ROADMAP.md V3.4/S7)

## 动机 (Why)

ARC 的 Code-Wiki 编译能力已就绪（310 tests green），但图谱当前处于"写了但没用"的状态。SROS 仓库不存在 `docs/code_wiki/` 目录（尚未首次编译），且开发者工作流中没有任何机制确保图谱与代码同步。

要让 Code-Wiki 真正发挥"大模型架构记忆"的威力，必须把它强制嵌入日常代码提交流水线和 AI Agent 的初始上下文中。

## 提议新增/修改的内容

### 1. 创建 `Makefile`（新文件）

在 SROS 仓库根目录创建 `Makefile`，包含 `update-wiki` 目标：

```makefile
.PHONY: update-wiki

update-wiki:
	@echo "==> Calling ARC to refresh SROS Code-Wiki..."
	cd .. && arc build-code-wiki --config 01-Core_Infra/SROS/arc_wiki.json
	git add docs/code_wiki/
	@echo "==> Code-Wiki updated and staged."
```

### 2. 创建或更新 `CLAUDE.md`（新增 Code-Wiki 读取硬性规定）

在 SROS `CLAUDE.md` 中增加：

```markdown
## Code-Wiki 架构图谱读取要求（硬性规定）

当你在修改本仓库的代码前：
1. **必须**先读取 `docs/code_wiki/` 下的相关图谱文件，了解你要修改的模块在架构中的连线关系
2. 如果不确定影响范围，使用 `claw-graph-query --action search --keyword <module_name>` 查询依赖关系
3. 修改完代码后，提醒用户运行 `make update-wiki` 刷新图谱

违反此规定的代码修改属于无效交付。
```

### 3. 首次手动编译 Code-Wiki（用户操作）

在 SROS 仓库中手动运行一次 ARC 编译，生成初始 `docs/code_wiki/`：

```bash
cd 01-Core_Infra/SROS
# 确保 arc_wiki.json 和 docs/code_schema.md 已就位（Phase 1 交付物 S4）
arc build-code-wiki --config arc_wiki.json
ls docs/code_wiki/
```

### 4. `.gitignore` 确认

确认 `docs/code_wiki/` **不在** `.gitignore` 中——Code-Wiki 是版本化产物，需随代码一起提交。

## 验收标准

- [x] SROS 仓库根目录存在 `Makefile`，`make update-wiki` 可执行
- [x] SROS `CLAUDE.md` 包含 Code-Wiki 读取硬性规定
- [x] `docs/code_wiki/` 存在且包含有效的 Code-Wiki 页面（首次编译成功，203 文件，51 源文件全覆盖）
- [x] `make update-wiki` 能成功调用 ARC 编译器并更新图谱（DeepSeek API，0 errors）
- [x] SROS ROADMAP.md 中 S4/S7 任务已创建，V3.4 里程碑已添加

## 参考实现

- ARC Makefile 模式：`01-Core_Infra/ARC-Engine/Makefile`（如有）
- 总 PRD Section 12.3：Code-Wiki 三管齐下激活方案
- Phase 1 交付物：`arc_wiki.json` + `docs/code_schema.md`（本提案的前置条件）
- 全局 ROADMAP.md 近期行动清单第 3 项：Code-Wiki 激活
