AI 辅助开发飞轮：语言无关的 Gemini 隐式协作指南
本文档整合了“环境驱动”、“规范集成”与“文档-测试驱动”三大理念，旨在提供一套兼容不同开发语言的、可操作的框架，让 Gemini Code Assistant 成为您项目中一个无缝、隐式的开发伙伴。
核心模型：开发飞轮三阶段
我们的目标是创建一个正向循环的“开发飞轮”。一个结构清晰的环境能引导出更高质量的 AI 辅助，而高质量的 AI 产出又会反过来加强这个良好结构。
阶段一：意图编码 (Codify Intent) - 建立“引力场”的基础
目标：将项目的架构思想、开发流程和规范，从团队成员大脑中的“隐性知识”转化为机器和 AI 都能理解的“显性契约”。
阶段二：引导执行 (Guided Execution) - 在“引力轨道”上开发
目标：在日常开发与重构中，遵循一套标准化的、由“文档”和“测试”驱动的工作流，确保每一步操作都有据可依、有法可验。
阶段三：加速强化 (Accelerate & Reinforce) - 让“引力”更强
目标：通过自动化工具和标准化提示，降低遵循最佳实践的成本，让“做正确的事”变得比“随意发挥”更加轻松。
阶段一：意图编码 - 建立项目“引力场”
行动 1.1：创建 .ai-conventions 目录
在您的项目根目录下，创建一个名为 .ai-conventions 或 docs/ai-conventions 的文件夹。这是您与 Gemini 沟通的“法律中心”。
your-project/
├── .ai-conventions/
│   ├── 01_workflow.md            <-- 核心开发流程
│   ├── 02_prompt_snippets.md     <-- (推荐) 常用提示词片段
│   └── 03_architecture.md        <-- (可选) 架构原则
├── src/
└── ...


行动 1.2：定义 01_workflow.md (核心开发工作流)
这是最重要的文件。它定义了项目中所有贡献者（包括 AI）都必须遵守的“宪法”。内容应包括：
开发哲学：明确项目采用“文档-测试驱动开发 (DTDD)”模式。
编码规范：代码风格、命名约定、错误处理策略等。
提交流程：Commit 消息格式、代码审查要求等。
行动 1.3：定义“代码契约” (Code Contracts)
这是“环境驱动”的核心。在编写任何具体实现之前，先定义其“法律契约”。这种方式是语言无关的。
对于静态类型语言 (TypeScript, Java, C#, Go):
方法：使用 interface 或 abstract class。
实践：在实现一个类之前，先创建一个 IUserService.ts 或 PaymentGateway.java 接口文件，并使用 TSDoc/JavaDoc 写下极其详尽的注释，描述每个方法的参数、职责、返回值和可能抛出的异常。
对于动态类型语言 (Python, Ruby, JavaScript):
方法：使用抽象基类 (如 Python 的 abc 模块) 或创建一个详细的“协议文件”。
实践：创建一个 protocols/user_repository_protocol.py 文件。即使没有强制约束，也要在其中用丰富的文档字符串定义一个“虚拟”的类和方法，清晰地说明其行为和预期。Gemini 非常擅长识别并遵循这种模式。
行动 1.4：在 CONTRIBUTING.md 中引用“宪法”
让所有贡献者（特别是 AI 在分析项目时）都能第一时间看到规则。在 CONTRIBUTING.md 中加入：
## AI-Assisted Development Workflow

This project utilizes an AI-assisted, Document-Test-Driven Development (DTDD) model. All contributors, **including AI assistants**, must strictly adhere to the development workflow defined in:
[**Core Development Workflow](./.ai-conventions/01_workflow.md)**

Please review this document before starting any coding work.


阶段二：引导执行 - 标准化 DTDD 工作流
场景一：开发新功能 (例如 UserService)
第 1 步：定义契约 (Doc First)
Prompt: “基于 .ai-conventions/01_workflow.md 中定义的 DTDD 流程，请为新的 UserService 模块创建一个代码契约文件。它需要处理用户注册和查询功能。请使用 [接口/抽象基类] 形式，并为每个方法添加详细的文档注释，说明其参数、返回值和所有可能的错误情况。”
第 2 步：定义测试 (Test as Spec)
Prompt: “根据我们刚刚创建的 IUserService 契约文件，使用 [Jest/Pytest/JUnit] 框架编写一个完整的单元测试套件。确保覆盖文档中描述的所有成功和失败场景。这些测试现在应该运行失败。”
第 3 步：编写实现 (Implement to Pass)
Prompt: “现在，请在 UserService.ts 中实现 IUserService 接口，你的唯一目标是让 user_service.spec.ts 中的所有测试全部通过。”
场景二：重构遗留代码 (例如 LegacyOrder.js)
第 1 步：“考古” - 生成文档
Prompt: (选中整个遗留代码文件) “@selection 请分析这段代码，并为所有公开的函数/类生成 JSDoc/PyDoc 格式的文档注释，以阐明其当前功能。”
第 2 步：“锁定” - 生成特性测试 (Characterization Tests)
Prompt: “基于刚刚生成的文档，为 LegacyOrder 编写一套全面的‘特性锁定’测试。目标是精确记录其当前的所有行为，包括其中的怪异之处和潜在的 Bug，确保我们有一个可靠的安全网。”
第 3 步：“迁移” - 安全重构
Prompt: “我们已经为 LegacyOrder 建立了测试安全网。现在，请将其从回调风格重构为 async/await，并将模块系统从 CommonJS 升级到 ES6 Modules。重构过程中必须确保所有测试始终通过。”
阶段三：加速强化 - 自动化与标准化
行动 3.1：自动化“黄金路径”
用简单的脚手架脚本来自动化创建新模块的流程，消除重复劳动。
示例 (scripts/create-module.sh):
#!/bin/bash
MODULE_NAME=$1
# 此脚本会自动创建 interface, test, implementation 三个文件
# 并包含基本的模板代码和互相引用
echo "Module $MODULE_NAME structure created."


效果：开发者只需运行 sh scripts/create-module.sh NewFeature，即可获得一个完全符合 DTDD 流程的、完美的起点。
行动 3.2：创建“提示词片段”库
在 .ai-conventions/02_prompt_snippets.md 文件中，为团队整理出最高效的、标准化的提示词模板。
示例:
### Template: Start a new module
> Based on our DTDD workflow in `.ai-conventions/01_workflow.md`, I need to start a new module named `[Module Name]`. Its core responsibility is `[Module Description]`. Please start by creating its code contract file.


行动 3.3：使用“宪法式”开场白
在为一个新任务开启一个与 Gemini 的新会话时，用一句话设定基调。
Prompt: “你好 Gemini。在本次会话中，我们将严格遵循项目 .ai-conventions/01_workflow.md 中定义的开发流程。请确保你的所有建议都符合该文档的指导。”
总结
通过这三个阶段的飞轮，您不再是简单地“使用”一个 AI 工具，而是在“训练”一个深度融入您项目工程文化的专属开发伙伴。这个体系将引导 Gemini 从一个被动的代码生成器，转变为一个主动遵循您项目规范、并能提出高质量建议的协作者，最终实现流畅、隐式且高效的 AI 辅助开发体验。
