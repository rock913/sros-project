"use strict";
/**
 * Phase 3.7 方案 B: Research Sessions Tree Provider
 *
 * Tree Data Provider for Research Sessions
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResearchSessionsTreeProvider = void 0;
const vscode = require("vscode");
const api_1 = require("./api");
const treeItems_1 = require("./treeItems");
class ResearchSessionsTreeProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.sessionsCache = new Map();
    }
    /**
     * Refresh the entire tree
     */
    refresh() {
        this.sessionsCache.clear();
        this._onDidChangeTreeData.fire();
    }
    /**
     * Refresh a specific item
     */
    refreshItem(item) {
        this._onDidChangeTreeData.fire(item);
    }
    /**
     * Get tree item representation
     */
    getTreeItem(element) {
        return element;
    }
    /**
     * Get children of an element
     */
    async getChildren(element) {
        try {
            if (!element) {
                // Root level: Return sessions
                return await this.getSessions();
            }
            if (element.contextValue === 'session') {
                // Session level: Return manuscripts, papers, analytics
                const sessionItem = element;
                return await this.getSessionChildren(sessionItem.sessionId);
            }
            if (element.contextValue === 'manuscript-group') {
                // Manuscript group: Return manuscript versions
                const groupItem = element;
                return await this.getManuscripts(groupItem.sessionId);
            }
            if (element.contextValue === 'papers-group') {
                // Papers group: Return paper list
                const groupItem = element;
                return await this.getPapers(groupItem.sessionId);
            }
            return [];
        }
        catch (error) {
            console.error('Failed to get tree children:', error);
            vscode.window.showErrorMessage(`Failed to load tree data: ${error}`);
            return [];
        }
    }
    /**
     * Get sessions list (root level)
     */
    async getSessions() {
        try {
            const response = await (0, api_1.getSessionsList)({ limit: 100, offset: 0 });
            if (!response.sessions || response.sessions.length === 0) {
                return [new treeItems_1.EmptyStateTreeItem('No research sessions yet')];
            }
            return response.sessions.map(apiSession => {
                const sessionData = {
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
                return new treeItems_1.SessionTreeItem(sessionData);
            });
        }
        catch (error) {
            console.error('Failed to load sessions:', error);
            vscode.window.showErrorMessage(`Failed to load research sessions: ${error}`);
            return [new treeItems_1.EmptyStateTreeItem('Failed to load sessions')];
        }
    }
    /**
     * Get session children (manuscripts, papers, analytics)
     */
    async getSessionChildren(sessionId) {
        try {
            // Check cache
            if (!this.sessionsCache.has(sessionId)) {
                const details = await (0, api_1.getSessionDetailsV2)(sessionId);
                this.sessionsCache.set(sessionId, details);
            }
            const details = this.sessionsCache.get(sessionId);
            const children = [];
            // Manuscripts group
            const reportCount = details.reports?.length || 0;
            children.push(new treeItems_1.ManuscriptGroupTreeItem(sessionId, reportCount));
            // Papers group
            const paperCount = details.papers?.length || 0;
            children.push(new treeItems_1.PapersGroupTreeItem(sessionId, paperCount));
            // Analytics
            children.push(new treeItems_1.AnalyticsTreeItem(sessionId, details.stats));
            return children;
        }
        catch (error) {
            console.error(`Failed to load session children for ${sessionId}:`, error);
            vscode.window.showErrorMessage(`Failed to load session details: ${error}`);
            return [];
        }
    }
    /**
     * Get manuscript versions
     */
    async getManuscripts(sessionId) {
        try {
            const details = this.sessionsCache.get(sessionId) || await (0, api_1.getSessionDetailsV2)(sessionId);
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
                const reportData = {
                    id: report.id,
                    session_id: sessionId,
                    title: report.title || details.session.research_topic,
                    content: report.content,
                    version: version,
                    created_at: report.created_at
                };
                return new treeItems_1.ManuscriptVersionTreeItem(sessionId, reportData, isLatest);
            });
        }
        catch (error) {
            console.error(`Failed to load manuscripts for ${sessionId}:`, error);
            return [];
        }
    }
    /**
     * Get papers list
     */
    async getPapers(sessionId) {
        try {
            const details = this.sessionsCache.get(sessionId) || await (0, api_1.getSessionDetailsV2)(sessionId);
            if (!details.papers || details.papers.length === 0) {
                return [];
            }
            return details.papers.map((paper, index) => {
                return new treeItems_1.PaperTreeItem(sessionId, paper, index + 1);
            });
        }
        catch (error) {
            console.error(`Failed to load papers for ${sessionId}:`, error);
            return [];
        }
    }
    /**
     * Extract version number from report
     */
    extractVersion(report) {
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
    mapStatus(status) {
        const statusMap = {
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
    clearSessionCache(sessionId) {
        this.sessionsCache.delete(sessionId);
    }
    /**
     * Clear all cache
     */
    clearAllCache() {
        this.sessionsCache.clear();
    }
}
exports.ResearchSessionsTreeProvider = ResearchSessionsTreeProvider;
//# sourceMappingURL=ResearchSessionsTreeProvider.js.map