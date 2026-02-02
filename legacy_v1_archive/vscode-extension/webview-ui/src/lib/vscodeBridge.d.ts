export interface VSCodeMessage {
  type: string;
  [key: string]: any;
}

export declare class VSCodeBridge {
  constructor(vscodeApi: any);
  postMessage(message: VSCodeMessage): void;
  requestData(requestType: string, params?: any): void;
  sendHITLResponse(requestId: string, decision: string, data?: any): void;
  requestSessionDetails(sessionId: string): void;
  requestSessionsList(filters?: any): void;
  startResearch(topic: string): void;
  updateFilter(filterType: string, value: any): void;
  exportManuscript(sessionId: string, format: 'md' | 'pdf'): void;
  openPaper(sessionId: string, paperId: string): void;
}