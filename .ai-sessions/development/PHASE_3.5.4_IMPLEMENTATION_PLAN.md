# Phase 3.5.4 实施计划：生产准备

**开始日期**: 2025-10-14  
**预计完成**: 2025-10-21 (7天)  
**状态**: 🚧 进行中

---

## 📋 总体目标

将系统从"功能完整"提升到"生产就绪"，确保稳定性、性能和可维护性。

**关键成功指标**:
- ✅ P95 API延迟 < 500ms
- ✅ 错误率 < 0.1%
- ✅ 测试覆盖率 > 85%
- ✅ 所有deprecation警告消除
- ✅ 完整文档和部署指南

---

## 📅 7天执行计划

### Day 1-2: 性能优化与Bug修复 (Oct 14-15)

#### Task 1.1: 修复 Chart.js Deprecation 警告 ⚠️ **Critical**

**问题**: Chart.js 4.4.0 使用了过时的API

**文件**: `vscode-extension/src/analyticsWebview.ts`

**修复内容**:
```typescript
// ❌ 旧API（已废弃）
scales: {
    x: { 
        ticks: { color: '#cccccc' }
    },
    y: {
        ticks: { color: '#cccccc' }
    }
}

// ✅ 新API（Chart.js 4.x）
scales: {
    x: { 
        ticks: { 
            color: (context) => '#cccccc'
        }
    },
    y: {
        ticks: {
            color: (context) => '#cccccc'
        }
    }
}
```

**验证命令**:
```bash
cd vscode-extension
docker exec vscode-dev bash -c "cd /workspaces/gemini-fullstack-langgraph-quickstart/vscode-extension && npm run compile 2>&1 | grep -i deprecation"
# 应该无输出
```

#### Task 1.2: 数据库索引优化 🚀 **High Priority**

**问题**: 大数据量时查询缓慢

**文件**: 创建 `backend/migrations/001_add_indexes.sql`

**索引清单**:
```sql
-- Papers表优化
CREATE INDEX IF NOT EXISTS idx_papers_session_id ON papers(session_id);
CREATE INDEX IF NOT EXISTS idx_papers_created_at ON papers(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi) WHERE doi IS NOT NULL;

-- Reports表优化
CREATE INDEX IF NOT EXISTS idx_reports_session_id ON reports(session_id);
CREATE INDEX IF NOT EXISTS idx_reports_version ON reports(session_id, version DESC);

-- Session Events表优化
CREATE INDEX IF NOT EXISTS idx_session_events_session_id ON session_events(session_id);
CREATE INDEX IF NOT EXISTS idx_session_events_timestamp ON session_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_session_events_type ON session_events(event_type);

-- Sessions表优化
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at DESC);
```

**执行命令**:
```bash
docker exec langgraph-postgres psql -U postgres -d postgres -f /path/to/001_add_indexes.sql
```

**性能基准测试**:
```bash
# 测试前
time curl http://localhost:8121/papers?limit=100

# 测试后（预期提升40%）
time curl http://localhost:8121/papers?limit=100
```

#### Task 1.3: WebSocket 心跳机制 💓

**问题**: 长时间无活动导致连接超时

**文件**: `backend/src/agent/app.py`

**实现**:
```python
async def stream_with_hitl_detection():
    last_heartbeat = time.time()
    HEARTBEAT_INTERVAL = 30  # 30秒
    
    try:
        async for chunk in graph.astream(input_data, config=config):
            # 检查心跳
            if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })
                last_heartbeat = time.time()
            
            # 现有消息处理逻辑...
            for node_name, state_update in chunk.items():
                # ...
```

**前端处理**:
```typescript
// vscode-extension/src/extension.ts
ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    
    if (message.type === 'heartbeat') {
        console.log('💓 Heartbeat received');
        return;
    }
    
    // 处理其他消息...
};
```

#### Task 1.4: 前端加载优化 ⚡

**问题**: Analytics Dashboard 加载时白屏

**文件**: `vscode-extension/src/analyticsWebview.ts`

