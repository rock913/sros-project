"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ManuscriptProvider = exports.AssetLibraryProvider = void 0;
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const api_1 = require("./api");
const analyticsWebview_1 = require("./analyticsWebview");
/**
 * Generates enhanced HTML for the AI Control Panel webview
 */
function generateControlPanelHTML(state, healthStatus) {
    const paperCount = state.literature_abstracts?.length || 0;
    const queryCount = state.search_queries?.length || 0;
    const loopCount = state.research_loop_count || 0;
    const topic = state.research_topic || 'Not specified';
    const isSufficient = state.is_sufficient !== undefined ? (state.is_sufficient ? 'Yes' : 'No') : 'Unknown';
    const reportLength = state.report ? state.report.length : 0;
    const reportWordCount = state.report ? state.report.split(/\s+/).length : 0;
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Control Panel</title>
        <style>
            body {
                font-family: var(--vscode-font-family);
                color: var(--vscode-foreground);
                background-color: var(--vscode-editor-background);
                padding: 20px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: var(--vscode-titleBar-activeForeground);
                border-bottom: 2px solid var(--vscode-panel-border);
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .status-card {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                border-left: 4px solid var(--vscode-textLink-foreground);
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 4px;
            }
            .status-ok {
                border-left-color: #4caf50;
            }
            .status-error {
                border-left-color: #f44336;
            }
            .metric-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .metric-card {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 15px;
                border-radius: 4px;
                text-align: center;
            }
            .metric-value {
                font-size: 32px;
                font-weight: bold;
                color: var(--vscode-textLink-activeForeground);
                margin: 10px 0;
            }
            .metric-label {
                font-size: 12px;
                text-transform: uppercase;
                color: var(--vscode-descriptionForeground);
            }
            .info-section {
                margin-top: 20px;
            }
            .info-row {
                display: flex;
                padding: 8px 0;
                border-bottom: 1px solid var(--vscode-panel-border);
            }
            .info-label {
                font-weight: bold;
                min-width: 180px;
                color: var(--vscode-textPreformat-foreground);
            }
            .info-value {
                flex: 1;
                color: var(--vscode-editor-foreground);
            }
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }
            .badge-success {
                background-color: #4caf50;
                color: white;
            }
            .badge-warning {
                background-color: #ff9800;
                color: white;
            }
            .badge-info {
                background-color: #2196f3;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Research Agent Control Panel</h1>
            
            <!-- Health Status -->
            <div class="status-card ${healthStatus === 'ok' ? 'status-ok' : 'status-error'}">
                <strong>Backend Status:</strong> 
                <span class="badge ${healthStatus === 'ok' ? 'badge-success' : 'badge-warning'}">
                    ${healthStatus.toUpperCase()}
                </span>
            </div>

            <!-- Key Metrics -->
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Papers Collected</div>
                    <div class="metric-value">${paperCount}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Search Queries</div>
                    <div class="metric-value">${queryCount}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Research Loops</div>
                    <div class="metric-value">${loopCount}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Report Words</div>
                    <div class="metric-value">${reportWordCount}</div>
                </div>
            </div>

            <!-- Detailed Information -->
            <div class="info-section">
                <h2>Research Details</h2>
                <div class="info-row">
                    <div class="info-label">Research Topic:</div>
                    <div class="info-value">${topic}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Information Sufficient:</div>
                    <div class="info-value">
                        <span class="badge ${isSufficient === 'Yes' ? 'badge-success' : isSufficient === 'No' ? 'badge-warning' : 'badge-info'}">
                            ${isSufficient}
                        </span>
                    </div>
                </div>
                ${state.knowledge_gap ? `
                <div class="info-row">
                    <div class="info-label">Knowledge Gap:</div>
                    <div class="info-value">${state.knowledge_gap}</div>
                </div>
                ` : ''}
                <div class="info-row">
                    <div class="info-label">Report Length:</div>
                    <div class="info-value">${reportLength} characters (${reportWordCount} words)</div>
                </div>
            </div>

            ${state.search_queries && state.search_queries.length > 0 ? `
            <div class="info-section">
                <h2>Search Queries</h2>
                <ul>
                    ${state.search_queries.map(q => `<li>${q}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
        </div>
    </body>
    </html>`;
}
/**
 * Phase 3.5.2: Generates HTML for Paper Details view
 */
function generatePaperDetailsHTML(paper) {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Paper Details</title>
        <style>
            body {
                font-family: var(--vscode-font-family);
                color: var(--vscode-foreground);
                background-color: var(--vscode-editor-background);
                padding: 20px;
                line-height: 1.6;
            }
            h1 {
                color: var(--vscode-titleBar-activeForeground);
                border-bottom: 2px solid var(--vscode-panel-border);
                padding-bottom: 10px;
            }
            .metadata {
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }
            .metadata-row {
                display: grid;
                grid-template-columns: 150px 1fr;
                margin: 8px 0;
            }
            .metadata-label {
                font-weight: bold;
                color: var(--vscode-textLink-foreground);
            }
            .abstract {
                margin: 20px 0;
                padding: 15px;
                background-color: var(--vscode-textBlockQuote-background);
                border-left: 4px solid var(--vscode-textLink-foreground);
            }
            a {
                color: var(--vscode-textLink-foreground);
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .tag {
                display: inline-block;
                padding: 3px 8px;
                margin: 2px;
                background-color: var(--vscode-badge-background);
                color: var(--vscode-badge-foreground);
                border-radius: 3px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <h1>${paper.title}</h1>
        
        <div class="metadata">
            <div class="metadata-row">
                <div class="metadata-label">Authors:</div>
                <div>${paper.authors.join(', ')}</div>
            </div>
            ${paper.doi ? `
            <div class="metadata-row">
                <div class="metadata-label">DOI:</div>
                <div><a href="https://doi.org/${paper.doi}">${paper.doi}</a></div>
            </div>
            ` : ''}
            ${paper.arxiv_id ? `
            <div class="metadata-row">
                <div class="metadata-label">arXiv ID:</div>
                <div><a href="https://arxiv.org/abs/${paper.arxiv_id}">${paper.arxiv_id}</a></div>
            </div>
            ` : ''}
            ${paper.url ? `
            <div class="metadata-row">
                <div class="metadata-label">URL:</div>
                <div><a href="${paper.url}">${paper.url}</a></div>
            </div>
            ` : ''}
            <div class="metadata-row">
                <div class="metadata-label">Collected:</div>
                <div>${new Date(paper.created_at).toLocaleString()}</div>
            </div>
            ${paper.extra_metadata.source ? `
            <div class="metadata-row">
                <div class="metadata-label">Source:</div>
                <div><span class="tag">${paper.extra_metadata.source.toUpperCase()}</span></div>
            </div>
            ` : ''}
            ${paper.extra_metadata.year ? `
            <div class="metadata-row">
                <div class="metadata-label">Year:</div>
                <div>${paper.extra_metadata.year}</div>
            </div>
            ` : ''}
        </div>

        ${paper.abstract ? `
        <div class="abstract">
            <h2>Abstract</h2>
            <p>${paper.abstract}</p>
        </div>
        ` : ''}
    </body>
    </html>`;
}
// Phase 3.5.2: Enhanced Asset Library Provider - shows all historical papers
class AssetLibraryProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.groupBy = 'session';
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    setGrouping(groupBy) {
        this.groupBy = groupBy;
        this.refresh();
    }
    getTreeItem(element) {
        return element;
    }
    async getChildren(element) {
        // If a group item is clicked, show its papers
        if (element && element.papers) {
            return element.papers.map(paper => new PaperTreeItem(paper.title, vscode.TreeItemCollapsibleState.None, undefined, paper));
        }
        // If a paper is clicked, no children
        if (element && element.paperDetail) {
            return [];
        }
        // Root level: fetch all papers and group them
        const { papers } = await (0, api_1.getAllPapers)({ limit: 500 });
        if (papers.length === 0) {
            const item = new PaperTreeItem('No papers found', vscode.TreeItemCollapsibleState.None);
            return [item];
        }
        // Group papers
        return this.groupPapers(papers);
    }
    groupPapers(papers) {
        if (this.groupBy === 'session') {
            return this.groupBySession(papers);
        }
        else if (this.groupBy === 'source') {
            return this.groupBySource(papers);
        }
        else {
            return this.groupByDate(papers);
        }
    }
    groupBySession(papers) {
        const groups = new Map();
        papers.forEach(paper => {
            const sessionId = paper.session_id;
            if (!groups.has(sessionId)) {
                groups.set(sessionId, []);
            }
            groups.get(sessionId).push(paper);
        });
        return Array.from(groups.entries()).map(([sessionId, sessionPapers]) => {
            const label = `Session ${sessionId.substring(0, 8)}... (${sessionPapers.length} papers)`;
            return new PaperTreeItem(label, vscode.TreeItemCollapsibleState.Collapsed, sessionPapers);
        });
    }
    groupBySource(papers) {
        const groups = new Map();
        papers.forEach(paper => {
            const source = paper.extra_metadata.source || 'unknown';
            if (!groups.has(source)) {
                groups.set(source, []);
            }
            groups.get(source).push(paper);
        });
        return Array.from(groups.entries()).map(([source, sourcePapers]) => {
            const label = `${source.toUpperCase()} (${sourcePapers.length} papers)`;
            return new PaperTreeItem(label, vscode.TreeItemCollapsibleState.Collapsed, sourcePapers);
        });
    }
    groupByDate(papers) {
        const groups = new Map();
        papers.forEach(paper => {
            const date = new Date(paper.created_at);
            const dateKey = date.toISOString().split('T')[0]; // YYYY-MM-DD
            if (!groups.has(dateKey)) {
                groups.set(dateKey, []);
            }
            groups.get(dateKey).push(paper);
        });
        // Sort by date descending
        const sorted = Array.from(groups.entries()).sort((a, b) => b[0].localeCompare(a[0]));
        return sorted.map(([date, datePapers]) => {
            const label = `${date} (${datePapers.length} papers)`;
            return new PaperTreeItem(label, vscode.TreeItemCollapsibleState.Collapsed, datePapers);
        });
    }
}
exports.AssetLibraryProvider = AssetLibraryProvider;
// Custom TreeItem for papers with additional metadata
class PaperTreeItem extends vscode.TreeItem {
    constructor(label, collapsibleState, papers, // For group items
    paperDetail // For individual paper items
    ) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.papers = papers;
        this.paperDetail = paperDetail;
        if (paperDetail) {
            // Individual paper styling
            this.description = paperDetail.authors.slice(0, 2).join(', ');
            this.tooltip = this.createTooltip(paperDetail);
            this.contextValue = 'paper';
            this.iconPath = new vscode.ThemeIcon('file-text');
            // Add command to view paper details
            this.command = {
                command: 'researchAgent.viewPaperDetails',
                title: 'View Paper Details',
                arguments: [paperDetail]
            };
        }
        else {
            // Group item styling
            this.contextValue = 'paperGroup';
            this.iconPath = new vscode.ThemeIcon('folder');
        }
    }
    createTooltip(paper) {
        let tooltip = `**${paper.title}**\n\n`;
        tooltip += `Authors: ${paper.authors.join(', ')}\n\n`;
        if (paper.abstract) {
            const shortAbstract = paper.abstract.substring(0, 200);
            tooltip += `Abstract: ${shortAbstract}${paper.abstract.length > 200 ? '...' : ''}\n\n`;
        }
        if (paper.doi) {
            tooltip += `DOI: ${paper.doi}\n`;
        }
        if (paper.url) {
            tooltip += `URL: ${paper.url}\n`;
        }
        tooltip += `Collected: ${new Date(paper.created_at).toLocaleString()}`;
        return tooltip;
    }
}
// Phase 3.5.2: Enhanced Manuscript Provider - shows all report versions
class ManuscriptProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    async getChildren(element) {
        // If a session item is clicked, show its reports
        if (element && element.reports) {
            return element.reports.map(report => new ReportTreeItem(`Version ${report.version}`, vscode.TreeItemCollapsibleState.None, undefined, report));
        }
        // If a report is clicked, no children
        if (element && element.reportDetail) {
            return [];
        }
        // Root level: fetch all reports and group by session
        const { reports } = await (0, api_1.getAllReports)({ limit: 500 });
        if (reports.length === 0) {
            const item = new ReportTreeItem('No reports found', vscode.TreeItemCollapsibleState.None);
            return [item];
        }
        // Group reports by session
        return this.groupBySession(reports);
    }
    groupBySession(reports) {
        const groups = new Map();
        reports.forEach(report => {
            const sessionId = report.session_id;
            if (!groups.has(sessionId)) {
                groups.set(sessionId, []);
            }
            groups.get(sessionId).push(report);
        });
        // Sort each session's reports by version descending
        groups.forEach((sessionReports) => {
            sessionReports.sort((a, b) => b.version - a.version);
        });
        return Array.from(groups.entries()).map(([sessionId, sessionReports]) => {
            const latestVersion = sessionReports[0].version;
            const label = `Session ${sessionId.substring(0, 8)}... (v${latestVersion}, ${sessionReports.length} versions)`;
            return new ReportTreeItem(label, vscode.TreeItemCollapsibleState.Collapsed, sessionReports);
        });
    }
}
exports.ManuscriptProvider = ManuscriptProvider;
// Custom TreeItem for reports with additional metadata
class ReportTreeItem extends vscode.TreeItem {
    constructor(label, collapsibleState, reports, // For group items (session)
    reportDetail // For individual report items
    ) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.reports = reports;
        this.reportDetail = reportDetail;
        if (reportDetail) {
            // Individual report styling
            const wordCount = reportDetail.extra_metadata.word_count || 0;
            const date = new Date(reportDetail.created_at).toLocaleDateString();
            this.description = `${wordCount} words • ${date}`;
            this.tooltip = this.createTooltip(reportDetail);
            this.contextValue = 'report';
            this.iconPath = new vscode.ThemeIcon('file-code');
            // Add command to view report
            this.command = {
                command: 'researchAgent.viewReport',
                title: 'View Report',
                arguments: [reportDetail]
            };
        }
        else {
            // Group item styling (session)
            this.contextValue = 'reportGroup';
            this.iconPath = new vscode.ThemeIcon('folder');
        }
    }
    createTooltip(report) {
        let tooltip = `**Report Version ${report.version}**\n\n`;
        tooltip += `Format: ${report.format}\n`;
        tooltip += `Created: ${new Date(report.created_at).toLocaleString()}\n`;
        if (report.extra_metadata.word_count) {
            tooltip += `Word Count: ${report.extra_metadata.word_count}\n`;
        }
        tooltip += `\nSession: ${report.session_id}`;
        return tooltip;
    }
}
function activate(context) {
    console.log('Congratulations, your extension "auto-researcher" is now active!');
    // Create provider instances
    const assetLibraryProvider = new AssetLibraryProvider();
    const manuscriptProvider = new ManuscriptProvider();
    // Register Tree Views
    vscode.window.registerTreeDataProvider('assetLibrary', assetLibraryProvider);
    vscode.window.registerTreeDataProvider('manuscript', manuscriptProvider);
    // Register Commands
    const showControlPanelCommand = vscode.commands.registerCommand('auto-researcher.showControlPanel', async () => {
        const panel = vscode.window.createWebviewPanel('aiControlPanel', 'AI Control Panel', vscode.ViewColumn.One, { enableScripts: true });
        // Show loading message
        panel.webview.html = '<html><body><h2>Loading...</h2><p>Fetching agent status from backend...</p></body></html>';
        let healthStatus = 'unknown';
        let agentState = {
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: '',
        };
        try {
            // Fetch health status
            const health = await (0, api_1.checkHealth)();
            healthStatus = health.status || 'unknown';
            // Fetch full agent state
            agentState = await (0, api_1.getAgentState)();
        }
        catch (err) {
            healthStatus = 'error';
            console.error('Error fetching agent data:', err);
        }
        // Generate and set the enhanced HTML
        panel.webview.html = generateControlPanelHTML(agentState, healthStatus);
    });
    const refreshAssetLibraryCommand = vscode.commands.registerCommand('auto-researcher.refreshAssetLibrary', () => {
        assetLibraryProvider.refresh();
        vscode.window.showInformationMessage('Asset Library refreshed.');
    });
    const refreshManuscriptCommand = vscode.commands.registerCommand('auto-researcher.refreshManuscript', () => {
        manuscriptProvider.refresh();
        vscode.window.showInformationMessage('Manuscript refreshed.');
    });
    // Phase 3.5.2: New commands for Paper management
    const viewPaperDetailsCommand = vscode.commands.registerCommand('researchAgent.viewPaperDetails', async (paper) => {
        const panel = vscode.window.createWebviewPanel('paperDetails', `Paper: ${paper.title}`, vscode.ViewColumn.Two, { enableScripts: true });
        panel.webview.html = generatePaperDetailsHTML(paper);
    });
    const exportPapersCommand = vscode.commands.registerCommand('researchAgent.exportPapers', async () => {
        // Ask user for export format
        const format = await vscode.window.showQuickPick(['BibTeX', 'RIS', 'JSON'], { placeHolder: 'Select export format' });
        if (!format) {
            return;
        }
        try {
            const formatMap = {
                'BibTeX': 'bibtex',
                'RIS': 'ris',
                'JSON': 'json'
            };
            const result = await (0, api_1.exportPapers)(formatMap[format]);
            // Create a new document with the exported content
            const doc = await vscode.workspace.openTextDocument({
                content: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
                language: format === 'JSON' ? 'json' : 'plaintext'
            });
            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`Papers exported as ${format}`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to export papers: ${error}`);
        }
    });
    // Phase 3.5.2: New commands for Report management
    const viewReportCommand = vscode.commands.registerCommand('researchAgent.viewReport', async (report) => {
        // Create or show the report document
        const doc = await vscode.workspace.openTextDocument({
            content: report.content,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc, vscode.ViewColumn.Two);
    });
    const exportReportCommand = vscode.commands.registerCommand('researchAgent.exportReport', async (report) => {
        const format = await vscode.window.showQuickPick(['Markdown', 'HTML'], { placeHolder: 'Select export format' });
        if (!format) {
            return;
        }
        try {
            const formatMap = {
                'Markdown': 'markdown',
                'HTML': 'html'
            };
            const content = await (0, api_1.exportReport)(report.id, formatMap[format]);
            const doc = await vscode.workspace.openTextDocument({
                content: content,
                language: format === 'HTML' ? 'html' : 'markdown'
            });
            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`Report exported as ${format}`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to export report: ${error}`);
        }
    });
    const compareReportsCommand = vscode.commands.registerCommand('researchAgent.compareReports', async (report) => {
        // Get all reports for the same session
        const { reports } = await (0, api_1.getAllReports)({ session_id: report.session_id });
        // Filter out the current report and show other versions
        const otherVersions = reports.filter(r => r.id !== report.id);
        if (otherVersions.length === 0) {
            vscode.window.showInformationMessage('No other versions to compare');
            return;
        }
        // Let user select which version to compare with
        const items = otherVersions.map(r => ({
            label: `Version ${r.version}`,
            description: new Date(r.created_at).toLocaleString(),
            report: r
        }));
        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: `Compare v${report.version} with...`
        });
        if (!selected) {
            return;
        }
        try {
            const comparison = await (0, api_1.compareReports)(selected.report.id, report.id);
            if (!comparison) {
                vscode.window.showErrorMessage('Failed to compare reports');
                return;
            }
            // Show diff in a new document
            const doc = await vscode.workspace.openTextDocument({
                content: comparison.diff,
                language: 'diff'
            });
            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`Comparing v${selected.report.version} → v${report.version}`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to compare reports: ${error}`);
        }
    });
    const changeGroupingCommand = vscode.commands.registerCommand('researchAgent.changeGrouping', async () => {
        const groupBy = await vscode.window.showQuickPick(['Session', 'Source', 'Date'], { placeHolder: 'Group papers by...' });
        if (!groupBy) {
            return;
        }
        const groupMap = {
            'Session': 'session',
            'Source': 'source',
            'Date': 'date'
        };
        assetLibraryProvider.setGrouping(groupMap[groupBy]);
        vscode.window.showInformationMessage(`Papers grouped by ${groupBy}`);
    });
    // Phase 3.5.3 Week 3: Analytics Dashboard Command
    const showAnalyticsCommand = vscode.commands.registerCommand('auto-researcher.showAnalytics', async () => {
        try {
            // Show loading notification
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: 'Loading Analytics Dashboard...',
                cancellable: false
            }, async (progress) => {
                progress.report({ message: 'Fetching statistics...' });
                // Load saved time range from workspace state, default to 7 days
                let currentTimeRange = context.workspaceState.get('analyticsTimeRange', '7d');
                const loadDashboardData = async (timeRange) => {
                    const [stats, trends, sessions] = await Promise.all([
                        (0, api_1.getSessionStats)(timeRange),
                        (0, api_1.getPaperTrends)(timeRange),
                        (0, api_1.getSessionsList)({ limit: 50, sort_by: 'created_at', order: 'desc' })
                    ]);
                    return { stats, trends, sessions };
                };
                const { stats, trends, sessions } = await loadDashboardData(currentTimeRange);
                // Create webview panel
                const panel = vscode.window.createWebviewPanel('analyticsDashboard', '📊 Analytics Dashboard', vscode.ViewColumn.One, {
                    enableScripts: true,
                    retainContextWhenHidden: true
                });
                // Set initial HTML
                panel.webview.html = (0, analyticsWebview_1.generateAnalyticsDashboardHTML)(stats, trends, sessions);
                // Handle messages from webview
                panel.webview.onDidReceiveMessage(async (message) => {
                    switch (message.command) {
                        case 'changeTimeRange':
                            currentTimeRange = message.range;
                            // Save time range preference
                            await context.workspaceState.update('analyticsTimeRange', currentTimeRange);
                            const newData = await loadDashboardData(currentTimeRange);
                            panel.webview.html = (0, analyticsWebview_1.generateAnalyticsDashboardHTML)(newData.stats, newData.trends, newData.sessions);
                            break;
                        case 'viewSessionDetails':
                            vscode.window.showInformationMessage(`Viewing session: ${message.sessionId.substring(0, 8)}`);
                            // TODO: Open session details view
                            break;
                        case 'startNewResearch':
                            // Close analytics panel and trigger new research
                            panel.dispose();
                            vscode.commands.executeCommand('auto-researcher.start');
                            break;
                    }
                }, undefined, context.subscriptions);
                vscode.window.showInformationMessage('Analytics Dashboard loaded successfully!');
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to load Analytics Dashboard: ${error}`);
        }
    });
    context.subscriptions.push(showControlPanelCommand, refreshAssetLibraryCommand, refreshManuscriptCommand, viewPaperDetailsCommand, exportPapersCommand, viewReportCommand, exportReportCommand, compareReportsCommand, changeGroupingCommand, showAnalyticsCommand);
    (0, api_1.checkHealth)()
        .then(data => {
        console.log('Backend health check successful:', data);
        vscode.window.showInformationMessage('Auto-Researcher: Connected to backend.');
    })
        .catch(error => {
        console.error('Backend health check failed:', error);
        vscode.window.showErrorMessage('Auto-Researcher: Failed to connect to backend.');
    });
}
function deactivate() { }
//# sourceMappingURL=extension.js.map