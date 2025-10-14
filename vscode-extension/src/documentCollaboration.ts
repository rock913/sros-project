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

import * as vscode from 'vscode';

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Document update message from backend WebSocket
 */
export interface DocumentUpdate {
    type: 'document_update';
    // eslint-disable-next-line @typescript-eslint/naming-convention
    session_id: string;
    node: string;
    action: 'insert' | 'modify' | 'delete' | 'unchanged';
    // eslint-disable-next-line @typescript-eslint/naming-convention
    paragraph_index: number;
    content: string;
    // eslint-disable-next-line @typescript-eslint/naming-convention
    old_content?: string;
    // eslint-disable-next-line @typescript-eslint/naming-convention
    line_range: {
        start: number;
        end: number;
    };
    rationale: string;
    timestamp: string;
}

/**
 * Pending change waiting for user approval
 */
interface PendingChange {
    update: DocumentUpdate;
    decoration: vscode.TextEditorDecorationType;
    range: vscode.Range;
    applied: boolean;
}

/**
 * Decoration types for different actions
 */
interface DecorationTypes {
    insert: vscode.TextEditorDecorationType;
    modify: vscode.TextEditorDecorationType;
    delete: vscode.TextEditorDecorationType;
}

// ============================================================================
// Document Collaboration Manager
// ============================================================================

/**
 * Manages real-time document collaboration between AI and user
 */
export class DocumentCollaborationManager {
    private decorationTypes: DecorationTypes;
    private pendingChanges: Map<string, PendingChange> = new Map();
    private codeLensProvider: DocumentCollaborationCodeLensProvider;
    private disposables: vscode.Disposable[] = [];

    constructor(context: vscode.ExtensionContext) {
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
        const codeLensDisposable = vscode.languages.registerCodeLensProvider(
            { language: 'markdown', scheme: 'file' },
            this.codeLensProvider
        );
        
        this.disposables.push(codeLensDisposable);

        // Register commands
        this.registerCommands();
    }

    /**
     * Register VS Code commands for document collaboration
     */
    private registerCommands(): void {
        // Accept change command
        const acceptCommand = vscode.commands.registerCommand(
            'gemini-research.acceptDocumentChange',
            (changeId: string) => this.acceptChange(changeId)
        );

        // Reject change command
        const rejectCommand = vscode.commands.registerCommand(
            'gemini-research.rejectDocumentChange',
            (changeId: string) => this.rejectChange(changeId)
        );

        // Accept all changes command
        const acceptAllCommand = vscode.commands.registerCommand(
            'gemini-research.acceptAllDocumentChanges',
            () => this.acceptAllChanges()
        );

        // Reject all changes command
        const rejectAllCommand = vscode.commands.registerCommand(
            'gemini-research.rejectAllDocumentChanges',
            () => this.rejectAllChanges()
        );

        this.disposables.push(acceptCommand, rejectCommand, acceptAllCommand, rejectAllCommand);
    }

    /**
     * Handle incoming document update from WebSocket
     * 
     * @param update - Document update message
     * @param documentUri - URI of the document to update
     */
    public async handleDocumentUpdate(update: DocumentUpdate, documentUri: vscode.Uri): Promise<void> {
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
        const pendingChange: PendingChange = {
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
        vscode.window.showInformationMessage(
            `AI ${action}: ${update.rationale}`,
            'Accept',
            'Reject'
        ).then(choice => {
            if (choice === 'Accept') {
                this.acceptChange(changeId);
            } else if (choice === 'Reject') {
                this.rejectChange(changeId);
            }
        });
    }

    /**
     * Calculate the range in the document for a given update
     */
    private calculateRange(document: vscode.TextDocument, update: DocumentUpdate): vscode.Range {
        const { line_range } = update;
        
        // VS Code uses 0-based indexing, backend sends 1-based
        const startLine = Math.max(0, line_range.start - 1);
        const endLine = Math.min(document.lineCount - 1, line_range.end - 1);
        
        return new vscode.Range(
            new vscode.Position(startLine, 0),
            new vscode.Position(endLine, document.lineAt(endLine).text.length)
        );
    }

    /**
     * Apply decorations to the active editor
     */
    private applyDecorations(editor: vscode.TextEditor): void {
        const insertRanges: vscode.Range[] = [];
        const modifyRanges: vscode.Range[] = [];
        const deleteRanges: vscode.Range[] = [];

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
    private async acceptChange(changeId: string): Promise<void> {
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

            vscode.window.showInformationMessage(
                `✅ Accepted ${update.action}: ${update.rationale}`
            );
        } else {
            vscode.window.showErrorMessage(
                `❌ Failed to apply ${update.action}`
            );
        }
    }

    /**
     * Reject a pending change and remove its decoration
     */
    private async rejectChange(changeId: string): Promise<void> {
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

        vscode.window.showInformationMessage(
            `❌ Rejected ${change.update.action}: ${change.update.rationale}`
        );
    }

    /**
     * Accept all pending changes
     */
    private async acceptAllChanges(): Promise<void> {
        const changeIds = Array.from(this.pendingChanges.keys());
        
        for (const changeId of changeIds) {
            await this.acceptChange(changeId);
        }

        vscode.window.showInformationMessage(
            `✅ Accepted all ${changeIds.length} change(s)`
        );
    }

    /**
     * Reject all pending changes
     */
    private async rejectAllChanges(): Promise<void> {
        const count = this.pendingChanges.size;
        this.pendingChanges.clear();

        const editor = vscode.window.activeTextEditor;
        if (editor) {
            this.applyDecorations(editor);
        }

        this.codeLensProvider.refresh();

        vscode.window.showInformationMessage(
            `❌ Rejected all ${count} change(s)`
        );
    }

    /**
     * Get all pending changes
     */
    public getPendingChanges(): Map<string, PendingChange> {
        return this.pendingChanges;
    }

    /**
     * Clear all pending changes (e.g., when session ends)
     */
    public clearAllChanges(): void {
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
    public dispose(): void {
        for (const disposable of this.disposables) {
            disposable.dispose();
        }
        
        this.decorationTypes.insert.dispose();
        this.decorationTypes.modify.dispose();
        this.decorationTypes.delete.dispose();
    }
}

// ============================================================================
// CodeLens Provider
// ============================================================================

/**
 * Provides CodeLens UI for accepting/rejecting document changes
 */
class DocumentCollaborationCodeLensProvider implements vscode.CodeLensProvider {
    private _onDidChangeCodeLenses = new vscode.EventEmitter<void>();
    public readonly onDidChangeCodeLenses = this._onDidChangeCodeLenses.event;

    constructor(private manager: DocumentCollaborationManager) {}

    /**
     * Provide CodeLenses for pending changes
     */
    public provideCodeLenses(
        _document: vscode.TextDocument,
        _token: vscode.CancellationToken
    ): vscode.CodeLens[] {
        const codeLenses: vscode.CodeLens[] = [];
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
    public refresh(): void {
        this._onDidChangeCodeLenses.fire();
    }
}
