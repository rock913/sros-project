# Phase 2 后端真实数据交互开发计划

**创建日期：** 2025-11-02  
**状态：** 📋 规划中  
**目标：** 将 VS Code 扩展从 Mock 模式升级到后端真实数据交互

---

## 📊 当前开发现状分析

### ✅ 已完成的工作

#### 1. **后端基础设施** (Phase 1 Complete)
- ✅ FastAPI 服务器运行在 `http://localhost:8121`
- ✅ PostgreSQL + pgvector 数据库已配置
- ✅ LangGraph Agent 四阶段研究流程已实现
- ✅ PostgresSaver Checkpointer 集成完成
- ✅ 多会话支持（thread-based）
- ✅ Langfuse 可观测性集成

#### 2. **VS Code 扩展框架** (Phase 2 Complete - Mock Mode)
- ✅ 三面板布局已实现：
  - **左侧**：Asset Library (TreeView)
  - **中间**：Manuscript (编辑器)
  - **右侧**：AI Control Panel (Webview)
- ✅ 基础命令已注册：
  - `auto-researcher.start` - 启动研究（Mock）
  - `auto-researcher.showControlPanel` - 显示控制面板
  - `auto-researcher.refreshAssetLibrary` - 刷新资源库
  - `researchAgent.viewPaperDetails` - 查看论文详情
  - `researchAgent.exportPapers` - 导出论文

#### 3. **API 客户端** (部分完成)
- ✅ API 基础配置：`http://langgraph-api:8000`
- ✅ 健康检查：`checkHealth()`
- ✅ 状态获取：`getAgentState()`
- ✅ Phase 3.5.2 API：
  - `getAllPapers()` - 获取所有论文
  - `getAllReports()` - 获取所有报告
  - `exportPapers()` - 导出论文
  - `compareReports()` - 比较报告

#### 4. **测试覆盖**
- ✅ 后端测试：25/25 通过 (Phase 3.5.2)
- ✅ 前端测试：15/15 通过 (Phase 3.5.2)
- ✅ Mock 模式验证：✅ 工作正常

---

### ❌ 当前限制

#### 1. **启动研究流程 (Mock 模式)**
```typescript
// 当前实现：vscode-extension/src/extension.ts 第 961-1004 行
vscode.window.showInformationMessage(
    '⚠️ WebSocket streaming not yet implemented. Using mock progress for now.'
);
// ... 模拟进度更新 ...
message: '✅ Research completed! (Mock mode)'
```

**问题：**
- ❌ 不调用后端 API 创建研究任务
- ❌ 不使用 WebSocket 获取实时进度
- ❌ 进度更新是模拟的 setTimeout
- ❌ 无法获取真实的论文和报告

#### 2. **HITL 交互 (Mock 模式)**
```typescript
// 第 1385-1472 行
// Create mock HITL request
let mockRequest: HITLRequest;
```

**问题：**
- ❌ 使用硬编码的 Mock 数据
- ❌ 不连接后端真实的 HITL 节点

#### 3. **文档协作 (Mock 模式)**
```typescript
// 第 1486-1518 行
const mockUpdates: DocumentUpdate[] = [...]
```

**问题：**
- ❌ 使用预定义的文档更新
- ❌ 不从后端流式接收文档变更

---

## 🎯 集成目标

### 核心目标
将 VS Code 扩展与后端 API 完全集成，实现：

1. **真实研究流程**
   - 用户输入 → 后端创建线程 → 启动 Agent → 实时进度 → 返回结果
   
2. **实时状态同步**
   - WebSocket 连接后端
   - 显示 Agent 思考过程
   - 更新论文列表和报告

3. **历史数据展示**
   - 显示所有历史会话
   - 查看已收集的论文
   - 浏览报告版本历史

---

## 📋 开发计划（3周）

### Week 1: 基础 API 集成与研究启动流程

#### 任务 1.1: 扩展后端 API 客户端 (2天)

**文件：** `vscode-extension/src/api.ts`

**新增功能：**

