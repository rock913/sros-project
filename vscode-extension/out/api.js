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
//# sourceMappingURL=api.js.map