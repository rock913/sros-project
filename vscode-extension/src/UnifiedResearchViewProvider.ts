/**
 * Phase 3.7: Unified Research View Provider
 * WebviewViewProvider for the master-detail research sessions view
 * Now uses React-based Collaboration UI instead of HTML strings
 */

import * as vscode from 'vscode';
import { getSessionsList, getSessionDetailsV2 } from './api';

export class UnifiedResearchViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'auto-researcher.researchSessionsView';

    private _view?: vscode.WebviewView;
    // @ts-ignore - Will be removed in React version
    private _sessions: any[] = []; // TODO: Remove if not needed in React version
    private _selectedSessionId: string | null = null;
    private _sessionDetails: any | null = null;

    constructor(
        private readonly _extensionContext: vscode.ExtensionContext,
    ) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        _context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionContext.extensionUri]
        };

        this._updateWebview();

        webviewView.webview.onDidReceiveMessage(
            async (message) => {
                await this._handleMessage(message);
            },
            undefined,
            this._extensionContext.subscriptions
        );

        this._loadSessions();
    }

    public refresh() {
        this._loadSessions();
    }

    private async _loadSessions() {
        try {
            const response = await getSessionsList({ limit: 50, offset: 0 });
            
            this._sessions = response.sessions.map(apiSession => ({
                id: apiSession.session_id,
                thread_id: apiSession.thread_id,
                title: apiSession.title || apiSession.research_topic,
                research_topic: apiSession.research_topic,
                created_at: apiSession.created_at,
                updated_at: apiSession.completed_at || apiSession.created_at,
                status: this._mapStatus(apiSession.status),
                paper_count: apiSession.papers_count || 0,
                report_count: 0, // Not available in SessionSummary
                tags: apiSession.tags || [],
                notes: undefined
            }));

            this._updateWebview();
        } catch (error) {
            console.error('Failed to load sessions:', error);
            vscode.window.showErrorMessage(`Failed to load research sessions: ${error}`);
        }
    }

    private async _loadSessionDetails(sessionId: string) {
        try {
            const details = await getSessionDetailsV2(sessionId);
            
            this._sessionDetails = {
                session: {
                    id: details.session.id,
                    thread_id: details.session.thread_id,
                    title: details.session.title || details.session.research_topic,
                    research_topic: details.session.research_topic,
                    created_at: details.session.created_at,
                    updated_at: details.session.updated_at,
                    status: this._mapStatus(details.session.status),
                    paper_count: details.stats.total_papers,
                    report_count: details.stats.total_reports,
                    tags: [],
                    notes: details.session.notes
                },
                manuscript: details.reports && details.reports.length > 0 ? {
                    content: details.reports[0].content,
                    title: details.reports[0].title
                } : undefined,
                papers: details.papers.map((paper: any) => ({
                    id: paper.id,
                    paper_id: paper.paper_id,
                    title: paper.title,
                    authors: paper.authors || [],
                    abstract: paper.abstract || '',
                    year: paper.year,
                    publication: paper.publication,
                    doi: paper.doi,
                    url: paper.url,
                    arxiv_id: paper.arxiv_id,
                    pdf_url: paper.pdf_url,
                    citation_count: paper.citation_count,
                    added_at: paper.added_at
                })),
                events: details.events,
                stats: details.stats
            };

            this._updateWebview();
        } catch (error) {
            console.error('Failed to load session details:', error);
            vscode.window.showErrorMessage(`Failed to load session details: ${error}`);
        }
    }

    private _mapStatus(status: string): 'completed' | 'in_progress' | 'paused' | 'failed' {
        const statusMap: { [key: string]: 'completed' | 'in_progress' | 'paused' | 'failed' } = {
            'completed': 'completed',
            'in_progress': 'in_progress',
            'active': 'in_progress',
            'running': 'in_progress',
            'paused': 'paused',
            'archived': 'paused',
            'failed': 'failed',
            'error': 'failed'
        };
        return statusMap[status.toLowerCase()] || 'in_progress';
    }

    private async _handleMessage(message: any) {
        switch (message.command) {
            case 'selectSession':
                await this._selectSession(message.sessionId);
                break;
            case 'createNewSession':
                await this._createNewSession();
                break;
            case 'loadMoreSessions':
                await this._loadMoreSessions();
                break;
            case 'exportManuscript':
                await this._exportManuscript(message.format);
                break;
            case 'openPDF':
                await this._openPDF(message.paperId);
                break;
            case 'openURL':
                await this._openURL(message.url);
                break;
            case 'copyBibTeX':
                await this._copyBibTeX(message.paperId);
                break;
        }
    }

    private async _selectSession(sessionId: string) {
        this._selectedSessionId = sessionId;
        await this._loadSessionDetails(sessionId);
    }

    private async _createNewSession() {
        await vscode.commands.executeCommand('auto-researcher.start');
    }

    private async _loadMoreSessions() {
        vscode.window.showInformationMessage('Load more sessions - coming soon!');
    }

    private async _exportManuscript(format: 'md' | 'pdf') {
        if (!this._sessionDetails?.manuscript) {
            vscode.window.showWarningMessage('No manuscript available to export');
            return;
        }

        if (format === 'md') {
            const uri = await vscode.window.showSaveDialog({
                defaultUri: vscode.Uri.file(`research-${this._selectedSessionId}.md`),
                filters: { 'Markdown': ['md'] }
            });

            if (uri) {
                const content = this._sessionDetails.manuscript.content;
                await vscode.workspace.fs.writeFile(uri, Buffer.from(content, 'utf8'));
                vscode.window.showInformationMessage(`Manuscript exported to ${uri.fsPath}`);
            }
        } else {
            vscode.window.showInformationMessage('PDF export - coming soon!');
        }
    }

    private async _openPDF(paperId: string) {
        const paper = this._sessionDetails?.papers.find((p: any) => p.id === paperId);
        if (!paper?.pdf_url) {
            vscode.window.showWarningMessage('PDF URL not available for this paper');
            return;
        }
        await vscode.env.openExternal(vscode.Uri.parse(paper.pdf_url));
    }

    private async _openURL(url: string) {
        await vscode.env.openExternal(vscode.Uri.parse(url));
    }

    private async _copyBibTeX(paperId: string) {
        const paper = this._sessionDetails?.papers.find((p: any) => p.id === paperId);
        if (!paper) {
            vscode.window.showWarningMessage('Paper not found');
            return;
        }

        const authors = paper.authors.join(' and ');
        const year = paper.year || new Date().getFullYear();
        const key = `${paper.authors[0]?.split(',')[0]?.toLowerCase() || 'unknown'}${year}`;

        const bibtex = `@article{${key},
  title={${paper.title}},
  author={${authors}},
  year={${year}}${paper.publication ? `,\n  journal={${paper.publication}}` : ''}${paper.doi ? `,\n  doi={${paper.doi}}` : ''}${paper.url ? `,\n  url={${paper.url}}` : ''}
}`;

        await vscode.env.clipboard.writeText(bibtex);
        vscode.window.showInformationMessage('BibTeX citation copied to clipboard!');
    }

    private _updateWebview() {
        if (this._view) {
            // Get the URI for the built webview assets
            const extensionUri = this._extensionContext.extensionUri;
            const webviewUri = vscode.Uri.joinPath(extensionUri, 'out', 'webview');

            // Convert URIs to webview URIs
            const scriptUri = this._view.webview.asWebviewUri(vscode.Uri.joinPath(webviewUri, 'webview.js'));
            const styleUri = this._view.webview.asWebviewUri(vscode.Uri.joinPath(webviewUri, 'style.css'));

            // Create the HTML that loads the React application
            this._view.webview.html = `<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Auto Researcher Webview</title>
                    <link rel="stylesheet" href="${styleUri}">
                </head>
                <body>
                    <div id="root"></div>
                    <script type="module" src="${scriptUri}"></script>
                </body>
                </html>`;
        }
    }
}
