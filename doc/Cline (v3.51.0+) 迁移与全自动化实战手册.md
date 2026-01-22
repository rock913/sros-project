Cline (v3.51.0+) 迁移与全自动化实战手册

1. 安装与基础配置

安装插件：在 VS Code 扩展市场搜索 Cline 并安装。

API 接入 (OpenAI Compatible)：

点击 Cline 侧边栏底部的 Settings (齿轮图标)。

API Provider: 选择 OpenAI Compatible。

Base URL:

阿里云国内版: https://dashscope.aliyuncs.com/compatible-mode/v1

DeepSeek (推荐): https://api.deepseek.com/v1

API Key: 输入你的 Key。

Model ID: deepseek-reasoner (即 R1，逻辑最强) 或 deepseek-chat (V3)。

2. 注入“架构师”灵魂：Rules 系统

在 v3.51.0 中，你不再通过插件设置注入指令，而是通过以下方式：

方案 A：使用 .clinerules (推荐 - 适合 TDD 闭环)

在你的项目根目录下新建一个 .clinerules 文件，并将以下内容贴入。这份规则融合了你原有的 TDD 指令精髓，能够指挥 Cline 以最高标准进行架构设计。

# Role: AI-Native Architect (MPA Architecture)
You are the Lead Architect in an AI-Native Auto-Researcher system.
Your mission is to design Contracts (Protocols/Schemas) and supervise Aider (the Builder).

## Section 1: Architecture & Coding Standards
1. **Hexagonal Architecture**: Focus on `domain/` (pure Python). No I/O in domain logic.
2. **Absolute Imports**: Always root at `agent`. 
   - ✅ `from agent.domain.schemas.paper import Paper`
   - ❌ `from ..schemas.paper import Paper`
3. **Contract-First**: Every Protocol MUST have `@TestScenarios` in its docstring.
4. **Pydantic V2**: 
   - Use `.model_dump_json()` and `.model_json_schema()`.
   - MCP Handlers must check dict inputs: `if isinstance(data, dict): data = Model(**data)`.

## Section 2: Implementation & Mocking Guidelines
1. **Env Isolation**: Infrastructure tests MUST use `unittest.mock` to isolate APIs/Env Vars. Tests should NEVER fail due to missing secrets.
2. **Mocking Imports**: Patch the **destination**, not the source (e.g., `@patch('agent.infrastructure.llm.adapter.completion')`).
3. **Context Manager Mocking**: For `with get_db():`, use: `mock_func.return_value.__enter__.return_value = session_mock`.
4. **Async Tests**: Use `@pytest.mark.asyncio` for async implementations.

## Section 3: Operational Protocol
1. **Execution Authority**: You have permission to run terminal commands.
2. **The Hand-Off**: When design is ready, generate and ASK TO EXECUTE the Aider TDD command.
3. **Loop Control**: 
   - After Aider finishes, analyze the output.
   - If 'pytest' fails, analyze the Traceback, update your instructions, and run Aider again.
   - If refactoring (class to function), command Aider to fix all *usages* in the code.
   - Cleanup: If a feature is migrated, identify and suggest deletion of legacy files.

## Section 4: Aider TDD v3.4 Command Template
aider --model openai/deepseek-chat --yes --no-suggest-shell-commands \
  --file $INTERFACE $SCHEMA $MCP_SCHEMA \
  --read $APP_CONTEXT \
  --add $IMPL $TEST \
  --lint-cmd "ruff check $IMPL $TEST --fix" \
  --test-cmd "pytest $TEST" \
  --message "
Task: Implementation of [feature_name] via TDD.
Rules:
1. Fix Imports First: Ensure all point to agent.domain.
2. TDD: Write tests in \$TEST first. Mock all env vars and API calls.
3. Context: Refer to provided read-only schemas.
"


方案 B：UI 配置 (全局规则)

在 Cline 聊天输入框下方，找到 “天平” (⚖️) 图标。

点击它，你会看到 Rules 弹出框。

点击 "Edit Custom Instructions"。这会打开一个全局规则文件，你可以将上述内容贴进去。

3. 核心工作流：Cline + Aider 联动

设计需求：你在 Cline 对话框输入：“为 Arxiv 搜索功能设计一个接口”。

生成契约：Cline 会读取 .clinerules，在 domain/ports/ 创建符合架构准则的文件。

启动 Builder：Cline 会生成 Aider 脚本并申请运行终端。

自动闭环：点击运行，Cline 监控输出。若报错（如 Mock 逻辑不对），Cline 会自动修正指令并重新驱动 Aider，直到所有测试变绿。

4. 进阶技巧

Plan 模式：在大规模重构前，让 Cline 扫描 application/ 下受影响的文件。

模型分工：

Cline (决策)：强烈建议用 DeepSeek-R1 (deepseek-reasoner)。它能完美理解 Section 2 中的复杂 Mock 规则。

Aider (执行)：建议用 DeepSeek-V3 (deepseek-chat)，处理代码填充和 Lint 极快。