```typescript
// 1. 创建研究线程
export interface CreateThreadRequest {
  metadata?: {
    research_topic?: string;
    [key: string]: any;
  };
}

export interface ThreadResponse {
  thread_id: string;
  created_at: string;
  metadata: any;
}

export async function createThread(
  request: CreateThreadRequest
): Promise<ThreadResponse> {
  const response = await axios.post(`${API_BASE_URL}/threads`, request);
  return response.data;
}

// 2. 启动研究任务
export interface StartResearchRequest {
  assistant_id: string;  // "agent"
  input: {
    messages: Array<{
      role: string;
      content: string;
    }>;
  };
  stream_mode: string[];  // ["values", "updates"]
}

export async function startResearch(
  threadId: string,
  topic: string
): Promise<string> {
  const request: StartResearchRequest = {
    assistant_id: "agent",
    input: {
      messages: [
        {
          role: "user",
          content: `Please research: ${topic}`
        }
      ]
    },
    stream_mode: ["values", "updates"]
  };
  
  const response = await axios.post(
    `${API_BASE_URL}/threads/${threadId}/runs/stream`,
    request
  );
  return response.data.run_id;
}

// 3. 获取线程状态
export interface ThreadState {
  values: AgentState;
  next: string[];
  metadata: any;
}

export async function getThreadState(
  threadId: string
): Promise<ThreadState> {
  const response = await axios.get(
    `${API_BASE_URL}/threads/${threadId}/state`
  );
  return response.data;
}
```

**验证：**
- [ ] 能成功创建线程
- [ ] 能启动研究任务
- [ ] 能获取线程状态

---

#### 任务 1.2: 重构研究启动命令 (3天)

**文件：** `vscode-extension/src/extension.ts`

**重构步骤：**

```typescript
// 替换 Mock 实现 (第 920-1007 行)
const startResearchCommand = vscode.commands.registerCommand(
  'auto-researcher.start',
  async () => {
    try {
      // 1. 检查后端健康状态
      const health = await checkHealth();
      if (!health || !health.ok) {
        vscode.window.showErrorMessage(
          '❌ Backend not available. Please check if the service is running.'
        );
        return;
      }

      // 2. 获取研究主题
      const topic = await vscode.window.showInputBox({
        prompt: 'Enter your research topic',
        placeHolder: 'e.g., "Latest advances in transformer architectures"',
        validateInput: (value) => {
          if (!value || value.trim().length < 5) {
            return 'Please enter a topic (at least 5 characters)';
          }
          if (value.trim().length > 200) {
            return 'Topic is too long (max 200 characters)';
          }
          return null;
        }
      });

      if (!topic) {
        return; // 用户取消
      }

      // 3. 创建线程
      vscode.window.showInformationMessage(
        `🚀 Creating research session for: "${topic}"`
      );

      const thread = await createThread({
        metadata: { research_topic: topic }
      });

      // 4. 创建进度面板
      const panel = vscode.window.createWebviewPanel(
        'researchProgress',
        `Research: ${topic.substring(0, 30)}${topic.length > 30 ? '...' : ''}`,
        vscode.ViewColumn.One,
        {
          enableScripts: true,
          retainContextWhenHidden: true
        }
      );

      // 5. 显示初始 HTML
      panel.webview.html = generateResearchProgressHTML(topic, thread.thread_id);

      // 6. 启动研究任务
      panel.webview.postMessage({
        command: 'updateProgress',
        message: '📝 Starting research agent...',
        progress: 10
      });

      const runId = await startResearch(thread.thread_id, topic);

      // 7. 轮询状态更新（暂时使用，Week 2 会改为 WebSocket）
      const pollInterval = setInterval(async () => {
        try {
          const state = await getThreadState(thread.thread_id);
          
          // 更新进度
          const progress = calculateProgress(state);
          panel.webview.postMessage({
            command: 'updateProgress',
            message: getProgressMessage(state),
            progress: progress
          });

          // 检查是否完成
          if (state.next.length === 0) {
            clearInterval(pollInterval);
            panel.webview.postMessage({
              command: 'complete',
              message: '✅ Research completed!',
              progress: 100
            });

            // 刷新视图
            assetLibraryProvider.refresh();
            manuscriptProvider.refresh();

            vscode.window.showInformationMessage(
              `✅ Research on "${topic}" completed! Check the panels for results.`
            );
          }
        } catch (error) {
          clearInterval(pollInterval);
          panel.webview.postMessage({
            command: 'error',
            message: `Error: ${error}`
          });
        }
      }, 2000); // 每2秒轮询一次

    } catch (error) {
      vscode.window.showErrorMessage(`Failed to start research: ${error}`);
    }
  }
);

// 辅助函数
function calculateProgress(state: ThreadState): number {
  // 根据 Agent 状态计算进度
  if (state.values.search_queries && state.values.search_queries.length > 0) {
    return 25;
  }
  if (state.values.literature_abstracts && state.values.literature_abstracts.length > 0) {
    return 50;
  }
  if (state.values.report && state.values.report.length > 0) {
    return 75;
  }
  return 10;
}

function getProgressMessage(state: ThreadState): string {
  if (state.values.report && state.values.report.length > 0) {
    return '✍️ Generating final report...';
  }
  if (state.values.literature_abstracts && state.values.literature_abstracts.length > 0) {
    return `📚 Collected ${state.values.literature_abstracts.length} papers...`;
  }
  if (state.values.search_queries && state.values.search_queries.length > 0) {
    return '🔍 Searching academic databases...';
  }
  return '📝 Generating search queries...';
}
```

