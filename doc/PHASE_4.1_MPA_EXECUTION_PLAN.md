# Phase 4.1: MPA (MetaGPT+PydanticAI+Aider) 架构落地执行规划

**版本**: 1.0
**日期**: 2026-01-16
**状态**: 🚀 LAUNCHING

## 1. 核心目标
将项目从传统的单体 AI 辅助模式，转型为符合 `AI-Native 自主开发系统架构蓝皮书 v1.1` 的 **MPA (Multi-Agent Protocol Architecture)** 架构。实现 "Copilot 设计，Aider 实现" 的流水线。

## 2. 角色分工与工具链

| 角色 | 职责 (Responsibility) | 担当 (Actor) | 权限范围 (Scope) | 交付物 (Deliverables) |
| :--- | :--- | :--- | :--- | :--- |
| **Architect** | 需求分析, 接口定义, 数据建模 | **GitHub Copilot** | `schemas/`, `ports/` | Pydantic Models, Python Protocols |
| **Builder** | 业务逻辑实现, 外部接口适配 | **Aider + Qwen Max** | `adapters/`, `logic/` | 具体实现代码, 依赖注入配置 |
| **Inspector** | 单元测试, 边界测试 | **Aider + Qwen Max** | `tests/` | Pytest 测试用例, Mock 对象 |

## 3. 环境配置 (setup)

### 3.1 Aider 配置 (Qwen Max)
为了让 Aider 使用 Qwen Max (通义千问)，我们需要配置 OpenAI 兼容模式。

**步骤**:
1. 获取 DashScope API Key (`sk-xxx`).
2. 配置项目根目录下的 `.aider.conf.yml` (见下文模板).
3. 设置环境变量 `QWEN_API_KEY`.

### 3.2 目录结构演进
我们将逐步重构 `backend/src/agent/` 目录，由扁平结构转向六边形架构：

```text
backend/src/agent/
├── domain/           # [Architect] 核心领域层 (纯 Python, 无依赖)
│   ├── schemas/      # Pydantic 数据模型
│   └── ports/        # Protocol 接口定义
├── application/      # [Architect/Builder] 应用逻辑层
│   └── workflows/    # LangGraph 流程定义
├── infrastructure/   # [Builder] 基础设施/适配器层 (脏活累活)
│   ├── llm/          # LLM 适配器
│   ├── tools/        # 工具实现
│   └── db/           # 数据库适配器
└── main.py           # 启动入口
```

## 4. 标准工作流 (SOP)

### Step 1: Architect Design (Copilot)
**触发**: 用户在 Chat 面板输入需求。
**Prompt**: "作为 Architect，请为 [功能X] 设计 Pydantic 模型和 Protocol 接口。请输出到 `backend/src/agent/domain/`。"
**产出**: Copilot 生成并写入 `schemas/xxx.py` 和 `ports/xxx.py`。

### Step 2: Builder Implementation (Aider)
**触发**: 用户在终端运行 Aider。
**命令**:
```bash
export OPENAI_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY=$QWEN_API_KEY
aider --model openai/qwen-max --file backend/src/agent/domain/ports/xxx.py backend/src/agent/infrastructure/xxx_impl.py
```
**Prompt**: "我是 Builder。请阅读 `ports/xxx.py` 中的接口定义，并在 `infrastructure/xxx_impl.py` 中实现它。请使用 Pydantic 进行类型检查。"

### Step 3: Inspector Verification (Aider)
**触发**: Builder 完成实现后。
**命令**: Aider 保持运行。
**Prompt**: "我是 Inspector。请为刚才实现的 `infrastructure/xxx_impl.py` 编写单元测试。使用 `unittest.mock` 模拟 port 接口，确保测试运行时间 < 0.1s。"

## 5. 试点任务 (Pilot Task)
建议从一个独立的、低风险的模块开始试点。
**建议任务**: 重构 `Unpaywall` 工具的调用逻辑。
1. **Architect**: 定义 `PaperFetcher` Protocol。
2. **Builder**: 实现 `UnpaywallAdapter`。
3. **Inspector**: 测试 API 响应处理。
