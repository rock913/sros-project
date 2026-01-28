/**
 * DraftWatcher Provider - VS Code Context Bridge (The Nerve)
 *
 * Real-time draft content synchronization and editing integration
 * for the Agentic Editor system.
 */

import * as vscode from 'vscode';
import { McpClient } from '../mcp_client';


export class DraftWatcherProvider {
    private mcpClient: McpClient;
    private statusBarItem: vscode.StatusBarItem;
    private currentDebounceTimer: NodeJS.Timeout | undefined;
    private readonly DEBOUNCE_DELAY = 2000; // 2 seconds
    private activeGaps: Array<any> = [];

    constructor(mcpClient: McpClient) {
        this.mcpClient = mcpClient;
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.initialize();
    }

    private initialize() {
        this.statusBarItem.text = "$(light-bulb) Agent";
        this.statusBarItem.tooltip = "Agentic Editor: Click to analyze draft";
        this.statusBarItem.command = 'autoResearcher.analyzeGaps';
        this.statusBarItem.show();

        // Set up document change listener
        vscode.workspace.onDidChangeTextDocument(this.handleDocumentChange, this);

        // Register commands
        vscode.commands.registerCommand('autoResearcher.analyzeGaps', this.analyzeCurrentDocument, this);
        vscode.commands.registerCommand('autoResearcher.proposeEdits', this.proposeEditsForGaps, this);
        vscode.commands.registerCommand('autoResearcher.acceptEdit', this.acceptEditSuggestion, this);
    }

    /**
     * Handle document changes with debouncing
     */
    private handleDocumentChange(event: vscode.TextDocumentChangeEvent) {
        // Only monitor markdown files
        if (event.document.languageId !== 'markdown') {
            return;
        }

        // Clear existing timer
        if (this.currentDebounceTimer) {
            clearTimeout(this.currentDebounceTimer);
        }

        // Skip if document is very large (>50KB)
        if (event.document.getText().length > 50000) {
            return;
        }

        // Set new timer for analysis
        this.currentDebounceTimer = setTimeout(() => {
            this.syncDocumentContent(event.document);
        }, this.DEBOUNCE_DELAY);
    }

    /**
     * Sync document content with backend for gap analysis
     */
    private async syncDocumentContent(document: vscode.TextDocument) {
        try {
            this.statusBarItem.text = "$(loading~spin) Analyzing...";

            // Get cursor position
            const cursor = vscode.window.activeTextEditor?.selection.active;
            const cursorLine = cursor?.line;
            const cursorColumn = cursor?.character;

            // Call MCP tool for gap analysis
            const result = await this.mcpClient.callTool('sync_draft_context', {
                content: document.getText(),
                cursor_line: cursorLine,
                cursor_column: cursorColumn
            });

            if (result.success) {
                this.activeGaps = result.gaps || [];
                this.updateGapsIndicators(this.activeGaps);

                // Update status bar with gap count
                const gapCount = this.activeGaps.length;
                if (gapCount > 0) {
                    this.statusBarItem.text = `$(warning) ${gapCount} gaps found`;
                    this.statusBarItem.tooltip = `Click to propose edits for ${gapCount} evidence gaps`;
                    this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');

                    // Show notification for high-confidence gaps
                    const highConfidenceGaps = this.activeGaps.filter((g: any) => g.is_high_confidence);
                    if (highConfidenceGaps.length > 0) {
                        vscode.window.showInformationMessage(
                            `Found ${highConfidenceGaps.length} high-confidence evidence gaps. Click status bar to fix them.`
                        );
                    }
                } else {
                    this.statusBarItem.text = "$(check) No gaps found";
                    this.statusBarItem.tooltip = "Research draft looks complete";
                    this.statusBarItem.backgroundColor = undefined;
                }
            } else {
                this.statusBarItem.text = "$(error) Analysis failed";
                vscode.window.showErrorMessage(`Gap analysis failed: ${result.error}`);
            }

        } catch (error) {
            console.error('Document sync error:', error);
            this.statusBarItem.text = "$(error) Sync error";
            vscode.window.showErrorMessage(`Failed to sync document: ${error}`);
        }
    }

    /**
     * Update VS Code UI with gap indicators (decorations, suggestions)
     */
    private updateGapsIndicators(gaps: Array<any>) {
        // Clear existing decorations and code lenses
        // Note: Full implementation would create decorations and code lenses here

        if (gaps.length > 0) {
            // Show code lenses for each gap
            this.registerGapCodeLenses(gaps);

            // Update tree view if available
            this.updateGapsTreeView(gaps);
        }
    }

    /**
     * Register code lenses for gap suggestions
     */
    private registerGapCodeLenses(_gaps: Array<any>) {
        // This would be implemented with vscode.languages.registerCodeLensProvider
        // For each gap, show a CodeLens like "✨ AI Suggestion Available (Click to Apply)"
    }

    /**
     * Update gaps tree view in sidebar
     */
    private updateGapsTreeView(_gaps: Array<any>) {
        // Send message to tree view provider to update gaps list
        // Implementation depends on the specific tree view setup
    }

