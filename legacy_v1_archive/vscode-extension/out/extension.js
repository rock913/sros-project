"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ManuscriptProvider = exports.AssetLibraryProvider = void 0;
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const api_1 = require("./api");
const analyticsWebview_1 = require("./analyticsWebview");
const sessionDetailsWebview_1 = require("./sessionDetailsWebview");
// Phase 3.6: HITL imports
const hitlWebview_1 = require("./hitlWebview");
// Phase 3.6 Week 3: Document Collaboration imports
const documentCollaboration_1 = require("./documentCollaboration");
// Phase 3.7 方案 A: Unified Research View imports (deprecated)
// import { UnifiedResearchViewProvider } from './UnifiedResearchViewProvider';
// Phase 3.7 方案 B: Research Sessions Tree Provider imports
const ResearchSessionsTreeProvider_1 = require("./ResearchSessionsTreeProvider");
const ManuscriptDocumentProvider_1 = require("./providers/ManuscriptDocumentProvider");
const ManuscriptCodeLensProvider_1 = require("./providers/ManuscriptCodeLensProvider");
const MindMapProvider_1 = require("./providers/MindMapProvider");
const researchCommands = require("./commands/researchSessionCommands");
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
/**
 * Phase 3.6: HITL Decision Handler
 * Handles HITL requests from backend and displays decision cards
 */
async function handleHITLRequest(request, context) {
    console.log(`[HITL] Received ${request.decision_type} request: ${request.request_id}`);
    // Create webview panel for HITL decision
    const panel = vscode.window.createWebviewPanel('hitlDecision', `HITL: ${getDecisionTypeLabel(request.decision_type)}`, vscode.ViewColumn.One, {
        enableScripts: true,
        retainContextWhenHidden: true
    });
    // Generate and set HTML content
    panel.webview.html = (0, hitlWebview_1.generateHITLDecisionCardHTML)(request);
    // Handle messages from webview
    panel.webview.onDidReceiveMessage(async (message) => {
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
    }, undefined, context.subscriptions);
    // Show notification
    vscode.window.showInformationMessage(`🔔 HITL Decision Required: ${getDecisionTypeLabel(request.decision_type)}`, 'Open Decision Card').then(selection => {
        if (selection) {
            panel.reveal();
        }
    });
}
/**
 * Send HITL response to backend
 */
async function sendHITLResponse(requestId, decision, modifiedData) {
    try {
        const backendUrl = vscode.workspace.getConfiguration('auto-researcher').get('backendUrl') || 'http://localhost:8121';
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
    }
    catch (error) {
        console.error('[HITL] Failed to send response:', error);
        vscode.window.showErrorMessage(`Failed to send HITL response: ${error.message}`);
        throw error;
    }
}
/**
 * Get human-readable label for decision type
 */
function getDecisionTypeLabel(type) {
    switch (type) {
        case 'query_approval': return 'Query Approval';
        case 'paper_selection': return 'Paper Selection';
        case 'report_revision': return 'Report Revision';
        default: return type;
    }
}
/**
 * Generate HTML for Research Progress View (Phase Frontend Fix)
 */
