# Phase 3.6 Implementation Guide: Real-time Collaboration & HITL
**Based on Technical Roadmap Vision vs. Current State Analysis**  
**Date**: October 14, 2025  
**Context**: Post Phase 3.5.3 completion, aligning with technical roadmap document

---

## 📋 Executive Summary

**Current Achievement**: Phase 3.5.3 完成，已实现：
- ✅ WebSocket实时通信 (Phase 3)
- ✅ 三栏式UI布局 (Left: Asset Library, Center: Editor, Right: Control Panel)
- ✅ 分析仪表板 (Analytics Dashboard with 4 charts)
- ✅ 历史数据管理 (Sessions, Papers, Reports tracking)

**Vision Gap**: 技术路线图第3章 "实时交互与动态协作" 尚未完全实现：
- ❌ **人在环路 (HITL)** 决策点 - 用户无法在关键环节干预AI
- ❌ **协同编辑** - AI无法直接修改VS Code编辑器中的文档
- ❌ **React-based Webview** - 当前Control Panel使用简单HTML，不是React

**Strategic Recommendation**: 优先实施 Phase 3.6 (3周)，完成核心协作功能，再进入Phase 4生态扩展。

---

## 🎯 Phase 3.6 详细规划

### Week 1-2: Human-in-the-Loop (HITL) Decision System

#### Vision Reference
> **技术路线图 Chapter 3**: "AI代理控制面板...包含任务控制台（自然语言指令）、'思考链'实时可视化器，以及用于'人在环路'决策的动态交互模块（如批准/拒绝卡片）。"

#### Current State Analysis
**已有基础**:
- ✅ WebSocket双向通信 (`/agent/stream`)
- ✅ Control Panel Webview (右侧面板)
- ✅ Session management (会话创建/跟踪)

**缺失部分**:
- ❌ LangGraph工作流暂停机制 (interrupt nodes)
- ❌ HITL决策UI组件 (批准/拒绝卡片)
- ❌ 用户决策反馈API (`POST /agent/hitl/respond`)

#### Implementation Tasks

##### Backend: LangGraph HITL Integration

**1. 修改 `backend/src/agent/graph.py` - 添加HITL节点**

```python
from langgraph.graph import StateGraph, interrupt

# 新增HITL决策节点
def query_approval_node(state: AgentState) -> AgentState:
    """
    阶段一后暂停：让用户批准/修改生成的搜索查询
    """
    queries = state["search_queries"]
    
    # 触发interrupt，向前端发送HITL请求
    user_decision = interrupt({
        "type": "hitl_request",
        "decision_point": "query_approval",
        "data": {
            "queries": queries,
            "prompt": "AI生成了以下搜索查询，请审核：",
            "actions": ["approve", "edit", "reject"]
        }
    })
    
    # 用户响应后恢复执行
    if user_decision["action"] == "approve":
        return state
    elif user_decision["action"] == "edit":
        state["search_queries"] = user_decision["edited_queries"]
        return state
    else:  # reject
        state["search_queries"] = []
        return state

def paper_selection_node(state: AgentState) -> AgentState:
    """
    阶段一后暂停：让用户筛选发现的论文
    """
    papers = state["literature_abstracts"]
    
    user_decision = interrupt({
        "type": "hitl_request",
        "decision_point": "paper_selection",
        "data": {
            "papers": [
                {"title": p.title, "abstract": p.abstract, "relevance": p.score}
                for p in papers
            ],
            "prompt": f"发现 {len(papers)} 篇论文，请选择要深入分析的：",
            "actions": ["select_all", "select_custom", "skip"]
        }
    })
    
    if user_decision["action"] == "select_custom":
        selected_ids = user_decision["selected_paper_ids"]
        state["literature_abstracts"] = [
            p for p in papers if p.id in selected_ids
        ]
    
    return state

# 修改图结构，插入HITL节点
graph_builder = StateGraph(AgentState)

# 原有节点
graph_builder.add_node("generate_queries", generate_queries_node)
graph_builder.add_node("search_literature", search_literature_node)
# ... 其他节点

# 新增HITL节点
graph_builder.add_node("query_approval", query_approval_node)
graph_builder.add_node("paper_selection", paper_selection_node)

# 重新编排边
graph_builder.add_edge("generate_queries", "query_approval")  # 查询生成后暂停
graph_builder.add_edge("query_approval", "search_literature")  # 用户批准后继续
graph_builder.add_edge("search_literature", "paper_selection")  # 搜索后暂停
graph_builder.add_edge("paper_selection", "extract_papers")  # 用户选择后继续
```

