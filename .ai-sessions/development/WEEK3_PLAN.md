# Phase 3.5.3 Week 3 实施计划

**日期**: 2025-10-14  
**任务**: Week 3 - Frontend Analytics Dashboard  
**预计完成**: 2025-10-28  
**依赖**: Week 1 ✅ + Week 2 ✅  

---

## 目标概述

在VS Code Extension中实现Analytics Dashboard，使用Chart.js可视化展示研究会话统计数据和趋势。

---

## 整体架构

```
VS Code Extension (TypeScript)
├── Analytics Webview (HTML + Chart.js)
│   ├── Summary Cards (Total/Completed/Success Rate)
│   ├── Session List (Table with filters)
│   ├── Trend Charts (Line/Bar/Pie)
│   └── Session Details (Timeline view)
├── API Client (api.ts)
│   └── 4个Analytics API调用函数
└── Command Registration
    └── auto-researcher.showAnalytics
```

---

## Week 3 详细任务

### [Task 3.1] API Client扩展 (Day 11)

**目标**: 在extension的api.ts中添加Analytics API调用函数

#### Step 3.1.1: 添加Analytics API函数

**修改文件**: `vscode-extension/src/api.ts`

**新增接口**:
```typescript
// Analytics Response Types
export interface SessionSummary {
    session_id: string;
    thread_id: string;
    title: string;
    research_topic: string;
    status: 'active' | 'completed' | 'archived' | 'failed';
    created_at: string;
    completed_at?: string;
    duration_seconds?: number;
    papers_count: number;
    events_count: number;
    tags: string[];
}

export interface SessionsListResponse {
    sessions: SessionSummary[];
    total: number;
    limit: number;
    offset: number;
    has_more: boolean;
}

export interface SessionStats {
    total_sessions: number;
    completed_sessions: number;
    failed_sessions: number;
    running_sessions: number;
    success_rate: number;
    total_papers_collected: number;
    avg_papers_per_session: number;
    avg_duration_seconds: number;
}

export interface DailyBreakdown {
    date: string;
    sessions: number;
    completed: number;
    failed: number;
}

export interface SessionStatsResponse {
    time_range: string;
    stats: SessionStats;
    daily_breakdown: DailyBreakdown[];
    top_topics: Array<{topic: string; count: number; avg_papers: number}>;
}

export interface PaperTrendsResponse {
    time_range: string;
    trends: {
        total_papers: number;
        unique_papers: number;
        avg_papers_per_day: number;
        papers_by_day: Array<{date: string; papers_count: number}>;
        top_venues: Array<{venue: string; papers_count: number; percentage: number}>;
        papers_by_year: Array<{year: number; count: number}>;
    };
}

export interface SessionDetailsResponse {
    session: SessionSummary & {
        notes?: string;
    };
    events: Array<{
        event_id: string;
        event_type: string;
        timestamp: string;
        metadata: any;
    }>;
    timeline: {
        total_duration_seconds: number;
        phases: Array<{
            phase: string;
            duration_seconds: number;
            percentage: number;
        }>;
    };
}
```

**新增函数**:
```typescript
/**
 * Get paginated list of research sessions
 */
export async function getSessionsList(params?: {
    limit?: number;
    offset?: number;
    status?: 'active' | 'completed' | 'archived';
    sort_by?: 'created_at' | 'duration' | 'papers_count';
    order?: 'asc' | 'desc';
}): Promise<SessionsListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    if (params?.status) queryParams.append('status', params.status);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.order) queryParams.append('order', params.order);
    
    const response = await axios.get(
        `${API_BASE_URL}/analytics/sessions?${queryParams.toString()}`
    );
    return response.data;
}

/**
 * Get aggregated session statistics
 */
export async function getSessionStats(
    timeRange: '24h' | '7d' | '30d' | 'all' = '7d'
): Promise<SessionStatsResponse> {
    const response = await axios.get(
        `${API_BASE_URL}/analytics/sessions/stats?time_range=${timeRange}`
    );
    return response.data;
}

/**
 * Get paper collection trends
 */
export async function getPaperTrends(
    timeRange: '24h' | '7d' | '30d' | 'all' = '7d'
): Promise<PaperTrendsResponse> {
    const response = await axios.get(
        `${API_BASE_URL}/analytics/papers/trends?time_range=${timeRange}`
    );
    return response.data;
}

/**
 * Get detailed analytics for a specific session
 */
export async function getSessionDetails(
    sessionId: string
): Promise<SessionDetailsResponse> {
    const response = await axios.get(
        `${API_BASE_URL}/analytics/sessions/${sessionId}`
    );
    return response.data;
}
```

---

