import { useState, useMemo } from 'react';

interface Paper {
  title: string;
  authors: string[];
  year?: number;
  doi?: string;
  arxiv_id?: string;
  abstract?: string;
}

interface PaperSelectionCardProps {
  requestId: string;
  prompt: string;
  papers: Paper[];
  totalCount: number;
  recommendation?: string;
  timeoutSeconds?: number;
  onResponse: (decision: string, data?: any) => void;
}

export function PaperSelectionCard({
  papers,
  totalCount,
  recommendation,
  timeoutSeconds,
  onResponse
}: PaperSelectionCardProps) {
  const [selectedPapers, setSelectedPapers] = useState<Set<number>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');

  const filteredPapers = useMemo(() => {
    if (!searchQuery.trim()) return papers;
    const query = searchQuery.toLowerCase();
    return papers.filter((paper) =>
      paper.title.toLowerCase().includes(query) ||
      paper.authors.some(author => author.toLowerCase().includes(query))
    );
  }, [papers, searchQuery]);

  const handlePaperToggle = (index: number) => {
    const newSelected = new Set(selectedPapers);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedPapers(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedPapers.size === filteredPapers.length) {
      setSelectedPapers(new Set());
    } else {
      setSelectedPapers(new Set(filteredPapers.map((_, index) => index)));
    }
  };

  const handleResponse = (decision: string) => {
    if (decision === 'select_subset') {
      const selectedPaperData = Array.from(selectedPapers).map(index => filteredPapers[index]);
      onResponse(decision, { selected_papers: selectedPaperData });
    } else {
      onResponse(decision);
    }
  };

  const formatAuthors = (authors: string[]) => {
    if (authors.length <= 2) {
      return authors.join(', ');
    }
    return `${authors.slice(0, 2).join(', ')} et al.`;
  };

  return (
    <div className="bg-neutral-700 rounded-lg border border-neutral-600 p-6 max-w-6xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <div className="text-2xl">📄</div>
        <div>
          <h1 className="text-xl font-semibold text-neutral-100">Paper Selection Required</h1>
          <p className="text-sm text-neutral-400">Found {totalCount} papers - select papers to analyze</p>
        </div>
      </div>

      <div className="bg-neutral-600 p-4 rounded-md mb-6">
        💡 <strong className="text-neutral-100">Recommendation:</strong> {recommendation || 'Select 10-20 most relevant papers for detailed analysis'}
      </div>

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4">
          <span className="text-sm text-neutral-300">
            {selectedPapers.size} / {filteredPapers.length} papers selected
          </span>
          <div className="flex gap-2">
            <button
              onClick={handleSelectAll}
              className="px-3 py-1 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded text-sm transition-colors"
            >
              {selectedPapers.size === filteredPapers.length ? 'Clear All' : 'Select All'}
            </button>
          </div>
        </div>
      </div>

      {filteredPapers.length > 5 && (
        <div className="mb-4">
          <input
            type="text"
            placeholder="🔍 Filter papers by title or author..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-3 py-2 bg-neutral-600 text-neutral-100 rounded border border-neutral-500 focus:outline-none focus:border-blue-400"
          />
        </div>
      )}

      <div className="max-h-96 overflow-y-auto mb-6 space-y-3">
        {filteredPapers.map((paper, index) => {
          const originalIndex = papers.indexOf(paper);
          const isSelected = selectedPapers.has(index);

          return (
            <div
              key={originalIndex}
              className={`border rounded-md p-4 cursor-pointer transition-colors ${
                isSelected
                  ? 'border-blue-400 bg-blue-900/20'
                  : 'border-neutral-500 bg-neutral-600 hover:border-neutral-400'
              }`}
              onClick={() => handlePaperToggle(index)}
            >
              <div className="flex items-start gap-3">
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => handlePaperToggle(index)}
                  className="mt-1 w-4 h-4 text-blue-600 bg-neutral-600 border-neutral-500 rounded focus:ring-blue-500"
                  onClick={(e) => e.stopPropagation()}
                />
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-neutral-100 mb-1">
                    [{index + 1}] {paper.title}
                  </h4>
                  <div className="text-xs text-neutral-400 mb-2">
                    {formatAuthors(paper.authors)}
                    {paper.year && ` (${paper.year})`}
                  </div>
                  <div className="flex gap-4 text-xs text-neutral-500 mb-2">
                    {paper.doi && (
                      <span>DOI: <span className="text-blue-400">{paper.doi}</span></span>
                    )}
                    {paper.arxiv_id && (
                      <span>arXiv: <span className="text-blue-400">{paper.arxiv_id}</span></span>
                    )}
                  </div>
                  {paper.abstract && (
                    <div className="text-xs text-neutral-300 line-clamp-3">
                      {paper.abstract.length > 200
                        ? `${paper.abstract.substring(0, 200)}...`
                        : paper.abstract
                      }
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
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
          onClick={() => handleResponse('select_subset')}
          disabled={selectedPapers.size === 0}
          className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-neutral-600 disabled:cursor-not-allowed text-white rounded-md font-medium transition-colors"
        >
          ✅ Submit Selection ({selectedPapers.size})
        </button>
        <button
          onClick={() => handleResponse('select_all')}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
        >
          📚 Analyze All Papers
        </button>
        <button
          onClick={() => handleResponse('reject')}
          className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors"
        >
          ❌ Cancel Research
        </button>
      </div>
    </div>
  );
}