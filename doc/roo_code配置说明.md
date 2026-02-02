Roo Code 自定义模式配置模板与进阶指南

本指南基于 Roo Code 2026 最新官方文档及 MPA（架构师-执行者）开发策略编写。建议使用 YAML 格式进行配置，以获得更好的可读性和多行字符串支持。

1. 核心配置属性说明

在配置 custom_modes.yaml 或 .roomodes 时，请参考以下关键属性：

UI 字段 / YAML 属性

描述

slug

内部唯一标识符（仅限字母、数字、连字符）。用于关联 .roo/rules-{slug}/ 规则文件夹。

name

UI 中显示的名称。

description

模式选择器中显示的简短摘要。

roleDefinition

核心身份定义。位于系统提示词开头，定义 Roo 的专业背景和行为准则。

groups

工具权限组。可选：read, edit, browser, command, mcp。可使用元组限制文件范围。

whenToUse

触发场景。帮助 Orchestrator 模式在任务切换时自动选择正确的模式。

customInstructions

附加行为指南，位于系统提示词末尾，是对角色定义的进一步补充。

2. 自定义模式模板 (MPA 架构优化版)

你可以将以下内容直接粘贴到你的 custom_modes.yaml (全局) 或 .roomodes (项目级) 文件中。

模式 1：MPA-Architect (架构总监)

该模式专注于高层设计和契约定义，通过限制 edit 权限来防止其陷入具体的实现细节。

customModes:
  - slug: mpa-arch
    name: MPA-Architect
    description: 专注于系统架构设计与契约（Protocol/Schema）定义。
    roleDefinition: >-
      你是一个资深的 AI 原生架构师。你的核心使命是在 AI-Native Auto-Researcher 系统中设计 Contract (Protocols/Schemas) 并监督 Aider。
      你严格遵守以下标准：
      1. 六边形架构：聚焦 domain/ (纯 Python)，领域逻辑严禁 I/O 操作。
      2. 绝对导入：始终以 agent 为根（例如 from agent.domain.schemas...）。
      3. 契约优先：每个 Protocol 文档字符串中必须包含 @TestScenarios。
      4. Pydantic V2：必须使用 model_dump_json() 及 model_json_schema()。
    whenToUse: "当需要进行系统架构设计、定义接口协议 (Ports) 或数据模型 (Schemas) 时使用。"
    groups:
      - read
      - browser
      - mcp
      - ["edit", { "fileRegex": "\\.(py|md)$", "description": "仅限接口定义与文档" }]
    customInstructions: >-
      - 尽量减少中间分析文件，逻辑清晰时直接在代码注释中说明。
      - 设计完成后，生成详细的任务描述并指示用户切换到 aider-build 模式。
      - 严禁编写具体的 Infrastructure 实现代码。


模式 2：Aider-Builder (TDD 执行员)

该模式配置为高性能搬砖工，擅长使用 Aider 运行 TDD 闭环。

customModes:
  - slug: aider-build
    name: Aider-Builder
    description: 专注于利用 Aider 或 execute_tdd_loop MCP 工具完成代码实现。
    roleDefinition: >-
      你是一个高效的 TDD 执行员。你的唯一职责是：
      1. 接收来自 mpa-arch 模式的设计协议，并在 infrastructure 层完成实现。
      2. 优先调用 aider-factory MCP 工具运行 execute_tdd_loop。
      3. 环境隔离：Infrastructure 测试必须使用 unittest.mock 隔离 API/环境变量。
      4. 严格遵守 Contract，不添加任何多余功能。
    whenToUse: "当架构设计完成，需要通过 Aider 自动化闭环完成具体功能实现时使用。"
    groups:
      - read
      - edit
      - command
      - mcp
    customInstructions: >-
      - 运行终端命令时，严禁打印超过 100 行输出，使用 | head -n 50 截断以防止 IDE 冻结。
      - 使用 aider 时，必须明确指定目标文件 ($IMPL $TEST) 和上下文 (--read)，防止全库扫描导致 Context 爆炸。
      - 如果 pytest 失败，必须分析 Traceback，更新指令并重新运行 Aider。


3. 进阶实战策略

3.1 粘性模型 (Sticky Models) 策略

Roo Code 会记住每个模式最后使用的模型。建议：

mpa-arch: 关联 Claude 3.5 Sonnet 或 Claude 4.5 (指令遵循度最高)。

aider-build: 关联 DeepSeek-Chat 或 Grok-Code-Fast-1 (性价比高，极速推理)。

3.2 模式特定规则文件夹

利用目录级指令（Preferred Method）来管理复杂的规则：

在项目根目录创建 .roo/rules-mpa-arch/ 存放架构规约。