    /**
     * Manual trigger for gap analysis on current document
     */
    private async analyzeCurrentDocument() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage("No active editor found");
            return;
        }

        if (editor.document.languageId !== 'markdown') {
            vscode.window.showWarningMessage("Gap analysis only works with Markdown files");
            return;
        }

        // Clear debounce timer and trigger immediate analysis
        if (this.currentDebounceTimer) {
            clearTimeout(this.currentDebounceTimer);
            this.currentDebounceTimer = undefined;
        }

        await this.syncDocumentContent(editor.document);
    }

    /**
     * Generate and propose edits for identified gaps
     */
    private async proposeEditsForGaps() {
        if (this.activeGaps.length === 0) {
            vscode.window.showInformationMessage("No evidence gaps found to fix");
            return;
        }

        try {
            this.statusBarItem.text = "$(loading~spin) Generating edits...";

            // Call MCP tool to propose edits
            const result = await this.mcpClient.callTool('propose_edits', {
                gaps: this.activeGaps,
                file_path: vscode.window.activeTextEditor?.document.fileName || "draft.md"
            });

            if (result.success && result.improvements?.length > 0) {
                this.showEditSuggestions(result.improvements);
                this.statusBarItem.text = "$(light-bulb) Edits ready";
                vscode.window.showInformationMessage(
                    `Generated ${result.improvements.length} improvement suggestions`
                );
            } else {
                this.statusBarItem.text = "$(warning) No edits generated";
                vscode.window.showWarningMessage(
                    result.message || "No improvement suggestions generated"
                );
            }

        } catch (error) {
            console.error('Edit proposal error:', error);
            this.statusBarItem.text = "$(error) Edit error";
            vscode.window.showErrorMessage(`Failed to generate edits: ${error}`);
        }
    }

    /**
     * Display edit suggestions to user (CodeLenses, Diff view, etc.)
     */
    private showEditSuggestions(improvements: Array<any>) {
        // Implementation options:
        // 1. Show CodeLens on each gap line: "✨ AI Suggestion (Accept/Reject)"
        // 2. Open Diff view showing before/after
        // 3. Show Webview with improvements list
        // 4. Quick pick menu with diff preview

        // For now, show a summary and allow user to accept individual edits
        const summary = improvements.map((imp: any, i: number) =>
            `${i + 1}. ${imp.suggested_insertion.substring(0, 100)}... (${imp.citations?.length || 0} citations)`
        ).join('\n');

        vscode.window.showInformationMessage(
            `AI Edit Suggestions Ready:\n${summary}`,
            "Apply All"
        ).then(selection => {
            if (selection === "Apply All") {
                this.applyAllEdits(improvements);
            }
        });
    }

    /**
     * Apply all approved edits to the document
     */
    private async applyAllEdits(improvements: Array<any>) {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        try {
            await editor.edit(editBuilder => {
                for (const improvement of improvements) {
                    // Find the location of the original snippet in document
                    const docText = editor.document.getText();
                    const snippetIndex = docText.indexOf(improvement.original_snippet);

                    if (snippetIndex !== -1) {
                        const startPos = editor.document.positionAt(snippetIndex);
                        const endPos = editor.document.positionAt(
                            snippetIndex + improvement.original_snippet.length
                        );

                        // Apply the suggested edit
                        editBuilder.replace(
                            new vscode.Range(startPos, endPos),
                            improvement.suggested_insertion
                        );
                    }
                }
            });

            // Clear active gaps since they've been applied
            this.activeGaps = [];
            this.statusBarItem.text = "$(check) Edits applied";
            vscode.window.showInformationMessage("All improvements applied successfully");

        } catch (error) {
            console.error('Edit application error:', error);
            vscode.window.showErrorMessage(`Failed to apply edits: ${error}`);
        }
    }

    /**
     * Accept individual edit suggestion
     */
    private async acceptEditSuggestion(editSpec: any) {
        // Apply single edit via MCP tool
        try {
            const result = await this.mcpClient.callTool('apply_edit', {
                file_path: editSpec.file_path,
                original_text: editSpec.original_text,
                new_text: editSpec.new_text,
                line_start: editSpec.line_start,
                line_end: editSpec.line_end
            });

            // Actually apply the edit in VS Code
            if (result.success && result.edit_spec) {
                const editor = vscode.window.activeTextEditor;
                if (editor && result.edit_spec) {
                    const edit = result.edit_spec;
                    await editor.edit(editBuilder => {
                        const startPos = new vscode.Position(edit.line_start, 0);
                        const endPos = new vscode.Position(edit.line_end, 0);

                        // Replace the range with improved text
                        editBuilder.replace(
                            new vscode.Range(startPos, endPos),
                            edit.new_text
                        );
                    });

                    vscode.window.showInformationMessage("Edit applied successfully");
                }
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to apply edit: ${error}`);
        }
    }

    /**
     * Clean up resources
     */
    public dispose() {
        if (this.currentDebounceTimer) {
            clearTimeout(this.currentDebounceTimer);
        }
        this.statusBarItem.dispose();
    }
}

// Export factory function for extension activation
export function createDraftWatcherProvider(mcpClient: McpClient): DraftWatcherProvider {
    return new DraftWatcherProvider(mcpClient);
}