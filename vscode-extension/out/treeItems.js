"use strict";
/**
 * Phase 3.7 方案 B: Tree View Items
 *
 * TreeItem 类定义用于 Research Sessions Tree View
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmptyStateTreeItem = exports.AnalyticsTreeItem = exports.PaperTreeItem = exports.PapersGroupTreeItem = exports.ManuscriptVersionTreeItem = exports.ManuscriptGroupTreeItem = exports.SessionTreeItem = exports.BaseTreeItem = void 0;
const vscode = require("vscode");
/**
 * Base class for all tree items
 */
class BaseTreeItem extends vscode.TreeItem {
    constructor(label, collapsibleState, itemType) {
        super(label, collapsibleState);
        this.itemType = itemType;
        this.contextValue = itemType;
    }
}
exports.BaseTreeItem = BaseTreeItem;
/**
 * Session Tree Item - 研究会话节点
 */
class SessionTreeItem extends BaseTreeItem {
    constructor(session) {
        const statusIcons = {
            'completed': '✅',
            'in_progress': '🔄',
            'active': '🔄',
            'failed': '❌',
            'paused': '⏸️',
            'archived': '📦'
        };
        super(session.research_topic, vscode.TreeItemCollapsibleState.Collapsed, 'session');
        this.sessionId = session.id;
        this.sessionData = session;
        // Status icon and description
        const statusIcon = statusIcons[session.status] || '📊';
        this.description = `${statusIcon} ${session.paper_count} papers`;
        // Tooltip with detailed info
        this.tooltip = new vscode.MarkdownString(`**${session.research_topic}**\n\n` +
            `- **Status**: ${session.status}\n` +
            `- **Papers**: ${session.paper_count}\n` +
            `- **Reports**: ${session.report_count}\n` +
            `- **Created**: ${new Date(session.created_at).toLocaleString()}\n` +
            `- **Session ID**: ${session.id}`);
        // Icon
        this.iconPath = new vscode.ThemeIcon('notebook');
    }
}
exports.SessionTreeItem = SessionTreeItem;
/**
 * Manuscript Group Tree Item - 手稿组节点
 */
class ManuscriptGroupTreeItem extends BaseTreeItem {
    constructor(sessionId, reportCount) {
        super(`Manuscripts (${reportCount})`, reportCount > 0
            ? vscode.TreeItemCollapsibleState.Expanded
            : vscode.TreeItemCollapsibleState.None, 'manuscript-group');
        this.sessionId = sessionId;
        this.reportCount = reportCount;
        this.description = reportCount === 0 ? 'No versions yet' : undefined;
        this.iconPath = new vscode.ThemeIcon('file-directory');
        this.tooltip = `${reportCount} manuscript version(s)`;
    }
}
exports.ManuscriptGroupTreeItem = ManuscriptGroupTreeItem;
/**
 * Manuscript Version Tree Item - 手稿版本节点
 */
class ManuscriptVersionTreeItem extends BaseTreeItem {
    constructor(sessionId, report, isLatest) {
        // Format date
        const date = new Date(report.created_at);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const label = `v${report.version}${isLatest ? ' (Latest)' : ''} - ${dateStr}`;
        super(label, vscode.TreeItemCollapsibleState.None, 'manuscript-version');
        this.sessionId = sessionId;
        this.reportId = report.id;
        this.version = report.version;
        this.isLatest = isLatest;
        this.reportData = report;
        // Word count
        const wordCount = report.content.split(/\s+/).length;
        this.description = `${wordCount} words`;
        // Tooltip
        this.tooltip = new vscode.MarkdownString(`**Manuscript v${report.version}**\n\n` +
            `- **Title**: ${report.title || 'Untitled'}\n` +
            `- **Words**: ${wordCount}\n` +
            `- **Created**: ${new Date(report.created_at).toLocaleString()}\n` +
            `- **Latest**: ${isLatest ? 'Yes' : 'No'}`);
        // Icon
        this.iconPath = new vscode.ThemeIcon(isLatest ? 'file-text' : 'file', isLatest ? new vscode.ThemeColor('charts.green') : undefined);
        // Click to open
        this.command = {
            command: 'auto-researcher.openManuscript',
            title: 'Open Manuscript',
            arguments: [sessionId, report.version, report]
        };
    }
}
exports.ManuscriptVersionTreeItem = ManuscriptVersionTreeItem;
/**
 * Papers Group Tree Item - 论文组节点
 */