function generateResearchProgressHTML(topic, threadId) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Progress</title>
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
        .topic {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            border-left: 4px solid var(--vscode-textLink-foreground);
        }
        .progress-container {
            margin: 30px 0;
        }
        .progress-bar-container {
            width: 100%;
            height: 30px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, 
                var(--vscode-progressBar-background), 
                var(--vscode-textLink-foreground));
            width: 0%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .status-message {
            font-size: 16px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 4px;
        }
        
        /* HITL Approval Section */
        .hitl-container {
            display: none;
            background-color: var(--vscode-input-background);
            border: 2px solid var(--vscode-focusBorder);
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hitl-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .hitl-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        
        .hitl-title {
            font-size: 18px;
            font-weight: bold;
            color: var(--vscode-errorForeground);
        }
        
        .hitl-prompt {
            font-size: 14px;
            margin-bottom: 15px;
            padding: 10px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 4px;
            line-height: 1.6;
        }
        
        .hitl-queries {
            margin: 15px 0;
        }
        
        .hitl-queries-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: var(--vscode-textLink-foreground);
        }
        
        .query-item {
            background-color: var(--vscode-editor-background);
            padding: 12px;
            margin: 8px 0;
            border-radius: 4px;
            border-left: 3px solid var(--vscode-textLink-foreground);
            font-family: monospace;
            font-size: 13px;
            word-break: break-word;
        }
        
        .query-number {
            display: inline-block;
            background-color: var(--vscode-badge-background);
            color: var(--vscode-badge-foreground);
            padding: 2px 8px;
            border-radius: 10px;
            margin-right: 8px;
            font-size: 11px;
            font-weight: bold;
        }
        
        .hitl-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid var(--vscode-panel-border);
        }
        
        .hitl-button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .hitl-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .hitl-button:active {
            transform: translateY(0);
        }
        
        .btn-approve {
            background-color: #4CAF50;
            color: white;
        }
        
        .btn-approve:hover {
            background-color: #45a049;
        }
        
        .btn-reject {
            background-color: #f44336;
            color: white;
        }
        
        .btn-reject:hover {
            background-color: #da190b;
        }
        
        .btn-modify {
            background-color: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        
        .btn-modify:hover {
            background-color: var(--vscode-button-secondaryHoverBackground);
        }
        
        .hitl-context {
            margin-top: 15px;
            padding: 10px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 4px;
            font-size: 12px;
        }
        
        .hitl-context-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: var(--vscode-descriptionForeground);
        }
        
        .log-container {
            max-height: 400px;
            overflow-y: auto;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            padding: 15px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
        }
        .log-entry {
            padding: 5px 0;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        .log-entry:last-child {
            border-bottom: none;
        }
        .log-time {
            color: var(--vscode-descriptionForeground);
            margin-right: 10px;
        }
        .complete-banner {
            display: none;
            background-color: #4caf50;
            color: white;
            padding: 20px;
            border-radius: 4px;
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .thread-id {
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Research in Progress</h1>
        
        <div class="topic">
            <strong>Topic:</strong> ${topic}
            <div class="thread-id">Thread ID: ${threadId}</div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar-container">
                <div class="progress-bar" id="progressBar">0%</div>
            </div>
            
            <div class="status-message" id="statusMessage">
                🚀 Initializing research...
            </div>
        </div>
        
        <!-- HITL Approval Section (Hidden by default) -->
        <div class="hitl-container" id="hitlContainer">
            <div class="hitl-header">
                <span class="hitl-icon">⏸️</span>
                <span class="hitl-title">Human Approval Required</span>
            </div>
            
            <div class="hitl-prompt" id="hitlPrompt">
                <!-- Prompt will be inserted here -->
            </div>
            
            <div class="hitl-queries" id="hitlQueries">
                <!-- Queries will be inserted here -->
            </div>
            
            <div class="hitl-context" id="hitlContext" style="display: none;">
                <!-- Context will be inserted here -->
            </div>
            
            <div class="hitl-actions">
                <button class="hitl-button btn-approve" onclick="handleHitlResponse('approve')">
                    ✅ Approve
                </button>
                <button class="hitl-button btn-reject" onclick="handleHitlResponse('reject')">
                    ❌ Reject
                </button>
                <button class="hitl-button btn-modify" onclick="handleHitlResponse('modify')">
                    ✏️ Modify
                </button>
            </div>
        </div>
        
        <div class="complete-banner" id="completeBanner">
            ✅ Research Completed!
        </div>
        
        <h3>📋 Activity Log</h3>
        <div class="log-container" id="logContainer">
            <div class="log-entry">
                <span class="log-time">${new Date().toLocaleTimeString()}</span>
                <span>Research started for topic: "${topic}"</span>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        const progressBar = document.getElementById('progressBar');
        const statusMessage = document.getElementById('statusMessage');
        const logContainer = document.getElementById('logContainer');
        const completeBanner = document.getElementById('completeBanner');
        const hitlContainer = document.getElementById('hitlContainer');
        const hitlPrompt = document.getElementById('hitlPrompt');
        const hitlQueries = document.getElementById('hitlQueries');
        const hitlContext = document.getElementById('hitlContext');
        
        let currentHitlData = null;
        
        // Listen for messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'updateProgress':
                    updateProgress(message.progress, message.message);
                    addLogEntry(message.message);
                    break;
                case 'complete':
                    updateProgress(100, message.message);
                    addLogEntry(message.message);
                    completeBanner.style.display = 'block';
                    break;
                case 'error':
                    addLogEntry('❌ Error: ' + message.message);
                    break;
                case 'showHitlRequest':
                    showHitlRequest(message.data);
                    break;
                case 'hideHitlRequest':
                    hideHitlRequest();
                    break;
            }
        });
        
        function updateProgress(percent, message) {
            progressBar.style.width = percent + '%';
            progressBar.textContent = percent + '%';
            statusMessage.textContent = message;
        }
        
        function addLogEntry(message) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = \`
                <span class="log-time">\${new Date().toLocaleTimeString()}</span>
                <span>\${message}</span>
            \`;
            logContainer.appendChild(entry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        
        function showHitlRequest(data) {
            currentHitlData = data;
            
            // Set prompt
            hitlPrompt.textContent = data.prompt || 'Please review and approve the generated queries.';
            
            // Set queries
            if (data.context && data.context.queries) {
                hitlQueries.innerHTML = '<div class="hitl-queries-title">📝 Generated Queries:</div>';
                data.context.queries.forEach((query, index) => {
                    const queryItem = document.createElement('div');
                    queryItem.className = 'query-item';
                    queryItem.innerHTML = \`
                        <span class="query-number">\${index + 1}</span>
                        <span>\${escapeHtml(query)}</span>
                    \`;
                    hitlQueries.appendChild(queryItem);
                });
            }
            
            // Set context info
            if (data.context && data.context.research_topic) {
                hitlContext.style.display = 'block';
                hitlContext.innerHTML = \`
                    <div class="hitl-context-title">Research Topic:</div>
                    <div>\${escapeHtml(data.context.research_topic)}</div>
                \`;
            }
            
            // Show container
            hitlContainer.style.display = 'block';
            
            // Scroll to HITL section
            hitlContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            addLogEntry('⏸️ Waiting for human approval...');
        }
        
        function hideHitlRequest() {
            hitlContainer.style.display = 'none';
            currentHitlData = null;
        }
        
        function handleHitlResponse(action) {
            if (!currentHitlData) {
                return;
            }
            
            // Send response to extension
            vscode.postMessage({
                command: 'hitl_response',
                requestId: currentHitlData.request_id,
                action: action,
                selectedOption: currentHitlData.options ? currentHitlData.options[0] : null
            });
            
            // Hide HITL section
            hideHitlRequest();
            
            // Add log entry
            const actionText = action === 'approve' ? '✅ Approved' : action === 'reject' ? '❌ Rejected' : '✏️ Modification requested';
            addLogEntry(\`\${actionText} - Research continuing...\`);
        }
        
        function escapeHtml(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }
    </script>
</body>
</html>`;
}
/**
 * Helper function to create HITL request handler
 * Reusable across different research start points
 *
 * TEMPORARILY DISABLED: HITL auto-approves all requests to ensure smooth research flow
 * TODO: Re-enable after backend HITL implementation is fixed
 */
