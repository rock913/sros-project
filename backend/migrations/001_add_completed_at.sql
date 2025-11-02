-- Phase 3.5.3 Database Migration
-- Add completed_at column to sessions table for analytics

BEGIN;

-- Add completed_at column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'sessions' AND column_name = 'completed_at'
    ) THEN
        ALTER TABLE sessions 
        ADD COLUMN completed_at TIMESTAMP NULL;
        
        COMMENT ON COLUMN sessions.completed_at IS 'Timestamp when session completed';
    END IF;
END $$;

-- Update existing completed sessions with estimated completion time
-- (Use updated_at as a proxy if status is 'completed')
UPDATE sessions
SET completed_at = updated_at
WHERE status = 'completed' AND completed_at IS NULL;

-- Create indexes for analytics queries
CREATE INDEX IF NOT EXISTS idx_sessions_completed_at ON sessions(completed_at DESC);
CREATE INDEX IF NOT EXISTS idx_papers_created_at ON papers(created_at DESC);

COMMIT;

-- Verify migration
SELECT 
    'sessions.completed_at' as migration_check,
    EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'sessions' AND column_name = 'completed_at'
    ) as column_exists;