**2. 修改 `backend/src/agent/app.py` - 添加HITL API**

```python
from fastapi import HTTPException
from typing import Dict, Any

# 存储暂停的会话（生产环境应使用Redis）
pending_hitl_requests: Dict[str, Any] = {}

@app.post("/agent/hitl/respond")
async def respond_to_hitl(
    session_id: str,
    decision_point: str,
    action: str,
    data: Dict[str, Any] = None
):
    """
    用户响应HITL决策请求
    """
    if session_id not in pending_hitl_requests:
        raise HTTPException(status_code=404, detail="No pending HITL request")
    
    # 恢复LangGraph执行，传入用户决策
    response = {
        "action": action,
        **(data or {})
    }
    
    # 触发图继续执行（需要修改WebSocket流逻辑）
    pending_hitl_requests.pop(session_id)
    
    return {"status": "resumed", "session_id": session_id}

@app.get("/agent/hitl/pending")
async def get_pending_hitl(user_id: str = None):
    """
    获取用户所有待处理的HITL请求
    """
    pending = [
        {"session_id": sid, **req}
        for sid, req in pending_hitl_requests.items()
        if user_id is None or req.get("user_id") == user_id
    ]
    return {"pending_requests": pending, "count": len(pending)}
```

**3. 修改 WebSocket 处理逻辑**

```python
@app.websocket("/agent/stream")
async def websocket_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # ... 原有代码
    
    try:
        # 在executor中执行图，捕获interrupt
        config = {"configurable": {"thread_id": session_id}}
        
        for chunk in graph.stream(initial_state, config):
            # 检查是否是HITL interrupt
            if "interrupt" in chunk:
                hitl_request = chunk["interrupt"]
                pending_hitl_requests[session_id] = hitl_request
                
                # 发送HITL请求到前端
                await websocket.send_json({
                    "type": "hitl_request",
                    "session_id": session_id,
                    **hitl_request
                })
                
                # 等待用户响应（通过POST /agent/hitl/respond）
                while session_id in pending_hitl_requests:
                    await asyncio.sleep(0.5)
                
                # 获取用户决策，继续执行
                # ... 恢复图执行逻辑
            else:
                # 正常进度消息
                await websocket.send_json(chunk)
    
    except Exception as e:
        await websocket.send_json({"type": "error", "error": str(e)})
```

##### Frontend: HITL UI Components

**1. 扩展 `vscode-extension/src/api.ts` - HITL API函数**

```typescript
export interface HITLRequest {
    session_id: string;
    decision_point: 'query_approval' | 'paper_selection' | 'report_feedback';
    data: {
        queries?: string[];
        papers?: Array<{title: string, abstract: string, relevance: number}>;
        report_draft?: string;
        prompt: string;
        actions: string[];
    };
}

export interface HITLResponse {
    action: string;
    edited_queries?: string[];
    selected_paper_ids?: string[];
    feedback?: string;
}

export async function respondToHITL(
    sessionId: string,
    decisionPoint: string,
    response: HITLResponse
): Promise<void> {
    await axios.post(`${API_BASE_URL}/agent/hitl/respond`, {
        session_id: sessionId,
        decision_point: decisionPoint,
        ...response
    });
}

export async function getPendingHITL(userId?: string): Promise<HITLRequest[]> {
    const { data } = await axios.get(`${API_BASE_URL}/agent/hitl/pending`, {
        params: { user_id: userId }
    });
    return data.pending_requests;
}
```

