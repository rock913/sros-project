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