class PapersGroupTreeItem extends BaseTreeItem {
    constructor(sessionId, paperCount) {
        super(`Papers (${paperCount})`, paperCount > 0
            ? vscode.TreeItemCollapsibleState.Collapsed
            : vscode.TreeItemCollapsibleState.None, 'papers-group');
        this.sessionId = sessionId;
        this.paperCount = paperCount;
        this.description = paperCount === 0 ? 'No papers yet' : undefined;
        this.iconPath = new vscode.ThemeIcon('library');
        this.tooltip = `${paperCount} paper(s) collected`;
    }
}
exports.PapersGroupTreeItem = PapersGroupTreeItem;
/**
 * Paper Tree Item - 论文节点
 */
class PaperTreeItem extends BaseTreeItem {
    constructor(sessionId, paper, refNumber) {
        // Use paper title directly (like Asset Library)
        const label = paper.title || `Paper ${refNumber}`;
        super(label, vscode.TreeItemCollapsibleState.None, 'paper');
        this.sessionId = sessionId;
        this.paperId = paper.id;
        this.refNumber = refNumber;
        this.paperData = paper;
        // Description: First author and year
        const firstAuthor = paper.authors[0]?.split(',')[0] || 'Unknown';
        this.description = `${firstAuthor} et al. (${paper.year || 'N/A'})`;
        // Tooltip with full info
        this.tooltip = new vscode.MarkdownString(`**${paper.title}**\n\n` +
            `- **Authors**: ${paper.authors.slice(0, 3).join(', ')}${paper.authors.length > 3 ? ' et al.' : ''}\n` +
            `- **Year**: ${paper.year || 'N/A'}\n` +
            `- **Publication**: ${paper.publication || 'N/A'}\n` +
            `- **DOI**: ${paper.doi || 'N/A'}\n` +
            `- **Citations**: ${paper.citation_count || 'N/A'}`);
        // Icon: document instead of PDF
        this.iconPath = new vscode.ThemeIcon('file-text');
        // Click to open paper details
        this.command = {
            command: 'auto-researcher.openPaper',
            title: 'Open Paper',
            arguments: [sessionId, refNumber - 1] // refNumber is 1-based, convert to 0-based index
        };
    }
}
exports.PaperTreeItem = PaperTreeItem;
/**
 * Analytics Tree Item - 分析统计节点
 */
class AnalyticsTreeItem extends BaseTreeItem {
    constructor(sessionId, stats) {
        super('Session Analytics', vscode.TreeItemCollapsibleState.None, 'session-analytics');
        this.sessionId = sessionId;
        this.stats = stats;
        this.description = `${stats.total_events || 0} events`;
        this.iconPath = new vscode.ThemeIcon('graph');
        // Tooltip
        this.tooltip = new vscode.MarkdownString(`**Session Analytics**\n\n` +
            `- **Total Events**: ${stats.total_events || 0}\n` +
            `- **Total Papers**: ${stats.total_papers || 0}\n` +
            `- **Total Reports**: ${stats.total_reports || 0}`);
        // Click to show analytics (Phase 3.7 Fix: Only pass sessionId)
        this.command = {
            command: 'auto-researcher.showSessionAnalytics',
            title: 'Show Analytics',
            arguments: [sessionId] // Fixed: Only pass sessionId, not stats
        };
    }
}
exports.AnalyticsTreeItem = AnalyticsTreeItem;
/**
 * Empty State Tree Item - 空状态节点
 */
class EmptyStateTreeItem extends BaseTreeItem {
    constructor(message) {
        super(message, vscode.TreeItemCollapsibleState.None, 'empty-state');
        this.description = 'Click "+" to create';
        this.iconPath = new vscode.ThemeIcon('info');
        this.tooltip = 'No research sessions yet. Start a new research to begin.';
    }
}
exports.EmptyStateTreeItem = EmptyStateTreeItem;
//# sourceMappingURL=treeItems.js.map