/**
 * Research Session Commands
 * 
 * Implements commands for interacting with research sessions,
 * manuscripts, and papers in the Research Sessions Tree View.
 */

import * as vscode from 'vscode';
import { buildManuscriptUri } from '../providers/ManuscriptDocumentProvider';
import { getSessionDetailsV2 } from '../api';

/**
 * Open a manuscript version in the editor as a .md document
 */
export async function openManuscript(sessionId: string, version: number, report?: any): Promise<void> {
    try {
        // If report data is provided directly, use it (like Manuscript Library)
        if (report && report.content) {
            const doc = await vscode.workspace.openTextDocument({
                content: report.content,
                language: 'markdown'
            });
            await vscode.window.showTextDocument(doc, vscode.ViewColumn.Two);
            return;
        }

        // Fallback: use ManuscriptDocumentProvider
        const uri = buildManuscriptUri(sessionId, version);
        const doc = await vscode.workspace.openTextDocument(uri);
        await vscode.window.showTextDocument(doc, {
            preview: false,
            preserveFocus: false
        });
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to open manuscript: ${error.message}`);
        console.error('Error opening manuscript:', error);
    }
}

/**
 * Compare two manuscript versions using VS Code's diff view
 */
export async function compareVersions(
    sessionId: string,
    oldVersion: number,
    newVersion: number
): Promise<void> {
    try {
        const oldUri = buildManuscriptUri(sessionId, oldVersion);
        const newUri = buildManuscriptUri(sessionId, newVersion);
        
        const title = `Version ${oldVersion} ↔ Version ${newVersion}`;
        
        await vscode.commands.executeCommand(
            'vscode.diff',
            oldUri,
            newUri,
            title
        );
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to compare versions: ${error.message}`);
        console.error('Error comparing versions:', error);
    }
}

/**
 * Open paper details (for now, show in webview or new document)
 * TODO: Decide whether to use webview or markdown document
 */
export async function openPaper(sessionId: string, paperIndex: number): Promise<void> {
    try {
        const details = await getSessionDetailsV2(sessionId);
        const papers = details?.papers || [];
        
        if (paperIndex >= papers.length) {
            vscode.window.showErrorMessage('Paper not found');
            return;
        }
        
        const paper = papers[paperIndex];
        
        // Open paper details directly (like Asset Library)
        await vscode.commands.executeCommand('researchAgent.viewPaperDetails', paper);
        
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to open paper: ${error.message}`);
        console.error('Error opening paper:', error);
    }
}

/**
 * Copy BibTeX citation for a paper
 */
export async function copyBibTeX(paper: any): Promise<void> {
    try {
        // Generate BibTeX citation
        const bibtex = generateBibTeX(paper);
        
        await vscode.env.clipboard.writeText(bibtex);
        vscode.window.showInformationMessage('BibTeX citation copied to clipboard');
        
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to copy BibTeX: ${error.message}`);
        console.error('Error copying BibTeX:', error);
    }
}

/**
 * Generate BibTeX citation from paper metadata
 */
function generateBibTeX(paper: any): string {
    const authors = paper.authors?.join(' and ') || 'Unknown';
    const year = paper.year || new Date().getFullYear();
    const title = paper.title || 'Untitled';
    const journal = paper.journal || paper.venue || '';
    const doi = paper.doi || '';
    
    // Generate citation key (first author last name + year)
    const firstAuthor = paper.authors?.[0]?.split(' ').pop() || 'Unknown';
    const citationKey = `${firstAuthor}${year}`;
    
    let bibtex = `@article{${citationKey},\n`;
    bibtex += `  author = {${authors}},\n`;
    bibtex += `  title = {${title}},\n`;
    bibtex += `  year = {${year}}`;
    
    if (journal) {
        bibtex += `,\n  journal = {${journal}}`;
    }
    
    if (doi) {
        bibtex += `,\n  doi = {${doi}}`;
    }
    
    if (paper.url) {
        bibtex += `,\n  url = {${paper.url}}`;
    }
    
    bibtex += `\n}`;
    
    return bibtex;
}

/**
 * Export manuscript to file system
 */
