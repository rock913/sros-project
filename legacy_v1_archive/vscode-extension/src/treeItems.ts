/**
 * Phase 3.7 方案 B: Tree View Items
 * 
 * TreeItem 类定义用于 Research Sessions Tree View
 */

import * as vscode from 'vscode';

export interface SessionData {
    id: string;
    thread_id: string;
    title: string;
    research_topic: string;
    created_at: string;
    updated_at: string;
    status: 'completed' | 'in_progress' | 'paused' | 'failed' | 'active' | 'archived';
    paper_count: number;
    report_count: number;
}

export interface ReportData {
    id: string;
    session_id: string;
    title: string;
    content: string;
    version: number;
    created_at: string;
}

export interface PaperData {
    id: string;
    paper_id: string;
    title: string;
    authors: string[];
    abstract: string;
    year?: number;
    publication?: string;
    doi?: string;
    url?: string;
    arxiv_id?: string;
    pdf_url?: string;
    citation_count?: number;
}

// Co-STORM MindMap types (Phase 5.3: Unified Frontend UI)
export interface MindMapNode {
    id: string;
    name: string;
    description: string;
    query_keywords: string[];
    papers?: Array<{
        doi?: string;
        title: string;
        authors: string[];
    }>;
    summary?: string;
}

export interface MindMap {
    root_topic: string;
    nodes: MindMapNode[];
}

/**
 * Base class for all tree items
 */
export abstract class BaseTreeItem extends vscode.TreeItem {
    constructor(
        label: string,
        collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly itemType: string
    ) {
        super(label, collapsibleState);
        this.contextValue = itemType;
    }
}

/**
 * Session Tree Item - 研究会话节点
 */
export class SessionTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly sessionData: SessionData;

    constructor(session: SessionData) {
        const statusIcons: Record<string, string> = {
            'completed': '✅',
            'in_progress': '🔄',
            'active': '🔄',
            'failed': '❌',
            'paused': '⏸️',
            'archived': '📦'
        };

        super(
            session.research_topic,
            vscode.TreeItemCollapsibleState.Collapsed,
            'session'
        );

        this.sessionId = session.id;
        this.sessionData = session;

        // Status icon and description
        const statusIcon = statusIcons[session.status] || '📊';
        this.description = `${statusIcon} ${session.paper_count} papers`;

        // Tooltip with detailed info
        this.tooltip = new vscode.MarkdownString(
            `**${session.research_topic}**\n\n` +
            `- **Status**: ${session.status}\n` +
            `- **Papers**: ${session.paper_count}\n` +
            `- **Reports**: ${session.report_count}\n` +
            `- **Created**: ${new Date(session.created_at).toLocaleString()}\n` +
            `- **Session ID**: ${session.id}`
        );

        // Icon
        this.iconPath = new vscode.ThemeIcon('notebook');
    }
}

/**
 * Manuscript Group Tree Item - 手稿组节点
 */
export class ManuscriptGroupTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly reportCount: number;

    constructor(sessionId: string, reportCount: number) {
        super(
            `Manuscripts (${reportCount})`,
            reportCount > 0 
                ? vscode.TreeItemCollapsibleState.Expanded 
                : vscode.TreeItemCollapsibleState.None,
            'manuscript-group'
        );

        this.sessionId = sessionId;
        this.reportCount = reportCount;

        this.description = reportCount === 0 ? 'No versions yet' : undefined;
        this.iconPath = new vscode.ThemeIcon('file-directory');
        this.tooltip = `${reportCount} manuscript version(s)`;
    }
}

/**
 * Manuscript Version Tree Item - 手稿版本节点
 */
export class ManuscriptVersionTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly reportId: string;
    public readonly version: number;
    public readonly isLatest: boolean;
    public readonly reportData: ReportData;

    constructor(sessionId: string, report: ReportData, isLatest: boolean) {
        // Format date
        const date = new Date(report.created_at);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const label = `v${report.version}${isLatest ? ' (Latest)' : ''} - ${dateStr}`;
        
        super(
            label,
            vscode.TreeItemCollapsibleState.None,
            'manuscript-version'
        );

        this.sessionId = sessionId;
        this.reportId = report.id;
        this.version = report.version;
        this.isLatest = isLatest;
        this.reportData = report;

        // Word count
        const wordCount = report.content.split(/\s+/).length;
        this.description = `${wordCount} words`;

        // Tooltip
        this.tooltip = new vscode.MarkdownString(
            `**Manuscript v${report.version}**\n\n` +
            `- **Title**: ${report.title || 'Untitled'}\n` +
            `- **Words**: ${wordCount}\n` +
            `- **Created**: ${new Date(report.created_at).toLocaleString()}\n` +
            `- **Latest**: ${isLatest ? 'Yes' : 'No'}`
        );

        // Icon
        this.iconPath = new vscode.ThemeIcon(
            isLatest ? 'file-text' : 'file',
            isLatest ? new vscode.ThemeColor('charts.green') : undefined
        );

        // Click to open
        this.command = {
            command: 'auto-researcher.openManuscript',
            title: 'Open Manuscript',
            arguments: [sessionId, report.version, report]
        };
    }
}

