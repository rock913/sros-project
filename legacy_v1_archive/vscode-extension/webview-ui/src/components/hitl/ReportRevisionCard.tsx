import { useState } from 'react';

interface ReportRevisionCardProps {
  requestId: string;
  prompt: string;
  report: string;
  wordCount: number;
  paperCount: number;
  researchTopic: string;
  timeoutSeconds?: number;
  onResponse: (decision: string, data?: any) => void;
}

export function ReportRevisionCard({
  report,
  wordCount,
  paperCount,
  researchTopic,
  timeoutSeconds,
  onResponse
}: ReportRevisionCardProps) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState('');

  const handleResponse = (decision: string) => {
    if (decision === 'modify') {
      if (!feedback.trim()) {
        alert('Please provide feedback before submitting modifications');
        return;
      }
      onResponse(decision, { feedback: feedback.trim() });
    } else {
      onResponse(decision);
    }
  };

  const handleModifyClick = () => {
    if (showFeedback) {
      handleResponse('modify');
    } else {
      setShowFeedback(true);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(report);
    // Could show a toast notification here
  };

  return (
    <div className="bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-6xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <div className="text-2xl">📝</div>
        <div>
          <h1 className="text-xl font-semibold text-neutral-100">Report Review Required</h1>
          <p className="text-sm text-neutral-400">Review and approve the research report</p>
        </div>
      </div>

      <div className="bg-neutral-600 p-4 rounded-md mb-6">
        <strong className="text-neutral-100">Research Topic:</strong> {researchTopic}
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-neutral-600 p-4 rounded-md">
          <div className="text-sm text-neutral-400">Word Count</div>
          <div className="text-xl font-bold text-neutral-100">{wordCount.toLocaleString()}</div>
        </div>
        <div className="bg-neutral-600 p-4 rounded-md">
          <div className="text-sm text-neutral-400">Papers Analyzed</div>
          <div className="text-xl font-bold text-neutral-100">{paperCount}</div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-medium text-neutral-100 mb-4">Generated Report</h3>
        <div className="bg-neutral-600 border border-neutral-500 rounded-md p-4 max-h-96 overflow-y-auto">
          <pre className="text-sm text-neutral-200 whitespace-pre-wrap font-sans">
            {report}
          </pre>
        </div>
      </div>

      {showFeedback && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-neutral-100 mb-4">Modification Feedback</h3>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Please provide specific feedback on what should be changed...

Examples:
- Add more details about methodology
- Focus more on recent papers (2023-2024)
- Include more quantitative results
- Expand the conclusion section"
            className="w-full h-32 px-3 py-2 bg-neutral-600 text-neutral-100 rounded border border-neutral-500 focus:outline-none focus:border-blue-400 resize-none"
            autoFocus
          />
        </div>
      )}

      {timeoutSeconds && (
        <div className="bg-yellow-900/20 border border-yellow-600/30 p-4 rounded-md mb-6">
          <div className="flex items-center gap-2 text-yellow-400">
            <span>⏰</span>
            <span>This request will timeout in {Math.floor(timeoutSeconds / 60)} minutes</span>
          </div>
        </div>
      )}

      <div className="flex gap-3 justify-end">
        <button
          onClick={() => handleResponse('approve')}
          className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-md font-medium transition-colors"
        >
          ✅ Approve Report
        </button>
        <button
          onClick={handleModifyClick}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
        >
          {showFeedback ? '💾 Submit Feedback' : '✏️ Request Modifications'}
        </button>
        <button
          onClick={copyToClipboard}
          className="px-6 py-3 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded-md font-medium transition-colors"
        >
          📋 Copy to Clipboard
        </button>
        <button
          onClick={() => handleResponse('reject')}
          className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors"
        >
          ❌ Reject & Stop
        </button>
      </div>
    </div>
  );
}