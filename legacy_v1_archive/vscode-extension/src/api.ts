import axios from 'axios';

// API Base URL
// Default to langgraph-api:8000 for Dev Container environment (service-to-service communication)
// For local host debugging, set VSCODE_RESEARCH_AGENT_URL=http://localhost:8121
const API_BASE_URL = process.env.VSCODE_RESEARCH_AGENT_URL || 'http://langgraph-api:8000';
console.log('[API] Using Base URL:', API_BASE_URL);

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

// Co-STORM MindMap types
export interface PerspectiveNode {
  id: string;
  name: string;
  description: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  query_keywords: string[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  papers?: Paper[];
  summary?: string;
}

export interface MindMap {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  root_topic: string;
  nodes: PerspectiveNode[];
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
  // Co-STORM fields
  mindmap?: MindMap;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  perspectives?: any[];
  documents?: { [nodeId: string]: Paper[] };
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
  } catch (error: any) {
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
  } catch (error: any) {
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

// ==================== Phase 2: Thread Management APIs ====================

/**
 * Request body for creating a new thread
 */
export interface CreateThreadRequest {
  metadata?: {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    research_topic?: string;
    [key: string]: any;
  };
}

/**
 * Response from creating a thread
 */
export interface ThreadResponse {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  thread_id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at: string;
  metadata: any;
}

/**
 * Thread state response including values, next steps, and metadata
 */
export interface ThreadState {
  values: AgentState;
  next: string[];
  metadata: any;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  parent_config?: any;
}

/**
 * Generates a UUID v4 for use as a thread ID.
 * LangGraph manages threads automatically - we just need to provide a unique ID.
 * @returns A new UUID v4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
 */
export function generateThreadId(): string {
  // Simple UUID v4 generator for browser/node environments
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * @deprecated Use generateThreadId() and invokeAgent() instead.
 * LangGraph API doesn't have a separate /threads endpoint.
 * Threads are created automatically when you call /agent/invoke with a new thread_id.
 */
export async function createThread(
  request: CreateThreadRequest = {}
): Promise<ThreadResponse> {
  // Generate a thread ID - the actual thread is created when invokeAgent is called
  const threadId = generateThreadId();
  return {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    thread_id: threadId,
    // eslint-disable-next-line @typescript-eslint/naming-convention
    created_at: new Date().toISOString(),
    metadata: request.metadata || {}
  };
}

/**
 * Request body for starting a research task
 */
export interface StartResearchRequest {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  assistant_id: string;
  input: {
    messages: Array<{
      role: string;
      content: string;
    }>;
  };
  // eslint-disable-next-line @typescript-eslint/naming-convention
  stream_mode?: string[];
  config?: any;
}

/**
 * Invokes the research agent using LangGraph API.
 * This is the correct way to start research - it automatically creates or continues a thread.
 * 
 * @param threadId - UUID v4 format thread identifier
 * @param topic - The research topic
 * @returns A promise that resolves with the agent's response
 */
export async function invokeAgent(
  threadId: string,
  topic: string
): Promise<AgentState> {
  try {
    const request = {
      input: {
        messages: [
          {
            role: 'user',
            content: `Please research: ${topic}`
          }
        ]
      },
      config: {
        configurable:
        {
          // eslint-disable-next-line @typescript-eslint/naming-convention
          thread_id: threadId
        }
      }
    };

    const response = await axios.post(
      `${API_BASE_URL}/agent/invoke`,
      request,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  } catch (error: any) {
    console.error('Error invoking agent:', error);
    throw new Error(`Failed to invoke agent: ${error.message}`);
  }
}

/**
 * @deprecated Use invokeAgent() instead.
 * This function signature doesn't match the actual LangGraph API.
 * Keeping for backwards compatibility but redirecting to invokeAgent.
 */
export async function startResearch(
  threadId: string,
  topic: string
): Promise<string> {
  await invokeAgent(threadId, topic);
  return threadId;
}

/**
 * Gets the current state of a thread from LangGraph checkpointer.
 * @param threadId - The thread ID to get state for (UUID v4 format)
 * @returns A promise that resolves with the agent state
 */
export async function getThreadState(threadId: string): Promise<AgentState> {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/agent/state/${threadId}`
    );
    const output = response.data.values || {};
    return {
      // Backend API uses snake_case, map to frontend property names
      // eslint-disable-next-line @typescript-eslint/naming-convention
      literature_abstracts: output.literature_abstracts || [],
      report: output.report || '',
      ...output,
    };
  } catch (error: any) {
    console.error('Error fetching thread state:', error);
    // Return empty state on error (e.g., thread not found yet)
    return {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
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
  } catch (error: any) {
    console.error('Error fetching sessions:', error);
    return [];
  }
}
// ==================== WebSocket Streaming ====================

import * as WebSocket from 'ws';

export interface ResearchProgressCallback {
  onStarted?: (data: { session_id: string; thread_id: string }) => void;
  onProgress?: (data: { node: string; message?: string }) => void;
  onComplete?: (data: { session_id: string; thread_id: string }) => void;
  onError?: (error: string) => void;
  onHitlRequest?: (data: {
    request_id: string;
    decision_type: string;
    prompt: string;
    options: any[];
    context: any;
    timeout_seconds: number;
    session_id: string;
    thread_id: string;
  }) => void;
  // Co-STORM specific callbacks
  onMindmapUpdate?: (data: {
    mindmap: MindMap;
    session_id: string;
    thread_id: string;
  }) => void;
  onMindmapNodeUpdate?: (data: {
    node_id: string;
    node: PerspectiveNode;
    session_id: string;
    thread_id: string;
  }) => void;
}

/**
 * Start a new research task via WebSocket streaming.
 * @param topic - The research topic
 * @param callbacks - Callbacks for progress updates
 * @param threadId - Optional thread_id to resume session
 * @returns Promise that resolves when research completes, and WebSocket instance for HITL responses
 */
export async function startResearchStream(
  topic: string,
  callbacks: ResearchProgressCallback,
  threadId?: string
): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/agent/stream';
    console.log(`[WebSocket] Connecting to ${wsUrl}...`);
    
    const ws = new WebSocket(wsUrl);

    ws.on('open', () => {
      console.log('[WebSocket] Connected');
      ws.send(JSON.stringify({
        messages: [{ role: 'user', 'content': topic }],
        thread_id: threadId,
        workflow: "costorm"
      }));

      // Return WebSocket instance immediately after connection
      resolve(ws);
    });

    ws.on('message', (data: WebSocket.Data) => {
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

          case 'mindmap_update':
            // Support both wrapped payload (Co-STORM V2.1) and flat structure
            const mindmapData = message.payload?.mindmap || message.mindmap;
            console.log('[WebSocket] MindMap updated:', mindmapData?.root_topic, mindmapData?.nodes?.length || 0, 'perspectives');
            
            // Normalize message for callbacks
            if (message.payload?.mindmap) {
                message.mindmap = message.payload.mindmap;
            }
            callbacks.onMindmapUpdate?.(message);
            break;

          case 'mindmap_node_update':
            console.log('[WebSocket] MindMap node updated:', message.node_id);
            callbacks.onMindmapNodeUpdate?.(message);
            break;

          case 'hitl_request':
            console.log('[WebSocket] HITL Request:', message.request_id, message.decision_type);
            callbacks.onHitlRequest?.(message);
            // Note: WebSocket stays open, waiting for hitl_response from frontend
            break;

          case 'heartbeat':
             // Quietly handle heartbeat to keep connection alive
             // console.debug('[WebSocket] Heartbeat received');
             break;

          case 'complete':
            console.log('[WebSocket] Research completed:', message);
            callbacks.onComplete?.(message);
            ws.close();
            break;

          case 'error':
            console.error('[WebSocket] Error:', message.message);
            callbacks.onError?.(message.message);
            ws.close();
            reject(new Error(message.message));
            break;

          default:
            console.warn('[WebSocket] Unknown message type:', message.type);
        }
      } catch (error: any) {
        console.error('[WebSocket] Parse error:', error);
        console.error('[WebSocket] Raw data:', data.toString());
        // Don't call onError for parse errors - connection might be closing
        // Just log the error and continue
      }
    });

    ws.on('error', (error) => {
      console.error('[WebSocket] Connection error:', error);
      callbacks.onError?.(error.message);
      reject(error);
    });

    ws.on('close', (code, reason) => {
      const reasonStr = reason?.toString() || 'No reason provided';
      console.log(`[WebSocket] Connection closed: Code ${code} - ${reasonStr}`);
      
      // Only treat as error if unexpected closure (not normal completion)
      if (code !== 1000 && code !== 1001) {
        console.warn(`[WebSocket] ⚠️ Unexpected closure code: ${code}`);
        // Note: This commonly happens when backend closes after sending HITL request
        // but before receiving hitl_response. This is a backend bug, not a frontend error.
      }
    });
  });
}

/**
 * Send HITL response through WebSocket
 * @param ws - The WebSocket connection
 * @param requestId - The HITL request ID
 * @param approved - Whether the request is approved
 * @param selectedOption - The selected option (if applicable)
 */
export function sendHitlResponse(
  ws: WebSocket,
  requestId: string,
  approved: boolean,
  selectedOption?: any
): void {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'hitl_response',
      request_id: requestId,
      approved: approved,
      selected_option: selectedOption
    }));
    console.log(`[WebSocket] Sent HITL response for ${requestId}: approved=${approved}`);
  } else {
    console.error('[WebSocket] Cannot send HITL response: connection not open');
  }
}


// ==================== Phase 3.5.3: Analytics APIs ====================

/**
 * Analytics Response Types for Dashboard
 */
export interface SessionSummary {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  thread_id: string;
  title: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  research_topic: string;
  status: 'active' | 'completed' | 'archived' | 'failed';
  // eslint-disable-next-line @typescript-eslint/naming-convention
  created_at: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  completed_at?: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  duration_seconds?: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  papers_count: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  events_count: number;
  tags: string[];
}

export interface SessionsListResponse {
  sessions: SessionSummary[];
  total: number;
  limit: number;
  offset: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  has_more: boolean;
}

export interface SessionStats {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  total_sessions: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  completed_sessions: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  failed_sessions: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  running_sessions: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  success_rate: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  total_papers_collected: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  avg_papers_per_session: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  avg_duration_seconds: number;
}

export interface DailyBreakdown {
  date: string;
  sessions: number;
  completed: number;
  failed: number;
}

export interface TopTopic {
  topic: string;
  count: number;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  avg_papers: number;
}

export interface SessionStatsResponse {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  time_range: string;
  stats: SessionStats;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  daily_breakdown: DailyBreakdown[];
  // eslint-disable-next-line @typescript-eslint/naming-convention
  top_topics: TopTopic[];
}

export interface PapersByDay {
  date: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  papers_count: number;
}

export interface TopVenue {
  venue: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  papers_count: number;
  percentage: number;
}

export interface PapersByYear {
  year: number;
  count: number;
}

export interface PaperTrendsResponse {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  time_range: string;
  trends: {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    total_papers: number;
    // eslint-disable-next-line @typescript-eslint/naming-convention
    unique_papers: number;
    // eslint-disable-next-line @typescript-eslint/naming-convention
    avg_papers_per_day: number;
    // eslint-disable-next-line @typescript-eslint/naming-convention
    papers_by_day: PapersByDay[];
    // eslint-disable-next-line @typescript-eslint/naming-convention
    top_venues: TopVenue[];
    // eslint-disable-next-line @typescript-eslint/naming-convention
    papers_by_year: PapersByYear[];
  };
}

export interface SessionEvent {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  event_id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  session_id: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  event_type: string;
  timestamp: string;
  metadata: any;
}

export interface TimelinePhase {
  phase: string;
  // eslint-disable-next-line @typescript-eslint/naming-convention
  duration_seconds: number;
  percentage: number;
}

export interface SessionDetailsResponse {
  session: SessionSummary & {
    notes?: string;
  };
  events: SessionEvent[];
  timeline: {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    total_duration_seconds: number;
    phases: TimelinePhase[];
  };
}

/**
 * Get paginated list of research sessions
 */
export async function getSessionsList(params?: {
  limit?: number;
  offset?: number;
  status?: 'active' | 'completed' | 'archived';
  // eslint-disable-next-line @typescript-eslint/naming-convention
  sort_by?: 'created_at' | 'duration' | 'papers_count';
  order?: 'asc' | 'desc';
}): Promise<SessionsListResponse> {
  const queryParams = new URLSearchParams();
  if (params?.limit) { queryParams.append('limit', params.limit.toString()); }
  if (params?.offset) { queryParams.append('offset', params.offset.toString()); }
  if (params?.status) { queryParams.append('status', params.status); }
  if (params?.sort_by) { queryParams.append('sort_by', params.sort_by); }
  if (params?.order) { queryParams.append('order', params.order); }
  
  const url = `${API_BASE_URL}/analytics/sessions?${queryParams.toString()}`;
  const response = await axios.get(url);
  return response.data;
}

/**
 * Get aggregated session statistics
 */
export async function getSessionStats(
  timeRange: '24h' | '7d' | '30d' | 'all' = '7d'
): Promise<SessionStatsResponse> {
  const response = await axios.get(
    `${API_BASE_URL}/analytics/sessions/stats?time_range=${timeRange}`
  );
  return response.data;
}

/**
 * Get paper collection trends
 */
export async function getPaperTrends(
  timeRange: '24h' | '7d' | '30d' | 'all' = '7d'
): Promise<PaperTrendsResponse> {
  const response = await axios.get(
    `${API_BASE_URL}/analytics/papers/trends?time_range=${timeRange}`
  );
  return response.data;
}

/**
 * Get detailed analytics for a specific session
 */
export async function getSessionDetails(
  sessionId: string
): Promise<SessionDetailsResponse> {
  const response = await axios.get(
    `${API_BASE_URL}/analytics/sessions/${sessionId}`
  );
  return response.data;
}

/**
 * Get comprehensive session details (Phase 3.5.4)
 */
export async function getSessionDetailsV2(sessionId: string): Promise<any> {
  try {
    const response = await axios.get(`${API_BASE_URL}/sessions/${sessionId}/details`);
    return response.data;
  } catch (error: any) {
    console.error('Error fetching session details:', error);
    throw error;
  }
}
