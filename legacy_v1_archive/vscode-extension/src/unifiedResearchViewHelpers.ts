/**
 * Phase 3.7: Helper Functions for Unified Research View
 * 
 * Utility functions for HTML generation, formatting, and interactions
 */

/**
 * Get CSS styles for the unified view
 */
export function getStyles(): string {
    return `
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            overflow: hidden;
        }
        
        /* Main Container */
        .unified-container {
            display: flex;
            height: 100vh;
            width: 100vw;
        }
        
        /* Left Panel: Session List (30%) */
        .session-list-panel {
            width: 30%;
            min-width: 280px;
            max-width: 400px;
            border-right: 1px solid var(--vscode-panel-border);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .panel-header h2 {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }
        
        .new-session-btn {
            padding: 6px 12px;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
        }
        
        .new-session-btn:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        /* Search and Filter */
        .search-filter-section {
            padding: 12px 16px;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .search-input {
            width: 100%;
            padding: 8px 12px;
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            font-size: 13px;
            margin-bottom: 8px;
        }
        
        .search-input:focus {
            outline: 1px solid var(--vscode-focusBorder);
        }
        
        .filter-chips {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }
        
        .filter-chip {
            padding: 4px 10px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            color: var(--vscode-foreground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 12px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        
        .filter-chip:hover {
            background-color: var(--vscode-list-hoverBackground);
        }
        
        .filter-chip.active {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border-color: var(--vscode-button-background);
        }
        
        /* Session Cards Container */
        .session-cards-container {
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }
        
        .session-card {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .session-card:hover {
            background-color: var(--vscode-list-hoverBackground);
            border-color: var(--vscode-focusBorder);
        }
        
        .session-card.selected {
            background-color: var(--vscode-list-activeSelectionBackground);
            border-color: var(--vscode-focusBorder);
            border-width: 2px;
            padding: 11px; /* Compensate for border width */
        }
        
        .session-card-header {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .status-icon {
            font-size: 18px;
            flex-shrink: 0;
        }
        
        .session-topic {
            font-size: 14px;
            font-weight: 600;
            margin: 0;
            line-height: 1.4;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        
        .session-card-meta {
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .meta-item .icon {
            font-size: 14px;
        }
        
        .load-more-btn {
            padding: 10px;
            text-align: center;
            background-color: transparent;
            color: var(--vscode-textLink-foreground);
            border: none;
            cursor: pointer;
            font-size: 13px;
        }
        
        .load-more-btn:hover {
            text-decoration: underline;
        }
        
        .empty-sessions {
            padding: 40px 20px;
            text-align: center;
            color: var(--vscode-descriptionForeground);
        }
        
        .empty-sessions .hint {
            font-size: 12px;
            margin-top: 8px;
        }
        
        /* Right Panel: Session Details (70%) */
        .session-details-panel {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        
        .session-info-card {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 20px;
        }
        
        .info-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        
        .info-header h2 {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
            flex: 1;
        }
        
        .status-badge {
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 12px;
        }
        
        .status-badge.status-completed {
            background-color: #10b981;
            color: white;
        }
        
        .status-badge.status-in_progress {
            background-color: #3b82f6;
            color: white;
        }
        
        .status-badge.status-paused {
            background-color: #f59e0b;
            color: white;
        }
        
        .status-badge.status-failed {
            background-color: #ef4444;
            color: white;
        }
        
        .info-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 13px;
            color: var(--vscode-descriptionForeground);
        }
        
        /* Manuscript Section */
        .manuscript-section {
            margin-bottom: 30px;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--vscode-panel-border);
        }
        
        .section-header h3 {
            font-size: 18px;
            font-weight: 600;
            margin: 0;
        }
        
        .manuscript-actions {
            display: flex;
            gap: 8px;
        }
        
        .action-btn {
            padding: 6px 12px;
            background-color: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
            border: 1px solid var(--vscode-button-border);
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: background-color 0.2s;
        }
        
        .action-btn:hover {
            background-color: var(--vscode-button-secondaryHoverBackground);
        }
        
        .action-btn.primary {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
        }
        
        .action-btn.primary:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
        
        .manuscript-content {
            background-color: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
            padding: 20px;
            line-height: 1.8;
        }
        
        /* Markdown styling */
        .markdown-body h1 {
            font-size: 28px;
            margin: 24px 0 16px;
            border-bottom: 2px solid var(--vscode-panel-border);
            padding-bottom: 8px;
        }
        
        .markdown-body h2 {
            font-size: 22px;
            margin: 20px 0 12px;
        }
        
        .markdown-body h3 {
            font-size: 18px;
            margin: 16px 0 10px;
        }
        
        .markdown-body p {
            margin: 12px 0;
        }
        
        .markdown-body a {
            color: var(--vscode-textLink-foreground);
            text-decoration: none;
        }
        
        .markdown-body a:hover {
            text-decoration: underline;
        }
        
        .markdown-body code {
            background-color: var(--vscode-textCodeBlock-background);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: var(--vscode-editor-font-family);
            font-size: 0.9em;
        }
        
        .markdown-body pre {
            background-color: var(--vscode-textCodeBlock-background);
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
        }
        
        /* Reference links in manuscript */
        .reference-link {
            color: var(--vscode-textLink-foreground);
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .reference-link:hover {
            text-decoration: underline;
            background-color: var(--vscode-editor-hoverHighlightBackground);
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        /* Papers Section */
        .papers-section {
            margin-bottom: 30px;
        }
        
        .paper-search {
            padding: 6px 12px;
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            font-size: 13px;
            width: 250px;
        }
        
        .papers-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        /* Paper Card */
        .paper-card {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
            padding: 16px;
            transition: all 0.3s;
            scroll-margin-top: 20px; /* For smooth scroll to target */
        }
        
        .paper-card.highlighted {
            border-color: var(--vscode-focusBorder);
            border-width: 2px;
            padding: 15px; /* Compensate for border */
            background-color: var(--vscode-list-activeSelectionBackground);
        }
        
        .paper-header {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 12px;
        }
        
        .reference-badge {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 700;
            flex-shrink: 0;
        }
        
        .paper-title {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
            line-height: 1.4;
        }
        
        .paper-authors {
            font-size: 13px;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 8px;
        }
        
        .paper-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 8px;
        }
        
        .paper-links {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 12px;
            margin-bottom: 12px;
        }
        
        .paper-links span {
            color: var(--vscode-textLink-foreground);
        }
        
        .paper-abstract {
            margin: 12px 0;
        }
        
        .toggle-abstract-btn {
            background: transparent;
            border: none;
            color: var(--vscode-textLink-foreground);
            cursor: pointer;
            font-size: 13px;
            padding: 4px 0;
        }
        
        .toggle-abstract-btn:hover {
            text-decoration: underline;
        }
        
        .abstract-content {
            margin-top: 8px;
            padding: 12px;
            background-color: var(--vscode-editor-background);
            border-left: 3px solid var(--vscode-textLink-foreground);
            border-radius: 4px;
        }
        
        .abstract-content p {
            margin: 0;
            line-height: 1.6;
            font-size: 13px;
        }
        
        .paper-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        
        /* Empty States */
        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--vscode-descriptionForeground);
            text-align: center;
            padding: 40px;
        }
        
        .empty-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .empty-state h3 {
            font-size: 18px;
            margin-bottom: 12px;
        }
        
        .empty-state p {
            margin: 8px 0;
        }
        
        .empty-state .hint {
            font-size: 13px;
            opacity: 0.7;
        }
        
        .empty-manuscript, .empty-papers {
            padding: 40px;
            text-align: center;
            color: var(--vscode-descriptionForeground);
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px dashed var(--vscode-panel-border);
            border-radius: 6px;
            margin: 20px 0;
        }
        
        .empty-manuscript p, .empty-papers p {
            margin: 8px 0;
        }
        
        .empty-manuscript .hint {
            font-size: 13px;
            opacity: 0.7;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--vscode-scrollbarSlider-background);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--vscode-scrollbarSlider-hoverBackground);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--vscode-scrollbarSlider-activeBackground);
        }
    `;
}

