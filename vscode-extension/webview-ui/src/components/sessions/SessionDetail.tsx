import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { ScrollArea } from '../ui/scroll-area';

interface Paper {
  id: string;
  title: string;
  authors: string[];
  year?: number;
  doi?: string;
  arxiv_id?: string;
  abstract?: string;
  pdf_url?: string;
}

interface Report {
  id: string;
  title: string;
  content: string;
  word_count: number;
  created_at: string;
}

interface SessionDetailData {
  id: string;
  title: string;
  research_topic: string;
  created_at: string;
  updated_at: string;
  status: string;
  papers: Paper[];
  reports: Report[];
  query_count: number;
  total_tokens: number;
  execution_time: number;
}

interface SessionDetailProps {
  sessionId: string;
  onBack: () => void;
  onOpenPaper: (sessionId: string, paperId: string) => void;
  onExportReport: (sessionId: string, reportId: string) => void;
}

export function SessionDetail({ sessionId, onBack, onOpenPaper, onExportReport }: SessionDetailProps) {
  const [sessionData, setSessionData] = useState<SessionDetailData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'papers' | 'reports'>('overview');

  useEffect(() => {
    loadSessionDetail();
  }, [sessionId]);

  const loadSessionDetail = async () => {
    setLoading(true);
    try {
      // Mock data - in real implementation, this would come from VSCodeBridge
      const mockData: SessionDetailData = {
        id: sessionId,
        title: 'AI in Healthcare Research',
        research_topic: 'Applications of artificial intelligence in healthcare diagnostics and treatment',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        status: 'completed',
        papers: [
          {
            id: 'paper-1',
            title: 'Deep Learning for Medical Image Analysis',
            authors: ['Smith, J.', 'Johnson, A.', 'Williams, R.'],
            year: 2023,
            doi: '10.1038/s41591-023-01234-5',
            abstract: 'This paper presents a comprehensive review of deep learning applications in medical imaging...'
          },
          {
            id: 'paper-2',
            title: 'AI-Driven Drug Discovery: Current Trends and Future Directions',
            authors: ['Brown, M.', 'Davis, L.'],
            year: 2024,
            arxiv_id: '2401.12345',
            abstract: 'Recent advances in artificial intelligence have revolutionized drug discovery processes...'
          }
        ],
        reports: [
          {
            id: 'report-1',
            title: 'Comprehensive Analysis of AI in Healthcare',
            content: '# AI in Healthcare: Current State and Future Prospects\n\n## Executive Summary\n\nArtificial intelligence is transforming healthcare delivery...',
            word_count: 2450,
            created_at: new Date().toISOString()
          }
        ],
        query_count: 15,
        total_tokens: 125000,
        execution_time: 1800 // seconds
      };
      setSessionData(mockData);
    } catch (error) {
      console.error('Failed to load session detail:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-neutral-700 rounded w-1/4"></div>
          <div className="h-64 bg-neutral-700 rounded"></div>
        </div>
      </div>
    );
  }

  if (!sessionData) {
    return (
      <div className="p-6 text-center">
        <p className="text-neutral-400">Failed to load session details</p>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 bg-neutral-600 hover:bg-neutral-500 text-neutral-100 rounded transition-colors"
        >
          ← Back to Sessions
        </button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={onBack}
          className="px-3 py-1 bg-neutral-700 hover:bg-neutral-600 text-neutral-300 rounded transition-colors"
        >
          ← Back
        </button>
        <div>
          <h1 className="text-2xl font-bold text-neutral-100">{sessionData.title}</h1>
          <p className="text-sm text-neutral-400">{sessionData.research_topic}</p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-1 mb-6 border-b border-neutral-700">
        {[
          { key: 'overview', label: 'Overview', icon: '📊' },
          { key: 'papers', label: 'Papers', icon: '📄', count: sessionData.papers.length },
          { key: 'reports', label: 'Reports', icon: '📝', count: sessionData.reports.length }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`px-4 py-2 rounded-t-md font-medium transition-colors ${
              activeTab === tab.key
                ? 'bg-neutral-700 text-neutral-100 border-b-2 border-blue-400'
                : 'text-neutral-400 hover:text-neutral-300'
            }`}
          >
            {tab.icon} {tab.label} {tab.count !== undefined && `(${tab.count})`}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="bg-neutral-700 border-neutral-600">
              <CardHeader>
                <CardTitle className="text-neutral-100 flex items-center gap-2">
                  📊 Statistics
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-neutral-400">Papers Found:</span>
                  <span className="text-neutral-100 font-medium">{sessionData.papers.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Queries Executed:</span>
                  <span className="text-neutral-100 font-medium">{sessionData.query_count}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Total Tokens:</span>
                  <span className="text-neutral-100 font-medium">{sessionData.total_tokens.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Execution Time:</span>
                  <span className="text-neutral-100 font-medium">{formatDuration(sessionData.execution_time)}</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-neutral-700 border-neutral-600">
              <CardHeader>
                <CardTitle className="text-neutral-100 flex items-center gap-2">
                  📅 Timeline
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-neutral-400">Created:</span>
                  <span className="text-neutral-100 font-medium text-sm">{formatDate(sessionData.created_at)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Last Updated:</span>
                  <span className="text-neutral-100 font-medium text-sm">{formatDate(sessionData.updated_at)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-400">Status:</span>
                  <span className={`font-medium ${
                    sessionData.status === 'completed' ? 'text-green-400' :
                    sessionData.status === 'in_progress' ? 'text-blue-400' :
                    sessionData.status === 'failed' ? 'text-red-400' : 'text-yellow-400'
                  }`}>
                    {sessionData.status.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-neutral-700 border-neutral-600">
              <CardHeader>
                <CardTitle className="text-neutral-100 flex items-center gap-2">
                  📈 Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-neutral-300 text-sm leading-relaxed">
                  This research session explored {sessionData.research_topic}.
                  Found {sessionData.papers.length} relevant papers and generated {sessionData.reports.length} comprehensive reports.
                </p>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'papers' && (
          <div className="space-y-4">
            {sessionData.papers.map(paper => (
              <Card key={paper.id} className="bg-neutral-700 border-neutral-600">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-neutral-100 text-lg">{paper.title}</CardTitle>
                      <p className="text-neutral-400 text-sm mt-1">
                        {paper.authors.join(', ')} {paper.year && `(${paper.year})`}
                      </p>
                    </div>
                    <button
                      onClick={() => onOpenPaper(sessionData.id, paper.id)}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
                    >
                      📖 Open
                    </button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-4 text-xs text-neutral-400 mb-3">
                    {paper.doi && <span>DOI: {paper.doi}</span>}
                    {paper.arxiv_id && <span>arXiv: {paper.arxiv_id}</span>}
                  </div>
                  {paper.abstract && (
                    <p className="text-neutral-300 text-sm leading-relaxed">
                      {paper.abstract.length > 300
                        ? `${paper.abstract.substring(0, 300)}...`
                        : paper.abstract
                      }
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="space-y-4">
            {sessionData.reports.map(report => (
              <Card key={report.id} className="bg-neutral-700 border-neutral-600">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-neutral-100 text-lg">{report.title}</CardTitle>
                      <p className="text-neutral-400 text-sm mt-1">
                        {formatDate(report.created_at)} • {report.word_count.toLocaleString()} words
                      </p>
                    </div>
                    <button
                      onClick={() => onExportReport(sessionData.id, report.id)}
                      className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded transition-colors"
                    >
                      💾 Export
                    </button>
                  </div>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="max-h-64">
                    <pre className="text-neutral-300 text-sm whitespace-pre-wrap font-sans">
                      {report.content.length > 1000
                        ? `${report.content.substring(0, 1000)}...`
                        : report.content
                      }
                    </pre>
                  </ScrollArea>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}