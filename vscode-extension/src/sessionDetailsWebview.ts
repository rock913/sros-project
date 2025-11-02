/**
 * Phase 3.5.4: Session Details Webview Generator
 * 
 * Generates comprehensive HTML view for individual research session details
 */

export function generateSessionDetailsHTML(sessionId: string, data: any): string {
    const { session, events, papers, reports, stats } = data;
    
    // Format duration
    const durationMinutes = Math.floor(stats.duration_seconds / 60);
    const durationSeconds = stats.duration_seconds % 60;
    const durationStr = durationMinutes > 0 
        ? `${durationMinutes}m ${durationSeconds}s` 
        : `${durationSeconds}s`;
    
    // Status badge color mapping
    const statusColors: Record<string, string> = {
        'completed': '#4caf50',
        'running': '#2196f3',
        'failed': '#f44336',
        'pending': '#ff9800',
        'archived': '#9e9e9e'
    };
    
    const statusColor = statusColors[session.status] || '#666';
    
    // Format timestamps
    const formatDate = (isoString: string) => {
        const date = new Date(isoString);
        return date.toLocaleString();
    };
    
    // Truncate long text
    const truncate = (text: string, maxLength: number) => {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    };
    
    return `<!DOCTYPE html>
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
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Header Section */
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
            font-weight: 600;
        }
        
        .status-badge {
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
            background-color: ${statusColor};
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            border-left: 4px solid var(--vscode-textLink-foreground);
        }
        
        .stat-card h3 {
            margin: 0 0 8px 0;
            font-size: 36px;
            font-weight: bold;
            color: var(--vscode-textLink-activeForeground);
        }
        
        .stat-card p {
            margin: 0;
            font-size: 13px;
            color: var(--vscode-descriptionForeground);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Section Containers */
        .section {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            padding: 25px;
            border-radius: 6px;
            margin-bottom: 25px;
        }
        
        .section h2 {
            margin: 0 0 20px 0;
            font-size: 18px;
            font-weight: 600;
            color: var(--vscode-textLink-foreground);
            border-bottom: 1px solid var(--vscode-panel-border);
            padding-bottom: 10px;
        }
        
        /* Session Info Table */
        .info-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .info-table tr {
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .info-table tr:last-child {
            border-bottom: none;
        }
        
        .info-table td {
            padding: 12px 0;
        }
        
        .info-table td:first-child {
            font-weight: 600;
            width: 180px;
            color: var(--vscode-descriptionForeground);
        }
        
        .info-table td:last-child {
            color: var(--vscode-foreground);
        }
        
        /* Timeline */
        .timeline {
            position: relative;
            padding-left: 35px;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: var(--vscode-panel-border);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: 25px;
            padding-left: 20px;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -25px;
            top: 8px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--vscode-textLink-foreground);
            border: 3px solid var(--vscode-editor-background);
            box-shadow: 0 0 0 2px var(--vscode-textLink-foreground);
        }
        
        .timeline-time {
            font-size: 11px;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 4px;
        }
        
        .timeline-type {
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
            margin-bottom: 6px;
            font-size: 14px;
        }
        
        .timeline-details {
            font-size: 13px;
            color: var(--vscode-foreground);
            background-color: var(--vscode-input-background);
            padding: 8px 12px;
            border-radius: 4px;
            border-left: 3px solid var(--vscode-textLink-foreground);
        }
        
        .timeline-error .timeline-type {
            color: #f44336;
        }
        
        .timeline-error::before {
            background-color: #f44336;
            box-shadow: 0 0 0 2px #f44336;
        }
        
        .timeline-error .timeline-details {
            border-left-color: #f44336;
        }
        
        /* Lists */
        .item-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .item-list li {
            padding: 12px;
            margin-bottom: 8px;
            background-color: var(--vscode-input-background);
            border-radius: 4px;
            border-left: 3px solid var(--vscode-textLink-foreground);
        }
        
        .item-list li strong {
            color: var(--vscode-textLink-activeForeground);
            display: block;
            margin-bottom: 4px;
        }
        
        .item-list li span {
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
        }
        
        /* Action Buttons */
        .action-buttons {
            display: flex;
            gap: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid var(--vscode-panel-border);
        }
        
        button {
            padding: 10px 20px;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background-color 0.2s;
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
        
        .secondary-button {
            background-color: transparent;
            border: 1px solid var(--vscode-button-background);
            color: var(--vscode-button-background);
        }
        
        .secondary-button:hover {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--vscode-descriptionForeground);
            font-style: italic;
        }
        
        /* Scrollbar */
        .timeline::-webkit-scrollbar {
            width: 8px;
        }
        
        .timeline::-webkit-scrollbar-track {
            background-color: var(--vscode-editor-background);
        }
        
        .timeline::-webkit-scrollbar-thumb {
            background-color: var(--vscode-scrollbarSlider-background);
            border-radius: 4px;
        }
        
        .timeline::-webkit-scrollbar-thumb:hover {
            background-color: var(--vscode-scrollbarSlider-hoverBackground);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>${truncate(session.title || 'Untitled Session', 60)}</h1>
            <span class="status-badge">${session.status}</span>
        </div>
        
        <!-- Statistics Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3>${stats.paper_count}</h3>
                <p>Papers Collected</p>
            </div>
            <div class="stat-card">
                <h3>${stats.report_count}</h3>
                <p>Report Versions</p>
            </div>
            <div class="stat-card">
                <h3>${durationStr}</h3>
                <p>Total Duration</p>
            </div>
            <div class="stat-card">
                <h3>$${stats.cost_estimate.toFixed(4)}</h3>
                <p>Estimated Cost</p>
            </div>
        </div>
        
        <!-- Session Information -->
        <div class="section">
            <h2>📊 Session Information</h2>
            <table class="info-table">
                <tr>
                    <td>Session ID</td>
                    <td><code>${session.id}</code></td>
                </tr>
                <tr>
                    <td>Thread ID</td>
                    <td><code>${session.thread_id}</code></td>
                </tr>
                <tr>
                    <td>Research Topic</td>
                    <td>${session.research_topic || 'N/A'}</td>
                </tr>
                <tr>
                    <td>Created At</td>
                    <td>${formatDate(session.created_at)}</td>
                </tr>
                <tr>
                    <td>Last Updated</td>
                    <td>${formatDate(session.updated_at)}</td>
                </tr>
                <tr>
                    <td>Total Events</td>
                    <td>${stats.total_events}</td>
                </tr>
                ${session.tags && session.tags.length > 0 ? `
                <tr>
                    <td>Tags</td>
                    <td>${session.tags.join(', ')}</td>
                </tr>
                ` : ''}
                ${session.notes ? `
                <tr>
                    <td>Notes</td>
                    <td>${session.notes}</td>
                </tr>
                ` : ''}
            </table>
        </div>
        
        <!-- Event Timeline -->
        <div class="section">
            <h2>📅 Event Timeline (Latest ${events.length})</h2>
            ${events.length > 0 ? `
                <div class="timeline">
                    ${events.map((event: any) => {
                        const isError = event.event_type === 'error_occurred';
                        const eventClass = isError ? 'timeline-error' : '';
                        
                        let details = '';
                        if (event.event_data) {
                            if (event.event_data.message) {
                                details = event.event_data.message;
                            } else if (event.event_data.error) {
                                details = `Error: ${event.event_data.error}`;
                            } else {
                                details = JSON.stringify(event.event_data, null, 2);
                            }
                        }
                        
                        return `
                            <div class="timeline-item ${eventClass}">
                                <div class="timeline-time">${formatDate(event.created_at)}</div>
                                <div class="timeline-type">${event.event_type.replace(/_/g, ' ').toUpperCase()}</div>
                                ${details ? `<div class="timeline-details">${truncate(details, 200)}</div>` : ''}
                            </div>
                        `;
                    }).join('')}
                </div>
            ` : '<div class="empty-state">No events recorded for this session</div>'}
        </div>
        
        <!-- Papers -->
        <div class="section">
            <h2>📚 Papers (${papers.length})</h2>
            ${papers.length > 0 ? `
                <ul class="item-list">
                    ${papers.slice(0, 10).map((paper: any) => `
                        <li>
                            <strong>${truncate(paper.title || 'Untitled Paper', 100)}</strong>
                            <span>${paper.authors?.join(', ') || 'Unknown authors'} • ${paper.publication_year || 'N/A'}</span>
                        </li>
                    `).join('')}
                    ${papers.length > 10 ? `
                        <li style="text-align: center; font-style: italic;">
                            <span>... and ${papers.length - 10} more papers</span>
                        </li>
                    ` : ''}
                </ul>
            ` : '<div class="empty-state">No papers collected in this session</div>'}
        </div>
        
        <!-- Reports -->
        <div class="section">
            <h2>📝 Reports (${reports.length} versions)</h2>
            ${reports.length > 0 ? `
                <ul class="item-list">
                    ${reports.map((report: any) => {
                        const wordCount = report.extra_metadata?.word_count || 0;
                        const paperCount = report.extra_metadata?.paper_count || 0;
                        return `
                            <li>
                                <strong>Version ${report.version}</strong>
                                <span>Created ${formatDate(report.created_at)} • ${wordCount} words • ${paperCount} papers</span>
                            </li>
                        `;
                    }).join('')}
                </ul>
            ` : '<div class="empty-state">No reports generated for this session</div>'}
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons">
            <button onclick="exportSession()">📥 Export Session Data</button>
            <button class="secondary-button" onclick="openInLangSmith()">🔍 View in LangSmith</button>
            <button class="secondary-button" onclick="refreshDetails()">🔄 Refresh</button>
            <button class="danger-button" onclick="deleteSession()">🗑️ Delete Session</button>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function exportSession() {
            vscode.postMessage({ 
                command: 'exportSession', 
                sessionId: '${sessionId}' 
            });
        }
        
        function openInLangSmith() {
            vscode.postMessage({ 
                command: 'openLangSmith', 
                sessionId: '${sessionId}',
                threadId: '${session.thread_id}'
            });
        }
        
        function refreshDetails() {
            vscode.postMessage({ 
                command: 'refreshDetails', 
                sessionId: '${sessionId}' 
            });
        }
        
        function deleteSession() {
            if (confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
                vscode.postMessage({ 
                    command: 'deleteSession', 
                    sessionId: '${sessionId}' 
                });
            }
        }
    </script>
</body>
</html>`;
}
