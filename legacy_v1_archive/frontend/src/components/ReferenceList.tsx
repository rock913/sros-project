import React from 'react';

interface Paper {
  title: string;
  authors: string[];
  summary: string;
  published?: string;
  doi?: string;
  isOa?: boolean;
  oaUrl?: string;
}

interface ReferenceListProps {
  papers: Paper[];
  isLoading?: boolean;
  onPaperSelect?: (paper: Paper) => void;
  selectedPaperId?: string;
}

/**
 * ReferenceList Component - Phase 5.2.3
 *
 * Displays a list of academic paper references in card format.
 * Used in VS Code extension to show search results from the MCP discovery workflow.
 */
export const ReferenceList: React.FC<ReferenceListProps> = ({
  papers,
  isLoading = false,
  onPaperSelect,
  selectedPaperId
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading papers...</span>
      </div>
    );
  }

  if (!papers || papers.length === 0) {
    return (
      <div className="text-center p-8">
        <div className="text-gray-400 text-lg mb-2">📚</div>
        <p className="text-gray-600">No papers found</p>
        <p className="text-sm text-gray-500">Try refining your search query</p>
      </div>
    );
  }

  const formatAuthors = (authors: string[]) => {
    if (!authors || authors.length === 0) return 'Unknown author';
    if (authors.length === 1) return authors[0];
    if (authors.length === 2) return authors.join(' & ');
    return `${authors[0]} et al.`;
  };

  const truncateSummary = (summary: string, maxLength: number = 200) => {
    if (!summary) return '';
    if (summary.length <= maxLength) return summary;
    return summary.substring(0, maxLength) + '...';
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Research Results
        </h2>
        <p className="text-gray-600">
          Found {papers.length} paper{papers.length !== 1 ? 's' : ''}
        </p>
      </div>

      <div className="space-y-4">
        {papers.map((paper, index) => {
          const paperId = paper.doi || `${index}`;
          const isSelected = selectedPaperId === paperId;

          return (
            <div
              key={paperId}
              className={`
                bg-white rounded-lg border shadow-sm hover:shadow-md transition-shadow
                cursor-pointer
                ${isSelected ? 'border-blue-500 shadow-md' : 'border-gray-200'}
              `}
              onClick={() => onPaperSelect?.(paper)}
            >
              <div className="p-6">
                {/* Title */}
                <h3 className="text-lg font-semibold text-gray-900 mb-2 leading-tight">
                  {paper.title || 'Untitled Paper'}
                </h3>

                {/* Metadata */}
                <div className="flex items-center justify-between mb-3">
                  <div className="text-sm text-gray-600">
                    {formatAuthors(paper.authors)}
                  </div>

                  {paper.published && (
                    <div className="text-sm text-gray-500">
                      {new Date(paper.published).getFullYear()}
                    </div>
                  )}
                </div>

                {/* Publication info */}
                {(paper.doi || paper.isOa) && (
                  <div className="flex items-center gap-2 mb-3">
                    {paper.doi && (
                      <a
                        href={`https://doi.org/${paper.doi}`}
                        className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                        onClick={(e) => e.stopPropagation()}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        DOI
                      </a>
                    )}
                    {paper.isOa && (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                        Open Access
                      </span>
                    )}
                  </div>
                )}

                {/* Abstract/Summary */}
                {paper.summary && (
                  <div className="mt-3">
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {truncateSummary(paper.summary)}
                    </p>
                  </div>
                )}

                {/* Actions */}
                <div className="mt-4 pt-3 border-t border-gray-100 flex justify-between items-center">
                  <div className="text-xs text-gray-500">
                    Click to view details
                  </div>

                  {(paper.isOa && paper.oaUrl) && (
                    <a
                      href={paper.oaUrl}
                      className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                      onClick={(e) => e.stopPropagation()}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View PDF
                    </a>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Load More - for future pagination */}
      {papers.length >= 10 && (
        <div className="mt-8 text-center">
          <button className="px-4 py-2 text-blue-600 border border-blue-600 rounded hover:bg-blue-50">
            Load More Results
          </button>
        </div>
      )}
    </div>
  );
};

export default ReferenceList;