/**
 * Get JavaScript code for the unified view
 */
export function getJavaScript(): string {
    return `
        const vscode = acquireVsCodeApi();
        
        // Select a session
        function selectSession(sessionId) {
            vscode.postMessage({
                command: 'selectSession',
                sessionId: sessionId
            });
        }
        
        // Create new session
        function createNewSession() {
            vscode.postMessage({
                command: 'createNewSession'
            });
        }
        
        // Handle search
        function handleSearch(query) {
            const cards = document.querySelectorAll('.session-card');
            cards.forEach(card => {
                const topic = card.querySelector('.session-topic').textContent.toLowerCase();
                if (topic.includes(query.toLowerCase())) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Handle filter
        function handleFilter(filter) {
            // Update active filter chip
            document.querySelectorAll('.filter-chip').forEach(chip => {
                chip.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Filter sessions
            const cards = document.querySelectorAll('.session-card');
            cards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                } else {
                    const statusIcon = card.querySelector('.status-icon').textContent;
                    const shouldShow = (
                        (filter === 'completed' && statusIcon === '✅') ||
                        (filter === 'in_progress' && statusIcon === '🔄') ||
                        (filter === 'failed' && statusIcon === '❌')
                    );
                    card.style.display = shouldShow ? 'block' : 'none';
                }
            });
        }
        
        // Load more sessions
        function loadMoreSessions() {
            vscode.postMessage({
                command: 'loadMoreSessions'
            });
        }
        
        // Toggle paper abstract
        function toggleAbstract(referenceNumber) {
            const abstractEl = document.getElementById('abstract-' + referenceNumber);
            const button = event.target;
            
            if (abstractEl.style.display === 'none') {
                abstractEl.style.display = 'block';
                button.textContent = '▲ Hide Abstract';
            } else {
                abstractEl.style.display = 'none';
                button.textContent = '▼ Show Abstract';
            }
        }
        
        // Scroll to paper when reference is clicked
        function scrollToPaper(referenceNumber) {
            const paperCard = document.getElementById('paper-' + referenceNumber);
            if (paperCard) {
                // Scroll to paper
                paperCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Highlight the paper temporarily
                paperCard.classList.add('highlighted');
                setTimeout(() => {
                    paperCard.classList.remove('highlighted');
                }, 3000);
            }
        }
        
        // Export manuscript
        function exportManuscript(format) {
            vscode.postMessage({
                command: 'exportManuscript',
                format: format
            });
        }
        
        // Open PDF
        function openPDF(paperId) {
            vscode.postMessage({
                command: 'openPDF',
                paperId: paperId
            });
        }
        
        // Open URL
        function openURL(url) {
            vscode.postMessage({
                command: 'openURL',
                url: url
            });
        }
        
        // Copy BibTeX
        function copyBibTeX(paperId) {
            vscode.postMessage({
                command: 'copyBibTeX',
                paperId: paperId
            });
        }
        
        // Handle paper search
        function handlePaperSearch(query) {
            const papers = document.querySelectorAll('.paper-card');
            papers.forEach(paper => {
                const title = paper.querySelector('.paper-title').textContent.toLowerCase();
                const authors = paper.querySelector('.paper-authors').textContent.toLowerCase();
                if (title.includes(query.toLowerCase()) || authors.includes(query.toLowerCase())) {
                    paper.style.display = 'block';
                } else {
                    paper.style.display = 'none';
                }
            });
        }
    `;
}