**2. 创建 `vscode-extension/src/hitlWebview.ts` - HITL决策卡片**

```typescript
export function generateHITLCardHTML(request: HITLRequest): string {
    const { decision_point, data } = request;
    
    if (decision_point === 'query_approval') {
        return `
            <div class="hitl-card query-approval">
                <h3>🔍 搜索查询审核</h3>
                <p>${data.prompt}</p>
                <ul>
                    ${data.queries!.map((q, i) => `
                        <li>
                            <input type="checkbox" id="query-${i}" checked />
                            <input type="text" value="${q}" id="query-input-${i}" />
                        </li>
                    `).join('')}
                </ul>
                <div class="actions">
                    <button onclick="approveQueries()">✅ 批准</button>
                    <button onclick="editQueries()">✏️ 修改</button>
                    <button onclick="rejectQueries()">❌ 拒绝</button>
                </div>
            </div>
        `;
    }
    
    if (decision_point === 'paper_selection') {
        return `
            <div class="hitl-card paper-selection">
                <h3>📄 论文筛选</h3>
                <p>${data.prompt}</p>
                <div class="paper-list">
                    ${data.papers!.map((p, i) => `
                        <div class="paper-item">
                            <input type="checkbox" id="paper-${i}" checked />
                            <div class="paper-info">
                                <strong>${p.title}</strong>
                                <p class="abstract">${p.abstract.substring(0, 200)}...</p>
                                <span class="relevance">相关度: ${(p.relevance * 100).toFixed(0)}%</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="actions">
                    <button onclick="selectAllPapers()">全选</button>
                    <button onclick="selectCustomPapers()">确认选择</button>
                    <button onclick="skipPapers()">跳过</button>
                </div>
            </div>
        `;
    }
    
    return '<p>未知决策类型</p>';
}
```

**3. 修改 `vscode-extension/src/extension.ts` - WebSocket HITL处理**

```typescript
await startResearchStream(topic, {
    onStarted: (data) => {
        progress.report({ message: `研究开始 (会话: ${data.session_id})` });
    },
    
    onProgress: (data) => {
        progress.report({ message: data.message });
    },
    
    // 新增：HITL请求处理
    onHITLRequest: async (request: HITLRequest) => {
        // 暂停进度通知，显示HITL决策面板
        const panel = vscode.window.createWebviewPanel(
            'hitlDecision',
            '🤔 AI需要您的决策',
            vscode.ViewColumn.Beside,
            { enableScripts: true }
        );
        
        panel.webview.html = generateHITLCardHTML(request);
        
        // 等待用户决策
        panel.webview.onDidReceiveMessage(async (message) => {
            if (message.command === 'respond') {
                await respondToHITL(
                    request.session_id,
                    request.decision_point,
                    message.response
                );
                panel.dispose();
                vscode.window.showInformationMessage('✅ 决策已提交，AI继续执行...');
            }
        });
    },
    
    onComplete: (data) => {
        vscode.window.showInformationMessage('✅ 研究完成！');
    },
    
    onError: (error) => {
        vscode.window.showErrorMessage(`❌ 错误: ${error}`);
    }
});
```

#### Testing Checklist

- [ ] Backend: LangGraph interrupt触发成功
- [ ] Backend: `/agent/hitl/respond` API正常工作
- [ ] WebSocket: HITL请求消息正确发送到前端
- [ ] Frontend: HITL决策卡片正确渲染
- [ ] Frontend: 用户批准后工作流恢复执行
- [ ] Frontend: 用户拒绝后工作流正确终止
- [ ] E2E: 完整研究流程中断→决策→恢复

#### Acceptance Criteria

1. ✅ 用户可以在查询生成后审核/修改搜索查询
2. ✅ 用户可以在论文发现后筛选要分析的论文
3. ✅ HITL请求显示在VS Code Webview中，带有清晰的UI
4. ✅ 用户决策后，工作流无缝恢复执行
5. ✅ 所有HITL决策记录在数据库中供审计

---

### Week 3: Real-time Document Collaboration

#### Vision Reference
> **技术路线图 Chapter 3**: "AI代理通过调用 vscode.workspace.applyEdit API，以非破坏性的方式（如插入、差异视图建议）与文档交互，确保用户始终拥有最终控制权。"

#### Current State Analysis
**已有基础**:
- ✅ Markdown报告生成 (在报告合成阶段)
- ✅ VS Code编辑器中显示报告 (只读)
- ✅ Reports表存储历史版本

**缺失部分**:
- ❌ AI无法直接编辑VS Code中打开的文档
- ❌ 没有变更高亮/追踪机制
- ❌ 缺少Accept/Reject变更的UI

#### Implementation Tasks

##### Backend: Document Streaming Protocol

**1. 修改 `backend/src/agent/graph.py` - 流式报告生成**

```python
def generate_report_streaming(state: AgentState) -> AgentState:
    """
    流式生成报告，逐段发送到前端
    """
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    
    # 使用streaming模式的LLM
    llm = get_llm(streaming=True)
    
    report_sections = []
    
    # 1. 生成Introduction
    intro_prompt = "根据以下论文摘要，撰写研究报告的引言部分..."
    for chunk in llm.stream(intro_prompt):
        # 通过WebSocket发送增量更新
        yield {
            "type": "document_update",
            "action": "append",
            "section": "introduction",
            "content": chunk,
            "rationale": "AI正在撰写引言..."
        }
        report_sections.append(("introduction", chunk))
    
    # 2. 生成Methods
    # ... 类似逻辑
    
    # 3. 生成Results
    # ... 类似逻辑
    
    # 4. 生成Conclusion
    # ... 类似逻辑
    
    state["report"] = "\n\n".join(section for _, section in report_sections)
    return state
