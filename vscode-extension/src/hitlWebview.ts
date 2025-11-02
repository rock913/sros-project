/**
 * HITL Decision Card Webview Generator
 * Phase 3.6: Human-in-the-Loop UI Components
 * 
 * Generates interactive decision cards for:
 * 1. Query Approval (approve/reject/modify)
 * 2. Paper Selection (select subset)
 * 3. Report Revision (approve/modify/reject)
 */

export interface HITLRequest {
    request_id: string;
    decision_type: 'query_approval' | 'paper_selection' | 'report_revision';
    prompt: string;
    options: string[];
    context: any;
    timeout_seconds?: number;
    session_id: string;
    thread_id: string;
}

/**
 * Main entry point for generating HITL decision card HTML
 */
export function generateHITLDecisionCardHTML(request: HITLRequest): string {
    const { decision_type } = request;
    
    switch (decision_type) {
        case 'query_approval':
            return generateQueryApprovalCard(request);
        case 'paper_selection':
            return generatePaperSelectionCard(request);
        case 'report_revision':
            return generateReportRevisionCard(request);
        default:
            return generateGenericCard(request);
    }
}

/**
 * Query Approval Card
 * User reviews and approves/rejects/modifies generated search queries
 */
function generateQueryApprovalCard(request: HITLRequest): string {
    const { context, request_id, timeout_seconds } = request;
    const queries = context.queries || [];
    const researchTopic = context.research_topic || 'Research Topic';
    
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Approval</title>
        <style>
            ${getCommonStyles()}
            .query-list {
                background: var(--vscode-editor-background);
                padding: 15px;
                border-radius: 6px;
                margin: 15px 0;
                max-height: 400px;
                overflow-y: auto;
            }
            .query-item {
                padding: 12px;
                margin: 8px 0;
                background: var(--vscode-input-background);
                border-left: 3px solid var(--vscode-textLink-activeForeground);
                border-radius: 4px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .query-number {
                font-weight: bold;
                color: var(--vscode-textLink-activeForeground);
                min-width: 30px;
            }
            .query-text {
                flex: 1;
                font-size: 14px;
                line-height: 1.5;
            }
            .edit-query {
                display: none;
                width: 100%;
                padding: 8px;
                margin-top: 8px;
                background: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                border: 1px solid var(--vscode-input-border);
                border-radius: 4px;
                font-family: inherit;
            }
            .query-item.editing .query-text {
                display: none;
            }
            .query-item.editing .edit-query {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="hitl-card">
            <div class="header">
                <div class="icon">🔍</div>
                <div>
                    <h1>Query Approval Required</h1>
                    <p class="subtitle">Review generated search queries</p>
                </div>
            </div>
            
            <div class="info-box">
                <strong>Research Topic:</strong> ${escapeHtml(researchTopic)}
            </div>
            
            <div class="section">
                <h3>Generated Queries (${queries.length})</h3>
                <div class="query-list" id="queryList">
                    ${queries.map((q: string, i: number) => `
                        <div class="query-item" data-index="${i}">
                            <span class="query-number">${i + 1}.</span>
                            <div style="flex: 1;">
                                <div class="query-text">${escapeHtml(q)}</div>
                                <textarea class="edit-query" data-original="${escapeHtml(q)}">${escapeHtml(q)}</textarea>
                            </div>
                            <button class="btn-secondary" onclick="toggleEdit(${i})">
                                ✏️ Edit
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            ${timeout_seconds ? `
                <div class="warning-box">
                    ⏰ This request will timeout in ${Math.floor(timeout_seconds / 60)} minutes
                </div>
            ` : ''}
            
            <div class="button-group">
                <button class="btn btn-approve" onclick="respond('approve')">
                    ✅ Approve All
                </button>
                <button class="btn btn-primary" onclick="respond('modify')" style="display: none;" id="modifyBtn">
                    💾 Save Changes
                </button>
                <button class="btn btn-reject" onclick="respond('reject')">
                    ❌ Reject & Stop
                </button>
            </div>
            
            <div id="status" class="status-message"></div>
        </div>
        
        <script>
            const vscode = acquireVsCodeApi();
            const requestId = '${request_id}';
            let modifiedQueries = ${JSON.stringify(queries)};
            let hasModifications = false;
            
            function toggleEdit(index) {
                const item = document.querySelector(\`.query-item[data-index="\${index}"]\`);
                const isEditing = item.classList.contains('editing');
                
                if (isEditing) {
                    // Save changes
                    const textarea = item.querySelector('.edit-query');
                    const newValue = textarea.value.trim();
                    if (newValue && newValue !== textarea.dataset.original) {
                        modifiedQueries[index] = newValue;
                        item.querySelector('.query-text').textContent = newValue;
                        hasModifications = true;
                        document.getElementById('modifyBtn').style.display = 'inline-block';
                    }
                    item.classList.remove('editing');
                    item.querySelector('button').textContent = '✏️ Edit';
                } else {
                    // Enter edit mode
                    item.classList.add('editing');
                    item.querySelector('button').textContent = '💾 Save';
                    item.querySelector('.edit-query').focus();
                }
            }
            
            function respond(decision) {
                const statusEl = document.getElementById('status');
                statusEl.textContent = '⏳ Sending response...';
                statusEl.className = 'status-message status-info';
                
                const response = {
                    type: 'hitl_response',
                    request_id: requestId,
                    decision: decision,
                    modified_data: decision === 'modify' ? {
                        queries: modifiedQueries
                    } : null
                };
                
                // Disable all buttons
                document.querySelectorAll('.btn').forEach(btn => btn.disabled = true);
                
                vscode.postMessage(response);
            }
            
            // Handle escape key to close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && !document.querySelector('.editing')) {
                    vscode.postMessage({ type: 'close_webview' });
                }
            });
        </script>
    </body>
    </html>`;
}

/**
 * Paper Selection Card
 * User selects papers from search results (triggered when > 20 papers found)
 */
function generatePaperSelectionCard(request: HITLRequest): string {
    const { context, request_id, timeout_seconds } = request;
    const papers = context.papers || [];
    const totalCount = context.total_count || papers.length;
    
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Paper Selection</title>
        <style>
            ${getCommonStyles()}
            .paper-list {
                max-height: 500px;
                overflow-y: auto;
                margin: 15px 0;
            }
            .paper-item {
                background: var(--vscode-editor-background);
                padding: 15px;
                margin: 10px 0;
                border-radius: 6px;
                border: 2px solid transparent;
                transition: all 0.2s;
                cursor: pointer;
            }
            .paper-item:hover {
                border-color: var(--vscode-textLink-activeForeground);
            }
            .paper-item.selected {
                background: var(--vscode-list-activeSelectionBackground);
                border-color: var(--vscode-textLink-activeForeground);
            }
            .paper-checkbox {
                float: right;
                transform: scale(1.3);
                cursor: pointer;
            }
            .paper-title {
                font-weight: bold;
                font-size: 15px;
                margin-bottom: 8px;
                color: var(--vscode-textLink-foreground);
            }
            .paper-meta {
                font-size: 13px;
                color: var(--vscode-descriptionForeground);
                margin-bottom: 8px;
            }
            .paper-abstract {
                font-size: 13px;
                line-height: 1.5;
                color: var(--vscode-foreground);
                opacity: 0.9;
            }
            .selection-stats {
                background: var(--vscode-textBlockQuote-background);
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .filter-box {
                margin-bottom: 15px;
                display: flex;
                gap: 10px;
            }
            .filter-input {
                flex: 1;
                padding: 8px 12px;
                background: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                border: 1px solid var(--vscode-input-border);
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="hitl-card">
            <div class="header">
                <div class="icon">📄</div>
                <div>
                    <h1>Paper Selection Required</h1>
                    <p class="subtitle">Found ${totalCount} papers - select papers to analyze</p>
                </div>
            </div>
            
            <div class="selection-stats">
                <div>
                    <strong id="selectedCount">0</strong> / ${papers.length} papers selected
                </div>
                <div>
                    <button class="btn-secondary" onclick="selectAll()">Select All</button>
                    <button class="btn-secondary" onclick="clearAll()">Clear All</button>
                </div>
            </div>
            
            ${papers.length > 10 ? `
                <div class="filter-box">
                    <input type="text" class="filter-input" id="filterInput" 
                           placeholder="🔍 Filter papers by title or author..." 
                           onkeyup="filterPapers()">
                </div>
            ` : ''}
            
            <div class="info-box">
                💡 <strong>Recommendation:</strong> ${context.recommendation || 'Select 10-20 most relevant papers for detailed analysis'}
            </div>
            
            <div class="paper-list" id="paperList">
                ${papers.map((paper: any, i: number) => `
                    <div class="paper-item" data-index="${i}" onclick="togglePaper(${i})">
                        <input type="checkbox" class="paper-checkbox" data-doi="${escapeHtml(paper.doi || '')}" 
                               onchange="updateSelection()">
                        <div class="paper-title">${escapeHtml(paper.title || 'Untitled')}</div>
                        <div class="paper-meta">
                            ${paper.authors?.join(', ') || 'Unknown authors'} 
                            ${paper.year ? `(${paper.year})` : ''}
                        </div>
                        ${paper.abstract ? `
                            <div class="paper-abstract">${escapeHtml(paper.abstract)}</div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
            
            ${timeout_seconds ? `
                <div class="warning-box">
                    ⏰ This request will timeout in ${Math.floor(timeout_seconds / 60)} minutes
                </div>
            ` : ''}
            
            <div class="button-group">
                <button class="btn btn-approve" onclick="respond('select_subset')" id="submitBtn" disabled>
                    ✅ Submit Selection (<span id="submitCount">0</span>)
                </button>
                <button class="btn btn-primary" onclick="respond('select_all')">
                    📚 Analyze All Papers
                </button>
                <button class="btn btn-reject" onclick="respond('reject')">
                    ❌ Cancel Research
                </button>
            </div>
            
            <div id="status" class="status-message"></div>
        </div>
        
        <script>
            const vscode = acquireVsCodeApi();
            const requestId = '${request_id}';
            const papers = ${JSON.stringify(papers)};
            
            function togglePaper(index) {
                const item = document.querySelector(\`.paper-item[data-index="\${index}"]\`);
                const checkbox = item.querySelector('.paper-checkbox');
                checkbox.checked = !checkbox.checked;
                updateSelection();
            }
            
            function updateSelection() {
                const checkboxes = document.querySelectorAll('.paper-checkbox:checked');
                const count = checkboxes.length;
                
                document.getElementById('selectedCount').textContent = count;
                document.getElementById('submitCount').textContent = count;
                document.getElementById('submitBtn').disabled = count === 0;
                
                // Update visual state
                document.querySelectorAll('.paper-item').forEach((item, i) => {
                    const checkbox = item.querySelector('.paper-checkbox');
                    if (checkbox.checked) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                });
            }
            
            function selectAll() {
                document.querySelectorAll('.paper-checkbox').forEach(cb => cb.checked = true);
                updateSelection();
            }
            
            function clearAll() {
                document.querySelectorAll('.paper-checkbox').forEach(cb => cb.checked = false);
                updateSelection();
            }
            
            function filterPapers() {
                const query = document.getElementById('filterInput').value.toLowerCase();
                document.querySelectorAll('.paper-item').forEach((item, i) => {
                    const paper = papers[i];
                    const text = (paper.title + ' ' + (paper.authors?.join(' ') || '')).toLowerCase();
                    item.style.display = text.includes(query) ? 'block' : 'none';
                });
            }
            
            function respond(decision) {
                const statusEl = document.getElementById('status');
                statusEl.textContent = '⏳ Sending response...';
                statusEl.className = 'status-message status-info';
                
                let selectedPapers = [];
                if (decision === 'select_subset') {
                    const selected = document.querySelectorAll('.paper-checkbox:checked');
                    selectedPapers = Array.from(selected).map((cb, i) => {
                        const index = parseInt(cb.closest('.paper-item').dataset.index);
                        return papers[index];
                    });
                }
                
                const response = {
                    type: 'hitl_response',
                    request_id: requestId,
                    decision: decision,
                    modified_data: decision === 'select_subset' ? {
                        selected_papers: selectedPapers
                    } : null
                };
                
                document.querySelectorAll('.btn').forEach(btn => btn.disabled = true);
                vscode.postMessage(response);
            }
        </script>
    </body>
    </html>`;
}

/**
 * Report Revision Card
 * User reviews and provides feedback on generated report
 */
function generateReportRevisionCard(request: HITLRequest): string {
    const { context, request_id, timeout_seconds } = request;
    const report = context.report || '';
    const wordCount = context.word_count || 0;
    const researchTopic = context.research_topic || 'Research Topic';
    
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report Revision</title>
        <style>
            ${getCommonStyles()}
            .report-preview {
                background: var(--vscode-editor-background);
                padding: 20px;
                border-radius: 6px;
                margin: 15px 0;
                max-height: 500px;
                overflow-y: auto;
                font-family: var(--vscode-editor-font-family);
                font-size: 14px;
                line-height: 1.8;
                white-space: pre-wrap;
            }
            .feedback-area {
                width: 100%;
                min-height: 100px;
                padding: 12px;
                background: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                border: 1px solid var(--vscode-input-border);
                border-radius: 4px;
                font-family: inherit;
                font-size: 14px;
                resize: vertical;
                margin: 15px 0;
            }
            .report-stats {
                display: flex;
                gap: 20px;
                margin: 15px 0;
                padding: 12px;
                background: var(--vscode-textBlockQuote-background);
                border-radius: 6px;
            }
            .stat-item {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .stat-value {
                font-weight: bold;
                color: var(--vscode-textLink-activeForeground);
            }
        </style>
    </head>
    <body>
        <div class="hitl-card">
            <div class="header">
                <div class="icon">📝</div>
                <div>
                    <h1>Report Review Required</h1>
                    <p class="subtitle">Review and approve the research report</p>
                </div>
            </div>
            
            <div class="info-box">
                <strong>Research Topic:</strong> ${escapeHtml(researchTopic)}
            </div>
            
            <div class="report-stats">
                <div class="stat-item">
                    <span>📊 Word Count:</span>
                    <span class="stat-value">${wordCount}</span>
                </div>
                <div class="stat-item">
                    <span>📄 Papers Analyzed:</span>
                    <span class="stat-value">${context.paper_count || 0}</span>
                </div>
            </div>
            
            <div class="section">
                <h3>Generated Report</h3>
                <div class="report-preview">${escapeHtml(report)}</div>
            </div>
            
            <div class="section" id="feedbackSection" style="display: none;">
                <h3>Modification Feedback</h3>
                <textarea class="feedback-area" id="feedbackText" 
                          placeholder="Please provide specific feedback on what should be changed...

Examples:
- Add more details about methodology
- Focus more on recent papers (2023-2024)
- Include more quantitative results
- Expand the conclusion section"></textarea>
            </div>
            
            ${timeout_seconds ? `
                <div class="warning-box">
                    ⏰ This request will timeout in ${Math.floor(timeout_seconds / 60)} minutes
                </div>
            ` : ''}
            
            <div class="button-group">
                <button class="btn btn-approve" onclick="respond('approve')">
                    ✅ Approve Report
                </button>
                <button class="btn btn-primary" onclick="showFeedback()">
                    ✏️ Request Modifications
                </button>
                <button class="btn btn-secondary" onclick="copyReport()">
                    📋 Copy to Clipboard
                </button>
                <button class="btn btn-reject" onclick="respond('reject')">
                    ❌ Reject & Stop
                </button>
            </div>
            
            <div id="status" class="status-message"></div>
        </div>
        
        <script>
            const vscode = acquireVsCodeApi();
            const requestId = '${request_id}';
            
            function showFeedback() {
                const section = document.getElementById('feedbackSection');
                if (section.style.display === 'none') {
                    section.style.display = 'block';
                    document.getElementById('feedbackText').focus();
                    event.target.textContent = '💾 Submit Feedback';
                    event.target.onclick = () => respond('modify');
                } else {
                    respond('modify');
                }
            }
            
            function copyReport() {
                const report = \`${report.replace(/`/g, '\\`')}\`;
                vscode.postMessage({
                    type: 'copy_to_clipboard',
                    text: report
                });
                
                const statusEl = document.getElementById('status');
                statusEl.textContent = '✅ Report copied to clipboard!';
                statusEl.className = 'status-message status-success';
                setTimeout(() => {
                    statusEl.textContent = '';
                }, 3000);
            }
            
            function respond(decision) {
                const statusEl = document.getElementById('status');
                
                if (decision === 'modify') {
                    const feedback = document.getElementById('feedbackText').value.trim();
                    if (!feedback) {
                        statusEl.textContent = '⚠️ Please provide feedback before submitting';
                        statusEl.className = 'status-message status-error';
                        return;
                    }
                }
                
                statusEl.textContent = '⏳ Sending response...';
                statusEl.className = 'status-message status-info';
                
                const response = {
                    type: 'hitl_response',
                    request_id: requestId,
                    decision: decision,
                    modified_data: decision === 'modify' ? {
                        feedback: document.getElementById('feedbackText').value.trim()
                    } : null
                };
                
                document.querySelectorAll('.btn').forEach(btn => btn.disabled = true);
                vscode.postMessage(response);
            }
        </script>
    </body>
    </html>`;
}

/**
 * Generic fallback card for unknown decision types
 */
function generateGenericCard(request: HITLRequest): string {
    const { prompt, options, request_id } = request;
    
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>${getCommonStyles()}</style>
    </head>
    <body>
        <div class="hitl-card">
            <h1>Decision Required</h1>
            <p>${escapeHtml(prompt)}</p>
            <div class="button-group">
                ${options.map(opt => `
                    <button class="btn btn-primary" onclick="respond('${escapeHtml(opt)}')">
                        ${escapeHtml(opt)}
                    </button>
                `).join('')}
            </div>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            function respond(decision) {
                vscode.postMessage({
                    type: 'hitl_response',
                    request_id: '${request_id}',
                    decision: decision
                });
            }
        </script>
    </body>
    </html>`;
}

/**
 * Common CSS styles for all HITL cards
 */
function getCommonStyles(): string {
    return `
        * {
            box-sizing: border-box;
        }
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 20px;
            margin: 0;
            line-height: 1.6;
        }
        .hitl-card {
            max-width: 900px;
            margin: 0 auto;
            background: var(--vscode-editor-inactiveSelectionBackground);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--vscode-panel-border);
        }
        .icon {
            font-size: 48px;
            line-height: 1;
        }
        h1 {
            margin: 0;
            font-size: 24px;
            color: var(--vscode-titleBar-activeForeground);
        }
        .subtitle {
            margin: 5px 0 0 0;
            font-size: 14px;
            color: var(--vscode-descriptionForeground);
        }
        .section {
            margin: 25px 0;
        }
        h3 {
            margin: 0 0 12px 0;
            font-size: 16px;
            color: var(--vscode-textLink-foreground);
        }
        .info-box {
            background: var(--vscode-textBlockQuote-background);
            border-left: 4px solid var(--vscode-textLink-activeForeground);
            padding: 12px 16px;
            margin: 15px 0;
            border-radius: 4px;
            font-size: 14px;
        }
        .warning-box {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 12px 16px;
            margin: 15px 0;
            border-radius: 4px;
            font-size: 14px;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 25px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .btn-approve {
            background: #4caf50;
            color: white;
        }
        .btn-primary {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        .btn-secondary {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        .btn-reject {
            background: #f44336;
            color: white;
        }
        .status-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 4px;
            font-size: 14px;
            display: none;
        }
        .status-message:not(:empty) {
            display: block;
        }
        .status-info {
            background: rgba(33, 150, 243, 0.1);
            border-left: 4px solid #2196f3;
        }
        .status-success {
            background: rgba(76, 175, 80, 0.1);
            border-left: 4px solid #4caf50;
        }
        .status-error {
            background: rgba(244, 67, 54, 0.1);
            border-left: 4px solid #f44336;
        }
    `;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(unsafe: string): string {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
