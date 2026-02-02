"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MindMapProvider = exports.MindMapTreeItem = void 0;
const vscode = require("vscode");
class MindMapTreeItem extends vscode.TreeItem {
    constructor(label, collapsibleState, node, mindmap) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.node = node;
        this.mindmap = mindmap;
        if (node) {
            // Individual perspective node
            this.tooltip = this.createTooltip(node);
            this.description = node.papers ? `${node.papers.length} papers` : '0 papers';
            this.iconPath = new vscode.ThemeIcon(node.summary ? 'check' : 'clock');
            // Add command to show node details
            this.command = {
                command: 'auto-researcher.showMindMapNode',
                title: 'View Perspective Details',
                arguments: [node]
            };
        }
        else if (mindmap) {
            // Root mindmap
            this.tooltip = `Research topic: ${mindmap.root_topic}`;
            this.description = `${mindmap.nodes.length} perspectives`;
            this.iconPath = new vscode.ThemeIcon('mind-map');
        }
    }
    createTooltip(node) {
        let tooltip = `**${node.name}**\n\n`;
        tooltip += `${node.description}\n\n`;
        if (node.papers && node.papers.length > 0) {
            tooltip += `📚 Papers: ${node.papers.length}\n`;
            node.papers.slice(0, 3).forEach((paper, idx) => {
                tooltip += `  ${idx + 1}. ${paper.title}\n`;
            });
            if (node.papers.length > 3) {
                tooltip += `  ... and ${node.papers.length - 3} more\n`;
            }
            tooltip += '\n';
        }
        if (node.summary) {
            const summaryPreview = node.summary.length > 200
                ? node.summary.substring(0, 200) + '...'
                : node.summary;
            tooltip += `📝 Summary: ${summaryPreview}`;
        }
        else {
            tooltip += `⏳ Summary: Pending analysis`;
        }
        return tooltip;
    }
}
exports.MindMapTreeItem = MindMapTreeItem;
class MindMapProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.currentMindMap = null;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    updateMindMap(mindMapJson) {
        try {
            // Parse the MindMap from JSON
            const mindmap = {
                root_topic: mindMapJson.root_topic,
                nodes: mindMapJson.nodes.map((node) => ({
                    id: node.id,
                    name: node.name,
                    description: node.description,
                    query_keywords: node.query_keywords || [],
                    papers: node.papers || [],
                    summary: node.summary
                }))
            };
            this.currentMindMap = mindmap;
            console.log('[MindMapProvider] Updated mindmap:', mindmap);
            // Notify that tree data has changed
            this.refresh();
            // Show notification
            const completeNodes = mindmap.nodes.filter(n => n.summary).length;
            vscode.window.showInformationMessage(`🧠 MindMap updated: ${completeNodes}/${mindmap.nodes.length} perspectives analyzed`);
        }
        catch (error) {
            console.error('[MindMapProvider] Failed to parse mindmap update:', error);
            vscode.window.showErrorMessage('Failed to update mindmap');
        }
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        // Root level: show mindmap if available
        if (!element) {
            if (this.currentMindMap) {
                return [new MindMapTreeItem(`🔬 ${this.currentMindMap.root_topic}`, vscode.TreeItemCollapsibleState.Expanded, undefined, this.currentMindMap)];
            }
            else {
                return [new MindMapTreeItem('No mindmap available', vscode.TreeItemCollapsibleState.None)];
            }
        }
        // Mindmap root: show perspective nodes
        if (element.mindmap) {
            return element.mindmap.nodes.map(node => new MindMapTreeItem(`🎯 ${node.name}`, vscode.TreeItemCollapsibleState.None, node));
        }
        return [];
    }
}
exports.MindMapProvider = MindMapProvider;
//# sourceMappingURL=MindMapProvider.js.map