/**
 * Papers Group Tree Item - 论文组节点
 */
export class PapersGroupTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly paperCount: number;

    constructor(sessionId: string, paperCount: number) {
        super(
            `Papers (${paperCount})`,
            paperCount > 0 
                ? vscode.TreeItemCollapsibleState.Collapsed 
                : vscode.TreeItemCollapsibleState.None,
            'papers-group'
        );

        this.sessionId = sessionId;
        this.paperCount = paperCount;

        this.description = paperCount === 0 ? 'No papers yet' : undefined;
        this.iconPath = new vscode.ThemeIcon('library');
        this.tooltip = `${paperCount} paper(s) collected`;
    }
}

/**
 * Paper Tree Item - 论文节点
 */
export class PaperTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly paperId: string;
    public readonly refNumber: number;
    public readonly paperData: PaperData;

    constructor(sessionId: string, paper: PaperData, refNumber: number) {
        // Use paper title directly (like Asset Library)
        const label = paper.title || `Paper ${refNumber}`;

        super(
            label,
            vscode.TreeItemCollapsibleState.None,
            'paper'
        );

        this.sessionId = sessionId;
        this.paperId = paper.id;
        this.refNumber = refNumber;
        this.paperData = paper;

        // Description: First author and year
        const firstAuthor = paper.authors[0]?.split(',')[0] || 'Unknown';
        this.description = `${firstAuthor} et al. (${paper.year || 'N/A'})`;

        // Tooltip with full info
        this.tooltip = new vscode.MarkdownString(
            `**${paper.title}**\n\n` +
            `- **Authors**: ${paper.authors.slice(0, 3).join(', ')}${paper.authors.length > 3 ? ' et al.' : ''}\n` +
            `- **Year**: ${paper.year || 'N/A'}\n` +
            `- **Publication**: ${paper.publication || 'N/A'}\n` +
            `- **DOI**: ${paper.doi || 'N/A'}\n` +
            `- **Citations**: ${paper.citation_count || 'N/A'}`
        );

        // Icon: document instead of PDF
        this.iconPath = new vscode.ThemeIcon('file-text');

        // Click to open paper details
        this.command = {
            command: 'auto-researcher.openPaper',
            title: 'Open Paper',
            arguments: [sessionId, refNumber - 1]  // refNumber is 1-based, convert to 0-based index
        };
    }
}

/**
 * Analytics Tree Item - 分析统计节点
 */
export class AnalyticsTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly stats: any;

    constructor(sessionId: string, stats: any) {
        super(
            'Session Analytics',
            vscode.TreeItemCollapsibleState.None,
            'session-analytics'
        );

        this.sessionId = sessionId;
        this.stats = stats;

        this.description = `${stats.total_events || 0} events`;
        this.iconPath = new vscode.ThemeIcon('graph');

        // Tooltip
        this.tooltip = new vscode.MarkdownString(
            `**Session Analytics**\n\n` +
            `- **Total Events**: ${stats.total_events || 0}\n` +
            `- **Total Papers**: ${stats.total_papers || 0}\n` +
            `- **Total Reports**: ${stats.total_reports || 0}`
        );

        // Click to show analytics (Phase 3.7 Fix: Only pass sessionId)
        this.command = {
            command: 'auto-researcher.showSessionAnalytics',
            title: 'Show Analytics',
            arguments: [sessionId]  // Fixed: Only pass sessionId, not stats
        };
    }
}

/**
 * Empty State Tree Item - 空状态节点
 */
export class EmptyStateTreeItem extends BaseTreeItem {
    constructor(message: string) {
        super(message, vscode.TreeItemCollapsibleState.None, 'empty-state');

        this.description = 'Click "+" to create';
        this.iconPath = new vscode.ThemeIcon('info');
        this.tooltip = 'No research sessions yet. Start a new research to begin.';
    }
}

// ========== Phase 5.3: Unified Frontend UI - Co-STORM Integration ==========

/**
 * Knowledge Graph Group Tree Item - 知识图谱组节点 (Co-STORM MindMap)
 */
export class KnowledgeGraphGroupTreeItem extends BaseTreeItem {
    public readonly sessionId: string;

