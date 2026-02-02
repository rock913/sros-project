/**
 * Phase 3.5.3: Analytics Dashboard Webview Generator
 * 
 * Generates HTML for the Analytics Dashboard with Chart.js visualizations
 */

import { SessionStatsResponse, PaperTrendsResponse, SessionsListResponse } from './api';

/**
 * Generate Analytics Dashboard HTML with embedded Chart.js
 */
export function generateAnalyticsDashboardHTML(
    stats: SessionStatsResponse,
    trends: PaperTrendsResponse,
    sessions: SessionsListResponse
): string {
    const daily = stats.daily_breakdown || [];
    const papersByDay = trends.trends.papers_by_day || [];
    const topTopics = stats.top_topics || [];
    
    // Extract recent topics from sessions for quick access
    const recentTopics = sessions.sessions
        .slice(0, 5)
        .map(s => s.research_topic)
        .filter((topic, index, self) => self.indexOf(topic) === index) // Remove duplicates
        .slice(0, 5);
    
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
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--vscode-panel-border);
        }
        
        h1 {
            font-size: 24px;
            margin: 0;
        }
        
        /* Research Starter Section */
        .research-starter {
            background: linear-gradient(135deg, 
                var(--vscode-editor-inactiveSelectionBackground) 0%, 
                var(--vscode-editor-background) 100%);
            border: 2px solid var(--vscode-textLink-foreground);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .research-starter h2 {
            font-size: 18px;
            margin: 0 0 16px 0;
            color: var(--vscode-textLink-foreground);
            font-weight: 600;
        }
        
        .research-input-container {
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }
        
        .research-input-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        #researchTopicInput {
            width: 100%;
            min-height: 64px;
            padding: 12px;
            font-size: 14px;
            font-family: var(--vscode-font-family);
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            resize: vertical;
        }
        
        #researchTopicInput:focus {
            outline: 1px solid var(--vscode-focusBorder);
            border-color: var(--vscode-focusBorder);
        }
        
        #researchTopicInput::placeholder {
            color: var(--vscode-input-placeholderForeground);
        }
        
        .char-counter {
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
            margin-top: 4px;
            text-align: right;
        }
        
        .char-counter.warning {
            color: var(--vscode-editorWarning-foreground);
        }
        
        .char-counter.error {
            color: var(--vscode-errorForeground);
        }
        
        .research-actions {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .primary-btn {
            height: 64px;
            padding: 0 24px;
            font-size: 15px;
            font-weight: 600;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            white-space: nowrap;
            transition: background-color 0.2s;
        }
        
        .primary-btn:hover:not(:disabled) {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        .primary-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .secondary-btn {
            height: 32px;
            padding: 0 16px;
            font-size: 13px;
            background-color: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: 1px solid var(--vscode-button-border);
            border-radius: 4px;
            cursor: pointer;
            white-space: nowrap;
        }
        
        .secondary-btn:hover {
            background-color: var(--vscode-button-secondaryHoverBackground);
        }
        
        .recent-topics-dropdown {
            position: relative;
        }
        
        .dropdown-menu {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 4px;
            background-color: var(--vscode-dropdown-background);
            border: 1px solid var(--vscode-dropdown-border);
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            min-width: 300px;
            max-width: 500px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
        }
        
        .dropdown-menu.show {
            display: block;
        }
        
        .dropdown-item {
            padding: 10px 16px;
            cursor: pointer;
            border-bottom: 1px solid var(--vscode-panel-border);
            font-size: 13px;
            transition: background-color 0.2s;
        }
        
        .dropdown-item:last-child {
            border-bottom: none;
        }
        
        .dropdown-item:hover {
            background-color: var(--vscode-list-hoverBackground);
        }
        
        .dropdown-item .topic-text {
            display: block;
            color: var(--vscode-foreground);
            margin-bottom: 4px;
        }
        
        .dropdown-item .topic-meta {
            font-size: 11px;
            color: var(--vscode-descriptionForeground);
        }
        
        .empty-topics {
            padding: 16px;
            text-align: center;
            color: var(--vscode-descriptionForeground);
            font-size: 13px;
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
        
        <!-- Research Starter Section -->
        <div class="research-starter">
            <h2>🚀 Start New Research</h2>
            <div class="research-input-container">
                <div class="research-input-wrapper">
                    <textarea 
                        id="researchTopicInput" 
                        placeholder="Enter your research topic (e.g., 'Latest advances in transformer architectures', 'Large language model hallucination mitigation')..."
                        maxlength="200"
                        oninput="updateCharCounter()"
                        onkeydown="handleInputKeydown(event)"
                    ></textarea>
                    <div id="charCounter" class="char-counter">0 / 200</div>
                </div>
                <div class="research-actions">
                    <button id="startResearchBtn" class="primary-btn" onclick="startResearchFromDashboard()" disabled>
                        🚀 Start Research
                    </button>
                    ${recentTopics.length > 0 ? `
                    <div class="recent-topics-dropdown">
                        <button class="secondary-btn" onclick="toggleRecentTopics()">
                            📝 Recent Topics ▼
                        </button>
                        <div id="recentTopicsMenu" class="dropdown-menu">
                            ${recentTopics.map(topic => `
                                <div class="dropdown-item" onclick="selectRecentTopic('${topic.replace(/'/g, "\\'")}')">
                                    <span class="topic-text">${topic}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
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
                        <tr class="session-row" data-session-id="${s.session_id}">
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
            console.log('[Analytics Dashboard] viewSessionDetails called with sessionId:', sessionId);
            vscode.postMessage({ command: 'viewSessionDetails', sessionId: sessionId });
            console.log('[Analytics Dashboard] Message posted to extension');
        }
        
        // Research Starter Functions
        function updateCharCounter() {
            const input = document.getElementById('researchTopicInput');
            const counter = document.getElementById('charCounter');
            const btn = document.getElementById('startResearchBtn');
            const length = input.value.trim().length;
            
            counter.textContent = length + ' / 200';
            
            // Update counter color based on length
            counter.classList.remove('warning', 'error');
            if (length > 180) {
                counter.classList.add('error');
            } else if (length > 150) {
                counter.classList.add('warning');
            }
            
            // Enable/disable button based on validation
            if (length >= 5 && length <= 200) {
                btn.disabled = false;
            } else {
                btn.disabled = true;
            }
        }
        
        function handleInputKeydown(event) {
            // Submit on Enter (but allow Shift+Enter for new line)
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                startResearchFromDashboard();
            }
            // Clear on Escape
            if (event.key === 'Escape') {
                document.getElementById('researchTopicInput').value = '';
                updateCharCounter();
            }
        }
        
        function startResearchFromDashboard() {
            const input = document.getElementById('researchTopicInput');
            const topic = input.value.trim();
            
            if (topic.length < 5) {
                alert('Please enter a topic (at least 5 characters)');
                return;
            }
            
            if (topic.length > 200) {
                alert('Topic is too long (max 200 characters)');
                return;
            }
            
            // Send message to extension
            vscode.postMessage({ 
                command: 'startResearchFromDashboard', 
                topic: topic 
            });
            
            // Clear input
            input.value = '';
            updateCharCounter();
        }
        
        function toggleRecentTopics() {
            const menu = document.getElementById('recentTopicsMenu');
            menu.classList.toggle('show');
            
            // Close dropdown when clicking outside
            if (menu.classList.contains('show')) {
                setTimeout(() => {
                    document.addEventListener('click', function closeDropdown(e) {
                        if (!e.target.closest('.recent-topics-dropdown')) {
                            menu.classList.remove('show');
                            document.removeEventListener('click', closeDropdown);
                        }
                    });
                }, 0);
            }
        }
        
        function selectRecentTopic(topic) {
            document.getElementById('researchTopicInput').value = topic;
            document.getElementById('recentTopicsMenu').classList.remove('show');
            updateCharCounter();
            
            // Auto-focus on input for easy editing
            document.getElementById('researchTopicInput').focus();
        }
        
        // Hide loading indicator and show dashboard after charts are rendered
        window.addEventListener('load', () => {
            console.log('[Analytics Dashboard] Window loaded, initializing...');
            
            // Set up event delegation for session table rows
            const sessionsTable = document.querySelector('.sessions-section tbody');
            if (sessionsTable) {
                console.log('[Analytics Dashboard] Found sessions table, adding click listener');
                sessionsTable.addEventListener('click', (e) => {
                    const row = e.target.closest('tr.session-row');
                    if (row) {
                        const sessionId = row.dataset.sessionId;
                        console.log('[Analytics Dashboard] Row clicked, sessionId:', sessionId);
                        viewSessionDetails(sessionId);
                    } else {
                        console.log('[Analytics Dashboard] Click target is not a session row:', e.target);
                    }
                });
            } else {
                console.error('[Analytics Dashboard] Sessions table tbody not found!');
            }
            
            // Hide loading, show dashboard
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
                console.log('[Analytics Dashboard] Dashboard displayed');
            }, 300); // Small delay to ensure Chart.js is fully initialized
        });
    </script>
</body>
</html>`;
}