export async function exportManuscript(sessionId: string, version: number): Promise<void> {
    try {
        const details = await getSessionDetailsV2(sessionId);
        
        if (!details) {
            vscode.window.showErrorMessage('Session not found');
            return;
        }
        
        const manuscripts = details.manuscripts || [];
        const manuscript = manuscripts.find((m: any) => {
            const v = extractVersion(m.report_title || m.id);
            return v === version;
        });
        
        if (!manuscript) {
            vscode.window.showErrorMessage(`Version ${version} not found`);
            return;
        }
        
        // Show save dialog
        const defaultFilename = sanitizeFilename(
            `${details.topic}_v${version}.md`
        );
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(defaultFilename),
            filters: {
                'Markdown': ['md'],
                'All Files': ['*']
            }
        });
        
        if (!uri) {
            return; // User cancelled
        }
        
        // Generate content (same as document provider)
        const content = generateManuscriptContent(
            details.topic,
            manuscript,
            version
        );
        
        // Write to file
        await vscode.workspace.fs.writeFile(
            uri,
            Buffer.from(content, 'utf-8')
        );
        
        vscode.window.showInformationMessage(`Manuscript exported to ${uri.fsPath}`);
        
        // Ask if user wants to open the file
        const action = await vscode.window.showInformationMessage(
            'Open exported file?',
            'Yes',
            'No'
        );
        
        if (action === 'Yes') {
            await vscode.commands.executeCommand('vscode.open', uri);
        }
        
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to export manuscript: ${error.message}`);
        console.error('Error exporting manuscript:', error);
    }
}

/**
 * Generate manuscript content (duplicated from DocumentProvider for export)
 */
function generateManuscriptContent(
    topic: string,
    manuscript: any,
    version: number
): string {
    const content = manuscript.report_content || 'No content available';
    const updatedAt = new Date(manuscript.updated_at).toLocaleString();
    
    const frontmatter = [
        '---',
        `title: "${topic}"`,
        `version: ${version}`,
        `updated_at: ${updatedAt}`,
        '---',
        ''
    ].join('\n');
    
    const header = [
        `# ${topic}`,
        '',
        `**Version ${version}**  `,
        `📅 Updated: ${updatedAt}`,
        '',
        '---',
        ''
    ].join('\n');
    
    return frontmatter + header + content;
}

/**
 * Extract version number from report title or ID
 */
function extractVersion(text: string): number {
    const match = text.match(/v(\d+)/i) || text.match(/version\s*(\d+)/i);
    return match ? parseInt(match[1], 10) : 1;
}

/**
 * Sanitize filename to remove invalid characters
 */
function sanitizeFilename(filename: string): string {
    return filename.replace(/[<>:"/\\|?*]/g, '_');
}

/**
 * Download paper PDF (if available)
 */
export async function downloadPDF(paper: any): Promise<void> {
    try {
        // Check if paper has PDF URL
        const pdfUrl = paper.pdf_url || paper.url;
        
        if (!pdfUrl) {
            vscode.window.showWarningMessage('No PDF URL available for this paper');
            return;
        }
        
        // Open PDF URL in external browser
        await vscode.env.openExternal(vscode.Uri.parse(pdfUrl));
        
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to download PDF: ${error.message}`);
        console.error('Error downloading PDF:', error);
    }
}

/**
 * Show session analytics
 */
export async function showSessionAnalytics(sessionId: string): Promise<void> {
    try {
        // Debug: Log incoming sessionId
        console.log('[showSessionAnalytics] Called with sessionId:', sessionId, 'type:', typeof sessionId);
        
        // Validate UUID format
        const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        if (!sessionId || typeof sessionId !== 'string' || !uuidPattern.test(sessionId)) {
            console.error('[showSessionAnalytics] Invalid sessionId format:', sessionId);
            vscode.window.showErrorMessage(`Invalid session ID format: ${sessionId}`);
            return;
        }
        
        const details = await getSessionDetailsV2(sessionId);
        
        if (!details) {
            vscode.window.showErrorMessage('Session not found');
            return;
        }
        
        const manuscripts = details.manuscripts || [];
        const papers = details.papers || [];
        
        const analytics = [
            `📊 Research Session Analytics`,
            ``,
            `**Topic:** ${details.topic}`,
            `**Status:** ${details.status}`,
            `**Created:** ${new Date(details.created_at).toLocaleString()}`,
            `**Updated:** ${new Date(details.updated_at).toLocaleString()}`,
            ``,
            `**Manuscripts:**`,
            `  • Total versions: ${manuscripts.length}`,
            manuscripts.length > 0 ? `  • Latest: v${manuscripts.length}` : '',
            ``,
            `**Papers:**`,
            `  • Total papers: ${papers.length}`,
            papers.length > 0 ? `  • Authors: ${new Set(papers.flatMap((p: any) => p.authors || [])).size}` : '',
            papers.length > 0 ? `  • Years: ${Math.min(...papers.map((p: any) => p.year || 9999))} - ${Math.max(...papers.map((p: any) => p.year || 0))}` : '',
        ].filter(Boolean).join('\n');
        
        // Show in information message or create a document
        const action = await vscode.window.showInformationMessage(
            'View analytics in:',
            'Message',
            'Document'
        );
        
        if (action === 'Document') {
            const doc = await vscode.workspace.openTextDocument({
                content: analytics,
                language: 'markdown'
            });
            await vscode.window.showTextDocument(doc);
        } else {
            vscode.window.showInformationMessage(analytics);
        }
        
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to show analytics: ${error.message}`);
        console.error('Error showing analytics:', error);
    }
}
