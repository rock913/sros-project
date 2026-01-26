/**
 * VS Code Webview Bridge
 * Handles communication between React components and VS Code extension host
 */

export class VSCodeBridge {
  constructor(vscodeApi) {
    this.vscode = vscodeApi;
  }

  /**
   * Send message to VS Code extension
   */
  postMessage(message) {
    if (this.vscode) {
      console.log('[VSCodeBridge] Sending message:', message);
      this.vscode.postMessage(message);
    } else {
      console.warn('[VSCodeBridge] VS Code API not available');
    }
  }

  /**
   * Request data from extension
   */
  requestData(requestType, params) {
    this.postMessage({
      type: 'request-data',
      requestType,
      params
    });
  }

  /**
   * Send HITL response
   */
  sendHITLResponse(requestId, decision, data) {
    this.postMessage({
      type: 'hitl_response',
      request_id: requestId,
      decision,
      data
    });
  }

  /**
   * Request session details
   */
  requestSessionDetails(sessionId) {
    this.requestData('session-details', { sessionId });
  }

  /**
   * Request sessions list
   */
  requestSessionsList(filters) {
    this.requestData('sessions-list', filters);
  }

  /**
   * Send research command
   */
  startResearch(topic) {
    this.postMessage({
      type: 'start-research',
      topic
    });
  }

  /**
   * Update session filter
   */
  updateFilter(filterType, value) {
    this.postMessage({
      type: 'update-filter',
      filterType,
      value
    });
  }

  /**
   * Export manuscript
   */
  exportManuscript(sessionId, format) {
    this.postMessage({
      type: 'export-manuscript',
      sessionId,
      format
    });
  }

  /**
   * Open paper
   */
  openPaper(sessionId, paperId) {
    this.postMessage({
      type: 'open-paper',
      sessionId,
      paperId
    });
  }
}