AI 辅助开发框架 3.0：现场快照驱动的调试
本指南是 2.1 版本的重大升级，专注于解决 AI 在复杂调试场景中因缺乏全局上下文而导致的效率瓶颈。我们引入“现场快照”机制，旨在为 AI 提供一个信息完整的“案发现场”，使其能够进行更精准、更高效的根本原因分析。

第一、二、四部分 (无重大变更)
第一部分：三层测试防护 依然是保证代码质量和目标一致性的基石。

第二部分：GEMINI.md 项目知识库 依然是提供全局架构和设计原则的“长期记忆”。

第四部分：领航员模式 依然是提升开发者与 AI 协作深度和广度的最佳实践。

第三部分 (核心升级)：创建“自动化调试现场快照”
这是本次升级的核心。我们不再满足于生成一个简单的 .log 文件，而是创建一个结构化的、信息丰富的 Markdown 文件 DEBUG_SESSION.md，它包含了 AI 进行高效调试所需的一切。

核心理念：从“提供日志”到“重建现场”
当测试失败时，我们自动执行一个增强脚本，它会：

捕获错误摘要和完整的堆栈跟踪 (Stack Trace)。

解析堆栈跟踪，识别出所有相关的源文件路径。

自动读取并嵌入相关源文件的代码到快照中。

关联 GEMINI.md 中的架构原则。

最终生成一个类似这样的文件：

.ai-debug/DEBUG_SESSION.md (示例)

# 调试会话快照 (2025-09-24 05:34 AM)

## 1. 核心目标
- **验收测试**: `features/user_auth.feature`
- **用户故事**: 用户登出时，其 session 应被正确清除。

## 2. 失败摘要
- **错误**: `TypeError: Cannot read properties of null (reading 'clearSession')`
- **测试文件**: `tests/integration/auth.integration.spec.ts`

## 3. 堆栈跟踪 (Stack Trace)

TypeError: Cannot read properties of null (reading 'clearSession')
at AuthService.logout (src/services/AuthService.ts:45:25)
at AuthController.handleLogout (src/controllers/AuthController.ts:32:18)
at Object.<anonymous> (tests/integration/auth.integration.spec.ts:55:10)


## 4. 相关代码上下文 (案发现场)

### `src/services/AuthService.ts`
```typescript
// ... (代码片段)
  async logout(userId: string): Promise<void> {
    const session = await this.sessionRepository.findByUserId(userId);
    // ...
    session.clearSession(); // 错误发生行
    // ...
  }
// ... (代码片段)

src/controllers/AuthController.ts
// ... (代码片段)
  async handleLogout(req: Request, res: Response) {
    const { userId } = req.user;
    await this.authService.logout(userId); // 调用栈上一层
    res.status(200).send({ message: 'Logged out' });
  }
// ... (代码片段)

5. 架构指导 (来自 GEMINI.md)
设计原则: Service 层不应假设 Repository 查询总能返回非空结果，必须进行空值检查。


### 实施步骤

1.  **更新 `package.json`**：
    ```json
    "scripts": {
      "test": "jest --testFailureExitCode=1",
      "test:debug": "npm test || node scripts/create_debug_snapshot.js"
    }
    ```
    *确保 `jest` 在失败时返回非零退出码。*

2.  **使用新的脚本**：用下面提供的 `create_debug_snapshot.js` 替换旧的脚本。

### 全新的高效调试工作流

1.  在终端中运行 `npm run test:debug`。
2.  测试失败后，`.ai-debug/DEBUG_SESSION.md` 文件被自动创建或更新。
3.  您的 Prompt 变得无比强大和简洁：
    > **Prompt (终极版):** “你好 Gemini。请分析 `.ai-debug/DEBUG_SESSION.md` 文件中记录的现场快照，找出问题的根本原因，并直接提供 `AuthService.ts` 文件的修复方案。”

这个快照文件解决了 AI 理解全局能力的不足，因为它**将被动地“大海捞针”变成了主动地“按图索骥”**，极大地减少了无效的反复尝试，显著提升了复杂问题的调试效率。

### 本项目的实践：动态调试快照

在本项目中，我们将“现场快照”的理念进一步发展为一套由 AI 代理在每次调试会话中动态执行的工作流。这套流程被称为“动态调试快照”。

它将调试的每一步——从复现问题、分析原因、尝试修复到验证结果——都实时记录下来，形成一个完整的、结构化的追踪文档。

关于此策略的详细定义和工作流程，请参阅我们的新文档：[动态调试快照策略 (DEBUGGING_STRATEGY.md)](./DEBUGGING_STRATEGY.md)。
