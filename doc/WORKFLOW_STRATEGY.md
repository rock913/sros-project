# AI 辅助开发框架 5.0：统一会话驱动工作流 (Session-Driven Workflow)

本文档是 `GEMINI.md` 的核心支撑策略，定义了一个统一的、由 AI 驱动的开发与调试工作流。它取代了旧有的、分离的开发和调试策略，旨在提供一个更流畅、一致且完全可追溯的开发体验。

## 核心理念：万物皆会话 (Everything is a Session)

我们不再区分“开发过程”和“调试过程”，而是将所有工作都视为一个 **“会话 (Session)”**。一个会话是从“定义目标”到“完成目标”的完整工作记录。调试不再是一个独立的流程，而是会话中一个可能被触发的 **“状态”**。

## 1. 文件组织与命名规范

所有会话日志都必须存储在项目根目录的 `/.ai-sessions/` 文件夹下，以确保所有工作的集中管理和可发现性。

### 标准化命名格式（2025-10-15 14:00 更新）

**通用格式**: `YYYY-MM-DD-HHmm-phase-X.Y-<category>-<description>.md`

**组成部分**:
1. **日期时间前缀**: `YYYY-MM-DD-HHmm` (ISO 8601 格式，24小时制，UTC+0)
   - 示例: `2025-10-15-1430` = 2025年10月15日 14:30 UTC
   - 用途: 确保文件按精确创建时间自然排序，支持同一天多次会话
   
2. **阶段标识**: `phase-X.Y` (小写，用连字符)
   - 示例: `phase-3.6`, `phase-4.1`, `phase-5.0`
   - 用途: 快速识别文件所属开发阶段
   
3. **类别标签**: `<category>` (单个单词，小写)
   - 可选值: `plan`, `progress`, `report`, `test`, `debug`, `analysis`, `summary`, `reference`
   - 用途: 区分文档类型和用途
   
4. **描述**: `<description>` (kebab-case，1-5个单词)
   - 示例: `day1-backend-hitl`, `unit-hitl-nodes`, `progress-optimization`
   - 用途: 简洁描述会话具体内容

### 类别详细定义

#### `plan` - 实施计划
-   **用途**: 用于记录阶段或功能的详细实施计划
-   **频率**: 每个阶段开始时 1-2 个
-   **命名示例**:
    - `2025-10-14-phase-3.6-plan-implementation-guide.md` - Phase 3.6 总体实施指南
    - `2025-10-15-phase-3.6-plan-week3-document-collaboration.md` - Week 3 文档协作计划
-   **典型内容**:
    - 阶段目标和成功标准
    - 任务分解（按天/周）
    - 技术设计概要
    - 依赖和风险评估

#### `progress` - 日常进度
-   **用途**: 用于记录每天或每个里程碑的开发进度
-   **频率**: 每天 1-3 个（取决于工作复杂度）
-   **命名示例**:
    - `2025-10-14-0900-phase-3.6-progress-day1-backend-hitl.md` - 上午的 Day 1 后端 HITL 开发进度
    - `2025-10-14-1430-phase-3.6-progress-day2-frontend-ui.md` - 下午的 Day 2 前端 UI 开发进度
    - `2025-10-15-1000-phase-3.6-progress-day4-streaming-protocol.md` - 上午的 Day 4 流式协议开发
-   **典型内容**:
    - 当天完成的任务列表
    - 遇到的问题和解决方案
    - 代码变更摘要
    - 下一步行动计划

#### `report` - 完成报告
-   **用途**: 用于记录阶段、周或重大里程碑的完成情况
-   **频率**: 每个里程碑 1 个
-   **命名示例**:
    - `2025-10-14-1800-phase-3.6-report-week1-2-hitl-complete.md` - Week 1-2 HITL 功能完成报告
    - `2025-10-20-1700-phase-3.6-report-final-completion.md` - Phase 3.6 最终完成报告
-   **典型内容**:
    - 交付成果统计
    - 质量指标（测试覆盖率、bug 数量）
    - 时间对比（计划 vs 实际）
    - 经验教训和下一步建议

#### `test` - 测试报告
-   **用途**: 用于记录单元测试、集成测试、E2E 测试的执行结果
-   **频率**: 每次重要测试执行后创建
-   **命名示例**:
    - `2025-10-14-1530-phase-3.6-test-unit-hitl-nodes.md` - HITL 节点单元测试报告
    - `2025-10-14-1630-phase-3.6-test-e2e-comprehensive.md` - 全面 E2E 测试报告
    - `2025-10-15-1415-phase-3.6-test-websocket-message-format.md` - WebSocket 消息格式测试
-   **典型内容**:
    - 测试用例列表和结果
    - 代码覆盖率统计
    - 发现的 bug 和修复状态
    - 性能指标（如果适用）

