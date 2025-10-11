"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ManuscriptProvider = exports.AssetLibraryProvider = void 0;
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const api_1 = require("./api");
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
// New provider that fetches data from the backend API
class AssetLibraryProvider {
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
        if (element) {
            // Child items are not expected for papers in this view
            return [];
        }
        const state = await (0, api_1.getAgentState)();
        const papers = state.literature_abstracts;
        if (!papers || papers.length === 0) {
            return [new vscode.TreeItem('No papers found', vscode.TreeItemCollapsibleState.None)];
        }
        return papers.map((paper) => {
            const item = new vscode.TreeItem(paper.title, vscode.TreeItemCollapsibleState.None);
            item.description = paper.authors.join(', ');
            item.tooltip = paper.abstract;
            return item;
        });
    }
}
exports.AssetLibraryProvider = AssetLibraryProvider;
// New provider for the manuscript view
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
        if (element) {
            return [];
        }
        const state = await (0, api_1.getAgentState)();
        const report = state.report;
        if (!report) {
            return [new vscode.TreeItem('No report found', vscode.TreeItemCollapsibleState.None)];
        }
        // Wrap long reports
        const item = new vscode.TreeItem(report, vscode.TreeItemCollapsibleState.None);
        item.tooltip = report;
        return [item];
    }
}
exports.ManuscriptProvider = ManuscriptProvider;
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
    context.subscriptions.push(showControlPanelCommand, refreshAssetLibraryCommand, refreshManuscriptCommand);
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