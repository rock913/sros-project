"use strict";
/**
 * Document Collaboration Module
 *
 * Phase 3.6 Week 3: Real-time Document Collaboration
 *
 * This module handles real-time document updates from the AI agent,
 * applying incremental changes to VS Code editor with visual feedback
 * and user approval workflow.
 *
 * Features:
 * - Real-time paragraph-level diffs from WebSocket
 * - Visual decorations (gutter icons, highlights)
 * - CodeLens for Accept/Reject actions
 * - Undo/Redo integration
 * - Conflict detection and resolution
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.DocumentCollaborationManager = void 0;
const vscode = require("vscode");
// ============================================================================
// Document Collaboration Manager
// ============================================================================
/**
 * Manages real-time document collaboration between AI and user
 */
class DocumentCollaborationManager {
    constructor(context) {
        this.pendingChanges = new Map();
        this.disposables = [];
        // Initialize decoration types with gutter icons
        this.decorationTypes = {
            insert: vscode.window.createTextEditorDecorationType({
                backgroundColor: new vscode.ThemeColor('diffEditor.insertedTextBackground'),
                border: '3px solid',
                borderColor: new vscode.ThemeColor('diffEditor.insertedLineBackground'),
                gutterIconPath: context.asAbsolutePath('resources/icons/add.svg'),
                gutterIconSize: 'contain',
                isWholeLine: true,
            }),
            modify: vscode.window.createTextEditorDecorationType({
                backgroundColor: new vscode.ThemeColor('diffEditor.modifiedTextBackground'),
                border: '3px solid',
                borderColor: new vscode.ThemeColor('diffEditor.modifiedLineBackground'),
                gutterIconPath: context.asAbsolutePath('resources/icons/edit.svg'),
                gutterIconSize: 'contain',
                isWholeLine: true,
            }),
            delete: vscode.window.createTextEditorDecorationType({
                backgroundColor: new vscode.ThemeColor('diffEditor.removedTextBackground'),
                border: '3px solid',
                borderColor: new vscode.ThemeColor('diffEditor.removedLineBackground'),
                gutterIconPath: context.asAbsolutePath('resources/icons/delete.svg'),
                gutterIconSize: 'contain',
                textDecoration: 'line-through',
                isWholeLine: true,
            }),
        };
        // Initialize CodeLens provider
        this.codeLensProvider = new DocumentCollaborationCodeLensProvider(this);
        // Register CodeLens provider for markdown files
        const codeLensDisposable = vscode.languages.registerCodeLensProvider({ language: 'markdown', scheme: 'file' }, this.codeLensProvider);
        this.disposables.push(codeLensDisposable);
        // Register commands
        this.registerCommands();
    }
    /**
     * Register VS Code commands for document collaboration
     */
    registerCommands() {
        // Accept change command
        const acceptCommand = vscode.commands.registerCommand('gemini-research.acceptDocumentChange', (changeId) => this.acceptChange(changeId));
        // Reject change command
        const rejectCommand = vscode.commands.registerCommand('gemini-research.rejectDocumentChange', (changeId) => this.rejectChange(changeId));
        // Accept all changes command
        const acceptAllCommand = vscode.commands.registerCommand('gemini-research.acceptAllDocumentChanges', () => this.acceptAllChanges());
        // Reject all changes command
        const rejectAllCommand = vscode.commands.registerCommand('gemini-research.rejectAllDocumentChanges', () => this.rejectAllChanges());
        this.disposables.push(acceptCommand, rejectCommand, acceptAllCommand, rejectAllCommand);
    }
    /**
     * Handle incoming document update from WebSocket
     *
     * @param update - Document update message
     * @param documentUri - URI of the document to update
     */
    async handleDocumentUpdate(update, documentUri) {
        // Skip unchanged actions
        if (update.action === 'unchanged') {
            return;
        }
        // Find or open the document
        const document = await vscode.workspace.openTextDocument(documentUri);
        // Show document in editor if not already visible
        const editor = await vscode.window.showTextDocument(document, {
            preview: false,
            preserveFocus: true,
        });
        // Generate unique change ID
        const changeId = `${update.session_id}_${update.paragraph_index}_${update.timestamp}`;
        // Calculate the range for this change
        const range = this.calculateRange(document, update);
        // Create decoration
        const decoration = this.decorationTypes[update.action];
        // Store as pending change
        const pendingChange = {
            update,
            decoration,
            range,
            applied: false,
        };
        this.pendingChanges.set(changeId, pendingChange);
        // Apply decoration to show the change
        this.applyDecorations(editor);
        // Refresh CodeLens
        this.codeLensProvider.refresh();
        // Show notification
        const action = update.action.charAt(0).toUpperCase() + update.action.slice(1);
        vscode.window.showInformationMessage(`AI ${action}: ${update.rationale}`, 'Accept', 'Reject').then(choice => {
            if (choice === 'Accept') {
                this.acceptChange(changeId);
            }
            else if (choice === 'Reject') {
                this.rejectChange(changeId);
            }
        });
    }
    /**
     * Calculate the range in the document for a given update
     */
    calculateRange(document, update) {
        const { line_range } = update;
        // VS Code uses 0-based indexing, backend sends 1-based
        const startLine = Math.max(0, line_range.start - 1);
        const endLine = Math.min(document.lineCount - 1, line_range.end - 1);
        return new vscode.Range(new vscode.Position(startLine, 0), new vscode.Position(endLine, document.lineAt(endLine).text.length));
    }
    /**
     * Apply decorations to the active editor
     */
    applyDecorations(editor) {
        const insertRanges = [];
        const modifyRanges = [];
        const deleteRanges = [];
        for (const [, change] of this.pendingChanges) {
            if (change.applied) {
                continue;
            }
            switch (change.update.action) {
                case 'insert':
                    insertRanges.push(change.range);
                    break;
                case 'modify':
                    modifyRanges.push(change.range);
                    break;
                case 'delete':
                    deleteRanges.push(change.range);
                    break;
            }
        }
        editor.setDecorations(this.decorationTypes.insert, insertRanges);
        editor.setDecorations(this.decorationTypes.modify, modifyRanges);
        editor.setDecorations(this.decorationTypes.delete, deleteRanges);
    }
    /**
     * Accept a pending change and apply it to the document
     */
    async acceptChange(changeId) {
        const change = this.pendingChanges.get(changeId);
        if (!change) {
            return;
        }
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        const edit = new vscode.WorkspaceEdit();
        const { update, range } = change;
        // Apply the change based on action type
        switch (update.action) {
            case 'insert':
                edit.insert(editor.document.uri, range.start, update.content + '\n\n');
                break;
            case 'modify':
                edit.replace(editor.document.uri, range, update.content);
                break;
            case 'delete':
                edit.delete(editor.document.uri, range);
                break;
        }
        // Apply the edit
        const success = await vscode.workspace.applyEdit(edit);
        if (success) {
            change.applied = true;
            this.pendingChanges.delete(changeId);
            // Refresh decorations
            this.applyDecorations(editor);
            // Refresh CodeLens
            this.codeLensProvider.refresh();
            vscode.window.showInformationMessage(`✅ Accepted ${update.action}: ${update.rationale}`);
        }
        else {
            vscode.window.showErrorMessage(`❌ Failed to apply ${update.action}`);
        }
    }
    /**
     * Reject a pending change and remove its decoration
     */
    async rejectChange(changeId) {
        const change = this.pendingChanges.get(changeId);
        if (!change) {
            return;
        }
        this.pendingChanges.delete(changeId);
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            this.applyDecorations(editor);
        }
        this.codeLensProvider.refresh();
        vscode.window.showInformationMessage(`❌ Rejected ${change.update.action}: ${change.update.rationale}`);
    }
    /**
     * Accept all pending changes
     */
    async acceptAllChanges() {
        const changeIds = Array.from(this.pendingChanges.keys());
        for (const changeId of changeIds) {
            await this.acceptChange(changeId);
        }
        vscode.window.showInformationMessage(`✅ Accepted all ${changeIds.length} change(s)`);
    }
    /**
     * Reject all pending changes
     */
    async rejectAllChanges() {
        const count = this.pendingChanges.size;
        this.pendingChanges.clear();
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            this.applyDecorations(editor);
        }
        this.codeLensProvider.refresh();
        vscode.window.showInformationMessage(`❌ Rejected all ${count} change(s)`);
    }
    /**
     * Get all pending changes
     */
    getPendingChanges() {
        return this.pendingChanges;
    }
    /**
     * Clear all pending changes (e.g., when session ends)
     */
    clearAllChanges() {
        this.pendingChanges.clear();
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            // Clear all decorations
            editor.setDecorations(this.decorationTypes.insert, []);
            editor.setDecorations(this.decorationTypes.modify, []);
            editor.setDecorations(this.decorationTypes.delete, []);
        }
        this.codeLensProvider.refresh();
    }
    /**
     * Dispose resources
     */
    dispose() {
        for (const disposable of this.disposables) {
            disposable.dispose();
        }
        this.decorationTypes.insert.dispose();
        this.decorationTypes.modify.dispose();
        this.decorationTypes.delete.dispose();
    }
}
exports.DocumentCollaborationManager = DocumentCollaborationManager;
// ============================================================================
// CodeLens Provider
// ============================================================================
/**
 * Provides CodeLens UI for accepting/rejecting document changes
 */