#### `debug` - 调试记录
-   **用途**: 用于记录独立的 Bug 修复过程（非功能开发流程中的 Bug）
-   **频率**: 按需创建（如 E2E 测试失败、用户报告 Bug）
-   **命名示例**:
    - `2025-10-15-1045-phase-3.6-debug-websocket-conflict-detection.md` - WebSocket 冲突检测 Bug
    - `2025-10-16-0930-phase-3.6-debug-e2e-test-failure.md` - E2E 测试失败调试
-   **典型内容**:
    - 错误重现步骤
    - 错误堆栈和日志
    - 假设和诊断过程
    - 修复方案和验证结果

#### `analysis` - 分析文档
-   **用途**: 用于记录战略分析、进度反思、技术评估
-   **频率**: 每周 1-2 个，或重大决策前
-   **命名示例**:
    - `2025-10-15-1400-phase-3.6-analysis-progress-optimization.md` - 进度对比与优化建议
    - `2025-10-18-1100-phase-3.6-analysis-conflict-resolution-strategy.md` - 冲突解决策略分析
-   **典型内容**:
    - 现状分析（进度、质量、风险）
    - 对比分析（计划 vs 实际）
    - 优化建议和决策依据
    - 风险评估和缓解方案

#### `summary` - 阶段总结
-   **用途**: 用于记录阶段或项目的整体总结
-   **频率**: 每个阶段结束时 1 个
-   **命名示例**:
    - `2025-10-20-1800-phase-3.6-summary-complete.md` - Phase 3.6 完整总结
    - `2025-11-30-1700-phase-4.1-summary-observability.md` - Phase 4.1 可观测性总结
-   **典型内容**:
    - 阶段目标达成情况
    - 关键成果和亮点
    - 遇到的挑战和解决方案
    - 对后续阶段的建议

#### `reference` - 快速参考
-   **用途**: 用于创建快速查阅的参考文档
-   **频率**: 每个阶段 1-2 个
-   **命名示例**:
    - `2025-10-15-0900-phase-3.6-reference-api-endpoints.md` - HITL API 端点快速参考
    - `2025-10-18-1030-phase-3.6-reference-websocket-protocol.md` - WebSocket 协议参考
-   **典型内容**:
    - API 文档摘要
    - 关键配置和命令
    - 常见问题和解决方案
    - 架构图和数据流图

### 目录结构

-   **`/.ai-sessions/development/`**
    -   **用途**: 用于记录 **功能驱动 (Feature-Driven)** 的工作，即为了实现一个新功能或新需求而启动的会话。
    -   **命名**: 遵循上述标准化格式
    -   **索引**: `README.md` 文件提供阶段和类别的快速索引

-   **`/.ai-sessions/debugging/`**
    -   **用途**: 用于记录 **独立 Bug 修复**（非功能开发流程中的调试），典型触发场景：
        -   E2E 测试 (`e2e_test.sh`) 失败
        -   来自用户的 Bug 报告
        -   周期性集成测试的失败
    -   **命名**: 遵循上述标准化格式（category 通常为 `debug`）

### 旧格式文件处理

**策略**: 保留现有文件不重命名，避免破坏 Git 历史和现有引用

**实施**:
1. 现有文件（如 `PHASE_3.6_DAY1_PROGRESS.md`）保持原样
2. 在 `README.md` 中创建索引，映射旧文件到新命名规范
3. 未来新创建的文件严格遵循新命名规范

**示例索引** (`.ai-sessions/development/README.md`):
```markdown
## Phase 3.6 Files

| 新格式（推荐） | 旧格式文件（已存在） | 日期 | 类别 |
|---------------|-------------------|------|------|
| 2025-10-14-phase-3.6-plan-implementation-guide.md | PHASE_3.6_IMPLEMENTATION_GUIDE.md | 2025-10-14 | plan |
| 2025-10-14-phase-3.6-progress-day1-backend-hitl.md | PHASE_3.6_DAY1_PROGRESS.md | 2025-10-14 | progress |
| 2025-10-14-phase-3.6-test-unit-hitl-nodes.md | PHASE_3.6_UNIT_TEST_REPORT.md | 2025-10-14 | test |
```

## 2. 统一会话工作流

**原则 0：契约先行 (Principle 0: Contract First)**

在任何涉及多组件（尤其是前后端）交互的功能开发中，我们严格遵循“API 契约先行”的原则。

-   **为什么？** 为了从根本上解决前后端开发步调不一致的问题，确保双方基于一个统一的、明确的规范进行工作，从而实现真正的并行开发并减少后期集成风险。
-   **如何做？** 使用 **OpenAPI (Swagger)** 规范来定义 API。该契约 (`openapi.yaml`) 是前后端交互的唯一“真相来源”。
-   **何时做？** 在功能开发的“初始化”阶段，定义或更新契约是最高优先级的任务。

