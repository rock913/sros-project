import * as vscode from 'vscode';
import { 
    checkHealth, 
    getAgentState, 
    AgentState,
    // Phase 3.5.2: New imports
    getAllPapers,
    getAllReports,
    exportPapers,
    exportReport,
    compareReports,
    PaperDetail,
    ReportDetail,
    // Phase 3.5.3 Week 3: Analytics imports
    getSessionStats,
    getPaperTrends,
    getSessionsList
} from './api';
import { generateAnalyticsDashboardHTML } from './analyticsWebview';
// Phase 3.6: HITL imports
import { generateHITLDecisionCardHTML, HITLRequest } from './hitlWebview';

/**
 * Generates enhanced HTML for the AI Control Panel webview
 */
function generateControlPanelHTML(state: AgentState, healthStatus: string): string {
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
function generatePaperDetailsHTML(paper: PaperDetail): string {
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
export class AssetLibraryProvider implements vscode.TreeDataProvider<PaperTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<PaperTreeItem | undefined | null | void> = new vscode.EventEmitter<PaperTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<PaperTreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private groupBy: 'session' | 'source' | 'date' = 'session';

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    setGrouping(groupBy: 'session' | 'source' | 'date'): void {
        this.groupBy = groupBy;
        this.refresh();
    }

    getTreeItem(element: PaperTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: PaperTreeItem): Promise<PaperTreeItem[]> {
        // If a group item is clicked, show its papers
        if (element && element.papers) {
            return element.papers.map(paper => new PaperTreeItem(
                paper.title,
                vscode.TreeItemCollapsibleState.None,
                undefined,
                paper
            ));
        }

        // If a paper is clicked, no children
        if (element && element.paperDetail) {
            return [];
        }

        // Root level: fetch all papers and group them
        const { papers } = await getAllPapers({ limit: 500 });
        
        if (papers.length === 0) {
            const item = new PaperTreeItem('No papers found', vscode.TreeItemCollapsibleState.None);
            return [item];
        }

        // Group papers
        return this.groupPapers(papers);
    }

    private groupPapers(papers: PaperDetail[]): PaperTreeItem[] {
        if (this.groupBy === 'session') {
            return this.groupBySession(papers);
        } else if (this.groupBy === 'source') {
            return this.groupBySource(papers);
        } else {
            return this.groupByDate(papers);
        }
    }

    private groupBySession(papers: PaperDetail[]): PaperTreeItem[] {
        const groups = new Map<string, PaperDetail[]>();
        
        papers.forEach(paper => {
            const sessionId = paper.session_id;
            if (!groups.has(sessionId)) {
                groups.set(sessionId, []);
            }
            groups.get(sessionId)!.push(paper);
        });

        return Array.from(groups.entries()).map(([sessionId, sessionPapers]) => {
            const label = `Session ${sessionId.substring(0, 8)}... (${sessionPapers.length} papers)`;
            return new PaperTreeItem(
                label,
                vscode.TreeItemCollapsibleState.Collapsed,
                sessionPapers
            );
        });
    }

    private groupBySource(papers: PaperDetail[]): PaperTreeItem[] {
        const groups = new Map<string, PaperDetail[]>();
        
        papers.forEach(paper => {
            const source = paper.extra_metadata.source || 'unknown';
            if (!groups.has(source)) {
                groups.set(source, []);
            }
            groups.get(source)!.push(paper);
        });

        return Array.from(groups.entries()).map(([source, sourcePapers]) => {
            const label = `${source.toUpperCase()} (${sourcePapers.length} papers)`;
            return new PaperTreeItem(
                label,
                vscode.TreeItemCollapsibleState.Collapsed,
                sourcePapers
            );
        });
    }

    private groupByDate(papers: PaperDetail[]): PaperTreeItem[] {
        const groups = new Map<string, PaperDetail[]>();
        
        papers.forEach(paper => {
            const date = new Date(paper.created_at);
            const dateKey = date.toISOString().split('T')[0]; // YYYY-MM-DD
            if (!groups.has(dateKey)) {
                groups.set(dateKey, []);
            }
            groups.get(dateKey)!.push(paper);
        });

        // Sort by date descending
        const sorted = Array.from(groups.entries()).sort((a, b) => b[0].localeCompare(a[0]));

        return sorted.map(([date, datePapers]) => {
            const label = `${date} (${datePapers.length} papers)`;
            return new PaperTreeItem(
                label,
                vscode.TreeItemCollapsibleState.Collapsed,
                datePapers
            );
        });
    }
}

// Custom TreeItem for papers with additional metadata
class PaperTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly papers?: PaperDetail[], // For group items
        public readonly paperDetail?: PaperDetail // For individual paper items
    ) {
        super(label, collapsibleState);

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
        } else {
            // Group item styling
            this.contextValue = 'paperGroup';
            this.iconPath = new vscode.ThemeIcon('folder');
        }
    }

    private createTooltip(paper: PaperDetail): string {
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
export class ManuscriptProvider implements vscode.TreeDataProvider<ReportTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<ReportTreeItem | undefined | null | void> = new vscode.EventEmitter<ReportTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<ReportTreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: ReportTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: ReportTreeItem): Promise<ReportTreeItem[]> {
        // If a session item is clicked, show its reports
        if (element && element.reports) {
            return element.reports.map(report => new ReportTreeItem(
                `Version ${report.version}`,
                vscode.TreeItemCollapsibleState.None,
                undefined,
                report
            ));
        }