class DocumentCollaborationCodeLensProvider {
    constructor(manager) {
        this.manager = manager;
        this._onDidChangeCodeLenses = new vscode.EventEmitter();
        this.onDidChangeCodeLenses = this._onDidChangeCodeLenses.event;
    }
    /**
     * Provide CodeLenses for pending changes
     */
    provideCodeLenses(_document, _token) {
        const codeLenses = [];
        const pendingChanges = this.manager.getPendingChanges();
        for (const [changeId, change] of pendingChanges) {
            if (change.applied) {
                continue;
            }
            const { range, update } = change;
            // Accept CodeLens
            const acceptLens = new vscode.CodeLens(range, {
                title: `✅ Accept ${update.action}`,
                command: 'gemini-research.acceptDocumentChange',
                arguments: [changeId],
            });
            // Reject CodeLens
            const rejectLens = new vscode.CodeLens(range, {
                title: `❌ Reject ${update.action}`,
                command: 'gemini-research.rejectDocumentChange',
                arguments: [changeId],
            });
            codeLenses.push(acceptLens, rejectLens);
        }
        // Add "Accept All" / "Reject All" at the top if there are pending changes
        if (pendingChanges.size > 0) {
            const topRange = new vscode.Range(0, 0, 0, 0);
            const acceptAllLens = new vscode.CodeLens(topRange, {
                title: `✅ Accept All (${pendingChanges.size})`,
                command: 'gemini-research.acceptAllDocumentChanges',
            });
            const rejectAllLens = new vscode.CodeLens(topRange, {
                title: `❌ Reject All (${pendingChanges.size})`,
                command: 'gemini-research.rejectAllDocumentChanges',
            });
            codeLenses.unshift(acceptAllLens, rejectAllLens);
        }
        return codeLenses;
    }
    /**
     * Refresh CodeLens display
     */
    refresh() {
        this._onDidChangeCodeLenses.fire();
    }
}
//# sourceMappingURL=documentCollaboration.js.map