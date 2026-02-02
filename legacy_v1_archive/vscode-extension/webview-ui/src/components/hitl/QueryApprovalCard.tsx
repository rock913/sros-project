import { useState } from 'react';

interface QueryApprovalCardProps {
  requestId: string;
  prompt: string;
  queries: string[];
  timeoutSeconds?: number;
  researchTopic: string;
  onResponse: (decision: string, data?: any) => void;
}

export function QueryApprovalCard({
  queries,
  timeoutSeconds,
  researchTopic,
  onResponse
}: QueryApprovalCardProps) {
  const [modifiedQueries, setModifiedQueries] = useState<string[]>(queries);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [hasModifications, setHasModifications] = useState(false);

  const handleEdit = (index: number) => {
    if (editingIndex === index) {
      // Save changes
      setEditingIndex(null);
      setHasModifications(true);
    } else {
      setEditingIndex(index);
    }
  };

  const handleQueryChange = (index: number, value: string) => {
    const newQueries = [...modifiedQueries];
    newQueries[index] = value;
    setModifiedQueries(newQueries);
  };

  const handleResponse = (decision: string) => {
    onResponse(decision, decision === 'modify' ? { queries: modifiedQueries } : undefined);
  };

  return (
    <div className="bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-4xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <div className="text-2xl">🔍</div>
        <div>
          <h1 className="text-xl font-semibold text-neutral-100">Query Approval Required</h1>
          <p className="text-sm text-neutral-400">Review generated search queries</p>
        </div>
      </div>

      <div className="bg-neutral-600 p-4 rounded-md mb-6">
        <strong className="text-neutral-100">Research Topic:</strong> {researchTopic}
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-medium text-neutral-100 mb-4">Generated Queries ({queries.length})</h3>
        <div className="space-y-3 max-h-60 overflow-y-auto">
          {queries.map((_query, index) => (
            <div key={index} className="bg-neutral-600 p-3 rounded-md border border-neutral-500">
              <div className="flex items-center gap-3">
                <span className="text-sm font-mono text-neutral-300 min-w-[2rem]">{index + 1}.</span>
                {editingIndex === index ? (
                  <input
                    type="text"
                    value={modifiedQueries[index]}
                    onChange={(e) => handleQueryChange(index, e.target.value)}
                    className="flex-1 bg-neutral-500 text-neutral-100 px-3 py-1 rounded border border-neutral-400 focus:outline-none focus:border-blue-400"
                    autoFocus
                  />
                ) : (
                  <span className="flex-1 text-sm text-neutral-200">{modifiedQueries[index]}</span>
                )}
                <button
                  onClick={() => handleEdit(index)}
                  className="px-3 py-1 bg-neutral-500 hover:bg-neutral-400 text-neutral-100 rounded text-sm transition-colors"
                >
                  {editingIndex === index ? '💾 Save' : '✏️ Edit'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

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
          ✅ Approve All
        </button>
        {hasModifications && (
          <button
            onClick={() => handleResponse('modify')}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
          >
            💾 Save Changes
          </button>
        )}
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