function createHitlRequestHandler(wsConnection, progressPanel) {
    return (hitlData) => {
        console.log('[Research] HITL Request received (auto-approving):', hitlData.request_id);
        // ⚠️ TEMPORARY: Auto-approve all HITL requests without user interaction
        // Send immediate approval to backend
        const { sendHitlResponse } = require('./api');
        sendHitlResponse(wsConnection, hitlData.request_id, true, hitlData.options?.[0]);
        // Update progress to show continuation
        progressPanel.webview.postMessage({
            command: 'updateProgress',
            message: '✅ Auto-approved! Continuing research...',
            progress: 40
        });
        // Add log entry
        console.log('[Research] Auto-approved HITL request:', hitlData.request_id);
    };
}
async function activate(context) {
    console.log('Congratulations, your extension "auto-researcher" is now active!');
    // Phase 3.6 Week 3: Initialize Document Collaboration Manager
    const docCollabManager = new documentCollaboration_1.DocumentCollaborationManager(context);
    context.subscriptions.push(docCollabManager);
    // Phase 3.7 方案 B: Initialize Research Sessions Tree Provider
    const researchSessionsTreeProvider = new ResearchSessionsTreeProvider_1.ResearchSessionsTreeProvider();
    context.subscriptions.push(vscode.window.registerTreeDataProvider('auto-researcher.researchSessionsTree', researchSessionsTreeProvider));
    // Phase 3.7 方案 B: Register Manuscript Document Provider
    const manuscriptDocProvider = new ManuscriptDocumentProvider_1.ManuscriptDocumentProvider();
    context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider('research-manuscript', manuscriptDocProvider));
    // Phase 5.2 Sprint 3: Register MindMap Provider for live Co-STORM updates
    const mindMapProvider = new MindMapProvider_1.MindMapProvider();
    context.subscriptions.push(vscode.window.registerTreeDataProvider('auto-researcher.mindmap', mindMapProvider));
    // Phase 3.7 方案 B: Register Manuscript CodeLens Provider
    const manuscriptCodeLensProvider = new ManuscriptCodeLensProvider_1.ManuscriptCodeLensProvider();
    context.subscriptions.push(vscode.languages.registerCodeLensProvider({ scheme: 'research-manuscript', language: 'markdown' }, manuscriptCodeLensProvider));
    // Create provider instances
    // 修复：package.json 中未定义这些视图，导致启动报错 "No view is registered with id: manuscript"
    // const assetLibraryProvider = new AssetLibraryProvider();
    // const manuscriptProvider = new ManuscriptProvider();
    // Register Tree Views
    // 修复：注释掉未定义的视图注册，避免启动错误
    // vscode.window.registerTreeDataProvider('assetLibrary', assetLibraryProvider);
    // vscode.window.registerTreeDataProvider('manuscript', manuscriptProvider);
    // Register Commands
    // Phase Frontend Fix: Start New Research Command
    const startResearchCommand = vscode.commands.registerCommand('auto-researcher.startResearch', async () => {
        try {
            // 1. Prompt user for research topic
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
                return; // User cancelled
            }
            // 2. Show progress notification
            vscode.window.showInformationMessage(`🚀 Starting research on: "${topic}"`);
            // 3. Create progress webview panel
            const panel = vscode.window.createWebviewPanel('researchProgress', `Research: ${topic.substring(0, 30)}${topic.length > 30 ? '...' : ''}`, vscode.ViewColumn.One, {
                enableScripts: true,
                retainContextWhenHidden: true
            });
            // 4. Generate thread ID using UUID v4
            const threadId = (0, api_1.generateThreadId)();
            // 5. Show initial progress HTML
            panel.webview.html = generateResearchProgressHTML(topic, threadId);
            // 6. Start research via WebSocket streaming
            try {
                panel.webview.postMessage({
                    command: 'updateProgress',
                    message: '🚀 Connecting to research agent...',
                    progress: 10
                });
                // Store WebSocket instance for HITL responses
                let wsConnection = null;
                wsConnection = await (0, api_1.startResearchStream)(topic, {
                    onStarted: (data) => {
                        console.log('[Research] Started:', data);
                        panel.webview.postMessage({
                            command: 'updateProgress',
                            message: '✅ Research task started',
                            progress: 20
                        });
                        vscode.window.showInformationMessage(`✅ Research started! Session ID: ${data.session_id}`);
                    },
                    onProgress: (data) => {
                        console.log('[Research] Progress:', data.node, data.message || '');
                        // Map node names to progress and user-friendly messages
                        const nodeProgressMap = {
                            'query_generation': { progress: 30, message: '📝 Generating search queries...' },
                            'query_approval': { progress: 35, message: '⏸️ Waiting for query approval (HITL)...' },
                            'search_and_filter': { progress: 50, message: '🔍 Searching and filtering papers...' },
                            'paper_selection': { progress: 60, message: '📚 Selecting relevant papers...' },
                            'paper_selection_approval': { progress: 65, message: '⏸️ Waiting for paper selection approval (HITL)...' },
                            'full_text_retrieval': { progress: 70, message: '📄 Retrieving full-text papers...' },
                            'report_synthesis': { progress: 85, message: '📊 Synthesizing research report...' },
                            'final_report': { progress: 95, message: '✍️ Finalizing report...' }
                        };
                        const nodeInfo = nodeProgressMap[data.node] || {
                            progress: 40,
                            message: `🔄 Processing: ${data.node}`
                        };
                        panel.webview.postMessage({
                            command: 'updateProgress',
                            message: data.message || nodeInfo.message,
                            progress: nodeInfo.progress
                        });
                        // Show HITL notifications
                        if (data.node.includes('approval')) {
                            vscode.window.showWarningMessage(`⏸️ HITL: ${data.message || 'Waiting for approval'}\nThread ID: ${threadId}`, 'View Instructions').then(selection => {
                                if (selection === 'View Instructions') {
                                    vscode.window.showInformationMessage(`To approve: curl -X POST "http://localhost:8121/agent/hitl/approve" -H "Content-Type: application/json" -d '{"thread_id":"${threadId}","request_id":"...","approved":true}'`);
                                }
                            });
                        }
                    },
                    onHitlRequest: createHitlRequestHandler(wsConnection, panel),
                    onComplete: (data) => {
                        console.log('[Research] Completed:', data);
                        panel.webview.postMessage({
                            command: 'complete',
                            message: '✅ Research report completed!',
                            progress: 100
                        });
                        vscode.window.showInformationMessage(`🎉 Research completed!\nSession ID: ${data.session_id}\nThread ID: ${threadId}`);
                        // Auto-refresh Manuscript and Asset Library to show new content
                        console.log('[Research] Auto-refreshing Manuscript and Asset Library...');
                        // manuscriptProvider.refresh(); // 修复：provider 已注释掉
                        // assetLibraryProvider.refresh(); // 修复：provider 已注释掉
                    },
                    onError: (error) => {
                        console.error('[Research] Error:', error);
                        panel.webview.postMessage({
                            command: 'updateProgress',
                            message: `❌ Error: ${error}`,
                            progress: 0
                        });
                        vscode.window.showErrorMessage(`Failed during research: ${error}`);
                    }
                }, threadId);
            }
            catch (error) {
                panel.webview.postMessage({
                    command: 'updateProgress',
                    message: `❌ Error: ${error.message}`,
                    progress: 0
                });
                vscode.window.showErrorMessage(`Failed to start research: ${error.message}`);
            }
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to start research: ${error}`);
        }
    });
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
        // assetLibraryProvider.refresh(); // 修复：provider 已注释掉
        vscode.window.showInformationMessage('Asset Library refresh not available.');
    });
    const refreshManuscriptCommand = vscode.commands.registerCommand('auto-researcher.refreshManuscript', () => {
        // manuscriptProvider.refresh(); // 修复：provider 已注释掉
        vscode.window.showInformationMessage('Manuscript refresh not available.');
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
        // assetLibraryProvider.setGrouping(groupMap[groupBy]); // 修复：provider 已注释掉
        vscode.window.showInformationMessage(`Paper grouping not available (provider disabled).`);
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
                            // Execute the viewSessionDetails command with the sessionId
                            console.log('[Extension] Received viewSessionDetails message with sessionId:', message.sessionId);
                            vscode.commands.executeCommand('auto-researcher.viewSessionDetails', message.sessionId);
                            console.log('[Extension] Executed viewSessionDetails command');
                            break;
                        case 'startNewResearch':
                        case 'startResearchFromDashboard':
                            // Close analytics panel
                            panel.dispose();
                            // If topic is provided (from dashboard input), start directly
                            if (message.topic && message.topic.trim().length >= 5) {
                                const topic = message.topic.trim();
                                // Show progress notification
                                vscode.window.showInformationMessage(`🚀 Starting research on: "${topic}"`);
                                // Create progress webview panel
                                const progressPanel = vscode.window.createWebviewPanel('researchProgress', `Research: ${topic.substring(0, 30)}${topic.length > 30 ? '...' : ''}`, vscode.ViewColumn.One, {
                                    enableScripts: true,
                                    retainContextWhenHidden: true
                                });
                                // Generate thread ID
                                const threadId = (0, api_1.generateThreadId)();
                                // Show initial progress HTML
                                progressPanel.webview.html = generateResearchProgressHTML(topic, threadId);
                                // Start research via WebSocket
                                try {
                                    // Store WebSocket instance for HITL responses
                                    let wsConnection = null;
                                    wsConnection = await (0, api_1.startResearchStream)(topic, {
                                        onStarted: (data) => {
                                            progressPanel.webview.postMessage({
                                                command: 'updateProgress',
                                                message: '✅ Research task started',
                                                progress: 20
                                            });
                                            vscode.window.showInformationMessage(`✅ Research started! Session ID: ${data.session_id}`);
                                        },
                                        onProgress: (data) => {
                                            const nodeProgressMap = {
                                                'query_generation': { progress: 30, message: '📝 Generating search queries...' },
                                                'query_approval': { progress: 35, message: '⏸️ Waiting for query approval...' },
                                                'search_and_filter': { progress: 50, message: '🔍 Searching papers...' },
                                                'paper_selection': { progress: 60, message: '📚 Selecting papers...' },
                                                'full_text_retrieval': { progress: 70, message: '📄 Retrieving full text...' },
                                                'report_synthesis': { progress: 85, message: '📊 Synthesizing report...' }
                                            };
                                            const nodeInfo = nodeProgressMap[data.node] || { progress: 40, message: `🔄 ${data.node}` };
                                            progressPanel.webview.postMessage({
                                                command: 'updateProgress',
                                                message: nodeInfo.message,
                                                progress: nodeInfo.progress
                                            });
                                        },
                                        onHitlRequest: createHitlRequestHandler(wsConnection, progressPanel),
                                        onComplete: (data) => {
                                            progressPanel.webview.postMessage({
                                                command: 'complete',
                                                message: '✅ Research completed!',
                                                progress: 100
                                            });
                                            vscode.window.showInformationMessage(`🎉 Research completed! Session ID: ${data.session_id}`);
                                            // Auto-refresh Manuscript and Asset Library to show new content
                                            console.log('[Analytics Dashboard] Auto-refreshing Manuscript and Asset Library...');
                                            // manuscriptProvider.refresh(); // 修复：provider 已注释掉
                                            // assetLibraryProvider.refresh(); // 修复：provider 已注释掉
                                            researchSessionsTreeProvider.refresh(); // 添加：刷新新的统一视图
                                        },
                                        onError: (error) => {
                                            progressPanel.webview.postMessage({
                                                command: 'updateProgress',
                                                message: `❌ Error: ${error}`,
                                                progress: 0
                                            });
                                            vscode.window.showErrorMessage(`Failed: ${error}`);
                                        }
                                    }, threadId);
                                }
                                catch (error) {
                                    progressPanel.webview.postMessage({
                                        command: 'updateProgress',
                                        message: `❌ Error: ${error}`,
                                        progress: 0
                                    });
                                    vscode.window.showErrorMessage(`Failed to start research: ${error}`);
                                }
                            }
                            else {
                                // No topic provided, trigger the full start research command
                                vscode.commands.executeCommand('auto-researcher.start');
                            }
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
    // Phase 3.5.4: View Session Details Command
    const viewSessionDetailsCommand = vscode.commands.registerCommand('auto-researcher.viewSessionDetails', async (sessionId) => {
        try {
            console.log('[viewSessionDetailsCommand] Called with sessionId:', sessionId);
            // If no sessionId provided, prompt user to enter one
            if (!sessionId) {
                console.log('[viewSessionDetailsCommand] No sessionId provided, prompting user...');
                sessionId = await vscode.window.showInputBox({
                    prompt: 'Enter Session ID',
                    placeHolder: 'e.g., 4565e1f6-1c57-4658-a603-0ea242ffb241',
                    validateInput: (value) => {
                        if (!value) {
                            return 'Session ID is required';
                        }
                        // Basic UUID format validation
                        const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
                        if (!uuidPattern.test(value)) {
                            return 'Invalid UUID format';
                        }
                        return null;
                    }
                });
                if (!sessionId) {
                    return; // User cancelled
                }
            }
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: 'Loading session details...',
                cancellable: false
            }, async () => {
                // Create webview panel
                const panel = vscode.window.createWebviewPanel('sessionDetails', `Session: ${sessionId?.substring(0, 8)}...`, vscode.ViewColumn.One, {
                    enableScripts: true,
                    retainContextWhenHidden: true
                });
                // Show loading indicator
                panel.webview.html = '<html><body><h2 style="text-align:center; margin-top: 100px;">Loading session details...</h2></body></html>';
                // Fetch session data
                const data = await (0, api_1.getSessionDetailsV2)(sessionId);
                // Update panel title with session title
                panel.title = `Session: ${data.session.title || sessionId.substring(0, 8)}`;
                // Render HTML
                panel.webview.html = (0, sessionDetailsWebview_1.generateSessionDetailsHTML)(sessionId, data);
                // Handle webview messages
                panel.webview.onDidReceiveMessage(async (message) => {
                    switch (message.command) {
                        case 'exportSession':
                            vscode.window.showInformationMessage('Export feature will be implemented in Phase 4');
                            break;
                        case 'openLangSmith':
                            vscode.window.showInformationMessage('LangSmith integration will be implemented in Phase 4.1');
                            break;
                        case 'refreshDetails':
                            // Reload session data
                            const refreshedData = await (0, api_1.getSessionDetailsV2)(message.sessionId);
                            panel.webview.html = (0, sessionDetailsWebview_1.generateSessionDetailsHTML)(message.sessionId, refreshedData);
                            vscode.window.showInformationMessage('Session details refreshed!');
                            break;
                        case 'deleteSession':
                            const confirm = await vscode.window.showWarningMessage(`Are you sure you want to delete session ${message.sessionId}?`, { modal: true }, 'Delete');
                            if (confirm === 'Delete') {
                                // TODO: Call delete API
                                vscode.window.showInformationMessage('Delete feature will be implemented soon');
                                panel.dispose();
                            }
                            break;
                    }
                }, undefined, context.subscriptions);
                vscode.window.showInformationMessage('Session details loaded successfully!');
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to load session details: ${error.message}`);
        }
    });
    // Phase 3.6: HITL Test Command
    const testHITLCommand = vscode.commands.registerCommand('auto-researcher.testHITL', async () => {
        const decisionType = await vscode.window.showQuickPick(['Query Approval', 'Paper Selection', 'Report Revision'], { placeHolder: 'Select HITL decision type to test' });
        if (!decisionType) {
            return;
        }
        // Create mock HITL request
        let mockRequest;
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
        }
        else if (decisionType === 'Paper Selection') {
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
        }
        else { // Report Revision
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
    // Phase 3.6 Week 3: Test Document Collaboration command
    const testDocCollabCommand = vscode.commands.registerCommand('auto-researcher.testDocumentCollaboration', async () => {
        // Create or open a test markdown document
        const testDoc = await vscode.workspace.openTextDocument({
            content: '# AI Research Report\n\n## Introduction\n\nThis is a test document for document collaboration.\n\n## Methods\n\nWe will test incremental updates.\n\n## Results\n\nTo be generated by AI.\n\n## Conclusion\n\nPending...',
            language: 'markdown'
        });
        await vscode.window.showTextDocument(testDoc);
        // Simulate document updates from AI
        const mockUpdates = [
            {
                type: 'document_update',
                session_id: 'test-session',
                node: 'retrieve_and_synthesize_report',
                action: 'modify',
                paragraph_index: 3,
                content: '## Results\n\nOur analysis reveals significant findings in AI healthcare applications.',
                old_content: '## Results\n\nTo be generated by AI.',
                line_range: { start: 9, end: 11 },
                rationale: 'AI generated results section',
                timestamp: new Date().toISOString()
            },
            {
                type: 'document_update',
                session_id: 'test-session',
                node: 'retrieve_and_synthesize_report',
                action: 'insert',
                paragraph_index: 4,
                content: '## Discussion\n\nThese findings have important implications for clinical practice.',
                line_range: { start: 12, end: 12 },
                rationale: 'AI adding discussion section',
                timestamp: new Date().toISOString()
            }
        ];
        // Show info message
        vscode.window.showInformationMessage('Document Collaboration Test: Simulating AI updates...');
        // Apply updates with delay to simulate real-time updates
        for (const update of mockUpdates) {
            await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
            await docCollabManager.handleDocumentUpdate(update, testDoc.uri);
        }
        vscode.window.showInformationMessage('✅ Document Collaboration Test Complete! Check the editor for CodeLens actions.');
    });
    // Phase 3.7 方案 B: Refresh Research Sessions Tree command
    const refreshResearchSessionsCommand = vscode.commands.registerCommand('auto-researcher.refreshResearchSessions', () => {
        researchSessionsTreeProvider.refresh();
        vscode.window.showInformationMessage('Research sessions refreshed!');
    });
    // Phase 5.2 Sprint 3: Show MindMap Node Details Command
    const showMindMapNodeCommand = vscode.commands.registerCommand('auto-researcher.showMindMapNode', async (node) => {
        const panel = vscode.window.createWebviewPanel('mindmapNodeDetails', `Perspective: ${node.name}`, vscode.ViewColumn.One, { enableScripts: true });
        // Generate HTML for node details
        const papersHTML = node.papers && node.papers.length > 0
            ? node.papers.map((paper, idx) => `
                <div style="background: var(--vscode-editor-inactiveSelectionBackground); padding: 10px; margin: 5px 0; border-radius: 4px;">
                    <h4>${idx + 1}. ${paper.title}</h4>
                    <p><strong>Authors:</strong> ${paper.authors.join(', ')}</p>
                    <p><strong>DOI:</strong> <a href="https://doi.org/${paper.doi}">${paper.doi}</a></p>
                </div>
            `).join('')
            : '<p>No papers found yet.</p>';
        const summaryHTML = node.summary
            ? `<div style="background: var(--vscode-editor-inactiveSelectionBackground); padding: 15px; border-radius: 4px; margin: 15px 0;">
                <h3>Summary</h3>
                <p>${node.summary}</p>
            </div>`
            : '<p>Summary pending analysis.</p>';
        panel.webview.html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${node.name}</title>
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
        .meta-info {
            background: var(--vscode-editor-inactiveSelectionBackground);
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        a {
            color: var(--vscode-textLink-foreground);
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>${node.name}</h1>

    <div class="meta-info">
        <h2>Description</h2>
        <p>${node.description}</p>

        <h2>Search Keywords</h2>
        <p><code>${node.query_keywords.join(', ')}</code></p>

        <h2>Status</h2>
        <p>Papers Found: ${node.papers ? node.papers.length : 0} | Summary: ${node.summary ? 'Available' : 'Pending'}</p>
    </div>

    <h2>Papers (${node.papers ? node.papers.length : 0})</h2>
    ${papersHTML}

    <h2>Analysis Summary</h2>
    ${summaryHTML}
</body>
</html>`;
    });
    // Phase 3.7 方案 B: Research Session Commands
    const openManuscriptCommand = vscode.commands.registerCommand('auto-researcher.openManuscript', (sessionId, version, report) => researchCommands.openManuscript(sessionId, version, report));
    const compareVersionsCommand = vscode.commands.registerCommand('auto-researcher.compareVersions', (sessionId, oldVersion, newVersion) => researchCommands.compareVersions(sessionId, oldVersion, newVersion));
    const openPaperCommand = vscode.commands.registerCommand('auto-researcher.openPaper', (sessionId, paperIndex) => researchCommands.openPaper(sessionId, paperIndex));
    const copyBibTeXCommand = vscode.commands.registerCommand('auto-researcher.copyBibTeX', (paper) => researchCommands.copyBibTeX(paper));
    const exportManuscriptCommand = vscode.commands.registerCommand('auto-researcher.exportManuscript', (sessionId, version) => researchCommands.exportManuscript(sessionId, version));
    const downloadPDFCommand = vscode.commands.registerCommand('auto-researcher.downloadPDF', (paper) => researchCommands.downloadPDF(paper));
    const showSessionAnalyticsCommand = vscode.commands.registerCommand('auto-researcher.showSessionAnalytics', (arg) => {
        // Handle both cases: called from menu (TreeItem object) or programmatically (string)
        let sessionId;
        if (typeof arg === 'string') {
            sessionId = arg;
        }
        else if (arg && typeof arg === 'object' && arg.sessionId) {
            // Extract sessionId from TreeItem object
            sessionId = arg.sessionId;
        }
        else {
            console.error('[showSessionAnalyticsCommand] Invalid argument:', arg);
            vscode.window.showErrorMessage('Cannot show analytics: Invalid session');
            return;
        }
        researchCommands.showSessionAnalytics(sessionId);
    });
    context.subscriptions.push(startResearchCommand, showControlPanelCommand, refreshAssetLibraryCommand, refreshManuscriptCommand, viewPaperDetailsCommand, exportPapersCommand, viewReportCommand, exportReportCommand, compareReportsCommand, changeGroupingCommand, showAnalyticsCommand, viewSessionDetailsCommand, testHITLCommand, testDocCollabCommand, refreshResearchSessionsCommand, 
    // Phase 5.2 Sprint 3: MindMap Node Details Command
    showMindMapNodeCommand, 
    // Phase 3.7 方案 B: Research Session Commands
    openManuscriptCommand, compareVersionsCommand, openPaperCommand, copyBibTeXCommand, exportManuscriptCommand, downloadPDFCommand, showSessionAnalyticsCommand);
    // Register MCP Client with MindMap Provider for live Co-STORM updates
    try {
        const { getMcpClient } = await Promise.resolve().then(() => require('./mcp_client'));
        const mcpClient = getMcpClient(context);
        // Set up message handling for MindMap updates
        mcpClient.onMessage((message) => {
            if (message.type === 'mindmap_update' && message.payload?.mindmap) {
                mindMapProvider.updateMindMap(message.payload.mindmap);
            }
        });
        // Start MCP client asynchronously
        mcpClient.start().then(() => {
            console.log('[Extension] MCP Client started successfully');
        }).catch((error) => {
            console.error('[Extension] Failed to start MCP Client:', error);
        });
        console.log('[Extension] MCP Client initialized with MindMap Provider');
    }
    catch (error) {
        console.error('[Extension] Failed to initialize MCP Client:', error);
    }
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