无论是开发还是调试，所有会话都遵循相同的基本结构和流程。

### 阶段一：初始化 (Initialization)

1.  **创建会话文件**: 根据工作意图，在 `development` 或 `debugging` 目录下创建一个新的会话文件。
2.  **定义核心目标 (The Goal)**: 在文件顶部清晰地说明本次会话需要达成的最终目标。
    -   **对于功能开发**: 目标是让某个 `*.feature` 验收测试通过。
    -   **对于 Bug 修复**: 目标是让某个失败的测试（如 `e2e_test.sh`）成功运行。
3.  **初步分析与计划 (Analysis & Plan)**:
    -   **分析**: 记录为了解现状而进行的分析、搜索和文件阅读。
    -   **计划**: 将工作分解为一系列清晰、可执行的步骤。
    -   **契约定义 (Contract Definition)**: 对于涉及前后端交互的功能，此阶段的**核心产出物**是 `openapi.yaml` 文件的创建或更新。在契约未经评审和确认前，不应开始任何编码实现。

### 阶段二：迭代执行 (Iterative Execution)

按计划逐一执行步骤，并在会话文件中实时记录。

**`[Step N: <描述>]`**

-   **`Action`**: 简要描述当前步骤的操作。
-   **`Tool Call`**: 记录用于执行该操作的精确工具调用（如 `replace`, `write_file`, `run_shell_command`）。
-   **`Verification`**:
    -   记录用于验证该步骤的命令（如 `make test`）。
    -   附上测试结果的摘要。
    -   标记状态：`✅ Success` 或 `❌ Failed`。
    > **Note**: For a complete catalog of available verification commands across the project, refer to the canonical `TESTING.md` document.

### 阶段三：调试状态 (Debugging State) - 条件触发

当任何 `Verification` 步骤的结果为 `❌ Failed` 时，会话 **在当前步骤下，就地进入“调试状态”**。

-   **`## 调试快照 (Debugging Snapshot)`**:
    -   **`Error`**: 完整粘贴复现的错误信息和堆栈跟踪。
    -   **`Hypothesis`**: 提出关于问题根源的明确假设。
    -   **`Fix Attempt`**: 记录用于尝试修复的 `Tool Call`。
    -   **`Verification`**: 重新运行失败的测试，记录结果。
        -   如果成功，调试状态结束，原 `[Step N]` 标记为 `✅ Success`，流程返回阶段二，继续执行下一个计划步骤。
        -   如果再次失败，则在同一个 `## 调试快照` 下启动新一轮的“诊断-修复-验证”循环。

### 阶段四：会话完成 (Completion)

当“核心目标”中定义的最终验收标准被满足时（例如，`*.feature` 或 `e2e_test.sh` 通过），会话完成。

1.  **最终确认**: 记录最终测试的成功结果。
2.  **总结 (Optional)**: 对本次会话的工作进行简要总结。
3.  **代码提交 (Optional)**: 运行 `git status` 和 `git diff`，起草 `commit message`，并等待用户确认。

## 3. Development Environment

To ensure the **Unified Session Workflow** is executed in a consistent and reproducible manner, this project relies on a containerized development environment powered by **VS Code Dev Containers**.

### Key Characteristics:

-   **Containerized:** The entire development environment is defined as code within Dockerfiles and Docker Compose files. This guarantees that every developer (human or AI) uses the exact same set of dependencies and tools.
-   **Pre-configured:** The Dev Containers are pre-configured for both frontend and backend development, with all necessary VS Code extensions and settings already installed.
-   **Separation of Concerns:** There are two distinct Dev Container configurations:
    -   **Frontend:** The default, for UI/UX and VS Code extension development.
    -   **Backend:** For development on the core Python agent.
    This separation allows for a focused development experience tailored to the specific task. Instructions for switching between them are in the main `README.md`.

### How it Supports the Workflow:

-   **Initialization:** When starting a new session, the developer can quickly launch the appropriate Dev Container, ensuring a clean slate for the task.
-   **Verification:** All verification steps (e.g., running tests) are executed within the container. This eliminates any potential for local machine configuration to affect the outcome, making the `✅ Success` or `❌ Failed` status a reliable signal.
-   **Debugging State:** When a test fails, the developer is already in a fully-equipped debugging environment. They can use the VS Code debugger, access the container's shell, and inspect the running services, all within the same context where the failure occurred.

## 4. Advantages

-   **流程统一**: 开发和调试遵循同一套心智模型和记录标准，降低了 AI 和人类的认知负荷。
-   **历史连贯**: 一个功能的完整生命周期，包括所有弯路和修复，都记录在单一、连续的文件中，提供了无与伦by的追溯能力。
-   **结构清晰**: 通过目录分离了工作的初始意图，同时通过内联调试状态保持了单个任务的叙事完整性。