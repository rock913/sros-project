-- Migration: Add Performance Indexes for Phase 3.5.4
-- Author: Development Team
-- Date: 2025-10-14
-- Description: Optimize database queries by adding strategic indexes

BEGIN;

-- ====================
-- Papers Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_papers_session_id 
ON papers(session_id);

-- Common query: sort by creation date
CREATE INDEX IF NOT EXISTS idx_papers_created_at 
ON papers(created_at DESC);

-- Common query: lookup by DOI
CREATE INDEX IF NOT EXISTS idx_papers_doi 
ON papers(doi) 
WHERE doi IS NOT NULL;

-- ====================
-- Reports Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_reports_session_id 
ON reports(session_id);

-- Common query: get latest version per session
CREATE INDEX IF NOT EXISTS idx_reports_session_version 
ON reports(session_id, version DESC);

-- ====================
-- Session Events Table Indexes
-- ====================

-- Most common query: filter by session_id
CREATE INDEX IF NOT EXISTS idx_session_events_session_id 
ON session_events(session_id);

-- Common query: sort by timestamp
CREATE INDEX IF NOT EXISTS idx_session_events_created_at 
ON session_events(created_at DESC);

-- Common query: filter by event type
CREATE INDEX IF NOT EXISTS idx_session_events_type 
ON session_events(event_type);

-- Composite index for timeline queries
CREATE INDEX IF NOT EXISTS idx_session_events_session_time 
ON session_events(session_id, created_at DESC);

-- ====================
-- Sessions Table Indexes
-- ====================

-- Common query: filter by status
CREATE INDEX IF NOT EXISTS idx_sessions_status 
ON sessions(status);

-- Common query: sort by creation date
CREATE INDEX IF NOT EXISTS idx_sessions_created_at 
ON sessions(created_at DESC);

-- Common query: filter by thread_id
CREATE INDEX IF NOT EXISTS idx_sessions_thread_id 
ON sessions(thread_id);

COMMIT;

-- ====================
-- Verification Queries
-- ====================
-- To verify indexes were created, run:
-- SELECT indexname, tablename FROM pg_indexes WHERE indexname LIKE 'idx_%' ORDER BY tablename, indexname;

-- ====================
-- Rollback Script
-- ====================
-- To rollback, run:
-- BEGIN;
-- DROP INDEX IF EXISTS idx_papers_session_id;
-- DROP INDEX IF EXISTS idx_papers_created_at;
-- DROP INDEX IF EXISTS idx_papers_doi;
-- DROP INDEX IF EXISTS idx_reports_session_id;
-- DROP INDEX IF EXISTS idx_reports_session_version;
-- DROP INDEX IF EXISTS idx_session_events_session_id;
-- DROP INDEX IF EXISTS idx_session_events_created_at;
-- DROP INDEX IF EXISTS idx_session_events_type;
-- DROP INDEX IF EXISTS idx_session_events_session_time;
-- DROP INDEX IF EXISTS idx_sessions_status;
-- DROP INDEX IF EXISTS idx_sessions_created_at;
-- DROP INDEX IF EXISTS idx_sessions_thread_id;
-- COMMIT;