**实现**:
```typescript
function generateAnalyticsDashboardHTML(...) {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .loading-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            .spinner {
                border: 4px solid rgba(255,255,255,0.1);
                border-left-color: #007acc;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            #dashboard { display: none; }
        </style>
    </head>
    <body>
        <div id="loading" class="loading-container">
            <div class="spinner"></div>
            <p>Loading analytics data...</p>
        </div>
        
        <div id="dashboard">
            <!-- Charts and stats -->
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
        <script>
            window.addEventListener('load', () => {
                // 数据加载完成后隐藏loading
                setTimeout(() => {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('dashboard').style.display = 'block';
                }, 500);
            });
        </script>
    </body>
    </html>
    `;
}
```

---

### Day 3-4: Session Details View 实现 (Oct 16-17)

#### Task 3.1: 后端 API 实现

**新建文件**: `backend/src/agent/app.py` (添加端点)

```python
@app.get("/sessions/{session_id}/details")
async def get_session_details(session_id: str):
    """
    获取Session完整详情
    
    Returns:
        - session: 基本信息
        - events: 事件时间线（最近50条）
        - papers: 相关论文列表
        - reports: 报告版本列表
        - stats: 聚合统计
    """
    try:
        # 获取基本信息
        session = db_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # 获取事件时间线
        events = db_manager.get_session_events(session_id, limit=50)
        
        # 获取相关论文
        papers = db_manager.list_papers(session_id=session_id)
        
        # 获取报告版本
        reports = db_manager.list_reports(session_id=session_id)
        
        # 计算统计数据
        stats = {
            "total_events": len(events),
            "duration_seconds": _calculate_duration(events),
            "paper_count": len(papers),
            "report_count": len(reports),
            "status": session.get("status", "unknown"),
            "cost_estimate": _estimate_cost(events)
        }
        
        return {
            "session": session,
            "events": events,
            "papers": papers,
            "reports": reports,
            "stats": stats
        }
    
    except Exception as e:
        logger.error(f"Error getting session details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_duration(events: list) -> int:
    """计算Session持续时间（秒）"""
    if not events:
        return 0
    
    start = min(e["created_at"] for e in events)
    end = max(e["created_at"] for e in events)
    
    # Parse ISO timestamps
    from dateutil.parser import parse
    duration = (parse(end) - parse(start)).total_seconds()
    return int(duration)


def _estimate_cost(events: list) -> float:
    """估算Session成本（基于token使用）"""
    # 简单估算：每1000 tokens约$0.01
    total_tokens = 0
    
    for event in events:
        if event.get("event_type") == "llm_call":
            data = event.get("event_data", {})
            total_tokens += data.get("input_tokens", 0)
            total_tokens += data.get("output_tokens", 0)
    
    return round(total_tokens / 1000 * 0.01, 4)
```

#### Task 3.2: 前端 Webview 实现

**新建文件**: `vscode-extension/src/sessionDetailsWebview.ts`

```typescript
export function generateSessionDetailsHTML(sessionId: string, data: any): string {
    const { session, events, papers, reports, stats } = data;
    
    // Format duration
    const durationMinutes = Math.floor(stats.duration_seconds / 60);
    const durationSeconds = stats.duration_seconds % 60;
    const durationStr = `${durationMinutes}m ${durationSeconds}s`;
    
    // Status badge color
    const statusColors: any = {
        'active': '#007acc',
        'completed': '#4caf50',
        'failed': '#f44336',
        'pending': '#ff9800'
    };
    
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Session Details</title>
        <style>
            body {
                font-family: var(--vscode-font-family);
                color: var(--vscode-foreground);
                background-color: var(--vscode-editor-background);
                padding: 20px;
                margin: 0;
            }
            
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid var(--vscode-panel-border);
            }
            
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            
            .status-badge {
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                color: white;
                background-color: ${statusColors[session.status] || '#666'};
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }
            
            .stat-card h3 {
                margin: 0 0 10px 0;
                font-size: 32px;
                color: var(--vscode-textLink-activeForeground);
            }
            
            .stat-card p {
                margin: 0;
                font-size: 14px;
                color: var(--vscode-descriptionForeground);
                text-transform: uppercase;
            }
            
            .section {
                margin-bottom: 30px;
            }
            
            .section h2 {
                margin-bottom: 15px;
                font-size: 18px;
                border-bottom: 1px solid var(--vscode-panel-border);
                padding-bottom: 10px;
            }
            
            .timeline {
                position: relative;
                padding-left: 30px;
            }
            
            .timeline::before {
                content: '';
                position: absolute;
                left: 8px;
                top: 0;
                bottom: 0;
                width: 2px;
                background-color: var(--vscode-panel-border);
            }
            
            .timeline-item {
                position: relative;
                margin-bottom: 20px;
                padding-left: 20px;
            }
            
            .timeline-item::before {
                content: '';
                position: absolute;
                left: -22px;
                top: 6px;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background-color: var(--vscode-textLink-foreground);
                border: 2px solid var(--vscode-editor-background);
            }
            
            .timeline-time {
                font-size: 12px;
                color: var(--vscode-descriptionForeground);
            }
            
            .timeline-type {
                font-weight: bold;
                color: var(--vscode-textLink-foreground);
                margin: 0 10px;
            }
            
            .timeline-details {
                font-size: 14px;
                color: var(--vscode-foreground);
            }
            
            .action-buttons {
                display: flex;
                gap: 10px;
                margin-top: 30px;
            }
            
            button {
                padding: 10px 20px;
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            
            button:hover {
                background-color: var(--vscode-button-hoverBackground);
            }
            
            .danger-button {
                background-color: #f44336;
            }
            
            .danger-button:hover {
                background-color: #d32f2f;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>${session.title || 'Untitled Session'}</h1>
            <span class="status-badge">${session.status}</span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>${stats.paper_count}</h3>
                <p>Papers Found</p>
            </div>
            <div class="stat-card">
                <h3>${stats.report_count}</h3>
                <p>Report Versions</p>
            </div>
            <div class="stat-card">
                <h3>${durationStr}</h3>
                <p>Duration</p>
            </div>
            <div class="stat-card">
                <h3>$${stats.cost_estimate.toFixed(4)}</h3>
                <p>Est. Cost</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Session Information</h2>
            <table>
                <tr>
                    <td><strong>Session ID:</strong></td>
                    <td>${session.id}</td>
                </tr>
                <tr>
                    <td><strong>Thread ID:</strong></td>
                    <td>${session.thread_id}</td>
                </tr>
                <tr>
                    <td><strong>Research Topic:</strong></td>
                    <td>${session.research_topic || 'N/A'}</td>
                </tr>
                <tr>
                    <td><strong>Created At:</strong></td>
                    <td>${new Date(session.created_at).toLocaleString()}</td>
                </tr>
                <tr>
                    <td><strong>Updated At:</strong></td>
                    <td>${new Date(session.updated_at).toLocaleString()}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>📅 Event Timeline (Latest ${events.length})</h2>
            <div class="timeline">
                ${events.map((event: any) => `
                    <div class="timeline-item">
                        <span class="timeline-time">${new Date(event.created_at).toLocaleTimeString()}</span>
                        <span class="timeline-type">${event.event_type}</span>
                        <span class="timeline-details">${event.event_data?.message || JSON.stringify(event.event_data || {})}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="section">
            <h2>📚 Papers (${papers.length})</h2>
            <ul>
                ${papers.slice(0, 10).map((paper: any) => `
                    <li><strong>${paper.title}</strong> - ${paper.authors?.join(', ') || 'Unknown authors'}</li>
                `).join('')}
                ${papers.length > 10 ? `<li><em>... and ${papers.length - 10} more</em></li>` : ''}
            </ul>
        </div>
        
        <div class="section">
            <h2>📝 Reports (${reports.length} versions)</h2>
            <ul>
                ${reports.map((report: any) => `
                    <li>Version ${report.version} - ${new Date(report.created_at).toLocaleString()} (${report.extra_metadata?.word_count || 0} words)</li>
                `).join('')}
            </ul>
        </div>
        
        <div class="action-buttons">
            <button onclick="exportSession()">📥 Export Session</button>
            <button onclick="openInLangSmith()">🔍 Debug in LangSmith</button>
            <button class="danger-button" onclick="deleteSession()">🗑️ Delete Session</button>
        </div>
        
        <script>
            const vscode = acquireVsCodeApi();
            
            function exportSession() {
                vscode.postMessage({ command: 'exportSession', sessionId: '${sessionId}' });
            }
            
            function openInLangSmith() {
                vscode.postMessage({ command: 'openLangSmith', sessionId: '${sessionId}' });
            }
            
            function deleteSession() {
                if (confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
                    vscode.postMessage({ command: 'deleteSession', sessionId: '${sessionId}' });
                }
            }
        </script>
    </body>
    </html>
    `;
}
```

#### Task 3.3: TreeView 命令注册

**文件**: `vscode-extension/src/extension.ts` (添加命令)

```typescript
// 导入
import { generateSessionDetailsHTML } from './sessionDetailsWebview';
import { getSessionDetails } from './api';

// 在activate()中注册命令
const viewSessionDetailsCommand = vscode.commands.registerCommand(
    'researchAgent.viewSessionDetails',
    async (session: Session) => {
        try {
            // 创建Webview Panel
            const panel = vscode.window.createWebviewPanel(
                'sessionDetails',
                `Session: ${session.title}`,
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );
            
            // 显示加载指示器
            panel.webview.html = '<html><body><h2>Loading session details...</h2></body></html>';
            
            // 获取数据
            const data = await getSessionDetails(session.id);
            
            // 渲染完整HTML
            panel.webview.html = generateSessionDetailsHTML(session.id, data);
            
            // 处理Webview消息
            panel.webview.onDidReceiveMessage(
                async (message) => {
                    switch (message.command) {
                        case 'exportSession':
                            // TODO: 实现导出功能
                            vscode.window.showInformationMessage('Export功能开发中...');
                            break;
                        case 'openLangSmith':
                            // TODO: Phase 4.1实现
                            vscode.window.showInformationMessage('LangSmith集成将在Phase 4.1实现');
                            break;
                        case 'deleteSession':
                            // TODO: 实现删除功能
                            vscode.window.showWarningMessage('Delete功能开发中...');
                            break;
                    }
                },
                undefined,
                context.subscriptions
            );
            
        } catch (error: any) {
            vscode.window.showErrorMessage(`Failed to load session details: ${error.message}`);
        }
    }
);

// 添加到subscriptions
context.subscriptions.push(viewSessionDetailsCommand);
```

#### Task 3.4: API 函数实现

**文件**: `vscode-extension/src/api.ts` (添加函数)

```typescript
/**
 * Get detailed session information
 */
export async function getSessionDetails(sessionId: string): Promise<any> {
    try {
        const response = await axios.get(`${API_BASE_URL}/sessions/${sessionId}/details`);
        return response.data;
    } catch (error: any) {
        console.error('Error fetching session details:', error);
        throw error;
    }
}
```

---

### Day 5: 文档完善与测试 (Oct 18)

#### Task 5.1: 更新 OpenAPI 规范

**文件**: `openapi.yaml`

```yaml
paths:
  /sessions/{session_id}/details:
    get:
      summary: Get detailed session information
      description: Returns comprehensive session details including events timeline, papers, reports, and statistics
      operationId: getSessionDetails
      tags:
        - Sessions
      parameters:
        - name: session_id
          in: path
          required: true
          description: UUID of the session
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Session details retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  session:
                    $ref: '#/components/schemas/Session'
                  events:
                    type: array
                    items:
                      $ref: '#/components/schemas/SessionEvent'
                  papers:
                    type: array
                    items:
                      $ref: '#/components/schemas/Paper'
                  reports:
                    type: array
                    items:
                      $ref: '#/components/schemas/Report'
                  stats:
                    type: object
                    properties:
                      total_events:
                        type: integer
                      duration_seconds:
                        type: integer
                      paper_count:
                        type: integer
                      report_count:
                        type: integer
                      status:
                        type: string
                      cost_estimate:
                        type: number
                        format: float
        '404':
          description: Session not found
        '500':
          description: Internal server error
```

#### Task 5.2: 集成测试脚本

**新建文件**: `backend/tests/test_phase_3.5.4.sh`

```bash
#!/bin/bash
set -e

echo "🧪 Phase 3.5.4 Integration Tests"
echo "================================="

# Test environment
API_URL="http://localhost:8121"
DB_CONTAINER="langgraph-postgres"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Database Indexes
echo ""
echo "Test 1: Database Indexes"
echo "------------------------"

INDEXES=$(docker exec $DB_CONTAINER psql -U postgres -d postgres -t -c "\di" | grep -E "idx_papers|idx_reports|idx_session")
if [ -n "$INDEXES" ]; then
    echo -e "${GREEN}✅ Database indexes created${NC}"
    echo "$INDEXES"
else
    echo -e "${RED}❌ Database indexes missing${NC}"
    exit 1
fi

# Test 2: Session Details API
echo ""
echo "Test 2: Session Details API"
echo "---------------------------"

# Get first session ID
SESSION_ID=$(curl -s $API_URL/sessions | jq -r '.[0].id' 2>/dev/null)

if [ "$SESSION_ID" != "null" ] && [ -n "$SESSION_ID" ]; then
    DETAILS=$(curl -s $API_URL/sessions/$SESSION_ID/details)
    
    # Check if response has required fields
    if echo "$DETAILS" | jq -e '.session, .events, .papers, .reports, .stats' > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Session Details API working${NC}"
        echo "  Session: $(echo $DETAILS | jq -r '.session.title')"
        echo "  Events: $(echo $DETAILS | jq -r '.stats.total_events')"
        echo "  Papers: $(echo $DETAILS | jq -r '.stats.paper_count')"
        echo "  Reports: $(echo $DETAILS | jq -r '.stats.report_count')"
    else
        echo -e "${RED}❌ Session Details API response incomplete${NC}"
        echo "$DETAILS" | jq .
        exit 1
    fi
else
    echo -e "${RED}⚠️  No sessions found - skipping test${NC}"
fi

# Test 3: Chart.js Deprecation Warnings
echo ""
echo "Test 3: Chart.js Deprecation Warnings"
echo "-------------------------------------"

cd vscode-extension
COMPILE_OUTPUT=$(docker exec vscode-dev bash -c "cd /workspaces/gemini-fullstack-langgraph-quickstart/vscode-extension && npm run compile 2>&1")

if echo "$COMPILE_OUTPUT" | grep -qi "deprecation"; then
    echo -e "${RED}❌ Still has deprecation warnings${NC}"
    echo "$COMPILE_OUTPUT" | grep -i deprecation
    exit 1
else
    echo -e "${GREEN}✅ No deprecation warnings${NC}"
fi

# Test 4: API Performance
echo ""
echo "Test 4: API Performance"
echo "----------------------"

# Test papers endpoint
START_TIME=$(date +%s%N)
curl -s $API_URL/papers?limit=100 > /dev/null
END_TIME=$(date +%s%N)
ELAPSED=$((($END_TIME - $START_TIME) / 1000000)) # Convert to milliseconds

if [ $ELAPSED -lt 500 ]; then
    echo -e "${GREEN}✅ Papers API response time: ${ELAPSED}ms (< 500ms target)${NC}"
else
    echo -e "${RED}❌ Papers API response time: ${ELAPSED}ms (> 500ms target)${NC}"
    exit 1
fi

# Summary
echo ""
echo "================================="
echo -e "${GREEN}🎉 All tests passed!${NC}"
echo "================================="
```

**执行权限**:
```bash
chmod +x backend/tests/test_phase_3.5.4.sh
```

---

### Day 6-7: 部署准备与收尾 (Oct 19-21)

#### Task 6.1: 数据库迁移脚本

**新建文件**: `backend/migrations/001_add_indexes.sql`

```sql
-- Migration: Add Performance Indexes for Phase 3.5.4
-- Author: Development Team
-- Date: 2025-10-14
-- Description: Optimize database queries by adding strategic indexes

BEGIN;

-- ====================
-- Papers Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_papers_session_id 
ON papers(session_id);

-- Common query: sort by creation date
CREATE INDEX IF NOT EXISTS idx_papers_created_at 
ON papers(created_at DESC);

-- Common query: lookup by DOI
CREATE INDEX IF NOT EXISTS idx_papers_doi 
ON papers(doi) 
WHERE doi IS NOT NULL;

-- ====================
-- Reports Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_reports_session_id 
ON reports(session_id);

-- Common query: get latest version per session
CREATE INDEX IF NOT EXISTS idx_reports_session_version 
ON reports(session_id, version DESC);

-- ====================
-- Session Events Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_session_events_session_id 
ON session_events(session_id);

-- Common query: sort by timestamp
CREATE INDEX IF NOT EXISTS idx_session_events_created_at 
ON session_events(created_at DESC);

-- Common query: filter by event type
CREATE INDEX IF NOT EXISTS idx_session_events_type 
ON session_events(event_type);

-- Composite index for timeline queries
CREATE INDEX IF NOT EXISTS idx_session_events_session_time 
ON session_events(session_id, created_at DESC);

-- ====================
-- Sessions Table Indexes
-- ====================

-- Common query: filter by status
CREATE INDEX IF NOT EXISTS idx_sessions_status 
ON sessions(status);

-- Common query: sort by creation date
CREATE INDEX IF NOT EXISTS idx_sessions_created_at 
ON sessions(created_at DESC);

-- Common query: filter by thread_id
CREATE INDEX IF NOT EXISTS idx_sessions_thread_id 
ON sessions(thread_id);

COMMIT;

-- ====================
-- Rollback Script
-- ====================
-- To rollback, run:
-- DROP INDEX IF EXISTS idx_papers_session_id;
-- DROP INDEX IF EXISTS idx_papers_created_at;
-- DROP INDEX IF EXISTS idx_papers_doi;
-- DROP INDEX IF EXISTS idx_reports_session_id;
-- DROP INDEX IF EXISTS idx_reports_session_version;
-- DROP INDEX IF EXISTS idx_session_events_session_id;
-- DROP INDEX IF EXISTS idx_session_events_created_at;
-- DROP INDEX IF EXISTS idx_session_events_type;
-- DROP INDEX IF EXISTS idx_session_events_session_time;
-- DROP INDEX IF EXISTS idx_sessions_status;
-- DROP INDEX IF EXISTS idx_sessions_created_at;
-- DROP INDEX IF EXISTS idx_sessions_thread_id;
```

#### Task 6.2: 环境变量文档

**更新文件**: `.env.example`

```bash
# ========================================
# Auto-Researcher Environment Configuration
# Phase 3.5.4 Production Ready
# ========================================

# ====================
# Backend API Configuration
# ====================

# Gemini API Key (Required)
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# LangSmith Tracing (Optional but Recommended)
# Get from: https://smith.langchain.com/
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=auto-researcher-prod
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# ====================
# Database Configuration
# ====================

# PostgreSQL Connection (Required)
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_URI=postgresql://postgres:postgres@langgraph-postgres:5432/postgres

# Redis Cache (Required)
REDIS_URI=redis://langgraph-redis:6379

# ====================
# LLM Provider Configuration
# ====================

# Primary LLM Provider
# Options: gemini, vertex, openai
GENERATION_LLM_PROVIDER=gemini

# Model Selection
# Gemini models: gemini-1.5-pro, gemini-1.5-flash
GENERATION_MODEL=gemini-1.5-pro

# ====================
# Performance Tuning
# ====================

# Maximum concurrent requests
MAX_CONCURRENT_REQUESTS=10

# Request timeout (seconds)
REQUEST_TIMEOUT_SECONDS=300

# WebSocket heartbeat interval (seconds)
WEBSOCKET_HEARTBEAT_INTERVAL=30

# ====================
# Observability (Phase 4.1 - Optional)
# ====================

# LangFuse Cost Tracking
# Get from: https://cloud.langfuse.com/
LANGFUSE_PUBLIC_KEY=pk_xxx
LANGFUSE_SECRET_KEY=sk_xxx
LANGFUSE_HOST=https://cloud.langfuse.com

# ====================
# Development Settings
# ====================

# Enable debug logging
DEBUG=false

# Python log level
LOG_LEVEL=INFO

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# ====================
# Security (Production)
# ====================

# API Key for external access (Optional)
API_KEY=

# Enable HTTPS
USE_HTTPS=false

# Session secret
SESSION_SECRET=change_this_in_production
```

#### Task 6.3: 健康检查增强

**文件**: `backend/src/agent/app.py`

```python
from typing import Dict
import asyncio

@app.get("/health")
async def health_check():
    """
    Enhanced health check with dependency validation
    
    Returns:
        - status: overall system health
        - checks: individual component status
        - timestamp: check execution time
    """
    checks: Dict[str, str] = {}
    
    # Check API
    checks["api"] = "ok"
    
    # Check Database
    try:
        # Simple query
        result = await asyncio.to_thread(
            db_manager.db.execute,
            "SELECT 1"
        )
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)[:50]}"
    
    # Check Redis
    try:
        import redis
        redis_client = redis.from_url(os.getenv("REDIS_URI", "redis://localhost:6379"))
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)[:50]}"
    
    # Check Gemini API
    try:
        from litellm import completion
        # Test with minimal tokens
        response = completion(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        checks["gemini_api"] = "ok"
    except Exception as e:
        checks["gemini_api"] = f"error: {str(e)[:50]}"
    
    # Determine overall status
    all_ok = all(v == "ok" for v in checks.values())
    overall_status = "healthy" if all_ok else "degraded"
    status_code = 200 if all_ok else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall_status,
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "3.5.4"
        }
    )
