import axios from 'axios';

const API_BASE_URL = 'http://langgraph-api:8000';

// Type definitions for the backend API response
export interface Paper {
  title: string;
  authors: string[];
  abstract: string;
  summary?: string;
  doi?: string;
  url?: string;
  // Add other fields if necessary
}

// Phase 3.5.2: Extended Paper interface from database
export interface PaperDetail {
  id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id: string;
  title: string;
  authors: string[];
  abstract: string | null;
  doi: string | null;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  arxiv_id: string | null;
  url: string | null;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  extra_metadata: {
    source?: string;
    year?: number;
    [key: string]: any;
  };
}

// Phase 3.5.2: Report interface from database
export interface ReportDetail {
  id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id: string;
  content: string;
  format: string;
  version: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  extra_metadata: {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    word_count?: number;
    [key: string]: any;
  };
}

// Phase 3.5.2: Session interface
export interface Session {
  id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  thread_id: string;
  title: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  research_topic: string | null;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  updated_at: string;
  status: string;
  tags: string[];
  notes: string | null;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  paper_count: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  report_count: number;
}

// Backend API uses snake_case naming convention
// eslint-disable-next-line @typescript-eslint/naming-convention
export interface AgentState {
  messages?: any[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  research_topic?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  search_queries?: string[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  literature_abstracts: Paper[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  literature_full_text?: string[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  papers_for_ingestion?: any[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  is_sufficient?: boolean;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  knowledge_gap?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  research_loop_count?: number;
  report: string;
  // Add other state fields if necessary
}

/**
 * Checks the health of the backend API.
 * @returns A promise that resolves with the response data.
 */
export async function checkHealth() {
  try {
    const response = await axios.get(`${API_BASE_URL}/ok`);
    return response.data;
  } catch (error) {
    console.error('Error checking backend health:', error);
    throw error;
  }
}

/**
 * Fetches the entire agent state from the backend.
 * @returns A promise that resolves with the full agent state.
 */
export async function getAgentState(): Promise<AgentState> {
  try {
    const response = await axios.get(`${API_BASE_URL}/agent/state`);
    const output = response.data;
    // Ensure a default state is returned if the response is partial
    return {
      // Backend API uses snake_case
      // eslint-disable-next-line @typescript-eslint/naming-convention
      literature_abstracts: output.literature_abstracts || [],
      report: output.report || '',
      ...output,
    };
  } catch (error) {
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
export async function getAllPapers(options?: {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id?: string;
  source?: string;
  keyword?: string;
  limit?: number;
  offset?: number;
}): Promise<{ papers: PaperDetail[]; total: number }> {
  try {
    const params = new URLSearchParams();
    if (options?.session_id) { params.append('session_id', options.session_id); }
    if (options?.source) { params.append('source', options.source); }
    if (options?.keyword) { params.append('keyword', options.keyword); }
    if (options?.limit) { params.append('limit', options.limit.toString()); }
    if (options?.offset) { params.append('offset', options.offset.toString()); }

    const response = await axios.get(`${API_BASE_URL}/papers?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching papers:', error);
    return { papers: [], total: 0 };
  }
}

/**
 * Fetches a single paper by ID.
 * @param paperId - The paper UUID
 * @returns A promise that resolves with the paper details
 */
export async function getPaperById(paperId: string): Promise<PaperDetail | null> {
  try {
    const response = await axios.get(`${API_BASE_URL}/papers/${paperId}`);
    return response.data;
  } catch (error) {
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
export async function exportPapers(
  format: 'bibtex' | 'ris' | 'json',
  options?: {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    session_id?: string;
    source?: string;
  }
): Promise<string | PaperDetail[]> {
  try {
    const params = new URLSearchParams();
    params.append('format', format);
    if (options?.session_id) { params.append('session_id', options.session_id); }
    if (options?.source) { params.append('source', options.source); }

    const response = await axios.get(`${API_BASE_URL}/papers/export?${params.toString()}`);
    return response.data;
  } catch (error) {
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
export async function getAllReports(options?: {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  start_date?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  end_date?: string;
  limit?: number;
  offset?: number;
}): Promise<{ reports: ReportDetail[]; total: number }> {
  try {
    const params = new URLSearchParams();
    if (options?.session_id) { params.append('session_id', options.session_id); }
    if (options?.start_date) { params.append('start_date', options.start_date); }
    if (options?.end_date) { params.append('end_date', options.end_date); }
    if (options?.limit) { params.append('limit', options.limit.toString()); }
    if (options?.offset) { params.append('offset', options.offset.toString()); }

    const response = await axios.get(`${API_BASE_URL}/reports?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching reports:', error);
    return { reports: [], total: 0 };
  }
}

/**
 * Fetches a single report by ID.
 * @param reportId - The report UUID
 * @returns A promise that resolves with the report details
 */
export async function getReportById(reportId: string): Promise<ReportDetail | null> {
  try {
    const response = await axios.get(`${API_BASE_URL}/reports/${reportId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching report ${reportId}:`, error);
    return null;
  }
}

/**
 * Fetches the latest report for a session.
 * @param sessionId - The session UUID
 * @returns A promise that resolves with the latest report
 */
export async function getLatestReport(sessionId: string): Promise<ReportDetail | null> {
  try {
    const response = await axios.get(`${API_BASE_URL}/sessions/${sessionId}/reports/latest`);
    return response.data;
  } catch (error) {
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
export async function exportReport(
  reportId: string,
  format: 'markdown' | 'html' | 'pdf'
): Promise<string> {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/reports/${reportId}/export?format=${format}`
    );
    return response.data;
  } catch (error) {
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
export async function compareReports(
  reportId1: string,
  reportId2: string
): Promise<{
  // eslint-disable-next-line @typescript-eslint/naming-convention
  report_1: ReportDetail;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  report_2: ReportDetail;
  diff: string;
} | null> {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/reports/compare?report_id_1=${reportId1}&report_id_2=${reportId2}`
    );
    return response.data;
  } catch (error) {
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
export async function getAllSessions(options?: {
  status?: string;
  limit?: number;
  offset?: number;
}): Promise<Session[]> {
  try {
    const params = new URLSearchParams();
    if (options?.status) { params.append('status', options.status); }
    if (options?.limit) { params.append('limit', options.limit.toString()); }
    if (options?.offset) { params.append('offset', options.offset.toString()); }

    const response = await axios.get(`${API_BASE_URL}/sessions?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching sessions:', error);
    return [];
  }
}