**验证：**
- [ ] 启动研究命令能创建真实线程
- [ ] 进度更新显示真实的 Agent 状态
- [ ] 完成后能看到真实的论文和报告
- [ ] 错误处理正常

---

#### 任务 1.3: 更新控制面板显示 (1天)

**文件：** `vscode-extension/src/extension.ts` (第 1009-1049 行)

**改进：**

```typescript
const showControlPanelCommand = vscode.commands.registerCommand(
  'auto-researcher.showControlPanel',
  async () => {
    // 添加线程选择
    const sessions = await getSessionsList({ limit: 10 });
    
    let selectedThreadId: string | undefined;
    
    if (sessions.sessions.length > 0) {
      const items = sessions.sessions.map(s => ({
        label: s.title || s.research_topic || 'Untitled Session',
        description: `${s.status} | ${s.paper_count} papers`,
        detail: new Date(s.created_at).toLocaleString(),
        threadId: s.thread_id
      }));

      const selected = await vscode.window.showQuickPick(items, {
        placeHolder: 'Select a research session'
      });

      if (selected) {
        selectedThreadId = selected.threadId;
      }
    }

    const panel = vscode.window.createWebviewPanel(
      'aiControlPanel',
      selectedThreadId 
        ? `Control Panel - ${selectedThreadId.substring(0, 8)}`
        : 'AI Control Panel',
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    panel.webview.html = '<html><body><h2>Loading...</h2></body></html>';

    let healthStatus = 'unknown';
    let agentState: AgentState = {
      literature_abstracts: [],
      report: '',
    };

    try {
      const health = await checkHealth();
      healthStatus = health.ok ? 'ok' : 'error';

      if (selectedThreadId) {
        const threadState = await getThreadState(selectedThreadId);
        agentState = threadState.values;
      } else {
        agentState = await getAgentState();
      }
    } catch (err) {
      healthStatus = 'error';
      console.error('Error fetching agent data:', err);
    }

    panel.webview.html = generateControlPanelHTML(agentState, healthStatus);
  }
);
```

**验证：**
- [ ] 能选择历史会话查看状态
- [ ] 显示真实的 Agent 数据
- [ ] 错误处理友好

---

### Week 2: WebSocket 集成与实时更新

#### 任务 2.1: 实现 WebSocket 客户端 (3天)

**新文件：** `vscode-extension/src/websocket.ts`

