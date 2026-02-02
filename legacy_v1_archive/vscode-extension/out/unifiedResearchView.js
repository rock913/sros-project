"use strict";
/**
 * Phase 3.7: Unified Research View
 * Main view generator for master-detail layout
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateUnifiedResearchViewHTML = generateUnifiedResearchViewHTML;
const unifiedResearchViewHelpers_1 = require("./unifiedResearchViewHelpers");
function generateUnifiedResearchViewHTML(sessions, selectedSessionId, sessionDetails) {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Research Sessions</title>
            <style>${(0, unifiedResearchViewHelpers_1.getStyles)()}</style>
        </head>
        <body>
            <div class="unified-container">
                <div class="session-list-panel">
                    <div class="panel-header">
                        <h2>Research Sessions</h2>
                        <button class="new-session-btn" onclick="createNewSession()">+ New Session</button>
                    </div>
                    <div class="search-filter-section">
                        <input type="text" class="search-input" placeholder="Search sessions..." oninput="handleSearch(this.value)"/>
                        <div class="filter-chips">
                            <button class="filter-chip active" onclick="handleFilter('all')">All</button>
                            <button class="filter-chip" onclick="handleFilter('completed')">Completed</button>
                            <button class="filter-chip" onclick="handleFilter('in_progress')">In Progress</button>
                            <button class="filter-chip" onclick="handleFilter('failed')">Failed</button>
                        </div>
                    </div>
                    ${generateSessionCards(sessions, selectedSessionId)}
                </div>
                <div class="session-details-panel">
                    ${generateSessionDetailsContent(sessionDetails)}
                </div>
            </div>
            <script>${(0, unifiedResearchViewHelpers_1.getJavaScript)()}</script>
        </body>
        </html>
    `;
}
function generateSessionCards(sessions, selectedSessionId) {
    if (sessions.length === 0) {
        return `
            <div class="empty-sessions">
                <div class="empty-icon">📚</div>
                <h3>No research sessions yet</h3>
                <p>Click "+ New Session" to start your first research</p>
            </div>
        `;
    }
    const cardsHTML = sessions.map(session => {
        const isSelected = session.id === selectedSessionId;
        const statusIcon = (0, unifiedResearchViewHelpers_1.getStatusIcon)(session.status);
        const truncatedTopic = (0, unifiedResearchViewHelpers_1.truncate)(session.research_topic, 80);
        return `
            <div class="session-card ${isSelected ? 'selected' : ''}" onclick="selectSession('${session.id}')" data-status="${session.status}">
                <div class="session-card-header">
                    <span class="status-icon">${statusIcon}</span>
                    <h3 class="session-topic" title="${(0, unifiedResearchViewHelpers_1.escapeHtml)(session.research_topic)}">${(0, unifiedResearchViewHelpers_1.escapeHtml)(truncatedTopic)}</h3>
                </div>
                <div class="session-card-meta">
                    <div class="meta-item"><span class="icon">📄</span><span>${session.paper_count} papers</span></div>
                    <div class="meta-item"><span class="icon">��</span><span>${(0, unifiedResearchViewHelpers_1.formatDate)(session.updated_at)}</span></div>
                </div>
            </div>
        `;
    }).join('');
    return `
        <div class="session-cards-container">
            ${cardsHTML}
            ${sessions.length >= 20 ? '<button class="load-more-btn" onclick="loadMoreSessions()">Load more...</button>' : ''}
        </div>
    `;
}
function generateSessionDetailsContent(sessionDetails) {
    if (!sessionDetails) {
        return `
            <div class="empty-state">
                <div class="empty-icon">👈</div>
                <h3>Select a session to view details</h3>
                <p>Choose a session from the left panel</p>
            </div>
        `;
    }
    const session = sessionDetails.session;
    const manuscript = sessionDetails.manuscript;
    const papers = sessionDetails.papers;
    const stats = sessionDetails.stats;
    return `
        <div class="session-info-card">
            <div class="info-header">
                <h2>${(0, unifiedResearchViewHelpers_1.escapeHtml)(session.research_topic)}</h2>
                <span class="status-badge status-${session.status}">${(0, unifiedResearchViewHelpers_1.getStatusLabel)(session.status)}</span>
            </div>
            <div class="info-meta">
                <span>📅 Created: ${(0, unifiedResearchViewHelpers_1.formatDateFull)(session.created_at)}</span>
                <span>🔄 Updated: ${(0, unifiedResearchViewHelpers_1.formatDateFull)(session.updated_at)}</span>
                <span>📊 Papers: ${stats.total_papers}</span>
                <span>📝 Reports: ${stats.total_reports}</span>
            </div>
        </div>
        ${generateManuscriptSection(manuscript, papers)}
        ${generatePapersSection(papers)}
    `;
}
function generateManuscriptSection(manuscript, papers) {
    if (!manuscript || !manuscript.content) {
        return `
            <div class="empty-manuscript">
                <h3>📝 No Manuscript Yet</h3>
                <p>The manuscript will appear here once the research is complete</p>
            </div>
        `;
    }
    const processedContent = (0, unifiedResearchViewHelpers_1.processManuscriptReferences)(manuscript.content, papers);
    return `
        <div class="manuscript-section">
            <div class="section-header">
                <h3>📝 Research Manuscript</h3>
                <div class="manuscript-actions">
                    <button class="action-btn" onclick="exportManuscript('md')">Export MD</button>
                    <button class="action-btn primary" onclick="exportManuscript('pdf')">Export PDF</button>
                </div>
            </div>
            <div class="manuscript-content markdown-body">${processedContent}</div>
        </div>
    `;
}
function generatePapersSection(papers) {
    if (!papers || papers.length === 0) {
        return `
            <div class="empty-papers">
                <h3>📚 No Papers Yet</h3>
                <p>Papers will appear here once the agent finds relevant research</p>
            </div>
        `;
    }
    return `
        <div class="papers-section">
            <div class="section-header">
                <h3>📚 Referenced Papers (${papers.length})</h3>
                <input type="text" class="paper-search" placeholder="Search papers..." oninput="handlePaperSearch(this.value)"/>
            </div>
            <div class="papers-container">
                ${papers.map((paper, index) => generatePaperCard(paper, index + 1)).join('')}
            </div>
        </div>
    `;
}
function generatePaperCard(paper, referenceNumber) {
    const authors = paper.authors.slice(0, 3).join(', ') + (paper.authors.length > 3 ? ' et al.' : '');
    const hasAbstract = paper.abstract && paper.abstract.length > 0;
    return `
        <div class="paper-card" id="paper-${referenceNumber}">
            <div class="paper-header">
                <div class="reference-badge">[${referenceNumber}]</div>
                <h4 class="paper-title">${(0, unifiedResearchViewHelpers_1.escapeHtml)(paper.title)}</h4>
            </div>
            <div class="paper-authors">${(0, unifiedResearchViewHelpers_1.escapeHtml)(authors)}</div>
            <div class="paper-meta">
                ${paper.year ? `<span>📅 ${paper.year}</span>` : ''}
                ${paper.publication ? `<span>📖 ${(0, unifiedResearchViewHelpers_1.escapeHtml)(paper.publication)}</span>` : ''}
                ${paper.citation_count ? `<span>📊 ${paper.citation_count} citations</span>` : ''}
            </div>
            <div class="paper-links">
                ${paper.doi ? `<span>DOI: <a href="https://doi.org/${paper.doi}" onclick="openURL('https://doi.org/${paper.doi}'); return false;">${paper.doi}</a></span>` : ''}
                ${paper.arxiv_id ? `<span>arXiv: <a href="https://arxiv.org/abs/${paper.arxiv_id}" onclick="openURL('https://arxiv.org/abs/${paper.arxiv_id}'); return false;">${paper.arxiv_id}</a></span>` : ''}
            </div>
            ${hasAbstract ? `
                <div class="paper-abstract">
                    <button class="toggle-abstract-btn" onclick="toggleAbstract(${referenceNumber})">▼ Show Abstract</button>
                    <div class="abstract-content" id="abstract-${referenceNumber}" style="display: none;">
                        <p>${(0, unifiedResearchViewHelpers_1.escapeHtml)(paper.abstract)}</p>
                    </div>
                </div>
            ` : ''}
            <div class="paper-actions">
                ${paper.pdf_url ? `<button class="action-btn primary" onclick="openPDF('${paper.id}')">📄 Open PDF</button>` : ''}
                ${paper.url ? `<button class="action-btn" onclick="openURL('${(0, unifiedResearchViewHelpers_1.escapeHtml)(paper.url)}')">🔗 View Online</button>` : ''}
                <button class="action-btn" onclick="copyBibTeX('${paper.id}')">📋 Copy BibTeX</button>
            </div>
        </div>
    `;
}
//# sourceMappingURL=unifiedResearchView.js.map