```

**2. 修改 WebSocket - 支持document_update消息**

```python
@app.websocket("/agent/stream")
async def websocket_stream_endpoint(websocket: WebSocket):
    # ... 原有代码
    
    for chunk in graph.stream(initial_state, config):
        if chunk.get("type") == "document_update":
            # 转发文档更新到前端
            await websocket.send_json({
                "type": "document_update",
                "action": chunk["action"],  # append, insert, replace, delete
                "section": chunk.get("section"),
                "content": chunk["content"],
                "range": chunk.get("range"),  # {startLine, startCol, endLine, endCol}
                "rationale": chunk.get("rationale")
            })
        else:
            # 正常进度消息
            await websocket.send_json(chunk)
```

##### Frontend: Document Editing Integration

**1. 扩展 `vscode-extension/src/api.ts` - Document Update类型**

```typescript
export interface DocumentUpdate {
    type: 'document_update';
    action: 'append' | 'insert' | 'replace' | 'delete';
    section?: string;
    content: string;
    range?: {
        startLine: number;
        startColumn: number;
        endLine: number;
        endColumn: number;
    };
    rationale: string;
}

export interface ResearchProgressCallback {
    // ... 原有回调
    onDocumentUpdate?: (update: DocumentUpdate) => void;
}
```

**2. 修改 `vscode-extension/src/extension.ts` - 文档编辑逻辑**

```typescript
import * as vscode from 'vscode';

// 全局状态：当前研究会话的文档URI
let currentReportDocument: vscode.Uri | null = null;
let pendingEdits: DocumentUpdate[] = [];