```typescript
import WebSocket from 'ws';

export type WebSocketMessageHandler = (message: any) => void;

export class ResearchWebSocketClient {
  private ws: WebSocket | null = null;
  private threadId: string;
  private handlers: Map<string, WebSocketMessageHandler[]> = new Map();

  constructor(threadId: string, baseUrl: string = 'ws://langgraph-api:8000') {
    this.threadId = threadId;
    this.connect(baseUrl);
  }

  private connect(baseUrl: string) {
    const url = `${baseUrl}/agent/stream?thread_id=${this.threadId}`;
    this.ws = new WebSocket(url);

    this.ws.on('open', () => {
      console.log(`WebSocket connected for thread ${this.threadId}`);
      this.emit('connected', { threadId: this.threadId });
    });

    this.ws.on('message', (data: string) => {
      try {
        const message = JSON.parse(data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    });

    this.ws.on('close', () => {
      console.log('WebSocket closed');
      this.emit('closed', {});
    });
  }

  private handleMessage(message: any) {
    // 根据消息类型分发
    if (message.type === 'state_update') {
      this.emit('state_update', message.data);
    } else if (message.type === 'progress') {
      this.emit('progress', message.data);
    } else if (message.type === 'hitl_request') {
      this.emit('hitl_request', message.data);
    } else if (message.type === 'document_update') {
      this.emit('document_update', message.data);
    } else if (message.type === 'complete') {
      this.emit('complete', message.data);
    }
  }

  public on(event: string, handler: WebSocketMessageHandler) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }
    this.handlers.get(event)!.push(handler);
  }

  private emit(event: string, data: any) {
    const handlers = this.handlers.get(event) || [];
    handlers.forEach(handler => handler(data));
  }

  public send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  public close() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
```

**验证：**
- [ ] WebSocket 能成功连接
- [ ] 能接收后端消息
- [ ] 能发送消息到后端
- [ ] 错误处理和重连机制

---

#### 任务 2.2: 集成 WebSocket 到研究流程 (2天)

**文件：** `vscode-extension/src/extension.ts`

**修改启动命令：**

```typescript
// 替换轮询为 WebSocket
const wsClient = new ResearchWebSocketClient(thread.thread_id);

wsClient.on('connected', () => {
  panel.webview.postMessage({
    command: 'updateProgress',
    message: '📝 Starting research agent...',
    progress: 10
  });
  
  // 启动研究
  startResearch(thread.thread_id, topic);
});

wsClient.on('state_update', (state: AgentState) => {
  const progress = calculateProgress({ values: state, next: [], metadata: {} });
  panel.webview.postMessage({
    command: 'updateProgress',
    message: getProgressMessage({ values: state, next: [], metadata: {} }),
    progress: progress,
    state: state
  });
});

wsClient.on('progress', (data: any) => {
  panel.webview.postMessage({
    command: 'updateProgress',
    message: data.message,
    progress: data.progress
  });
});

wsClient.on('complete', (data: any) => {
  panel.webview.postMessage({
    command: 'complete',
    message: '✅ Research completed!',
    progress: 100
  });

  // 刷新视图
  assetLibraryProvider.refresh();
  manuscriptProvider.refresh();

  vscode.window.showInformationMessage(
    `✅ Research on "${topic}" completed!`
  );

  wsClient.close();
});

wsClient.on('error', (error) => {
  panel.webview.postMessage({
    command: 'error',
    message: `Error: ${error}`
  });
  vscode.window.showErrorMessage(`Research error: ${error}`);
});

// 清理
panel.onDidDispose(() => {
  wsClient.close();
});
```

**验证：**
- [ ] 实时进度更新流畅
- [ ] 状态变化即时反映
- [ ] 面板关闭时连接正确关闭

---

#### 任务 2.3: 更新 TreeView 数据源 (2天)

**文件：** `vscode-extension/src/extension.ts`

**修改 AssetLibraryProvider：**

