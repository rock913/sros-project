import { useState, useEffect } from 'react';

interface Session {
  id: string;
  thread_id: string;
  title: string;
  research_topic: string;
  created_at: string;
  updated_at: string;
  status: 'completed' | 'in_progress' | 'paused' | 'failed';
  paper_count: number;
  report_count: number;
  tags: string[];
}

interface SessionListProps {
  onSelectSession: (sessionId: string) => void;
  onCreateNewSession: () => void;
}

export function SessionList({ onSelectSession, onCreateNewSession }: SessionListProps) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'completed' | 'in_progress' | 'failed'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    setLoading(true);
    try {
      // In a real implementation, this would use VSCodeBridge to request data
      // For now, we'll show a placeholder
      const mockSessions: Session[] = [
        {
          id: 'session-1',
          thread_id: 'thread-1',
          title: 'AI in Healthcare Research',
          research_topic: 'Applications of artificial intelligence in healthcare',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          status: 'completed',
          paper_count: 15,
          report_count: 1,
          tags: ['healthcare', 'ai']
        },
        {
          id: 'session-2',
          thread_id: 'thread-2',
          title: 'Machine Learning Algorithms',
          research_topic: 'Latest advances in machine learning algorithms',
          created_at: new Date(Date.now() - 86400000).toISOString(),
          updated_at: new Date(Date.now() - 86400000).toISOString(),
          status: 'in_progress',
          paper_count: 8,
          report_count: 0,
          tags: ['ml', 'algorithms']
        }
      ];
      setSessions(mockSessions);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅';
      case 'in_progress': return '🔄';
      case 'paused': return '⏸️';
      case 'failed': return '❌';
      default: return '❓';
    }
  };

  const filteredSessions = sessions.filter(session => {
    const matchesFilter = filter === 'all' || session.status === filter;
    const matchesSearch = !searchQuery ||
      session.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      session.research_topic.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-neutral-700 h-24 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-neutral-100">Research Sessions</h2>
        <button
          onClick={onCreateNewSession}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
        >
          + New Session
        </button>
      </div>

      <div className="mb-4 space-y-3">
        <input
          type="text"
          placeholder="Search sessions..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-3 py-2 bg-neutral-700 text-neutral-100 rounded border border-neutral-600 focus:outline-none focus:border-blue-400"
        />

        <div className="flex gap-2">
          {(['all', 'completed', 'in_progress', 'failed'] as const).map(status => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                filter === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 text-neutral-300 hover:bg-neutral-600'
              }`}
            >
              {status === 'all' ? 'All' :
               status === 'completed' ? 'Completed' :
               status === 'in_progress' ? 'In Progress' : 'Failed'}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        {filteredSessions.length === 0 ? (
          <div className="text-center py-8 text-neutral-400">
            <div className="text-4xl mb-4">📚</div>
            <p>No sessions found</p>
            <p className="text-sm">Try adjusting your search or filters</p>
          </div>
        ) : (
          filteredSessions.map(session => (
            <div
              key={session.id}
              onClick={() => onSelectSession(session.id)}
              className="bg-neutral-700 border border-neutral-600 rounded-lg p-4 cursor-pointer hover:border-neutral-500 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{getStatusIcon(session.status)}</span>
                    <h3 className="font-medium text-neutral-100">{session.title}</h3>
                  </div>

                  <p className="text-sm text-neutral-300 mb-3 line-clamp-2">
                    {session.research_topic}
                  </p>

                  <div className="flex items-center gap-4 text-xs text-neutral-400">
                    <span>📄 {session.paper_count} papers</span>
                    <span>📝 {session.report_count} reports</span>
                    <span>📅 {formatDate(session.updated_at)}</span>
                  </div>

                  {session.tags.length > 0 && (
                    <div className="flex gap-2 mt-3">
                      {session.tags.slice(0, 3).map(tag => (
                        <span
                          key={tag}
                          className="px-2 py-1 bg-neutral-600 text-neutral-300 text-xs rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}