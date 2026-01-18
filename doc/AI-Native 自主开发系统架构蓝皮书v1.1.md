版本: 1.1.0
日期: 2025-12-16
状态: 🟢 APPROVED
技术栈: MetaGPT (编排) + PydanticAI (协议) + Aider (执行)
1. 核心哲学：自主开发的缩放定律 (The Scaling Law of Autonomy)
在从 "AI 辅助 (Copilot)" 转向 "AI 自主 (Agent)" 的过程中，我们必须遵循以下工程定律：
1.1 代码库复杂度定律 (Codebase Complexity Law)
传统代码库中，随着代码行数 ($N$) 增加，上下文关联度呈 $O(N^2)$ 增长。对于 Context Window 有限的 AI 模型，这意味着项目越大，AI 越笨（更容易产生幻觉、逻辑遗忘）。
我们的目标: 通过强接口隔离，将 AI 需要理解的上下文复杂度恒定在 $O(1)$。
Autonomy \propto \frac{Interface Stability \times Type Safety}{Coupling \times Context Size}
自主性 正比于 接口稳定性 和 类型安全。
自主性 反比于 耦合度 和 上下文大小。
1.2 认知分层原则 (Cognitive Layering)
AI 不应同时扮演架构师、工程师和测试员。
架构师 (High Logic): 只需要看 Pydantic Models 和 Protocols。
工程师 (Implementation): 只需要看当前函数的输入输出。
测试员 (Verification): 只需要看接口定义和 Mock 对象。
2. 系统架构：MPA 混合协议架构 (The MPA Stack)
为了落地上述定律，本系统采用 "MPA" (MetaGPT + PydanticAI + Aider) 混合技术栈，构建六边形架构。
2.1 核心层 (The Core Sanctum) - Powered by PydanticAI
特征: 纯 Python 代码，无 I/O，无第三方重型依赖。
技术标准: 采用 PydanticAI 的 RunContext 进行依赖管理。
组成:
schemas/*.py: Pydantic 数据模型（AI 的数据字典）。
ports/*.py: Python Protocols（AI 的行为契约）。
logic/*.py: 纯业务逻辑（Functional Core）。
AI 策略: 这里是 Architect Agent 的领地。严禁随意修改。
2.2 适配器层 (The Adapters) - Powered by Aider
特征: 处理所有的脏活累活（读文件、连数据库、发请求）。
组成: adapters/*.py。
AI 策略: 这里是 Builder Agent 的领地。AI 可以随意重写这一层，只要它符合 Core 层的 Protocol 定义。
3. 开发策略：AI-Native 代码宪法
为了适配 PydanticAI 和 Aider，所有代码必须遵循以下“宪法”：
3.1 协议优先 (Protocol-First)
禁止在没有定义 Protocol 的情况下编写具体类。
Bad: def process(data_loader): ...
Good: def process(loader: DataProvider): ...
工具支持: 使用 Architect Agent 预先生成 ports/ 文件。
3.2 强类型契约 (Schema-First)
禁止使用 dict 或 Any 传递复杂数据。必须使用 Pydantic。
价值: Pydantic 的类定义就是最好的 Prompt。它在运行时自动拦截 AI 的逻辑错误。
PydanticAI 规范: 使用 BaseModel 定义所有 Agent 的 result_type。
3.3 显式依赖注入 (Explicit DI)
禁止在业务逻辑中 import 具体实现类（如 h5py）。必须通过 __init__ 或 PydanticAI 的 deps 注入接口。
价值: 这让 Inspector Agent 可以在 0.1秒内生成并运行 Mock 测试。
4. 多智能体编排方案 (Multi-Agent Orchestration)
我们将单体 Copilot 拆解为三个角色，并指定对应的开源工具支持。
角色 1: The Architect (架构师)
对应工具: MetaGPT (借鉴其 SOP 思想) / Claude 3.5 Sonnet
权限: 只读所有文件，只写 domain/ 和 ports/。
任务:
"分析需求。生成 System Design (Mermaid) 和 Interface Definition (Python Protocol)。不要写实现代码。"
角色 2: The Builder (工程师)
对应工具: Aider (CLI)
权限: 只读接口定义，读写 adapters/ 和 logic/。
任务:
"查看 ports/xxx.py。使用 repo-map 理解上下文。请在 adapters/ 中实现这个接口。你需要处理所有的 I/O 细节。"
角色 3: The Inspector (测试官)
对应工具: Aider (with test-cmd) / DeepSeek V3
权限: 只读代码，读写 tests/。
任务:
"为 logic/ 编写测试。使用 unittest.mock 模拟 ports/。专注于边缘情况（边界值、空值、异常）。"
5. 落地路线图 (Migration Roadmap)
Phase 0: 基础设施 (Infrastructure)
安装 aider-chat 和 pydantic-ai。
配置 .aider.architect.conf.yml (只读模式) 和 .aider.builder.conf.yml (读写模式)。
Phase 1: 隔离 (Isolation)
选取一个简单的模块（如数据加载）。
Architect: 使用 PydanticAI 定义 schemas/data.py。
Architect: 定义 ports/loader.py Protocol。
Phase 2: 重构 (Refactor)
Builder (Aider): aider --config .aider.builder.conf.yml 重写模块实现，注入依赖。
Inspector: 编写 Mock 测试，移除旧的 H5 依赖测试。
Phase 3: 扩展 (Scale)
对所有业务模块重复 Phase 1-2。
编写简单的 Python 脚本 (orchestrator.py) 来串联 Architect 和 Builder 的调用。
6. 附录：AI 指令集 (System Prompts)
针对 Architect 的 Prompt (MetaGPT Style)
Role: System Architect
Context: You are designing a Type-Safe, AI-Native system using PydanticAI.
Action: Define strict interfaces (Protocols) and data models (Pydantic).
Constraint: DO NOT write implementation logic. Output must be pure Python definition files.

针对 Builder 的 Prompt (Aider Style)
Role: Implementation Engineer
Context: You are using Aider to implement protocols.
Action: Implement the interfaces defined in `ports/` into `adapters/`.
Constraint: Strictly follow Pydantic schemas. Use Dependency Injection. Do not modify `ports/`.

针对 Inspector 的 Prompt
Role: QA Engineer
Action: Write unit tests using `pytest`.
Constraint: Mock all external dependencies defined in `ports/`. Tests must run in <0.1s.



MPA 技术栈实战指南：MetaGPT + PydanticAI + Aider