```typescript
class AssetLibraryProvider implements vscode.TreeDataProvider<AssetItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<AssetItem | undefined | null | void> = 
    new vscode.EventEmitter<AssetItem | undefined | null | void>();
  readonly onDidChangeTreeData: vscode.Event<AssetItem | undefined | null | void> = 
    this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: AssetItem): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: AssetItem): Promise<AssetItem[]> {
    if (!element) {
      // 根节点：显示分组
      return [
        new AssetItem('Recent Papers', vscode.TreeItemCollapsibleState.Expanded, 'group'),
        new AssetItem('All Sessions', vscode.TreeItemCollapsibleState.Collapsed, 'group')
      ];
    }

    if (element.label === 'Recent Papers') {
      // 获取最近的论文
      try {
        const result = await getAllPapers({ limit: 20 });
        return result.papers.map(p => 
          new AssetItem(
            p.title,
            vscode.TreeItemCollapsibleState.None,
            'paper',
            {
              command: 'researchAgent.viewPaperDetails',
              title: 'View Paper',
              arguments: [p]
            },
            p
          )
        );
      } catch (error) {
        console.error('Failed to load papers:', error);
        return [];
      }
    }

    if (element.label === 'All Sessions') {
      // 获取所有会话
      try {
        const result = await getSessionsList({ limit: 50 });
        return result.sessions.map(s =>
          new AssetItem(
            s.title || s.research_topic || 'Untitled',
            vscode.TreeItemCollapsibleState.Collapsed,
            'session',
            undefined,
            s
          )
        );
      } catch (error) {
        console.error('Failed to load sessions:', error);
        return [];
      }
    }

    if (element.contextValue === 'session') {
      // 显示会话下的论文
      try {
        const session = element.data as Session;
        const result = await getAllPapers({ session_id: session.id, limit: 100 });
        return result.papers.map(p =>
          new AssetItem(
            p.title,
            vscode.TreeItemCollapsibleState.None,
            'paper',
            {
              command: 'researchAgent.viewPaperDetails',
              title: 'View Paper',
              arguments: [p]
            },
            p
          )
        );
      } catch (error) {
        console.error('Failed to load session papers:', error);
        return [];
      }
    }

    return [];
  }
}

class AssetItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly contextValue: string,
    public readonly command?: vscode.Command,
    public readonly data?: any
  ) {
    super(label, collapsibleState);
    
    if (contextValue === 'paper') {
      this.iconPath = new vscode.ThemeIcon('file-text');
      this.tooltip = data?.abstract?.substring(0, 100) + '...';
    } else if (contextValue === 'session') {
      this.iconPath = new vscode.ThemeIcon('folder');
      this.tooltip = `${data?.paper_count || 0} papers`;
    }
  }
}
```

**类似修改 ManuscriptProvider：**

```typescript
class ManuscriptProvider implements vscode.TreeDataProvider<ManuscriptItem> {
  // ... 类似实现，显示报告历史 ...
  
  async getChildren(element?: ManuscriptItem): Promise<ManuscriptItem[]> {
    if (!element) {
      // 根节点
      return [
        new ManuscriptItem('Recent Reports', vscode.TreeItemCollapsibleState.Expanded, 'group')
      ];
    }

    if (element.label === 'Recent Reports') {
      try {
        const result = await getAllReports({ limit: 20 });
        return result.reports.map(r =>
          new ManuscriptItem(
            `Report v${r.version} - ${new Date(r.created_at).toLocaleDateString()}`,
            vscode.TreeItemCollapsibleState.None,
            'report',
            {
              command: 'researchAgent.openReport',
              title: 'Open Report',
              arguments: [r]
            },
            r
          )
        );
      } catch (error) {
        console.error('Failed to load reports:', error);
        return [];
      }
    }

    return [];
  }
}
```

**验证：**
- [ ] Asset Library 显示真实论文
- [ ] Manuscript 显示真实报告
- [ ] 点击项目能正确打开详情

---

### Week 3: HITL 集成与文档协作

#### 任务 3.1: HITL 决策集成 (3天)

**文件：** `vscode-extension/src/extension.ts`

**修改 HITL 命令（删除 Mock）：**

```typescript
// WebSocket 监听 HITL 请求
wsClient.on('hitl_request', async (request: HITLRequest) => {
  await handleHITLRequest(request, context);
});

// 实际的 HITL 处理（替换第 1385-1472 行）
async function handleHITLRequest(request: HITLRequest, context: vscode.ExtensionContext) {
  const panel = vscode.window.createWebviewPanel(
    'hitlDecision',
    `Decision Required: ${request.type}`,
    vscode.ViewColumn.Two,
    {
      enableScripts: true,
      retainContextWhenHidden: true
    }
  );

  panel.webview.html = generateHITLDecisionCardHTML(request);

  // 监听用户决策
  panel.webview.onDidReceiveMessage(
    async message => {
      if (message.command === 'submitDecision') {
        try {
          // 发送决策到后端
          await axios.post(`${API_BASE_URL}/agent/hitl/respond`, {
            request_id: request.id,
            decision: message.decision,
            feedback: message.feedback
          });

          panel.dispose();
          vscode.window.showInformationMessage('✅ Decision submitted');
        } catch (error) {
          vscode.window.showErrorMessage(`Failed to submit decision: ${error}`);
        }
      }
    },
    undefined,
    context.subscriptions
  );
}
```