        // If a report is clicked, no children
        if (element && element.reportDetail) {
            return [];
        }

        // Root level: fetch all reports and group by session
        const { reports } = await getAllReports({ limit: 500 });
        
        if (reports.length === 0) {
            const item = new ReportTreeItem('No reports found', vscode.TreeItemCollapsibleState.None);
            return [item];
        }

        // Group reports by session
        return this.groupBySession(reports);
    }

    private groupBySession(reports: ReportDetail[]): ReportTreeItem[] {
        const groups = new Map<string, ReportDetail[]>();
        
        reports.forEach(report => {
            const sessionId = report.session_id;
            if (!groups.has(sessionId)) {
                groups.set(sessionId, []);
            }
            groups.get(sessionId)!.push(report);
        });

        // Sort each session's reports by version descending
        groups.forEach((sessionReports) => {
            sessionReports.sort((a, b) => b.version - a.version);
        });

        return Array.from(groups.entries()).map(([sessionId, sessionReports]) => {
            const latestVersion = sessionReports[0].version;
            const label = `Session ${sessionId.substring(0, 8)}... (v${latestVersion}, ${sessionReports.length} versions)`;
            return new ReportTreeItem(
                label,
                vscode.TreeItemCollapsibleState.Collapsed,
                sessionReports
            );
        });
    }
}

