/**
 * Manuscript Document Provider
 * 
 * Provides TextDocument content for manuscripts using custom URI scheme.
 * URI format: research-manuscript://session-{sessionId}/v{version}
 * 
 * This allows manuscripts to be opened as .md files in the editor,
 * enabling native editing, syntax highlighting, and CodeLens integration.
 */

import * as vscode from 'vscode';
import { getSessionDetailsV2 } from '../api';

/**
 * Parse manuscript URI to extract session ID and version
 */
interface ManuscriptUri {
  sessionId: string;
  version: number;
}

function parseManuscriptUri(uri: vscode.Uri): ManuscriptUri {
  // URI format: research-manuscript://session-abc123/v2
  const authority = uri.authority; // session-abc123
  const path = uri.path; // /v2

  // Robust session ID extraction - handle potential prefixes or malformed URIs
  let sessionId = authority;
  if (authority.startsWith('session-')) {
    sessionId = authority.replace('session-', '');
  }

  // Validate UUID format - if not valid, try to extract from path or other parts
  const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
  if (!uuidRegex.test(sessionId)) {
    // Try extracting from the full URI string as fallback
    const fullUri = uri.toString();
    const sessionMatch = fullUri.match(/session-([0-9a-fA-F-]{36})/);
    if (sessionMatch) {
      sessionId = sessionMatch[1];
    } else {
      console.warn(`[ManuscriptProvider] Could not extract valid UUID from URI: ${fullUri}`);
      // Return a placeholder that will trigger an error message
      sessionId = 'invalid-session-id';
    }
  }

  const versionMatch = path.match(/^\/v(\d+)$/);
  const version = versionMatch ? parseInt(versionMatch[1], 10) : 1;

  return { sessionId, version };
}

/**
 * Build manuscript URI from session ID and version
 */
export function buildManuscriptUri(sessionId: string, version: number): vscode.Uri {
  return vscode.Uri.parse(`research-manuscript://session-${sessionId}/v${version}`);
}

/**
 * Manuscript Document Provider
 * 
 * Implements vscode.TextDocumentContentProvider to provide
 * markdown content for manuscripts.
 */
export class ManuscriptDocumentProvider implements vscode.TextDocumentContentProvider {
  
  // Event emitter for document changes (for future real-time updates)
  private _onDidChangeEmitter = new vscode.EventEmitter<vscode.Uri>();
  public readonly onDidChange = this._onDidChangeEmitter.event;
  
  // Cache for manuscript content (avoid repeated API calls)
  private contentCache = new Map<string, string>();
  
  /**
   * Provide text document content for a manuscript URI
   */
  async provideTextDocumentContent(uri: vscode.Uri): Promise<string> {
    try {
      const { sessionId, version } = parseManuscriptUri(uri);
      
      // Check cache first
      const cacheKey = `${sessionId}-v${version}`;
      if (this.contentCache.has(cacheKey)) {
        return this.contentCache.get(cacheKey)!;
      }
      
      // Fetch session details
      const details = await getSessionDetailsV2(sessionId);
      
      if (!details) {
        return this.generateErrorContent('Session not found', sessionId);
      }
      
      // Find the specific version from reports
      const reports = details.reports || [];
      
      // Sort reports by created_at to ensure consistent versioning
      const sortedReports = [...reports].sort((a: any, b: any) => 
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      );
      
      // Use 1-based index as version number
      const report = sortedReports[version - 1];
      
      if (!report) {
        return this.generateErrorContent(`Version ${version} not found`, sessionId);
      }
      
      // Generate markdown content
      const content = this.generateManuscriptContent(
        details.session.research_topic,
        report,
        version,
        reports.length,
        details.session.status
      );
      
      // Cache the content
      this.contentCache.set(cacheKey, content);
      
      return content;
      
    } catch (error: any) {
      console.error('Error providing manuscript content:', error);
      return this.generateErrorContent(
        `Failed to load manuscript: ${error.message}`,
        ''
      );
    }
  }
  
  /**
   * Generate markdown content for a manuscript
   */
  private generateManuscriptContent(
    topic: string,
    report: any,
    version: number,
    totalVersions: number,
    status: string
  ): string {
    const content = report.content || 'No content available';
    const createdAt = new Date(report.created_at).toLocaleString();
    const isLatest = version === totalVersions;
    
    // Generate frontmatter
    const frontmatter = [
      '---',
      `title: "${topic}"`,
      `version: ${version}`,
      `total_versions: ${totalVersions}`,
      `status: ${status}`,
      `created_at: ${createdAt}`,
      `is_latest: ${isLatest}`,
      '---',
      ''
    ].join('\n');
    
    // Generate header
    const header = [
      `# ${topic}`,
      '',
      `**Version ${version}** ${isLatest ? '✨ (Latest)' : ''}  `,
      `📅 Created: ${createdAt}  `,
      `📊 Status: ${this.formatStatus(status)}`,
      '',
      '---',
      ''
    ].join('\n');
    
    // Combine
    return frontmatter + header + content;
  }
  
  /**
   * Generate error content when manuscript cannot be loaded
   */
  private generateErrorContent(errorMessage: string, sessionId: string): string {
    return [
      '# ⚠️ Error Loading Manuscript',
      '',
      `**Error:** ${errorMessage}`,
      '',
      sessionId ? `**Session ID:** ${sessionId}` : '',
      '',
      '---',
      '',
      'Please try refreshing the Research Sessions view or check the connection to the backend.',
      '',
      '**Troubleshooting:**',
      '- Ensure the backend is running',
      '- Check that the session exists',
      '- Verify the version number is correct',
      '- Try refreshing the view with the refresh icon'
    ].join('\n');
  }
  
  /**
   * Format status for display
   */
  private formatStatus(status: string): string {
    const statusMap: Record<string, string> = {
      'in_progress': '🔄 In Progress',
      'active': '🔄 Active',
      'completed': '✅ Completed',
      'failed': '❌ Failed',
      'paused': '⏸️ Paused',
      'archived': '📦 Archived'
    };
    return statusMap[status] || status;
  }
  
  /**
   * Extract version number from report object
   * (Currently unused - version is passed directly in openManuscript)
   */
  // private extractVersion(report: any): number {
  //   // Try to extract from title first
  //   if (report.title) {
  //     const match = report.title.match(/v(\d+)/i) || report.title.match(/version\s*(\d+)/i);
  //     if (match) {
  //       return parseInt(match[1], 10);
  //     }
  //   }
  //   
  //   // Fallback: use report ID hash
  //   return report.id ? parseInt(report.id.slice(-4), 16) % 100 : 1;
  // }
  
  /**
   * Refresh a specific manuscript URI
   * (for future real-time updates)
   */
  public refresh(uri: vscode.Uri): void {
    const { sessionId, version } = parseManuscriptUri(uri);
    const cacheKey = `${sessionId}-v${version}`;
    this.contentCache.delete(cacheKey);
    this._onDidChangeEmitter.fire(uri);
  }
  
  /**
   * Clear all cached content
   */
  public clearCache(): void {
    this.contentCache.clear();
  }
}