```

---

## ✅ 验收标准

### 性能指标
- [ ] P95 API延迟 < 500ms
- [ ] 数据库查询平均提升 > 30%
- [ ] 前端加载时间 < 2秒

### 功能完整性
- [ ] Session Details View 正常工作
- [ ] 所有API端点正常响应
- [ ] WebSocket连接稳定（无超时）

### 代码质量
- [ ] 0 Chart.js deprecation warnings
- [ ] 0 TypeScript compile errors
- [ ] 0 ESLint errors

### 文档完整性
- [ ] OpenAPI规范更新
- [ ] 环境变量文档完整
- [ ] 集成测试脚本可执行

### 测试覆盖
- [ ] 集成测试 > 85% 覆盖
- [ ] 所有新API有测试
- [ ] 性能基准测试通过

---

## 📊 进度追踪

| Day | 任务 | 状态 | 完成时间 |
|-----|------|------|---------|
| Day 1-2 | 性能优化与Bug修复 | 🚧 | - |
| Day 3-4 | Session Details View | 📋 | - |
| Day 5 | 文档完善与测试 | 📋 | - |
| Day 6-7 | 部署准备与收尾 | 📋 | - |

---

## 🎯 完成后里程碑

✅ **Phase 3.5.4 Complete** → 系统生产就绪  
📋 **Ready for Phase 3.6** → HITL系统开发  
🚀 **Performance Optimized** → 40% query speed improvement  
📚 **Documentation Complete** → Full API docs + deployment guide

---

**创建时间**: 2025-10-14  
**最后更新**: 2025-10-14  
**负责人**: Development Team