/**
 * Utility functions
 */
export function getStatusIcon(status: string): string {
    const icons: Record<string, string> = {
        'completed': '✅',
        'in_progress': '🔄',
        'paused': '⏸️',
        'failed': '❌'
    };
    return icons[status] || '📊';
}

export function getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
        'completed': 'Completed',
        'in_progress': 'In Progress',
        'paused': 'Paused',
        'failed': 'Failed'
    };
    return labels[status] || status;
}

export function truncate(text: string, maxLength: number): string {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

export function escapeHtml(text: string): string {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

export function formatDate(isoString: string): string {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 60) {
        return `${diffMins}m ago`;
    } else if (diffHours < 24) {
        return `${diffHours}h ago`;
    } else if (diffDays < 7) {
        return `${diffDays}d ago`;
    } else {
        return date.toLocaleDateString();
    }
}

export function formatDateFull(isoString: string): string {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Process manuscript markdown to make references clickable
 */
export function processManuscriptReferences(markdown: string, _papers: any[]): string {
    // Simple markdown to HTML conversion (you may want to use a library like marked.js)
    let html = markdown
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^\s*$/gm, '')
        .replace(/^(.+)$/gm, '<p>$1</p>');
    
    // Make references clickable: [1] -> <a href="#" onclick="scrollToPaper(1)">[1]</a>
    html = html.replace(/\[(\d+)\]/g, (_match, num) => {
        return `<a href="#" class="reference-link" onclick="scrollToPaper(${num}); return false;" title="Click to view paper #${num}">[${num}]</a>`;
    });
    
    return html;
}
