"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkHealth = checkHealth;
exports.getAgentState = getAgentState;
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
        // The backend agent endpoint might require a specific payload format.
        // For now, we send an empty messages array as a placeholder.
        const payload = { messages: [] };
        const response = await axios_1.default.post(`${API_BASE_URL}/agent`, payload);
        // Ensure a default state is returned if the response is partial
        return {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: response.data.literature_abstracts || [],
            report: response.data.report || '',
            ...response.data,
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
//# sourceMappingURL=api.js.map