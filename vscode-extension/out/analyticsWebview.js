"use strict";
/**
 * Phase 3.5.3: Analytics Dashboard Webview Generator
 *
 * Generates HTML for the Analytics Dashboard with Chart.js visualizations
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateAnalyticsDashboardHTML = generateAnalyticsDashboardHTML;
/**
 * Generate Analytics Dashboard HTML with embedded Chart.js
 */
function generateAnalyticsDashboardHTML(stats, trends, sessions) {
    const daily = stats.daily_breakdown || [];
    const papersByDay = trends.trends.papers_by_day || [];
    const topTopics = stats.top_topics || [];
    // Check if there's any data
    const hasData = stats.stats.total_sessions > 0;
    // Generate empty state message if no data
    if (!hasData) {
        return generateEmptyStateHTML();
    }
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
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
            padding-bottom: 20px;
            border-bottom: 2px solid var(--vscode-panel-border);
        }
        
        h1 {
            font-size: 24px;
            margin: 0;
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
            font-size: 14px;
        }
        
        .btn:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        .btn.active {
            background-color: var(--vscode-button-hoverBackground);
            font-weight: bold;
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
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .card-value {
            font-size: 36px;
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
            color: var(--vscode-textLink-foreground);
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
        
        .sessions-section h2 {
            font-size: 18px;
            margin-bottom: 15px;
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
            color: var(--vscode-descriptionForeground);
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        tr:hover {
            background-color: var(--vscode-list-hoverBackground);
            cursor: pointer;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
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
        
        .status-archived {
            background-color: #9e9e9e;
            color: white;
        }
        
        /* Loading Indicator */
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-left-color: var(--vscode-textLink-foreground);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            margin-top: 20px;
            font-size: 16px;
            color: var(--vscode-descriptionForeground);
        }
        
        #dashboard { display: none; }
    </style>
</head>
<body>
    <!-- Loading Indicator -->
    <div id="loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">Loading analytics data...</p>
    </div>
    
    <!-- Dashboard Content -->
    <div id="dashboard" class="dashboard-container">
        <div class="header">
            <h1>📊 Research Analytics Dashboard</h1>
            <div class="time-range-selector">
                <button class="btn ${stats.time_range === '24h' ? 'active' : ''}" onclick="changeTimeRange('24h')">24h</button>
                <button class="btn ${stats.time_range === '7d' ? 'active' : ''}" onclick="changeTimeRange('7d')">7d</button>
                <button class="btn ${stats.time_range === '30d' ? 'active' : ''}" onclick="changeTimeRange('30d')">30d</button>
                <button class="btn ${stats.time_range === 'all' ? 'active' : ''}" onclick="changeTimeRange('all')">All</button>
            </div>
        </div>
        
        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="card">
                <div class="card-title">Total Sessions</div>
                <div class="card-value">${stats.stats.total_sessions}</div>
                <div class="card-subtitle">${stats.stats.running_sessions} active · ${stats.stats.failed_sessions} failed</div>
            </div>
            <div class="card">
                <div class="card-title">Success Rate</div>
                <div class="card-value">${stats.stats.success_rate.toFixed(1)}%</div>
                <div class="card-subtitle">${stats.stats.completed_sessions} of ${stats.stats.total_sessions} completed</div>
            </div>
            <div class="card">
                <div class="card-title">Total Papers</div>
                <div class="card-value">${stats.stats.total_papers_collected}</div>
                <div class="card-subtitle">${stats.stats.avg_papers_per_session.toFixed(1)} avg per session</div>
            </div>
            <div class="card">
                <div class="card-title">Avg Duration</div>
                <div class="card-value">${(stats.stats.avg_duration_seconds / 60).toFixed(1)}m</div>
                <div class="card-subtitle">Average completion time</div>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">📈 Daily Sessions Trend</div>
                <canvas id="dailySessionsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">📄 Papers Collection</div>
                <canvas id="papersTrendChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">🎯 Session Status Distribution</div>
                <canvas id="statusPieChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">🔥 Top Research Topics</div>
                <canvas id="topTopicsChart"></canvas>
            </div>
        </div>
        
        <!-- Sessions Table -->
        <div class="sessions-section">
            <h2>📋 Recent Sessions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Research Topic</th>
                        <th>Status</th>
                        <th>Papers</th>
                        <th>Duration</th>
                        <th>Created</th>
                    </tr>
                </thead>
                <tbody>
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
        
        // Chart colors (VS Code theme compatible)
        const colors = {
            primary: '#007acc',
            success: '#4caf50',
            danger: '#f44336',
            warning: '#ff9800',
            info: '#2196f3',
            secondary: '#9e9e9e'
        };
        
        // Daily Sessions Chart
        const dailyData = ${JSON.stringify(daily)};
        new Chart(document.getElementById('dailySessionsChart'), {
            type: 'line',
            data: {
                labels: dailyData.map(d => d.date),
                datasets: [
                    {
                        label: 'Completed',
                        data: dailyData.map(d => d.completed),
                        borderColor: colors.success,
                        backgroundColor: colors.success + '40',
                        tension: 0.4
                    },
                    {
                        label: 'Failed',
                        data: dailyData.map(d => d.failed),
                        borderColor: colors.danger,
                        backgroundColor: colors.danger + '40',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // Papers Trend Chart
        const papersData = ${JSON.stringify(papersByDay)};
        new Chart(document.getElementById('papersTrendChart'), {
            type: 'bar',
            data: {
                labels: papersData.map(d => d.date),
                datasets: [{
                    label: 'Papers Collected',
                    data: papersData.map(d => d.papers_count),
                    backgroundColor: colors.info + '80',
                    borderColor: colors.info,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // Status Pie Chart
        new Chart(document.getElementById('statusPieChart'), {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Running', 'Failed'],
                datasets: [{
                    data: [
                        ${stats.stats.completed_sessions},
                        ${stats.stats.running_sessions},
                        ${stats.stats.failed_sessions}
                    ],
                    backgroundColor: [
                        colors.success,
                        colors.info,
                        colors.danger
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
        
        // Top Topics Chart
        const topicsData = ${JSON.stringify(topTopics.slice(0, 5))};
        new Chart(document.getElementById('topTopicsChart'), {
            type: 'bar',
            data: {
                labels: topicsData.map(t => t.topic.substring(0, 40) + '...'),
                datasets: [{
                    label: 'Sessions',
                    data: topicsData.map(t => t.count),
                    backgroundColor: colors.warning + '80',
                    borderColor: colors.warning,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { beginAtZero: true }
                }
            }
        });
        
        // Event handlers
        function changeTimeRange(range) {
            vscode.postMessage({ command: 'changeTimeRange', range: range });
        }
        
        function viewSessionDetails(sessionId) {
            vscode.postMessage({ command: 'viewSessionDetails', sessionId: sessionId });
        }
        
        // Hide loading indicator and show dashboard after charts are rendered
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
            }, 300); // Small delay to ensure Chart.js is fully initialized
        });
    </script>
</body>
</html>`;
}
/**
 * Generate empty state HTML when no data is available
 */
function generateEmptyStateHTML() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 20px;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        
        .empty-state {
            text-align: center;
            max-width: 500px;
            padding: 40px;
        }
        
        .empty-icon {
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        
        .empty-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--vscode-foreground);
        }
        
        .empty-description {
            font-size: 14px;
            line-height: 1.6;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 30px;
        }
        
        .empty-action {
            display: inline-block;
            padding: 10px 20px;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
        }
        
        .empty-action:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        .suggestions {
            margin-top: 30px;
            text-align: left;
        }
        
        .suggestions h3 {
            font-size: 16px;
            margin-bottom: 12px;
            color: var(--vscode-foreground);
        }
        
        .suggestions ul {
            list-style: none;
            padding: 0;
        }
        
        .suggestions li {
            padding: 8px 0;
            color: var(--vscode-descriptionForeground);
            font-size: 13px;
        }
        
        .suggestions li::before {
            content: "→ ";
            color: var(--vscode-textLink-foreground);
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="empty-state">
        <div class="empty-icon">📊</div>
        <h1 class="empty-title">暂无分析数据</h1>
        <p class="empty-description">
            还没有研究会话数据。开始你的第一次AI驱动的文献研究，我们将自动收集和分析数据。
        </p>
        <button class="empty-action" onclick="startNewResearch()">
            🚀 开始新研究
        </button>
        
        <div class="suggestions">
            <h3>💡 快速开始</h3>
            <ul>
                <li>使用命令面板 (Ctrl+Shift+P) 搜索 "Auto Researcher"</li>
                <li>输入你的研究主题，例如 "大语言模型的幻觉问题"</li>
                <li>等待AI完成文献收集和分析</li>
                <li>完成后即可在此查看详细统计数据</li>
            </ul>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function startNewResearch() {
            vscode.postMessage({ command: 'startNewResearch' });
        }
    </script>
</body>
</html>`;
}
//# sourceMappingURL=analyticsWebview.js.map