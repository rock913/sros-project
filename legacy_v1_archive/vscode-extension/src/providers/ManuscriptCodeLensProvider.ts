/**
 * Manuscript CodeLens Provider
 * 
 * Provides CodeLens actions for paper references in manuscript documents.
 * Detects reference lines (e.g., "[1] Author et al. (2020)...") and provides:
 * - View Paper Details
 * - Copy BibTeX
 * - Download PDF
 */

import * as vscode from 'vscode';
import { getSessionDetailsV2 } from '../api';

/**
 * CodeLens Provider for manuscript documents
 */
export class ManuscriptCodeLensProvider implements vscode.CodeLensProvider {
    
    private _onDidChangeCodeLensesEmitter = new vscode.EventEmitter<void>();
    public readonly onDidChangeCodeLenses = this._onDidChangeCodeLensesEmitter.event;
    
    /**
     * Provide CodeLens for a manuscript document
     */
    async provideCodeLenses(
        document: vscode.TextDocument,
        _token: vscode.CancellationToken
    ): Promise<vscode.CodeLens[]> {
        const codeLenses: vscode.CodeLens[] = [];
        
        // Only process research-manuscript:// URIs
        if (document.uri.scheme !== 'research-manuscript') {
            return codeLenses;
        }
        
        try {
            // Parse session ID from URI
            const sessionId = this.extractSessionId(document.uri);
            
            if (!sessionId) {
                return codeLenses;
            }
            
            // Fetch session details to get paper metadata
            const details = await getSessionDetailsV2(sessionId);
            
            if (!details || !details.papers) {
                return codeLenses;
            }
            
            const papers = details.papers;
            
            // Scan document for reference lines
            // Pattern: [N] ... where N is a number (1-based index)
            const referencePattern = /^\[(\d+)\]\s+(.+)$/gm;
            
            for (let lineIndex = 0; lineIndex < document.lineCount; lineIndex++) {
                const line = document.lineAt(lineIndex);
                const match = referencePattern.exec(line.text);
                
                if (match) {
                    const refNumber = parseInt(match[1], 10);
                    const paperIndex = refNumber - 1; // Convert to 0-based
                    
                    // Verify paper exists
                    if (paperIndex >= 0 && paperIndex < papers.length) {
                        const paper = papers[paperIndex];
                        const range = new vscode.Range(lineIndex, 0, lineIndex, line.text.length);
                        
                        // Create CodeLens actions
                        codeLenses.push(
                            // View Paper Details
                            new vscode.CodeLens(range, {
                                title: '$(book) View Details',
                                command: 'auto-researcher.openPaper',
                                arguments: [sessionId, paperIndex],
                                tooltip: `View details for: ${paper.title}`
                            }),
                            
                            // Copy BibTeX
                            new vscode.CodeLens(range, {
                                title: '$(copy) Copy BibTeX',
                                command: 'auto-researcher.copyBibTeX',
                                arguments: [paper],
                                tooltip: 'Copy BibTeX citation to clipboard'
                            })
                        );
                        
                        // Download PDF (if available)
                        if (paper.pdf_url || paper.url) {
                            codeLenses.push(
                                new vscode.CodeLens(range, {
                                    title: '$(cloud-download) Download PDF',
                                    command: 'auto-researcher.downloadPDF',
                                    arguments: [paper],
                                    tooltip: 'Open PDF in browser'
                                })
                            );
                        }
                    }
                }
                
                // Reset regex lastIndex for next iteration
                referencePattern.lastIndex = 0;
            }
            
            return codeLenses;
            
        } catch (error: any) {
            console.error('Error providing CodeLens:', error);
            return codeLenses;
        }
    }
    
    /**
     * Extract session ID from manuscript URI
     * URI format: research-manuscript://session-{sessionId}/v{version}
     */
    private extractSessionId(uri: vscode.Uri): string | null {
        const authority = uri.authority; // session-abc123
        return authority.replace('session-', '');
    }
    
    /**
     * Refresh CodeLens (for future updates)
     */
    public refresh(): void {
        this._onDidChangeCodeLensesEmitter.fire();
    }
}