**验证：**
- [ ] HITL 请求能正确显示
- [ ] 用户决策能提交到后端
- [ ] Agent 能根据决策继续执行

---

#### 任务 3.2: 文档协作集成 (3天)

**文件：** `vscode-extension/src/documentCollaboration.ts`

**修改文档更新处理（删除 Mock）：**

```typescript
export class DocumentCollaborationManager implements vscode.Disposable {
  // ... 现有代码 ...

  public async handleDocumentUpdate(update: DocumentUpdate): Promise<void> {
    // 不再使用 Mock 数据，而是从 WebSocket 接收真实更新
    
    // 1. 找到或创建报告文档
    const docUri = await this.getOrCreateReportDocument(update.session_id);
    
    // 2. 应用编辑
    const doc = await vscode.workspace.openTextDocument(docUri);
    const edit = new vscode.WorkspaceEdit();
    
    if (update.action === 'insert') {
      edit.insert(docUri, this.convertToPosition(doc, update.range.start), update.content);
    } else if (update.action === 'delete') {
      edit.delete(docUri, this.convertToRange(doc, update.range));
    } else if (update.action === 'replace') {
      edit.replace(docUri, this.convertToRange(doc, update.range), update.content);
    }
    
    await vscode.workspace.applyEdit(edit);
    
    // 3. 显示变更理由
    if (update.rationale) {
      this.showChangeRationale(update.rationale, update.range);
    }
  }

  private async getOrCreateReportDocument(sessionId: string): Promise<vscode.Uri> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
      throw new Error('No workspace folder open');
    }

    const reportsDir = vscode.Uri.joinPath(workspaceFolder.uri, 'reports');
    const docPath = vscode.Uri.joinPath(reportsDir, `${sessionId}.md`);

    try {
      await vscode.workspace.fs.stat(docPath);
    } catch {
      // 文件不存在，创建
      await vscode.workspace.fs.createDirectory(reportsDir);
      await vscode.workspace.fs.writeFile(
        docPath,
        Buffer.from(`# Research Report\n\n_Generated: ${new Date().toISOString()}_\n\n`)
      );
    }

    return docPath;
  }
}
```

**在启动命令中集成：**

```typescript
// WebSocket 监听文档更新
wsClient.on('document_update', async (update: DocumentUpdate) => {
  await docCollabManager.handleDocumentUpdate(update);
});
```

**验证：**
- [ ] 文档更新能实时应用
- [ ] 变更理由正确显示
- [ ] 多个更新顺序正确

---

#### 任务 3.3: 端到端测试与优化 (1天)

**创建测试文件：** `vscode-extension/src/test/integration/realBackend.test.ts`

```typescript
import * as assert from 'assert';
import * as vscode from 'vscode';
import { createThread, startResearch, getThreadState } from '../../api';

