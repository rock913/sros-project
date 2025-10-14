"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkHealth = checkHealth;
exports.getAgentState = getAgentState;
exports.getAllPapers = getAllPapers;
exports.getPaperById = getPaperById;
exports.exportPapers = exportPapers;
exports.getAllReports = getAllReports;
exports.getReportById = getReportById;
exports.getLatestReport = getLatestReport;
exports.exportReport = exportReport;
exports.compareReports = compareReports;
exports.getAllSessions = getAllSessions;
exports.startResearchStream = startResearchStream;
exports.getSessionsList = getSessionsList;
exports.getSessionStats = getSessionStats;
exports.getPaperTrends = getPaperTrends;
exports.getSessionDetails = getSessionDetails;
exports.getSessionDetailsV2 = getSessionDetailsV2;
const axios_1 = require("axios");
const API_BASE_URL = 'http://langgraph-api:8000';
/**
 * Checks the health of the backend API.
 * @returns A promise that resolves with the response data.
 */
async function checkHealth() {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/ok`);
        return response.data;
    }
    catch (error) {
        console.error('Error checking backend health:', error);
        throw error;
    }
}
/**
 * Fetches the entire agent state from the backend.
 * @returns A promise that resolves with the full agent state.
 */
async function getAgentState() {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/agent/state`);
        const output = response.data;
        // Ensure a default state is returned if the response is partial
        return {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: output.literature_abstracts || [],
            report: output.report || '',
            ...output,
        };
    }
    catch (error) {
        console.error('Error fetching agent state:', error);
        // Return a default empty state on error to prevent view crashes
        return {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: '',
        };
    }
}
// ==================== Phase 3.5.2: Paper Management APIs ====================
/**
 * Fetches all papers with optional filtering.
 * @param options - Filter options (session_id, source, keyword, limit, offset)
 * @returns A promise that resolves with papers and total count
 */
async function getAllPapers(options) {
    try {
        const params = new URLSearchParams();
        if (options?.session_id) {
            params.append('session_id', options.session_id);
        }
        if (options?.source) {
            params.append('source', options.source);
        }
        if (options?.keyword) {
            params.append('keyword', options.keyword);
        }
        if (options?.limit) {
            params.append('limit', options.limit.toString());
        }
        if (options?.offset) {
            params.append('offset', options.offset.toString());
        }
        const response = await axios_1.default.get(`${API_BASE_URL}/papers?${params.toString()}`);
        return response.data;
    }
    catch (error) {
        console.error('Error fetching papers:', error);
        return { papers: [], total: 0 };
    }
}
/**
 * Fetches a single paper by ID.
 * @param paperId - The paper UUID
 * @returns A promise that resolves with the paper details
 */
async function getPaperById(paperId) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/papers/${paperId}`);
        return response.data;
    }
    catch (error) {
        console.error(`Error fetching paper ${paperId}:`, error);
        return null;
    }
}
/**
 * Exports papers to a specific format.
 * @param format - Export format: 'bibtex', 'ris', or 'json'
 * @param options - Filter options
 * @returns A promise that resolves with the exported content
 */
async function exportPapers(format, options) {
    try {
        const params = new URLSearchParams();
        params.append('format', format);
        if (options?.session_id) {
            params.append('session_id', options.session_id);
        }
        if (options?.source) {
            params.append('source', options.source);
        }
        const response = await axios_1.default.get(`${API_BASE_URL}/papers/export?${params.toString()}`);
        return response.data;
    }
    catch (error) {
        console.error('Error exporting papers:', error);
        throw error;
    }
}
// ==================== Phase 3.5.2: Report Management APIs ====================
/**
 * Fetches all reports with optional filtering.
 * @param options - Filter options (session_id, start_date, end_date, limit, offset)
 * @returns A promise that resolves with reports and total count
 */
async function getAllReports(options) {
    try {
        const params = new URLSearchParams();
        if (options?.session_id) {
            params.append('session_id', options.session_id);
        }
        if (options?.start_date) {
            params.append('start_date', options.start_date);
        }
        if (options?.end_date) {
            params.append('end_date', options.end_date);
        }
        if (options?.limit) {
            params.append('limit', options.limit.toString());
        }
        if (options?.offset) {
            params.append('offset', options.offset.toString());
        }
        const response = await axios_1.default.get(`${API_BASE_URL}/reports?${params.toString()}`);
        return response.data;
    }
    catch (error) {
        console.error('Error fetching reports:', error);
        return { reports: [], total: 0 };
    }
}
/**
 * Fetches a single report by ID.
 * @param reportId - The report UUID
 * @returns A promise that resolves with the report details
 */
async function getReportById(reportId) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/reports/${reportId}`);
        return response.data;
    }
    catch (error) {
        console.error(`Error fetching report ${reportId}:`, error);
        return null;
    }
}
/**
 * Fetches the latest report for a session.
 * @param sessionId - The session UUID
 * @returns A promise that resolves with the latest report
 */