创建 .roo/rules-aider-build/ 存放 Mock 编写指南和测试命令规范。

这样可以防止搬砖工模式被庞大的架构设计文档干扰，从而节省 Token。

3.3 文件正则限制 (fileRegex)

对于 Architect 模式，强烈建议设置 fileRegex，使其只能编辑 domain/ 和 docs/ 下的文件，确保它不会在无意中开始编写实现代码，强制执行“设计与实现分离”的策略。

3.4 解决 Pending 状态

在 aider-build 的自定义指令中强调：

"在执行 Shell 命令（特别是 Aider）时，确保在末尾添加 && exit 0，以防止 Roo Code 的终端监听器在命令完成后依然处于 Pending 状态。"

提示：在 Roo Code 中点击“模式菜单”下的“3 级设置图标”即可导入/导出上述 YAML 配置。

4. Codebase Indexing 实战指南
4.1 核心价值
语义发现：让 Roo 能够通过自然语言找到跨文件的相关代码。

规避上下文爆炸：通过 RAG 只提取相关片段，有效缓解推理模型（如 QwQ）的输入 Token 限制。

4.2 🔴 避坑指南：DashScope 的 Batch Size 冲突
问题现象：配置 DashScope text-embedding-v3 时报 HTTP 400: Value error, batch size is invalid, it should not be larger than 10。

原因：阿里云 API 强制限制单次 Embedding 请求数量 ≤ 10，而 Roo Code 默认批处理大小通常远超此值且不可调。

结论：不建议直接通过 OpenAI Compatible 接口在 Roo Code 中使用 DashScope 进行全库索引。

4.3 ✅ 推荐方案：容器化 Ollama 服务
Ollama 不仅仅是一个命令行工具，它本质上是一个 API 服务。将 Ollama 和 Qdrant 封装在 Docker 中是最佳实践，能实现“一键拉起”整个 AI 索引后端。
最佳实践：Docker Compose 一键部署
使用以下配置可以同时运行索引数据库和 Embedding 服务：
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_data:/qdrant/storage
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    # 如果你有 NVIDIA GPU，请取消下面注释以实现硬件加速
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
```

**配置步骤：**
1. **启动服务**：`docker-compose -f docker-compose.ai-index.yaml up -d`。
2. **下载模型**：`docker exec -it ollama-container-name ollama run nomic-embed-text`。
3. **Roo Code 设置 (Indexing 面板)**：
   - **Embedder Provider**: `Ollama`
   - **Base URL**: `http://localhost:11434`
   - **Model ID**: `nomic-embed-text`
   - **Qdrant URL**: `http://localhost:6333`

### 4.4 搜索调优建议
* **Search Score Threshold**: 建议设置为 **0.4 - 0.5**。
* **Maximum Search Results**: 建议设置为 **20-30**。
* **更新策略**：在大规模重构后，点击 “Clear Index Data” 重新索引，以保证搜索结果的准确性。

**提示**：在 Roo Code 中点击“模式菜单”下的“3 级设置图标”即可导入/导出上述 YAML 配置。

## 5. Qwen Code CLI 配置指南 (Qwen3 Coder)

本指南介绍如何在 Roo Code 中配置阿里云 Qwen Code CLI Provider，以支持 Qwen3 Coder 模型（1M 上下文，支持 OAuth 自动刷新）。

### 5.1 前置准备

1.  **安装 Qwen 客户端**：从官方网站下载并安装。
2.  **身份验证**：运行客户端并登录，生成 OAuth 凭据。
    *   默认凭据路径：`~/.qwen/oauth_creds.json`
3.  **Roo Code 配置**：在 Provider 列表中选择 "Qwen Code CLI API"。

### 5.2 核心特性

*   **1M Context**：支持百万级 Token 上下文。
*   **OAuth 2.0**：安全认证与自动 Token 刷新（30秒缓冲）。
*   **免费额度**：推广期内提供 2,000 次/天及 60 次/分钟的免费调用（无 Token 限制）。
*   **Thinking Blocks**：完整支持思维链（Reasoning）。

### 5.3 常见问题排查

*   **"Cannot find credentials file"**：
    *   请确保已运行 Qwen 客户端完成认证。
    *   检查 `~/.qwen/oauth_creds.json` 是否存在。

*   **"Token refresh failed"**：
    *   检查网络连接。
    *   重新在 Qwen 客户端中进行认证。

*   **"401 Unauthorized"**：
    *   通常会自动刷新，请检查日志。
    *   若问题持续，请删除凭据文件并重新认证。

### 5.4 推荐模型

在配置 Provider 后，建议在 Roo Code 中选择以下模型：
*   **Qwen2.5-Coder-32B-Instruct** (通用编码)
*   **Qwen3-Coder** (体验最新 1M Context)