const startResearchCommand = vscode.commands.registerCommand(
    'auto-researcher.startResearch', 
    async () => {
        const topic = await vscode.window.showInputBox({
            prompt: '输入研究主题'
        });
        
        if (!topic) return;
        
        // 创建空白Markdown文档
        const reportUri = vscode.Uri.file(`/tmp/research-${Date.now()}.md`);
        const doc = await vscode.workspace.openTextDocument(reportUri);
        const editor = await vscode.window.showTextDocument(doc, vscode.ViewColumn.One);
        currentReportDocument = reportUri;
        
        await startResearchStream(topic, {
            onStarted: (data) => {
                // 插入标题
                editor.edit(edit => {
                    edit.insert(new vscode.Position(0, 0), `# ${topic}\n\n`);
                });
            },
            
            onDocumentUpdate: async (update: DocumentUpdate) => {
                if (!currentReportDocument) return;
                
                // 获取当前编辑器
                const editor = vscode.window.visibleTextEditors.find(
                    e => e.document.uri.toString() === currentReportDocument!.toString()
                );
                
                if (!editor) return;
                
                // 应用编辑
                const success = await editor.edit(editBuilder => {
                    if (update.action === 'append') {
                        // 追加到文档末尾
                        const lastLine = editor.document.lineCount;
                        editBuilder.insert(
                            new vscode.Position(lastLine, 0),
                            update.content
                        );
                    } else if (update.action === 'insert' && update.range) {
                        // 插入到指定位置
                        editBuilder.insert(
                            new vscode.Position(update.range.startLine, update.range.startColumn),
                            update.content
                        );
                    } else if (update.action === 'replace' && update.range) {
                        // 替换指定范围
                        editBuilder.replace(
                            new vscode.Range(
                                update.range.startLine, update.range.startColumn,
                                update.range.endLine, update.range.endColumn
                            ),
                            update.content
                        );
                    } else if (update.action === 'delete' && update.range) {
                        // 删除指定范围
                        editBuilder.delete(
                            new vscode.Range(
                                update.range.startLine, update.range.startColumn,
                                update.range.endLine, update.range.endColumn
                            )
                        );
                    }
                });
                
                if (success) {
                    // 添加装饰（高亮AI编辑的部分）
                    const decorationType = vscode.window.createTextEditorDecorationType({
                        backgroundColor: 'rgba(100, 200, 100, 0.2)',  // 绿色背景
                        isWholeLine: false,
                        overviewRulerColor: 'green',
                        overviewRulerLane: vscode.OverviewRulerLane.Right
                    });
                    
                    const range = new vscode.Range(
                        update.range?.startLine || editor.document.lineCount - 1,
                        update.range?.startColumn || 0,
                        update.range?.endLine || editor.document.lineCount,
                        update.range?.endColumn || 0
                    );
                    
                    editor.setDecorations(decorationType, [range]);
                    
                    // 显示AI编辑原因
                    vscode.window.showInformationMessage(
                        `🤖 AI编辑: ${update.rationale}`,
                        '接受', '撤销'
                    ).then(selection => {
                        if (selection === '撤销') {
                            // 撤销最后一次编辑
                            vscode.commands.executeCommand('undo');
                        }
                    });
                    
                    // 存储编辑记录
                    pendingEdits.push(update);
                }
            },
            
            onComplete: (data) => {
                vscode.window.showInformationMessage('✅ 报告生成完成！');
                currentReportDocument = null;
            }
        });
    }
);
```

**3. 创建 `vscode-extension/src/documentCollaboration.ts` - 变更管理**

```typescript
import * as vscode from 'vscode';

export interface EditHistory {
    timestamp: Date;
    action: string;
    range: vscode.Range;
    content: string;
    rationale: string;
}

export class DocumentCollaborationManager {
    private editHistory: EditHistory[] = [];
    private decorationTypes: Map<string, vscode.TextEditorDecorationType> = new Map();
    
    constructor(private editor: vscode.TextEditor) {}
    
    applyUpdate(update: DocumentUpdate): Promise<boolean> {
        return this.editor.edit(editBuilder => {
            // ... 编辑逻辑（同上）
        }).then(success => {
            if (success) {
                this.recordEdit(update);
                this.highlightChange(update);
            }
            return success;
        });
    }
    
    private recordEdit(update: DocumentUpdate) {
        this.editHistory.push({
            timestamp: new Date(),
            action: update.action,
            range: new vscode.Range(
                update.range?.startLine || 0,
                update.range?.startColumn || 0,
                update.range?.endLine || 0,
                update.range?.endColumn || 0
            ),
            content: update.content,
            rationale: update.rationale
        });
    }
    
