# SROS 局部开发法则

> 本文件是 SROS 子项目的"地方法规"。Aider 在修改本目录下文件时自动读取。
> 全局宪法见根目录 `AI_RULES.md`。
> 功能规格见 `docs/PRD.md`。

## 技术栈
- Python 3.10+，**严禁**使用 3.12+ 语法 (PEP 695 type params 等)
- FastAPI + JSON-RPC (MCP Gateway — SSE transport)
- DuckDB (OLAP 查询引擎，8 表 DDL)
- Pydantic v2 (数据模型 + 序列化)
- Click (CLI 框架，`--raw` JSON 输出模式)

## 架构红线 (Hard Boundaries)
1. **Gateway 不含业务逻辑**：所有实现通过 `src/sros/skills/rpc.py` 的 `dispatch_tool()` 分发到 handler
2. **Skill-First**：所有能力通过 `sros-skill` CLI 暴露，`--raw` 输出纯 JSON
3. **Workspace-Relative Paths**：所有路径 workspace-relative，禁止 `../` 遍历
4. **IDE-as-UI**：Claude Code / Aider 通过 MCP 协议调用 SROS tools

## 新增 MCP Tool 的强制操作
1. 在对应的 `src/sros/servers/<domain>/` 中实现 handler
2. 在 `src/sros/skills/rpc.py` 的 TOOL_TABLE 中注册
3. 更新 `contracts/mcp/sros_tools.json` 契约快照
4. 运行 `make update-wiki` 刷新 Code-Wiki 图谱
5. 新增 ≥ 2 个单元测试

## 测试铁律
- **TDD 强制**：先写 failing test (`tests/unit/test_<module>.py`) → 实现 → `pytest` 绿灯
- 运行：`make test-sros` (从根目录) 或 `python3 -m pytest tests/ -v`
- 当前基线：138 tests green

## 禁止行为
- ❌ `import graphmri_lite` / `import arc_engine` (import-linter 拦截)
- ❌ 在 Gateway 中写业务代码
- ❌ 直接修改 `docs/code_wiki/` (由 `make update-wiki` 自动生成)
- ❌ 提交未格式化的代码
- ❌ push main 分支 (SLAIB: checkout feature branch → PR → Squash Merge)

## 关键文件速查
| 文件 | 用途 |
|------|------|
| `src/sros/gateway/main.py` | FastAPI MCP SSE Hub |
| `src/sros/skills/rpc.py` | Tool 分发器 (~50 tool names → handlers) |
| `config/duckdb/schema.sql` | 8 表 DDL |
| `docs/code_wiki/index.md` | 架构图谱入口 |
| `sros-sdk/` | Phase 9: AI4S DSL 科学编译器 |