suite('Real Backend Integration Tests', () => {
  test('Complete research workflow', async function() {
    this.timeout(60000); // 60秒超时

    // 1. 创建线程
    const thread = await createThread({
      metadata: { research_topic: 'test' }
    });
    assert.ok(thread.thread_id);

    // 2. 启动研究
    const runId = await startResearch(thread.thread_id, 'test topic');
    assert.ok(runId);

    // 3. 等待完成（轮询）
    let completed = false;
    for (let i = 0; i < 30; i++) {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const state = await getThreadState(thread.thread_id);
      
      if (state.next.length === 0) {
        completed = true;
        break;
      }
    }

    assert.ok(completed, 'Research should complete within 60 seconds');

    // 4. 验证结果
    const finalState = await getThreadState(thread.thread_id);
    assert.ok(finalState.values.literature_abstracts.length > 0);
    assert.ok(finalState.values.report.length > 0);
  });
});
```

**优化清单：**
- [ ] 添加加载指示器
- [ ] 改进错误消息
- [ ] 添加取消操作支持
- [ ] 优化 UI 响应速度

---

## 📊 验收标准

### 功能验收

#### 1. 研究启动流程 ✅
- [ ] 用户输入研究主题
- [ ] 后端创建线程成功
- [ ] 实时进度更新显示
- [ ] 完成后论文和报告正确显示
- [ ] 错误处理友好

#### 2. 历史数据显示 ✅
- [ ] Asset Library 显示所有历史论文
- [ ] 可按会话分组查看
- [ ] Manuscript 显示报告历史
- [ ] 可比较不同版本报告

#### 3. 实时交互 ✅
- [ ] WebSocket 连接稳定
- [ ] HITL 决策正常工作
- [ ] 文档协作实时更新
- [ ] 网络中断能优雅处理

### 性能验收

- [ ] API 调用响应时间 < 1秒
- [ ] WebSocket 消息延迟 < 100ms
- [ ] UI 刷新流畅（60fps）
- [ ] 内存使用稳定（< 500MB）

### 测试覆盖

- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试通过率 100%
- [ ] 端到端测试通过率 100%

---

## 🛠️ 技术栈总结

### 后端
- **框架：** FastAPI
- **数据库：** PostgreSQL + pgvector
- **Agent：** LangGraph + LangChain
- **检查点：** PostgresSaver
- **可观测性：** Langfuse
- **通信：** HTTP + WebSocket

### 前端
- **平台：** VS Code Extension API
- **语言：** TypeScript
- **HTTP 客户端：** Axios
- **WebSocket：** ws
- **UI：** TreeView + Webview

### 开发工具
- **容器化：** Docker + Docker Compose
- **测试：** pytest (后端) + Mocha (前端)
- **文档：** OpenAPI + Swagger UI

---

## 📅 时间线

| 周次 | 时间 | 主要任务 | 交付物 |
|------|------|---------|--------|
| Week 1 | Day 1-2 | API 客户端扩展 | `api.ts` 新增 5 个函数 |
| Week 1 | Day 3-5 | 研究启动流程重构 | 真实 Agent 集成 |
| Week 1 | Day 6-7 | 控制面板更新 | 会话选择功能 |
| Week 2 | Day 1-3 | WebSocket 客户端 | `websocket.ts` 完成 |
| Week 2 | Day 4-5 | WebSocket 集成 | 实时进度更新 |
| Week 2 | Day 6-7 | TreeView 数据源 | 显示历史数据 |
| Week 3 | Day 1-3 | HITL 集成 | 真实决策流程 |
| Week 3 | Day 4-6 | 文档协作集成 | 实时编辑功能 |
| Week 3 | Day 7 | 测试与优化 | 完整验收 |

---

## 🚀 快速开始

### 1. 启动后端服务

```bash
# 使用开发版 docker-compose
docker compose -f docker-compose-dev.yml up -d

# 验证服务
curl http://localhost:8121/ok
```

### 2. 启动 VS Code 扩展开发

```bash
cd vscode-extension
npm install
code .
# 按 F5 启动调试
```

### 3. 测试基础 API

```bash
# 创建线程
curl -X POST http://localhost:8121/threads \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"test": "true"}}'

# 启动研究
THREAD_ID="<your_thread_id>"
curl -X POST "http://localhost:8121/threads/${THREAD_ID}/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {
      "messages": [{"role": "user", "content": "Research LangGraph"}]
    },
    "stream_mode": ["values"]
  }'
```

---

## 📚 参考文档

- [GEMINI.md](../GEMINI.md) - AI 辅助开发框架
- [ROADMAP.md](../ROADMAP.md) - 完整路线图
- [backend/API_DOCUMENTATION.md](../backend/API_DOCUMENTATION.md) - API 文档
- [PHASE2_DEBUG_GUIDE.md](./PHASE2_DEBUG_GUIDE.md) - 调试指南
- [PHASE3_WEBSOCKET_SUMMARY.md](./PHASE3_WEBSOCKET_SUMMARY.md) - WebSocket 指南

---

**更新日期：** 2025-11-02  
**维护者：** AutoBrainLab Team  
**状态：** 📋 待实施