    private highlightChange(update: DocumentUpdate) {
        const decorationType = vscode.window.createTextEditorDecorationType({
            backgroundColor: 'rgba(100, 200, 100, 0.2)',
            after: {
                contentText: ' 🤖',
                color: 'green'
            }
        });
        
        const range = new vscode.Range(
            update.range?.startLine || this.editor.document.lineCount - 1,
            update.range?.startColumn || 0,
            update.range?.endLine || this.editor.document.lineCount,
            update.range?.endColumn || 0
        );
        
        this.editor.setDecorations(decorationType, [range]);
        this.decorationTypes.set(update.content, decorationType);
        
        // 30秒后移除高亮
        setTimeout(() => {
            decorationType.dispose();
            this.decorationTypes.delete(update.content);
        }, 30000);
    }
    
    getEditHistory(): EditHistory[] {
        return this.editHistory;
    }
    
    undoAllAIEdits() {
        // 撤销所有AI编辑
        const editCount = this.editHistory.length;
        for (let i = 0; i < editCount; i++) {
            vscode.commands.executeCommand('undo');
        }
        this.editHistory = [];
    }
}
```

#### Testing Checklist

- [ ] Backend: 报告流式生成成功
- [ ] WebSocket: document_update消息正确发送
- [ ] Frontend: `editor.edit()` 正确应用变更
- [ ] Frontend: 变更高亮显示
- [ ] Frontend: Accept/Undo按钮功能正常
- [ ] Conflict: 用户同时编辑时冲突检测工作
- [ ] History: 所有编辑记录在session_events表

#### Acceptance Criteria

1. ✅ AI可以实时追加内容到Markdown文档
2. ✅ AI编辑的部分用绿色背景高亮显示
3. ✅ 每次AI编辑后显示通知，带Accept/Undo按钮
4. ✅ 用户可以撤销单个或全部AI编辑
5. ✅ 编辑器gutter显示🤖图标标记AI修改行
6. ✅ Hover提示显示AI编辑原因
7. ✅ 用户手动编辑不会被AI覆盖（冲突检测）

---

## 🚧 Known Technical Challenges

### Challenge 1: LangGraph Interrupt Async Limitation

**Problem**: LangGraph的`interrupt()`函数可能不支持async/await模式。

**Workaround**: 
- 使用同步模式执行图，通过`run_in_executor`包装
- 或等待LangGraph更新支持async interrupts

**Monitoring**: 关注LangGraph GitHub Issues:
- https://github.com/langchain-ai/langgraph/issues

### Challenge 2: VS Code Edit Conflict Detection

**Problem**: 同时有用户编辑和AI编辑时，可能产生冲突。

**Solution**:
- 实现document version tracking (基于hash)
- 检测到冲突时暂停AI编辑，显示合并UI
- 提供三方合并视图 (base, user, AI)

**Implementation**:
```typescript
import * as crypto from 'crypto';

function getDocumentHash(doc: vscode.TextDocument): string {
    return crypto.createHash('sha256')
        .update(doc.getText())
        .digest('hex');
}

let lastKnownHash: string;

