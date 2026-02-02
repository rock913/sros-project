import * as vscode from 'vscode';

export interface MindMapNode {
    id: string;
    name: string;
    description: string;
    query_keywords: string[];
    papers?: Array<{
        doi: string;
        title: string;
        authors: string[];
    }>;
    summary?: string;
}

export interface MindMap {
    root_topic: string;
    nodes: MindMapNode[];
}

export class MindMapTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly node?: MindMapNode,
        public readonly mindmap?: MindMap
    ) {
        super(label, collapsibleState);

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
        } else if (mindmap) {
            // Root mindmap
            this.tooltip = `Research topic: ${mindmap.root_topic}`;
            this.description = `${mindmap.nodes.length} perspectives`;
            this.iconPath = new vscode.ThemeIcon('mind-map');
        }
    }

    private createTooltip(node: MindMapNode): string {
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
        } else {
            tooltip += `⏳ Summary: Pending analysis`;
        }

        return tooltip;
    }
}

export class MindMapProvider implements vscode.TreeDataProvider<MindMapTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<MindMapTreeItem | undefined | null | void> =
        new vscode.EventEmitter<MindMapTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<MindMapTreeItem | undefined | null | void> =
        this._onDidChangeTreeData.event;

    private currentMindMap: MindMap | null = null;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    updateMindMap(mindMapJson: any): void {
        try {
            // Parse the MindMap from JSON
            const mindmap: MindMap = {
                root_topic: mindMapJson.root_topic,
                nodes: mindMapJson.nodes.map((node: any) => ({
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
            vscode.window.showInformationMessage(
                `🧠 MindMap updated: ${completeNodes}/${mindmap.nodes.length} perspectives analyzed`
            );

        } catch (error) {
            console.error('[MindMapProvider] Failed to parse mindmap update:', error);
            vscode.window.showErrorMessage('Failed to update mindmap');
        }
    }

    getTreeItem(element: MindMapTreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: MindMapTreeItem): MindMapTreeItem[] {
        // Root level: show mindmap if available
        if (!element) {
            if (this.currentMindMap) {
                return [new MindMapTreeItem(
                    `🔬 ${this.currentMindMap.root_topic}`,
                    vscode.TreeItemCollapsibleState.Expanded,
                    undefined,
                    this.currentMindMap
                )];
            } else {
                return [new MindMapTreeItem(
                    'No mindmap available',
                    vscode.TreeItemCollapsibleState.None
                )];
            }
        }

        // Mindmap root: show perspective nodes
        if (element.mindmap) {
            return element.mindmap.nodes.map(node => new MindMapTreeItem(
                `🎯 ${node.name}`,
                vscode.TreeItemCollapsibleState.None,
                node
            ));
        }

        return [];
    }
}