### [Task 3.2] Analytics Webview UI (Day 12-13)

**目标**: 创建Analytics Dashboard Webview

#### Step 3.2.1: 创建Analytics Dashboard HTML

**新建文件**: `vscode-extension/src/analyticsWebview.ts`

**内容结构**:
```typescript
export function generateAnalyticsDashboardHTML(
    stats: SessionStatsResponse,
    trends: PaperTrendsResponse,
    sessions: SessionsListResponse
): string {
    return `<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Analytics Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
        <style>
            /* VS Code Theme CSS */
            body {
                font-family: var(--vscode-font-family);
                color: var(--vscode-foreground);
                background-color: var(--vscode-editor-background);
                padding: 20px;
                margin: 0;
            }
            
            .dashboard-container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }
            
            .time-range-selector {
                display: flex;
                gap: 10px;
            }
            
            .btn {
                padding: 8px 16px;
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            
            .btn.active {
                background-color: var(--vscode-button-hoverBackground);
            }
            
            /* Summary Cards */
            .summary-cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .card {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                border-left: 4px solid var(--vscode-textLink-foreground);
                padding: 20px;
                border-radius: 4px;
            }
            
            .card-title {
                font-size: 14px;
                color: var(--vscode-descriptionForeground);
                margin-bottom: 10px;
            }
            
            .card-value {
                font-size: 32px;
                font-weight: bold;
                color: var(--vscode-textLink-activeForeground);
                margin-bottom: 5px;
            }
            
            .card-subtitle {
                font-size: 12px;
                color: var(--vscode-descriptionForeground);
            }
            
            /* Charts Section */
            .charts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .chart-container {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 20px;
                border-radius: 4px;
            }
            
            .chart-title {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            
            canvas {
                max-height: 300px;
            }
            
            /* Sessions Table */
            .sessions-section {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 20px;
                border-radius: 4px;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
            }
            
            th {
                text-align: left;
                padding: 12px;
                border-bottom: 2px solid var(--vscode-panel-border);
                font-weight: bold;
            }
            
            td {
                padding: 12px;
                border-bottom: 1px solid var(--vscode-panel-border);
            }
            
            .status-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            
            .status-completed {
                background-color: #4caf50;
                color: white;
            }
            
            .status-failed {
                background-color: #f44336;
                color: white;
            }
            
            .status-active {
                background-color: #2196f3;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="header">
                <h1>📊 Research Analytics Dashboard</h1>
                <div class="time-range-selector">
                    <button class="btn" onclick="changeTimeRange('24h')">24h</button>
                    <button class="btn active" onclick="changeTimeRange('7d')">7d</button>
                    <button class="btn" onclick="changeTimeRange('30d')">30d</button>
                    <button class="btn" onclick="changeTimeRange('all')">All</button>
                </div>
            </div>
            
            <!-- Summary Cards -->
            <div class="summary-cards">
                <div class="card">
                    <div class="card-title">Total Sessions</div>
                    <div class="card-value">${stats.stats.total_sessions}</div>
                    <div class="card-subtitle">All research sessions</div>
                </div>
                <div class="card">
                    <div class="card-title">Success Rate</div>
                    <div class="card-value">${stats.stats.success_rate.toFixed(1)}%</div>
                    <div class="card-subtitle">${stats.stats.completed_sessions} completed</div>
                </div>
                <div class="card">
                    <div class="card-title">Total Papers</div>
                    <div class="card-value">${stats.stats.total_papers_collected}</div>
                    <div class="card-subtitle">${stats.stats.avg_papers_per_session.toFixed(1)} avg per session</div>
                </div>
                <div class="card">
                    <div class="card-title">Avg Duration</div>
                    <div class="card-value">${(stats.stats.avg_duration_seconds / 60).toFixed(1)}</div>
                    <div class="card-subtitle">minutes per session</div>
                </div>
            </div>
            
            <!-- Charts -->
            <div class="charts-grid">
                <div class="chart-container">
                    <div class="chart-title">Daily Sessions</div>
                    <canvas id="dailySessionsChart"></canvas>
                </div>
                <div class="chart-container">
                    <div class="chart-title">Papers Collection Trend</div>
                    <canvas id="papersTrendChart"></canvas>
                </div>
                <div class="chart-container">
                    <div class="chart-title">Session Status Distribution</div>
                    <canvas id="statusPieChart"></canvas>
                </div>
                <div class="chart-container">
                    <div class="chart-title">Top Research Topics</div>
                    <canvas id="topTopicsChart"></canvas>
                </div>
            </div>
            
            <!-- Sessions Table -->
            <div class="sessions-section">
                <h2>Recent Sessions</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Topic</th>
                            <th>Status</th>
                            <th>Papers</th>
                            <th>Duration</th>
                            <th>Created</th>
                        </tr>
                    </thead>
                    <tbody id="sessionsTable">
                        ${sessions.sessions.slice(0, 10).map(s => `
                            <tr onclick="viewSessionDetails('${s.session_id}')">
                                <td>${s.research_topic || s.title}</td>
                                <td><span class="status-badge status-${s.status}">${s.status}</span></td>
                                <td>${s.papers_count}</td>
                                <td>${s.duration_seconds ? (s.duration_seconds / 60).toFixed(1) + 'm' : '-'}</td>
                                <td>${new Date(s.created_at).toLocaleString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            const vscode = acquireVsCodeApi();
            
            // Chart.js initialization
            // ... (Chart code to be added)
            
            function changeTimeRange(range) {
                vscode.postMessage({ command: 'changeTimeRange', range });
            }
            
            function viewSessionDetails(sessionId) {
                vscode.postMessage({ command: 'viewSessionDetails', sessionId });
            }
        </script>
    </body>
    </html>`;
}
```

---

### [Task 3.3] Chart.js Integration (Day 14)

**目标**: 实现4个关键图表

#### Charts to Implement:
1. **Daily Sessions Line Chart** - 每日会话数量趋势
2. **Papers Trend Chart** - 论文收集趋势
3. **Status Pie Chart** - 会话状态分布
4. **Top Topics Bar Chart** - 热门研究主题

---

### [Task 3.4] Command Registration (Day 15)

**目标**: 注册Analytics命令并集成到Extension

#### Step 3.4.1: 添加Analytics命令

**修改文件**: `vscode-extension/src/extension.ts`

**添加内容**:
```typescript
const showAnalyticsCommand = vscode.commands.registerCommand(
    'auto-researcher.showAnalytics',
    async () => {
        const panel = vscode.window.createWebviewPanel(
            'analyticsPanel',
            'Research Analytics',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );
        
        // Show loading
        panel.webview.html = '<html><body><h2>Loading analytics...</h2></body></html>';
        
        try {
            // Fetch all analytics data
            const [stats, trends, sessions] = await Promise.all([
                getSessionStats('7d'),
                getPaperTrends('7d'),
                getSessionsList({ limit: 50 })
            ]);
            
            // Generate and set HTML
            panel.webview.html = generateAnalyticsDashboardHTML(stats, trends, sessions);
            
            // Handle webview messages
            panel.webview.onDidReceiveMessage(async (message) => {
                switch (message.command) {
                    case 'changeTimeRange':
                        // Reload data with new time range
                        const newStats = await getSessionStats(message.range);
                        const newTrends = await getPaperTrends(message.range);
                        panel.webview.html = generateAnalyticsDashboardHTML(
                            newStats, newTrends, sessions
                        );
                        break;
                    
                    case 'viewSessionDetails':
                        // Open session details
                        const details = await getSessionDetails(message.sessionId);
                        // Show in new webview or update current
                        break;
                }
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to load analytics: ${error}`);
        }
    }
);

context.subscriptions.push(showAnalyticsCommand);
```

---

## 技术栈

- **Frontend**: VS Code Webview API
- **Charting**: Chart.js 4.4.0 (CDN)
- **Styling**: VS Code CSS Variables
- **API Client**: axios (existing)
- **TypeScript**: Type-safe interfaces

---

## 实施优先级

**Day 11** (高优先级):
1. API Client函数 (必需)
2. TypeScript接口定义

**Day 12-13** (中优先级):
3. Basic Webview HTML
4. Summary Cards
5. Sessions Table

**Day 14** (中优先级):
6. Chart.js集成
7. 4个关键图表

**Day 15** (低优先级):
8. Command注册
9. 交互功能优化
10. 错误处理完善

---

## 验收标准

- [ ] 4个Analytics API函数可调用
- [ ] TypeScript类型定义完整
- [ ] Dashboard Webview可打开
- [ ] 4张Summary Cards显示
- [ ] 4个Chart.js图表渲染
- [ ] Sessions Table交互
- [ ] Time Range切换功能
- [ ] Session Details导航
- [ ] 错误处理完善
- [ ] TypeScript编译通过

---

## 下一步

Week 3完成后，Phase 3.5.3的3周计划将全部完成，系统具备完整的：
1. ✅ 实时交互能力 (WebSocket)
2. ✅ 后端分析APIs (Analytics)
3. 📋 前端可视化Dashboard (Week 3目标)

---

**当前状态**: Week 2 ✅ | Week 3 📋 Ready to Start  
**预计交付**: 2025-10-21 (压缩为5天)
