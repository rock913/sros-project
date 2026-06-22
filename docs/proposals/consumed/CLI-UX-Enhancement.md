> 本文档从 Meta 层 proposal 下沉而来。原文件：meta-docs/proposals/delivered/SROS-CLI-UX-Enhancement.md。下沉日期：2026-06-21。

# SROS PRD 更新提案：CLI 结构化终端输出增强

> 目标主 PRD：`01-Core_Infra/SROS/doc/SROS_V4.0.md`
> 提案日期：2026-05-17
> 驱动来源：`meta-docs/strategy/四系统协同：游戏化开发与生态世界观构建战略.md` Section 3.1 + Section 5 隔离原则

## 动机 (Why)

SROS 作为开发者日常接触频率最高的 CLI 工具，当前输出风格为传统 print() 级纯文本，缺乏结构化视觉反馈。在全局游戏化战略的驱动下，Meta 层认可"终端质感升级"的价值——但根据架构级隔离原则，升级方案必须用 IEEE 软件工程标准语言描述，不得在 SROS PRD/源码中出现"基地""反应堆""掉落物"等游戏隐喻。

**核心区分**：
- SROS CLI 面向开发者（DevX 升级 = 提升调试效率与状态可见性）
- GraphMRI-Lite WebUI 面向临床用户（UX 升级 = 降低非技术用户焦虑）
- 两者目标不同，不共享任何游戏化语言

## 提议新增章节

在 SROS V4.0 PRD 中新增以下章节：

### 新增：Section X — 结构化终端输出增强 (Structured Terminal Output Enhancement)

```markdown
## X. 结构化终端输出增强

### X.1 目标

将 SROS CLI 从传统的无格式 print() 输出升级为结构化视觉反馈系统，
提升开发者在以下场景的认知效率：
- 多服务启动状态检查（`sros start`）
- 批量数据摄入进度追踪（`sros db ingest`）
- HPC 作业生命周期监控（`sros hpc status`）
- 系统健康诊断（`sros doctor`）

### X.2 技术方案

采用 Python Rich 库（或 Textual 框架）实现：
- 进度条 (Progress Bar)：长时间运行操作提供实时完成百分比
- 层级面板 (Panel)：将相关状态信息分组展示
- 表格渲染 (Table)：结构化数据（作业列表、数据库行数）的格式化输出
- 语法高亮 (Syntax Highlighting)：日志级别颜色编码 (ERROR=红, WARN=黄, INFO=绿)

### X.3 CLI 输出契约

- `--raw` 模式：保持现有 stdout=JSON 契约，不受视觉增强影响
- 默认模式：启用 Rich 渲染，stderr 保留原始日志流
- 非 TTY 环境（管道/重定向）：自动降级为纯文本

### X.4 关键命令规格

#### `sros start` — 服务启动状态面板

输出自检面板，展示每个子服务的启动状态：
- 服务名称
- 健康状态 (OK/WARN/FAIL)
- 延迟 (ms)
- 端口绑定信息

#### `sros db ingest` — 数据摄入进度

长时间运行操作显示：
- 总文件计数
- 已处理文件数 + 百分比进度条
- 当前处理文件名
- 预计剩余时间 (ETA)
- 完成摘要：成功/跳过/失败计数

#### `sros doctor` — 系统诊断报告

按子系统分组的 Panel 布局：
- SROS Gateway 健康
- DuckDB 连接状态
- ARC 安装版本 + Code-Wiki 新鲜度
- HPC 登录节点可达性
- 每个检查项的色彩编码 (绿/黄/红)

### X.5 验收标准

- [ ] `sros start` 输出结构化 Panel 布局，非纯文本流
- [ ] `sros db ingest` 长时间运行有实时进度条 + ETA
- [ ] `sros doctor` 诊断报告按子系统分组 + 色彩编码
- [ ] `--raw` 模式输出不受视觉增强影响
- [ ] 管道/重定向场景自动降级为纯文本
- [ ] 新增 `python3 -m pytest tests/unit/test_cli_output.py` 验证 TTY/非TTY 双路径
```

## 验收标准

- [ ] SROS V4.0 PRD 中新增「结构化终端输出增强」章节
- [ ] CLI 输出增强规格与 `--raw` JSON 契约不冲突
- [ ] 章节全文使用 IEEE 规范术语，不包含任何游戏隐喻
- [ ] SROS ROADMAP.md 中新增对应任务项

## 参考实现

- `01-Core_Infra/SROS/src/sros/gateway/` — 现有 MCP Gateway 状态输出格式
- `01-Core_Infra/SROS/src/sros/skills/rpc.py` — `dispatch_tool()` 的 JSON 响应格式
- `01-Core_Infra/GraphMRI-Lite/cli/main.py` — Click CLI `--raw` 双模式参考
- Python Rich 库：https://rich.readthedocs.io/
