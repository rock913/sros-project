/**
 * Suggestion UI Provider - Handles AI Edit Suggestions and Diff Views
 *
 * Provides CodeLens, Diff views, and interactive UI for accepting/rejecting
 * AI-generated improvements to research drafts.
 */

import * as vscode from 'vscode';
import { McpClient } from '../mcp_client';


export interface EditSuggestion {
    gap_id: string;
    original_snippet: string;
    suggested_insertion: string;
    citations: string[];
    rationale: string;
    has_citations: boolean;
}

export class SuggestionUIProvider implements vscode.CodeLensProvider, vscode.InlineCompletionItemProvider {
    // @ts-ignore - intentionally unused field, features not fully implemented yet
    private _mcpClient: McpClient;
    private currentSuggestions: Map<string, EditSuggestion[]> = new Map();
    private statusBarItem: vscode.StatusBarItem;

    constructor(_mcpClient: McpClient) {
        this._mcpClient = _mcpClient;
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 99);
        this.initialize();
    }

    private initialize() {
        // Register as CodeLens provider for markdown files
        vscode.languages.registerCodeLensProvider(
            { language: 'markdown' },
            this
        );

        // Register inline completion provider
        vscode.languages.registerInlineCompletionItemProvider(
            { language: 'markdown' },
            this
        );

        // Register commands for accept/reject
        vscode.commands.registerCommand('autoResearcher.acceptSuggestion', this.acceptSuggestion, this);
        vscode.commands.registerCommand('autoResearcher.rejectSuggestion', this.rejectSuggestion, this);
        vscode.commands.registerCommand('autoResearcher.showDiff', this.showDiffView, this);
        vscode.commands.registerCommand('autoResearcher.batchApplySuggestions', this.batchApplySuggestions, this);
    }

    /**
     * Update suggestions for a document
     */
    public updateSuggestions(documentUri: string, suggestions: EditSuggestion[]) {
        this.currentSuggestions.set(documentUri, suggestions);
        this.refreshCodeLenses(documentUri);
    }

    /**
     * Provide CodeLens for suggestions
     */
    public provideCodeLenses(document: vscode.TextDocument): vscode.CodeLens[] {
        const suggestions = this.currentSuggestions.get(document.uri.toString()) || [];
        const lenses: vscode.CodeLens[] = [];

        for (const suggestion of suggestions) {
            // Find the line where the original snippet appears
            const docText = document.getText();
            const snippetIndex = docText.indexOf(suggestion.original_snippet);

            if (snippetIndex !== -1) {
                const line = document.positionAt(snippetIndex).line;

                // Create CodeLens with accept/reject commands
                const acceptLens = new vscode.CodeLens(
                    new vscode.Range(line, 0, line, 0),
                    {
                        title: "$(check) Accept AI Suggestion",
                        tooltip: `Insert: ${suggestion.suggested_insertion.substring(0, 50)}...`,
                        command: 'autoResearcher.acceptSuggestion',
                        arguments: [document.uri, suggestion]
                    }
                );

                const rejectLens = new vscode.CodeLens(
                    new vscode.Range(line, 0, line, 0),
                    {
                        title: "$(x) Reject Suggestion",
                        tooltip: "Dismiss this AI suggestion",
                        command: 'autoResearcher.rejectSuggestion',
                        arguments: [document.uri, suggestion]
                    }
                );

                const diffLens = new vscode.CodeLens(
                    new vscode.Range(line, 0, line, 0),
                    {
                        title: "$(diff) Show Diff",
                        tooltip: "View before/after diff",
                        command: 'autoResearcher.showDiff',
                        arguments: [document.uri, suggestion]
                    }
                );

                lenses.push(acceptLens, rejectLens, diffLens);
            }
        }

        return lenses;
    }

    /**
     * Show diff view for a suggestion
     */
    private async showDiffView(_documentUri: vscode.Uri, suggestion: EditSuggestion) {
        // Create temporary files for diff view
        const originalUri = vscode.Uri.parse('untitled:Original.md');
        const improvedUri = vscode.Uri.parse('untitled:AI Suggested.md');

        try {
            // Open diff view
            await vscode.commands.executeCommand('vscode.diff',
                originalUri,
                improvedUri,
                `Evidence Gap: ${suggestion.rationale}`,
                {
                    preview: true,
                    selection: undefined
                }
            );

            // Insert content into virtual documents
            // @ts-ignore - intentionally unused variables for diff view setup
            const _originalDoc = await vscode.workspace.openTextDocument(originalUri);
            // @ts-ignore - intentionally unused variables for diff view setup
            const _improvedDoc = await vscode.workspace.openTextDocument(improvedUri);

            const originalEdit = new vscode.WorkspaceEdit();
            originalEdit.insert(improvedUri, new vscode.Position(0, 0),
                `BEFORE (Original Text):\n\n${suggestion.original_snippet}\n\n---`);

            const improvedEdit = new vscode.WorkspaceEdit();
            improvedEdit.insert(improvedUri, new vscode.Position(0, 0),
                `AFTER (AI Suggested):\n\n${suggestion.suggested_insertion}\n\n---\n\nRationale: ${suggestion.rationale}\n\nCitations: ${suggestion.citations.join(', ')}`);

            await vscode.workspace.applyEdit(originalEdit);
            await vscode.workspace.applyEdit(improvedEdit);

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to show diff: ${error}`);
        }
    }

    /**
     * Accept an AI suggestion and apply it to the document
     */
    private async acceptSuggestion(documentUri: vscode.Uri, suggestion: EditSuggestion) {
        try {
            const document = vscode.workspace.textDocuments.find(doc => doc.uri.toString() === documentUri.toString());
            if (!document) {
                vscode.window.showErrorMessage("Document not found");
                return;
            }

            // Find the original snippet location
            const docText = document.getText();
            const snippetIndex = docText.indexOf(suggestion.original_snippet);

            if (snippetIndex === -1) {
                vscode.window.showErrorMessage("Could not locate original text in document");
                return;
            }

            // Apply the edit
            const editor = vscode.window.activeTextEditor;
            if (editor && editor.document.uri.toString() === documentUri.toString()) {
                const startPos = document.positionAt(snippetIndex);
                const endPos = document.positionAt(snippetIndex + suggestion.original_snippet.length);

                await editor.edit(editBuilder => {
                    editBuilder.replace(
                        new vscode.Range(startPos, endPos),
                        suggestion.suggested_insertion
                    );
                });

                // Remove this suggestion from tracking
                this.removeSuggestion(documentUri.toString(), suggestion.gap_id);

                vscode.window.showInformationMessage(
                    `Applied AI suggestion: ${suggestion.suggested_insertion.substring(0, 50)}...`
                );
            }

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to apply suggestion: ${error}`);
        }
    }

    /**
     * Reject an AI suggestion
     */
    private async rejectSuggestion(documentUri: vscode.Uri, suggestion: EditSuggestion) {
        // Remove from tracking
        this.removeSuggestion(documentUri.toString(), suggestion.gap_id);

        vscode.window.showInformationMessage("AI suggestion dismissed");
    }

    /**
     * Batch apply all suggestions for a document
     */
    private async batchApplySuggestions(documentUri: vscode.Uri) {
        const suggestions = this.currentSuggestions.get(documentUri.toString()) || [];

        if (suggestions.length === 0) {
            vscode.window.showWarningMessage("No suggestions available to apply");
            return;
        }

        // Confirm with user
        const result = await vscode.window.showWarningMessage(
            `Apply all ${suggestions.length} AI suggestions to the document?`,
            { modal: true },
            "Yes, Apply All",
            "Cancel"
        );

        if (result === "Yes, Apply All") {
            for (const suggestion of suggestions) {
                await this.acceptSuggestion(documentUri, suggestion);
            }

            vscode.window.showInformationMessage(
                `Applied ${suggestions.length} AI suggestions successfully`
            );
        }
    }

    /**
     * Provide inline completions (ghost text) for AI suggestions
     */
    public provideInlineCompletionItems(_document: vscode.TextDocument, _position: vscode.Position): vscode.ProviderResult<vscode.InlineCompletionList> {
        // This could show ghost text suggestions
        // For now, return empty list
        return new vscode.InlineCompletionList([]);
    }

    /**
     * Remove a suggestion from tracking
     */
    private removeSuggestion(documentUri: string, gapId: string) {
        const suggestions = this.currentSuggestions.get(documentUri) || [];
        const filtered = suggestions.filter(s => s.gap_id !== gapId);
        this.currentSuggestions.set(documentUri, filtered);
        this.refreshCodeLenses(documentUri);
    }

    /**
     * Refresh CodeLens for a document
     */
    private refreshCodeLenses(documentUri: string) {
        vscode.commands.executeCommand('vscode.executeCodeLensProvider', vscode.Uri.parse(documentUri));
    }

    /**
     * Clear all suggestions for a document
     */
    public clearSuggestions(documentUri: string) {
        this.currentSuggestions.delete(documentUri);
        this.refreshCodeLenses(documentUri);
    }

    /**
     * Get current suggestions count for status display
     */
    public getSuggestionsCount(documentUri: string): number {
        return this.currentSuggestions.get(documentUri)?.length || 0;
    }

    /**
     * Dispose resources
     */
    public dispose() {
        this.currentSuggestions.clear();
        this.statusBarItem.dispose();
    }
}

// Export factory function
export function createSuggestionUIProvider(mcpClient: McpClient): SuggestionUIProvider {
    return new SuggestionUIProvider(mcpClient);
}