/**
 * Phase 3.7 方案 B: Research Sessions Tree Provider
 * 
 * Tree Data Provider for Research Sessions
 */

import * as vscode from 'vscode';
import { getSessionsList, getSessionDetailsV2 } from './api';
import {
    BaseTreeItem,
    SessionTreeItem,
    ManuscriptGroupTreeItem,
    ManuscriptVersionTreeItem,
    PapersGroupTreeItem,
    PaperTreeItem,
    AnalyticsTreeItem,
    EmptyStateTreeItem,
    SessionData,
    ReportData
} from './treeItems';

export class ResearchSessionsTreeProvider implements vscode.TreeDataProvider<BaseTreeItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<BaseTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    private sessionsCache: Map<string, any> = new Map();

    /**
     * Refresh the entire tree
     */
    refresh(): void {
        this.sessionsCache.clear();
        this._onDidChangeTreeData.fire();
    }

    /**
     * Refresh a specific item
     */
    refreshItem(item?: BaseTreeItem): void {
        this._onDidChangeTreeData.fire(item);
    }

    /**
     * Get tree item representation
     */
    getTreeItem(element: BaseTreeItem): vscode.TreeItem {
        return element;
    }

    /**
     * Get children of an element
     */
    async getChildren(element?: BaseTreeItem): Promise<BaseTreeItem[]> {
        try {
            if (!element) {
                // Root level: Return sessions
                return await this.getSessions();
            }

            if (element.contextValue === 'session') {
                // Session level: Return manuscripts, papers, analytics
                const sessionItem = element as SessionTreeItem;
                return await this.getSessionChildren(sessionItem.sessionId);
            }

            if (element.contextValue === 'manuscript-group') {
                // Manuscript group: Return manuscript versions
                const groupItem = element as ManuscriptGroupTreeItem;
                return await this.getManuscripts(groupItem.sessionId);
            }

            if (element.contextValue === 'papers-group') {
                // Papers group: Return paper list
                const groupItem = element as PapersGroupTreeItem;
                return await this.getPapers(groupItem.sessionId);
            }

            return [];
        } catch (error) {
            console.error('Failed to get tree children:', error);
            vscode.window.showErrorMessage(`Failed to load tree data: ${error}`);
            return [];
        }
    }

    /**
     * Get sessions list (root level)
     */
    private async getSessions(): Promise<BaseTreeItem[]> {
        try {
            const response = await getSessionsList({ limit: 100, offset: 0 });

            if (!response.sessions || response.sessions.length === 0) {
                return [new EmptyStateTreeItem('No research sessions yet')];
            }

            return response.sessions.map(apiSession => {
                const sessionData: SessionData = {
                    id: apiSession.session_id,
                    thread_id: apiSession.thread_id,
                    title: apiSession.title,
                    research_topic: apiSession.research_topic,
                    created_at: apiSession.created_at,
                    updated_at: apiSession.completed_at || apiSession.created_at,
                    status: this.mapStatus(apiSession.status),
                    paper_count: apiSession.papers_count || 0,
                    report_count: 0 // Will be fetched from details
                };

                return new SessionTreeItem(sessionData);
            });
        } catch (error) {
            console.error('Failed to load sessions:', error);
            vscode.window.showErrorMessage(`Failed to load research sessions: ${error}`);
            return [new EmptyStateTreeItem('Failed to load sessions')];
        }
    }

    /**
     * Get session children (manuscripts, papers, analytics)
     */
    private async getSessionChildren(sessionId: string): Promise<BaseTreeItem[]> {
        try {
            // Check cache
            if (!this.sessionsCache.has(sessionId)) {
                const details = await getSessionDetailsV2(sessionId);
                this.sessionsCache.set(sessionId, details);
            }

            const details = this.sessionsCache.get(sessionId);
            const children: BaseTreeItem[] = [];

            // Manuscripts group
            const reportCount = details.reports?.length || 0;
            children.push(new ManuscriptGroupTreeItem(sessionId, reportCount));

            // Papers group
            const paperCount = details.papers?.length || 0;
            children.push(new PapersGroupTreeItem(sessionId, paperCount));

            // Analytics
            children.push(new AnalyticsTreeItem(sessionId, details.stats));

            return children;
        } catch (error) {
            console.error(`Failed to load session children for ${sessionId}:`, error);
            vscode.window.showErrorMessage(`Failed to load session details: ${error}`);
            return [];
        }
    }

    /**
     * Get manuscript versions
     */
    private async getManuscripts(sessionId: string): Promise<BaseTreeItem[]> {
        try {
            const details = this.sessionsCache.get(sessionId) || await getSessionDetailsV2(sessionId);
            
            if (!details.reports || details.reports.length === 0) {
                return [];
            }

            // Sort reports by version descending (latest first)
            const sortedReports = [...details.reports].sort((a, b) => {
                const versionA = this.extractVersion(a);
                const versionB = this.extractVersion(b);
                return versionB - versionA;
            });

            const latestVersion = this.extractVersion(sortedReports[0]);

            return sortedReports.map(report => {
                const version = this.extractVersion(report);
                const isLatest = version === latestVersion;

                const reportData: ReportData = {
                    id: report.id,
                    session_id: sessionId,
                    title: report.title || details.session.research_topic,
                    content: report.content,
                    version: version,
                    created_at: report.created_at
                };

                return new ManuscriptVersionTreeItem(sessionId, reportData, isLatest);
            });
        } catch (error) {
            console.error(`Failed to load manuscripts for ${sessionId}:`, error);
            return [];
        }
    }

    /**
     * Get papers list
     */
    private async getPapers(sessionId: string): Promise<BaseTreeItem[]> {
        try {
            const details = this.sessionsCache.get(sessionId) || await getSessionDetailsV2(sessionId);
            
            if (!details.papers || details.papers.length === 0) {
                return [];
            }

            return details.papers.map((paper: any, index: number) => {
                return new PaperTreeItem(sessionId, paper, index + 1);
            });
        } catch (error) {
            console.error(`Failed to load papers for ${sessionId}:`, error);
            return [];
        }
    }

    /**
     * Extract version number from report
     */
    private extractVersion(report: any): number {
        // First, try to use the version field directly
        if (typeof report.version === 'number') {
            return report.version;
        }
        
        // Try to extract version from title (e.g., "v3", "version 3")
        const titleMatch = report.title?.match(/v(\d+)|version\s+(\d+)/i);
        if (titleMatch) {
            return parseInt(titleMatch[1] || titleMatch[2]);
        }

        // Fallback: use report ID or created_at timestamp
        // For now, assume reports are returned in chronological order
        return report.id ? parseInt(report.id.slice(-4), 16) % 100 : 1;
    }

    /**
     * Map API status to UI status
     */
    private mapStatus(status: string): SessionData['status'] {
        const statusMap: Record<string, SessionData['status']> = {
            'completed': 'completed',
            'in_progress': 'in_progress',
            'active': 'active',
            'running': 'in_progress',
            'paused': 'paused',
            'archived': 'archived',
            'failed': 'failed',
            'error': 'failed'
        };
        return statusMap[status.toLowerCase()] || 'in_progress';
    }

    /**
     * Clear cache for a specific session
     */
    clearSessionCache(sessionId: string): void {
        this.sessionsCache.delete(sessionId);
    }

    /**
     * Clear all cache
     */
    clearAllCache(): void {
        this.sessionsCache.clear();
    }
}