editor.edit(editBuilder => {
    const currentHash = getDocumentHash(editor.document);
    
    if (currentHash !== lastKnownHash) {
        // 检测到用户修改，暂停AI编辑
        vscode.window.showWarningMessage(
            '检测到文档被修改，AI已暂停编辑。是否继续？',
            '继续', '取消'
        ).then(selection => {
            if (selection === '继续') {
                // 更新hash，继续编辑
                lastKnownHash = getDocumentHash(editor.document);
                // ... apply AI edit
            }
        });
        return;
    }
    
    // ... apply AI edit
    lastKnownHash = getDocumentHash(editor.document);
});
```

### Challenge 3: React Migration Effort

**Problem**: 当前Control Panel使用简单HTML，技术路线图要求React。

**Options**:
1. **Incremental Migration** (推荐):
   - Phase 3.6继续使用HTML实现HITL功能
   - Phase 4.1专门用4周迁移到React
   - 优点：不阻塞核心功能，专注一个任务
   
2. **Full Rewrite**:
   - Phase 3.6开始就用React重写Control Panel
   - 缺点：时间翻倍（2周 → 4周），延迟HITL交付

**Recommendation**: 选择Option 1，先交付功能，后优化架构。

---

## 📚 Reference Documents

1. **技术路线图**: `doc/技术开放文档2: 基于 VS Code 的自动化科研平台.md`
   - Chapter 3: 三栏式IDE设计
   - Chapter 4: LangGraph工作流
   - Chapter 5: 分阶段路线图

2. **Phase 3.5.3完成报告**: `.ai-sessions/development/PHASE_3.5.3_FINAL_COMPLETION_REPORT.md`
   - 已完成功能清单
   - WebSocket实现细节
   - Analytics Dashboard架构

3. **LangGraph文档**:
   - Human-in-the-Loop: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
   - Interrupts: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/

4. **VS Code API**:
   - TextEditor.edit: https://code.visualstudio.com/api/references/vscode-api#TextEditor
   - WorkspaceEdit: https://code.visualstudio.com/api/references/vscode-api#WorkspaceEdit
   - Webview: https://code.visualstudio.com/api/extension-guides/webview

---

## ✅ Success Criteria

Phase 3.6成功交付的标志：

1. **HITL功能** (Week 1-2):
   - [ ] 用户可以在3个关键点干预AI决策
   - [ ] HITL UI清晰直观，带有明确的行动按钮
   - [ ] 工作流暂停/恢复无缝衔接
   - [ ] 所有决策记录在数据库中

2. **协同编辑功能** (Week 3):
   - [ ] AI可以实时编辑Markdown文档
   - [ ] 用户可以看到AI正在编辑的内容
   - [ ] 变更高亮、Accept/Reject UI完整
   - [ ] 冲突检测和解决机制工作正常

3. **质量指标**:
   - [ ] TypeScript编译0错误
   - [ ] 至少20个E2E测试场景通过
   - [ ] 代码覆盖率 >80%
   - [ ] 用户体验流畅（无卡顿、无闪烁）

4. **文档完整性**:
   - [ ] OpenAPI更新包含所有新端点
   - [ ] README包含HITL和协同编辑使用指南
   - [ ] 视频演示展示核心功能

---

## 🎯 Next Steps

### Immediate Actions (本周)

1. **环境准备**:
   ```bash
   # 安装必要依赖
   pip install langgraph>=0.2.0
   
   # 创建Phase 3.6分支
   git checkout -b phase-3.6-hitl-collaboration
   ```

2. **创建任务看板**:
   - GitHub Projects: 创建"Phase 3.6 HITL & Collaboration"项目
   - 任务卡片:
     - Task 3.6.1: LangGraph HITL Nodes (2天)
     - Task 3.6.2: Backend HITL API (1天)
     - Task 3.6.3: Frontend HITL UI (3天)
     - Task 3.6.4: Document Streaming Backend (2天)
     - Task 3.6.5: VS Code Edit Integration (3天)
     - Task 3.6.6: Conflict Resolution (2天)
     - Task 3.6.7: E2E Testing (2天)

3. **技术调研**:
   - [ ] 阅读LangGraph HITL官方文档
   - [ ] 研究VS Code TextEditor API示例
   - [ ] 搭建本地测试环境（WebSocket + HITL mock）

### Week 1 Kickoff

**Day 1-2**: Backend HITL Infrastructure
- 修改`graph.py`添加interrupt nodes
- 实现`/agent/hitl/respond` API
- 单元测试

**Day 3-4**: Frontend HITL UI
- 创建`hitlWebview.ts`
- 实现决策卡片组件
- WebSocket集成

**Day 5**: HITL E2E测试
- 完整研究流程测试
- 性能基准测试
- 用户验收测试

---

**Author**: Development Team  
**Last Updated**: October 14, 2025  
**Status**: Ready for Implementation  
**Estimated Effort**: 3 weeks (15 working days)