// Custom TreeItem for reports with additional metadata
class ReportTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly reports?: ReportDetail[], // For group items (session)
        public readonly reportDetail?: ReportDetail // For individual report items
    ) {
        super(label, collapsibleState);

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
        } else {
            // Group item styling (session)
            this.contextValue = 'reportGroup';
            this.iconPath = new vscode.ThemeIcon('folder');
        }
    }

    private createTooltip(report: ReportDetail): string {
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

/**
 * Phase 3.6: HITL Decision Handler
 * Handles HITL requests from backend and displays decision cards
 */
async function handleHITLRequest(request: HITLRequest, context: vscode.ExtensionContext): Promise<void> {
    console.log(`[HITL] Received ${request.decision_type} request: ${request.request_id}`);
    
    // Create webview panel for HITL decision
    const panel = vscode.window.createWebviewPanel(
        'hitlDecision',
        `HITL: ${getDecisionTypeLabel(request.decision_type)}`,
        vscode.ViewColumn.One,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );
    
    // Generate and set HTML content
    panel.webview.html = generateHITLDecisionCardHTML(request);
    
    // Handle messages from webview
    panel.webview.onDidReceiveMessage(
        async (message) => {
            switch (message.type) {
                case 'hitl_response':
                    await sendHITLResponse(message.request_id, message.decision, message.modified_data);
                    panel.dispose();
                    vscode.window.showInformationMessage(`✅ HITL response sent: ${message.decision}`);
                    break;
                
                case 'copy_to_clipboard':
                    await vscode.env.clipboard.writeText(message.text);
                    break;
                
                case 'close_webview':
                    panel.dispose();
                    break;
            }
        },
        undefined,
        context.subscriptions
    );
    
    // Show notification
    vscode.window.showInformationMessage(
        `🔔 HITL Decision Required: ${getDecisionTypeLabel(request.decision_type)}`,
        'Open Decision Card'
    ).then(selection => {
        if (selection) {
            panel.reveal();
        }
    });
}

/**
 * Send HITL response to backend
 */
async function sendHITLResponse(requestId: string, decision: string, modifiedData: any): Promise<void> {
    try {
        const backendUrl = vscode.workspace.getConfiguration('auto-researcher').get<string>('backendUrl') || 'http://localhost:8121';
        
        const response = await fetch(`${backendUrl}/agent/hitl/respond`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                request_id: requestId,
                decision: decision,
                modified_data: modifiedData
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log(`[HITL] Response sent successfully:`, data);
        
    } catch (error: any) {
        console.error('[HITL] Failed to send response:', error);
        vscode.window.showErrorMessage(`Failed to send HITL response: ${error.message}`);
        throw error;
    }
}

/**
 * Get human-readable label for decision type
 */
function getDecisionTypeLabel(type: string): string {
    switch (type) {
        case 'query_approval': return 'Query Approval';
        case 'paper_selection': return 'Paper Selection';
        case 'report_revision': return 'Report Revision';
        default: return type;
    }
}

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "auto-researcher" is now active!');

    // Create provider instances
    const assetLibraryProvider = new AssetLibraryProvider();
    const manuscriptProvider = new ManuscriptProvider();

    // Register Tree Views
    vscode.window.registerTreeDataProvider('assetLibrary', assetLibraryProvider);
    vscode.window.registerTreeDataProvider('manuscript', manuscriptProvider);

    // Register Commands
    const showControlPanelCommand = vscode.commands.registerCommand('auto-researcher.showControlPanel', async () => {
        const panel = vscode.window.createWebviewPanel(
            'aiControlPanel',
            'AI Control Panel',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );
        
        // Show loading message
        panel.webview.html = '<html><body><h2>Loading...</h2><p>Fetching agent status from backend...</p></body></html>';
        
        let healthStatus = 'unknown';
        let agentState: AgentState = {
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: '',
        };
        
        try {
            // Fetch health status
            const health = await checkHealth();
            healthStatus = health.status || 'unknown';
            
            // Fetch full agent state
            agentState = await getAgentState();
        } catch (err) {
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
    const viewPaperDetailsCommand = vscode.commands.registerCommand('researchAgent.viewPaperDetails', async (paper: PaperDetail) => {
        const panel = vscode.window.createWebviewPanel(
            'paperDetails',
            `Paper: ${paper.title}`,
            vscode.ViewColumn.Two,
            { enableScripts: true }
        );

        panel.webview.html = generatePaperDetailsHTML(paper);
    });

    const exportPapersCommand = vscode.commands.registerCommand('researchAgent.exportPapers', async () => {
        // Ask user for export format
        const format = await vscode.window.showQuickPick(
            ['BibTeX', 'RIS', 'JSON'],
            { placeHolder: 'Select export format' }
        );

        if (!format) { return; }

        try {
            const formatMap: { [key: string]: 'bibtex' | 'ris' | 'json' } = {
                'BibTeX': 'bibtex',
                'RIS': 'ris',
                'JSON': 'json'
            };

            const result = await exportPapers(formatMap[format]);
            
            // Create a new document with the exported content
            const doc = await vscode.workspace.openTextDocument({
                content: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
                language: format === 'JSON' ? 'json' : 'plaintext'
            });

            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`Papers exported as ${format}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to export papers: ${error}`);
        }
    });

    // Phase 3.5.2: New commands for Report management
    const viewReportCommand = vscode.commands.registerCommand('researchAgent.viewReport', async (report: ReportDetail) => {
        // Create or show the report document
        const doc = await vscode.workspace.openTextDocument({
            content: report.content,
            language: 'markdown'
        });

        await vscode.window.showTextDocument(doc, vscode.ViewColumn.Two);
    });

    const exportReportCommand = vscode.commands.registerCommand('researchAgent.exportReport', async (report: ReportDetail) => {
        const format = await vscode.window.showQuickPick(
            ['Markdown', 'HTML'],
            { placeHolder: 'Select export format' }
        );

        if (!format) { return; }

        try {
            const formatMap: { [key: string]: 'markdown' | 'html' } = {
                'Markdown': 'markdown',
                'HTML': 'html'
            };

            const content = await exportReport(report.id, formatMap[format]);
            
            const doc = await vscode.workspace.openTextDocument({
                content: content,
                language: format === 'HTML' ? 'html' : 'markdown'
            });

            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`Report exported as ${format}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to export report: ${error}`);
        }
    });

    const compareReportsCommand = vscode.commands.registerCommand('researchAgent.compareReports', async (report: ReportDetail) => {
        // Get all reports for the same session
        const { reports } = await getAllReports({ session_id: report.session_id });
        
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

        if (!selected) { return; }

        try {
            const comparison = await compareReports(selected.report.id, report.id);
            
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
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to compare reports: ${error}`);
        }
    });

    const changeGroupingCommand = vscode.commands.registerCommand('researchAgent.changeGrouping', async () => {
        const groupBy = await vscode.window.showQuickPick(
            ['Session', 'Source', 'Date'],
            { placeHolder: 'Group papers by...' }
        );

        if (!groupBy) { return; }

        const groupMap: { [key: string]: 'session' | 'source' | 'date' } = {
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
                let currentTimeRange: '24h' | '7d' | '30d' | 'all' = 
                    context.workspaceState.get('analyticsTimeRange', '7d');

                const loadDashboardData = async (timeRange: '24h' | '7d' | '30d' | 'all') => {
                    const [stats, trends, sessions] = await Promise.all([
                        getSessionStats(timeRange),
                        getPaperTrends(timeRange),
                        getSessionsList({ limit: 50, sort_by: 'created_at', order: 'desc' })
                    ]);

                    return { stats, trends, sessions };
                };

                const { stats, trends, sessions } = await loadDashboardData(currentTimeRange);

                // Create webview panel
                const panel = vscode.window.createWebviewPanel(
                    'analyticsDashboard',
                    '📊 Analytics Dashboard',
                    vscode.ViewColumn.One,
                    {
                        enableScripts: true,
                        retainContextWhenHidden: true
                    }
                );

                // Set initial HTML
                panel.webview.html = generateAnalyticsDashboardHTML(stats, trends, sessions);

                // Handle messages from webview
                panel.webview.onDidReceiveMessage(
                    async (message) => {
                        switch (message.command) {
                            case 'changeTimeRange':
                                currentTimeRange = message.range;
                                // Save time range preference
                                await context.workspaceState.update('analyticsTimeRange', currentTimeRange);
                                const newData = await loadDashboardData(currentTimeRange);
                                panel.webview.html = generateAnalyticsDashboardHTML(newData.stats, newData.trends, newData.sessions);
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
                    },
                    undefined,
                    context.subscriptions
                );

                vscode.window.showInformationMessage('Analytics Dashboard loaded successfully!');
            });

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to load Analytics Dashboard: ${error}`);
        }
    });

    // Phase 3.6: HITL Test Command
    const testHITLCommand = vscode.commands.registerCommand('auto-researcher.testHITL', async () => {
        const decisionType = await vscode.window.showQuickPick(
            ['Query Approval', 'Paper Selection', 'Report Revision'],
            { placeHolder: 'Select HITL decision type to test' }
        );
        
        if (!decisionType) { return; }
        
        // Create mock HITL request
        let mockRequest: HITLRequest;
        
        if (decisionType === 'Query Approval') {
            mockRequest = {
                request_id: 'test_' + Date.now(),
                decision_type: 'query_approval',
                prompt: 'Please review and approve the generated queries',
                options: ['approve', 'modify', 'reject'],
                context: {
                    research_topic: 'Artificial Intelligence in Healthcare',
                    queries: [
                        'artificial intelligence healthcare applications',
                        'machine learning medical diagnosis',
                        'AI patient care optimization',
                        'deep learning radiology imaging'
                    ]
                },
                timeout_seconds: 300,
                session_id: 'test-session',
                thread_id: 'test-thread'
            };
        } else if (decisionType === 'Paper Selection') {
            mockRequest = {
                request_id: 'test_' + Date.now(),
                decision_type: 'paper_selection',
                prompt: 'Select papers to analyze',
                options: ['select_all', 'select_subset', 'reject'],
                context: {
                    total_count: 45,
                    papers: Array.from({ length: 25 }, (_, i) => ({
                        title: `Research Paper ${i + 1}: Impact of AI on Medical Outcomes`,
                        authors: ['Smith, J.', 'Johnson, K.', 'Williams, M.'],
                        year: 2023 - (i % 3),
                        doi: `10.1234/example.${i}`,
                        abstract: 'This paper explores the intersection of artificial intelligence and healthcare, focusing on diagnostic accuracy and patient outcomes...'
                    })),
                    recommendation: 'Select 10-15 most relevant papers for detailed analysis'
                },
                timeout_seconds: 600,
                session_id: 'test-session',
                thread_id: 'test-thread'
            };
        } else { // Report Revision
            mockRequest = {
                request_id: 'test_' + Date.now(),
                decision_type: 'report_revision',
                prompt: 'Please review the research report',
                options: ['approve', 'modify', 'reject'],
                context: {
                    research_topic: 'Artificial Intelligence in Healthcare',
                    report: `# Research Report: Artificial Intelligence in Healthcare

## Executive Summary

This report examines the current state and future prospects of artificial intelligence applications in healthcare. Through analysis of 25 recent papers, we identify key trends, challenges, and opportunities in this rapidly evolving field.

## Key Findings

1. **Diagnostic Accuracy**: AI systems have demonstrated accuracy rates comparable to or exceeding human experts in several domains, particularly in radiology and pathology.

2. **Patient Outcomes**: Studies show significant improvements in patient outcomes when AI-assisted decision support systems are properly integrated into clinical workflows.

3. **Challenges**: Major barriers include data privacy concerns, regulatory compliance, and the need for extensive validation in diverse clinical settings.

## Methodology

We analyzed 25 peer-reviewed papers published between 2021-2024, focusing on empirical studies with quantitative results. Papers were selected based on citation count, journal impact factor, and relevance to clinical applications.

## Recommendations

- Continued investment in robust validation studies
- Development of explainable AI systems for clinical use
- Establishment of clear regulatory frameworks

## Conclusion

AI holds tremendous promise for transforming healthcare delivery, but successful implementation requires careful attention to validation, integration, and regulatory considerations.`,
                    word_count: 187,
                    paper_count: 25
                },
                timeout_seconds: 900,
                session_id: 'test-session',
                thread_id: 'test-thread'
            };
        }
        
        await handleHITLRequest(mockRequest, context);
    });

    context.subscriptions.push(
        showControlPanelCommand,
        refreshAssetLibraryCommand,
        refreshManuscriptCommand,
        viewPaperDetailsCommand,
        exportPapersCommand,
        viewReportCommand,
        exportReportCommand,
        compareReportsCommand,
        changeGroupingCommand,
        showAnalyticsCommand,
        testHITLCommand
    );

    checkHealth()
        .then(data => {
            console.log('Backend health check successful:', data);
            vscode.window.showInformationMessage('Auto-Researcher: Connected to backend.');
        })
        .catch(error => {
            console.error('Backend health check failed:', error);
            vscode.window.showErrorMessage('Auto-Researcher: Failed to connect to backend.');
        });
}

export function deactivate() {}