    constructor(sessionId: string, mindmap?: MindMap) {
        const perspectivesCount = mindmap?.nodes?.length || 0;
        const completeCount = mindmap?.nodes?.filter(n => n.summary).length || 0;

        super(
            `Knowledge Graph${perspectivesCount > 0 ? ` (${completeCount}/${perspectivesCount})` : ''}`,
            perspectivesCount > 0
                ? vscode.TreeItemCollapsibleState.Collapsed
                : vscode.TreeItemCollapsibleState.None,
            'knowledge-graph-group'
        );

        this.sessionId = sessionId;

        if (perspectivesCount === 0) {
            this.description = 'No perspectives yet';
            this.iconPath = new vscode.ThemeIcon('mind-map', new vscode.ThemeColor('charts.gray'));
        } else {
            this.description = `${completeCount}/${perspectivesCount} perspectives`;
            this.iconPath = completeCount === perspectivesCount
                ? new vscode.ThemeIcon('mind-map', new vscode.ThemeColor('charts.green'))
                : new vscode.ThemeIcon('mind-map', new vscode.ThemeColor('charts.orange'));

            const topic = mindmap?.root_topic || 'Research Topic';
            this.tooltip = `Co-STORM Mind Map for "${topic}"\n${perspectivesCount} perspectives, ${completeCount} analyzed`;
        }
    }
}

/**
 * MindMap Perspective Tree Item - 思维导图视角节点
 */
export class MindMapPerspectiveTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly nodeId: string;
    public readonly mindMapNode: MindMapNode;

    constructor(sessionId: string, node: MindMapNode) {
        const paperCount = node.papers?.length || 0;
        const hasPapers = paperCount > 0;
        const isAnalyzed = !!node.summary;

        super(
            node.name,
            hasPapers ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None,
            'mindmap-perspective'
        );

        this.sessionId = sessionId;
        this.nodeId = node.id;
        this.mindMapNode = node;

        // Description: Analysis status and paper count
        const status = isAnalyzed ? '✅ Analyzed' : '⏳ Exploring';
        this.description = `${status} • ${paperCount} papers`;

        // Tooltip with details
        const tooltip = new vscode.MarkdownString();
        tooltip.appendMarkdown(`**🎯 ${node.name}**\n\n`);
        tooltip.appendMarkdown(`${node.description}\n\n`);

        if (node.query_keywords?.length > 0) {
            tooltip.appendMarkdown(`**Query Keywords:**\n`);
            node.query_keywords.forEach(keyword => {
                tooltip.appendMarkdown(`• ${keyword}\n`);
            });
            tooltip.appendMarkdown('\n');
        }

        if (node.summary) {
            const summaryPreview = node.summary.length > 200
                ? node.summary.substring(0, 200) + '...'
                : node.summary;
            tooltip.appendMarkdown(`**Analysis:**\n${summaryPreview}\n\n`);
        } else {
            tooltip.appendMarkdown(`*Analysis pending...*\n\n`);
        }

        if (node.papers && node.papers.length > 0) {
            tooltip.appendMarkdown(`**Papers Found:** ${node.papers.length}`);
        }

        this.tooltip = tooltip;

        // Icon based on analysis status
        this.iconPath = isAnalyzed
            ? new vscode.ThemeIcon('check-circle', new vscode.ThemeColor('charts.green'))
            : new vscode.ThemeIcon('clock', new vscode.ThemeColor('charts.blue'));

        // Command to show perspective details
        this.command = {
            command: 'auto-researcher.showMindMapPerspective',
            title: 'View Perspective Details',
            arguments: [sessionId, node]
        };
    }
}

/**
 * MindMap Paper Tree Item - 视角下的论文节点
 */
export class MindMapPaperTreeItem extends BaseTreeItem {
    public readonly sessionId: string;
    public readonly nodeId: string;
    public readonly mindMapPaper: {
        doi: string;
        title: string;
        authors: string[];
    };

    constructor(sessionId: string, nodeId: string, paper: any) {
        const label = paper.title || paper.doi || 'Unknown Paper';

        super(
            label,
            vscode.TreeItemCollapsibleState.None,
            'mindmap-paper'
        );

        this.sessionId = sessionId;
        this.nodeId = nodeId;
        this.mindMapPaper = paper;

        // Description: Authors and DOI
        const authors = paper.authors?.slice(0, 2).join(', ') || 'Unknown';
        const suffix = paper.authors?.length > 2 ? ' et al.' : '';
        this.description = `${authors}${suffix} • ${paper.doi ? 'DOI' : 'No DOI'}`;

        // Tooltip
        const tooltip = new vscode.MarkdownString();
        tooltip.appendMarkdown(`**📄 ${paper.title}**\n\n`);
        tooltip.appendMarkdown(`**Authors:** ${paper.authors?.join(', ') || 'Unknown'}\n`);
        if (paper.doi) {
            tooltip.appendMarkdown(`**DOI:** ${paper.doi}\n`);
        }

        this.tooltip = tooltip;

        // Icon
        this.iconPath = new vscode.ThemeIcon('file-text');

        // Command to open paper
        this.command = {
            command: 'auto-researcher.openMindMapPaper',
            title: 'Open MindMap Paper',
            arguments: [sessionId, nodeId, paper]
        };
    }
}