async function getLatestReport(sessionId) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/sessions/${sessionId}/reports/latest`);
        return response.data;
    }
    catch (error) {
        console.error(`Error fetching latest report for session ${sessionId}:`, error);
        return null;
    }
}
/**
 * Exports a report to a specific format.
 * @param reportId - The report UUID
 * @param format - Export format: 'markdown', 'html', or 'pdf'
 * @returns A promise that resolves with the exported content
 */
async function exportReport(reportId, format) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/reports/${reportId}/export?format=${format}`);
        return response.data;
    }
    catch (error) {
        console.error('Error exporting report:', error);
        throw error;
    }
}
/**
 * Compares two report versions.
 * @param reportId1 - First report UUID (older version)
 * @param reportId2 - Second report UUID (newer version)
 * @returns A promise that resolves with both reports and their diff
 */
async function compareReports(reportId1, reportId2) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/reports/compare?report_id_1=${reportId1}&report_id_2=${reportId2}`);
        return response.data;
    }
    catch (error) {
        console.error('Error comparing reports:', error);
        return null;
    }
}
// ==================== Phase 3.5.2: Session Management APIs ====================
/**
 * Fetches all sessions with optional filtering.
 * @param options - Filter options (status, limit, offset)
 * @returns A promise that resolves with sessions list
 */
async function getAllSessions(options) {
    try {
        const params = new URLSearchParams();
        if (options?.status) {
            params.append('status', options.status);
        }
        if (options?.limit) {
            params.append('limit', options.limit.toString());
        }
        if (options?.offset) {
            params.append('offset', options.offset.toString());
        }
        const response = await axios_1.default.get(`${API_BASE_URL}/sessions?${params.toString()}`);
        return response.data;
    }
    catch (error) {
        console.error('Error fetching sessions:', error);
        return [];
    }
}
// ==================== WebSocket Streaming ====================
const WebSocket = require("ws");
/**
 * Start a new research task via WebSocket streaming.
 * @param topic - The research topic
 * @param callbacks - Callbacks for progress updates
 * @param threadId - Optional thread_id to resume session
 * @returns Promise that resolves when research completes
 */
async function startResearchStream(topic, callbacks, threadId) {
    return new Promise((resolve, reject) => {
        const wsUrl = API_BASE_URL.replace('http', 'ws') + '/agent/stream';
        console.log(`[WebSocket] Connecting to ${wsUrl}...`);
        const ws = new WebSocket(wsUrl);
        ws.on('open', () => {
            console.log('[WebSocket] Connected');
            ws.send(JSON.stringify({
                messages: [{ role: 'user', 'content': topic }],
                thread_id: threadId
            }));
        });
        ws.on('message', (data) => {
            try {
                const message = JSON.parse(data.toString());
                switch (message.type) {
                    case 'started':
                        console.log('[WebSocket] Research started:', message);
                        callbacks.onStarted?.(message);
                        break;
                    case 'progress':
                        console.log('[WebSocket] Progress:', message.node);
                        callbacks.onProgress?.(message);
                        break;
                    case 'complete':
                        console.log('[WebSocket] Research completed:', message);
                        callbacks.onComplete?.(message);
                        ws.close();
                        resolve();
                        break;
                    case 'error':
                        console.error('[WebSocket] Error:', message.message);
                        callbacks.onError?.(message.message);
                        ws.close();
                        reject(new Error(message.message));
                        break;
                }
            }
            catch (error) {
                console.error('[WebSocket] Parse error:', error);
                callbacks.onError?.('Failed to parse server message');
            }
        });
        ws.on('error', (error) => {
            console.error('[WebSocket] Connection error:', error);
            callbacks.onError?.(error.message);
            reject(error);
        });
        ws.on('close', () => {
            console.log('[WebSocket] Connection closed');
        });
    });
}
/**
 * Get paginated list of research sessions
 */
async function getSessionsList(params) {
    const queryParams = new URLSearchParams();
    if (params?.limit) {
        queryParams.append('limit', params.limit.toString());
    }
    if (params?.offset) {
        queryParams.append('offset', params.offset.toString());
    }
    if (params?.status) {
        queryParams.append('status', params.status);
    }
    if (params?.sort_by) {
        queryParams.append('sort_by', params.sort_by);
    }
    if (params?.order) {
        queryParams.append('order', params.order);
    }
    const url = `${API_BASE_URL}/analytics/sessions?${queryParams.toString()}`;
    const response = await axios_1.default.get(url);
    return response.data;
}
/**
 * Get aggregated session statistics
 */
async function getSessionStats(timeRange = '7d') {
    const response = await axios_1.default.get(`${API_BASE_URL}/analytics/sessions/stats?time_range=${timeRange}`);
    return response.data;
}
/**
 * Get paper collection trends
 */
async function getPaperTrends(timeRange = '7d') {
    const response = await axios_1.default.get(`${API_BASE_URL}/analytics/papers/trends?time_range=${timeRange}`);
    return response.data;
}
/**
 * Get detailed analytics for a specific session
 */
async function getSessionDetails(sessionId) {
    const response = await axios_1.default.get(`${API_BASE_URL}/analytics/sessions/${sessionId}`);
    return response.data;
}
/**
 * Get comprehensive session details (Phase 3.5.4)
 */
async function getSessionDetailsV2(sessionId) {
    try {
        const response = await axios_1.default.get(`${API_BASE_URL}/sessions/${sessionId}/details`);
        return response.data;
    }
    catch (error) {
        console.error('Error fetching session details:', error);
        throw error;
    }
}
//# sourceMappingURL=api.js.map