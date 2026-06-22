> 本文档从 Meta 层策略文档下沉编译而来。原文档：upgrade-notes/0615-DeepSeek v4 Pro 架构适配与非对称成本优势指南.md。下沉日期：2026-06-21。

# MCP-to-OpenAI Adapter 设计论据

## 一、模型选型决策的工程经济学分析

主控模型选型确立为 DeepSeek v4 Pro。该选型与"以 TDD 契约替代流程化 SOP"的架构战略高度契合，其 API 定价结构（通常为同级竞品的 1/5 到 1/10）从根本上改变了自动化反馈循环的设计约束。

### 1.1 自动化重试循环的成本可行性

在基于测试反馈的自动化开发循环中，执行引擎（AI Agent）的典型行为模式为：尝试修复、运行测试、发现失败、分析根因、重新修复。此循环在单次任务中可能迭代 10-20 次。

使用高定价模型时，架构师在设计循环时面临经济约束：高重试上限意味着高预期成本，导致倾向于设置较低的 max_retries（如 3-5 次），降低了自动修复的成功概率。

DeepSeek v4 Pro 的定价结构消除了这一约束。在同样的任务场景下，可以将重试上限设置为 20 次或更高，显著提升自动修复的成功率，而预期成本保持在可接受范围内。

**工程体现**：在资源调度场景（如 CUDA OOM 恢复）中，系统可配置为在隔离环境中自主排查、迭代调整超参数多达 20 次，直至测试通过。这种"用低单位推理成本换取高自动化成功率"的策略，即 DeepSeek 赋予自动化管线的核心经济优势。

### 1.2 测试驱动开发范式的模型适配性

DeepSeek 的训练数据分布中，代码和数学逻辑语料占比较高。

"只提供验收标准（Test Cases），不提供操作步骤（SOP）"的交互范式恰好匹配 DeepSeek 的推理优势区间。当输入是明确的 pytest 失败堆栈和 Python 函数签名时，其修复准确率表现优异。相比之下，该模型在模糊的自然语言任务上不占优势，但 TDD 工作流本质上是结构化输入（测试失败 = 精确的错误信号），避免了模糊性。

## 二、工程影响与必要适配

### 2.1 MCP 协议翻译层

**问题陈述**：

MCP（Model Context Protocol）由 Anthropic 发起，Claude 官方 SDK 和 Claude Code 提供原生 MCP 支持。DeepSeek 提供的 API 完全兼容 OpenAI 格式（`tools` 和 `tool_choice` 字段）。两者之间存在协议格式断层：

- **MCP 输出格式**：JSON-RPC 2.0 包装，`method: "tools/list"` 返回 `[{name, description, inputSchema}]`
- **DeepSeek 期望格式**：OpenAI Function Calling 格式，`[{type: "function", function: {name, description, parameters}}]`

**架构决策**：

SROS Gateway 的 MCP 实现保持标准化（JSON-RPC 2.0），不因后端模型切换而修改——这是维护对外接口先进性和标准化所必需的。

在中间件层（Gateway 或 Hermes 集成层）增加一个轻量级 Python 适配模块，负责双向翻译：

1. **MCP → OpenAI 方向**：将 `tools/list` 响应中的 `inputSchema` 字段映射为 OpenAI Function Calling 的 `parameters` 字段（JSON Schema 子集兼容）
2. **OpenAI → MCP 方向**：将 OpenAI 返回的 `tool_call` 结构解析为 MCP `tools/call` 请求格式

**参考实现**：`src/sros/gateway/mcp_openai_adapter.py`（MCP-OpenAI-Adapter-Proposal.md 中定义的核心模块，含 `mcp_tools_to_openai()` + `openai_tool_call_to_mcp()` + `build_deepseek_request()` 三个核心函数）

### 2.2 系统提示词的风格适应

不同模型对指令风格存在差异化的响应特性：

- **Claude 系模型**：对角色定位、自然语言引导、详细上下文有较好的响应
- **DeepSeek 模型**：对结构化指令、明确的输入输出 schema、伪代码风格约束有更强的推理性能

**架构调整**：在全局 Agent 行为宪法（`AI_RULES.md`）和各子项目的 `CONVENTIONS.md` 中，指令应保持紧凑、强调逻辑边界、明确声明输入输出的 JSON Schema。避免过多的自然语言修饰和角色扮演式 preamble。

### 2.3 DSPy 编译器的后端配置

DSPy 框架通过 OpenAI 兼容接口支持 DeepSeek 作为后端大模型。

配置方法：
```python
import dspy

dspy_lm = dspy.OpenAI(
    model='deepseek-v4-pro',
    api_base='https://api.deepseek.com',
    api_key='...'
)
dspy.configure(lm=dspy_lm)
```

此配置使 DSPy 的硬约束断言（`dspy.Assert` / `dspy.Suggest`）和自动 prompt 优化管线可直接在 DeepSeek 上运行，无需修改 DSPy 业务逻辑。

## 三、对设计路线图的具体影响

### 3.1 终端 Agent 工具的可替换性

原设计强依赖特定 CLI 工具的 `--permission-mode auto` 模式。应替换为支持模型切换的开源终端 Agent 工具（如 Aider、OpenHands 或 SWE-agent），并将其底层大模型配置为 DeepSeek v4 Pro。

Aider 在使用 DeepSeek 模型时表现出的代码编辑能力可作为替代方案的参考基线。

### 3.2 MCP-to-OpenAI Adapter 在基础设施层的定位

在 SROS Gateway 层增加 MCP-to-OpenAI 适配端点，确保 SROS 提供给 AI Agent 的所有 MCP 工具都能被 DeepSeek 的 OpenAI 兼容 API 正确解析和调用。

具体任务已通过 `MCP-OpenAI-Adapter-Proposal.md`（提案 `SROS-MCP-OpenAI-Adapter.md`）交付实现。

### 3.3 AgenticOps 成本可观测性指标

在可观测层 Dashboard 中增加以下工程经济学指标：

- **单次自动修复预期成本（USD/Fix）**：每次自动 TDD 循环完成一次修复的平均 API 调用成本
- **自动化成功率 vs. 成本分布**：按 retry count 分桶的成功率与累计成本
- **模型效率对比**：同任务在不同模型下的 (成功率, 成本, 耗时) 三维对比

在 DeepSeek 的定价水平下，预期单次修复成本可达到极低水平，这一数据将直接支撑"全面自动化循环"架构决策的信心。

## 四、总结

切换到 DeepSeek v4 Pro 是一个务实的工程决策。其定价结构使"只提供测试契约和原子工具，由机器自主迭代试错"的架构哲学在成本上完全可行。基础设施越快完成以下两个方向的收敛，就越能充分利用该模型的推理能力：

1. **向上提供**：标准化的验收测试（pytest）和原子化的 MCP 工具
2. **向下适配**：MCP-to-OpenAI 协议翻译层，确保工具列表和调用双向无损转换
