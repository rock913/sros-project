import React, { useState, useEffect } from 'react';
import { VSCodeBridge } from './lib/vscodeBridge';
import { ActivityTimeline, ProcessedEvent } from './components/ActivityTimeline';
import { QueryApprovalCard, PaperSelectionCard, ReportRevisionCard } from './components/hitl';
import { SessionList, SessionDetail } from './components/sessions';

declare global {
  interface Window {
    acquireVsCodeApi(): any;
  }
}

const vscode = window.acquireVsCodeApi();

interface HITLRequest {
  request_id: string;
  decision_type: 'query_approval' | 'paper_selection' | 'report_revision';
  prompt: string;
  options: string[];
  context: any;
  timeout_seconds?: number;
  session_id: string;
  thread_id: string;
}

type ViewMode = 'research' | 'sessions' | 'session-detail';

const App: React.FC = () => {
  const [processedEvents, setProcessedEvents] = useState<ProcessedEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>('Loading Auto Researcher Webview...');
  const [currentHITLRequest, setCurrentHITLRequest] = useState<HITLRequest | null>(null);
  const [currentView, setCurrentView] = useState<ViewMode>('research');
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);

  useEffect(() => {
    // Initialize VS Code bridge
    const bridge = new VSCodeBridge(vscode);

    // Listen for messages from extension
    const messageHandler = (event: MessageEvent) => {
      const message = event.data;
      console.log('[Webview] Received message:', message);

      switch (message.type) {
        case 'init':
          setMessage('Webview initialized successfully!');
          break;
        case 'research-progress':
          handleResearchProgress(message);
          break;
        case 'research-started':
          handleResearchStarted(message);
          break;
        case 'research-completed':
          handleResearchCompleted(message);
          break;
        case 'research-error':
          handleResearchError(message);
          break;
        case 'hitl-request':
          handleHITLRequest(message);
          break;
        default:
          console.log('[Webview] Unknown message type:', message.type);
      }
    };

    window.addEventListener('message', messageHandler);

    // Send ready message to extension
    bridge.postMessage({ type: 'webview-ready' });

    return () => {
      window.removeEventListener('message', messageHandler);
    };
  }, []);

  const handleResearchStarted = (message: any) => {
    setIsLoading(true);
    setProcessedEvents([]);
    setMessage(`Research started: ${message.topic || 'Unknown topic'}`);
  };

  const handleResearchProgress = (message: any) => {
    const event: ProcessedEvent = {
      title: getEventTitle(message.node || 'processing'),
      data: message.message || message.data || ''
    };

    setProcessedEvents(prev => [...prev, event]);
    setMessage(`Processing: ${event.title}`);
  };

  const handleResearchCompleted = (message: any) => {
    setIsLoading(false);
    const event: ProcessedEvent = {
      title: 'Research Completed',
      data: `Session ID: ${message.session_id}`
    };
    setProcessedEvents(prev => [...prev, event]);
    setMessage(`Research completed successfully!`);
  };

  const handleResearchError = (message: any) => {
    setIsLoading(false);
    const event: ProcessedEvent = {
      title: 'Research Error',
      data: message.error || 'An error occurred'
    };
    setProcessedEvents(prev => [...prev, event]);
    setMessage(`Research failed: ${message.error}`);
  };

  const handleHITLRequest = (message: any) => {
    setCurrentHITLRequest(message);
    setIsLoading(false); // Pause loading indicator when HITL is active
    setMessage(`HITL Required: ${message.decision_type}`);
  };

  const handleHITLResponse = (decision: string, data?: any) => {
    if (!currentHITLRequest) return;

    const bridge = new VSCodeBridge(vscode);
    bridge.sendHITLResponse(currentHITLRequest.request_id, decision, data);

    setCurrentHITLRequest(null);
    setMessage(`HITL response sent: ${decision}`);
  };

  const handleSelectSession = (sessionId: string) => {
    setSelectedSessionId(sessionId);
    setCurrentView('session-detail');
  };

  const handleBackToSessions = () => {
    setSelectedSessionId(null);
    setCurrentView('sessions');
  };

  const handleCreateNewSession = () => {
    const bridge = new VSCodeBridge(vscode);
    bridge.startResearch('New Research Topic'); // This could open a dialog for topic input
    setCurrentView('research');
  };

  const handleOpenPaper = (sessionId: string, paperId: string) => {
    const bridge = new VSCodeBridge(vscode);
    bridge.openPaper(sessionId, paperId);
  };

  const handleExportReport = (sessionId: string) => {
    const bridge = new VSCodeBridge(vscode);
    bridge.exportManuscript(sessionId, 'md'); // Default to markdown export
  };

  const getEventTitle = (node: string): string => {
    const titleMap: { [key: string]: string } = {
      'query_generation': 'Generating Search Queries',
      'query_approval': 'Waiting for Query Approval',
      'search_and_filter': 'Searching and Filtering Papers',
      'paper_selection': 'Selecting Relevant Papers',
      'paper_selection_approval': 'Waiting for Paper Selection Approval',
      'full_text_retrieval': 'Retrieving Full-Text Papers',
      'report_synthesis': 'Synthesizing Research Report',
      'final_report': 'Finalizing Report',
      'reflection_and_refinement': 'Reflecting and Refining Strategy'
    };
    return titleMap[node] || `Processing: ${node}`;
  };

  const renderHITLCard = () => {
    if (!currentHITLRequest) return null;

    const { decision_type, context, request_id, timeout_seconds } = currentHITLRequest;

    switch (decision_type) {
      case 'query_approval':
        return (
          <QueryApprovalCard
            requestId={request_id}
            prompt={currentHITLRequest.prompt}
            queries={context.queries || []}
            timeoutSeconds={timeout_seconds}
            researchTopic={context.research_topic || 'Research Topic'}
            onResponse={handleHITLResponse}
          />
        );
      case 'paper_selection':
        return (
          <PaperSelectionCard
            requestId={request_id}
            prompt={currentHITLRequest.prompt}
            papers={context.papers || []}
            totalCount={context.total_count || context.papers?.length || 0}
            recommendation={context.recommendation}
            timeoutSeconds={timeout_seconds}
            onResponse={handleHITLResponse}
          />
        );
      case 'report_revision':
        return (
          <ReportRevisionCard
            requestId={request_id}
            prompt={currentHITLRequest.prompt}
            report={context.report || ''}
            wordCount={context.word_count || 0}
            paperCount={context.paper_count || 0}
            researchTopic={context.research_topic || 'Research Topic'}
            timeoutSeconds={timeout_seconds}
            onResponse={handleHITLResponse}
          />
        );
      default:
        return (
          <div className="bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-4xl mx-auto">
            <h2 className="text-xl font-semibold text-neutral-100 mb-4">
              Unknown HITL Request Type: {decision_type}
            </h2>
            <pre className="text-sm text-neutral-300 bg-neutral-800 p-4 rounded overflow-auto">
              {JSON.stringify(currentHITLRequest, null, 2)}
            </pre>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-neutral-800 text-neutral-100 p-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-primary">
                🤖 Auto Researcher Webview
              </h1>
              <p className="text-neutral-400 mt-2">
                React-based Collaboration UI for MCP-powered Research
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('research')}
                className={`px-4 py-2 rounded-md font-medium transition-colors ${
                  currentView === 'research'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-700 text-neutral-300 hover:bg-neutral-600'
                }`}
              >
                🔬 Research
              </button>
              <button
                onClick={() => setCurrentView('sessions')}
                className={`px-4 py-2 rounded-md font-medium transition-colors ${
                  currentView === 'sessions'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-700 text-neutral-300 hover:bg-neutral-600'
                }`}
              >
                📚 Sessions
              </button>
            </div>
          </div>
        </header>

        <main className="space-y-6">
          {currentHITLRequest ? (
            renderHITLCard()
          ) : (
            <>
              {currentView === 'research' && (
                <>
                  <ActivityTimeline
                    processedEvents={processedEvents}
                    isLoading={isLoading}
                  />

                  <div className="bg-neutral-700 p-6 rounded-lg border border-neutral-600">
                    <h2 className="text-xl font-semibold mb-4 text-neutral-100">Debug Status</h2>
                    <p className="text-sm text-neutral-300">{message}</p>
                    <div className="mt-4 text-xs text-neutral-400">
                      Events: {processedEvents.length} | Loading: {isLoading ? 'Yes' : 'No'}
                    </div>
                  </div>
                </>
              )}

              {currentView === 'sessions' && (
                <SessionList
                  onSelectSession={handleSelectSession}
                  onCreateNewSession={handleCreateNewSession}
                />
              )}

              {currentView === 'session-detail' && selectedSessionId && (
                <SessionDetail
                  sessionId={selectedSessionId}
                  onBack={handleBackToSessions}
                  onOpenPaper={handleOpenPaper}
                  onExportReport={handleExportReport}
                />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
