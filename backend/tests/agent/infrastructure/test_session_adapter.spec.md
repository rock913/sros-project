# Session Adapter Behavior Specification

This document describes the expected behavior of SessionManager implementations (PostgresSessionAdapter and InMemorySessionAdapter) for Phase 3.5.1. These specifications serve as the acceptance criteria for Aider TDD implementation.

## Core Behaviors

### 1. Session Creation
- **Given**: Valid topic (3-200 chars) and optional description
- **When**: `create_session` is called
- **Then**: Returns `ResearchSession` with:
  - Generated UUID `id`
  - Status "active"
  - Current UTC timestamps for `created_at` and `updated_at`
  - Empty lists for `papers`, `reports`, `events`

### 2. Duplicate Topic Handling
- **Given**: Two sessions with identical topics
- **When**: Both are created
- **Then**: Both are saved with different UUIDs and timestamps
- **Note**: Duplicate topics are allowed (research on same topic at different times)

### 3. Invalid Topic Handling
- **Given**: Empty or whitespace-only topic
- **When**: `create_session` is called
- **Then**: Raises `ValueError` with message "Topic cannot be empty or whitespace"

### 4. Database Connection Failure
- **Given**: Database is unreachable
- **When**: Any SessionManager method is called
- **Then**: Raises `ConnectionError` with descriptive message

### 5. Session Retrieval
- **Given**: Existing session ID
- **When**: `get_session` is called
- **Then**: Returns the complete `ResearchSession` object

### 6. Non-existent Session Retrieval
- **Given**: Non-existent session ID
- **When**: `get_session` is called
- **Then**: Returns `None`

### 7. Session Listing with Pagination
- **Given**: 10 sessions in database
- **When**: `list_sessions(limit=5, offset=0)` is called
- **Then**: Returns first 5 sessions ordered by `created_at` (newest first)
- **When**: `list_sessions(limit=5, offset=5)` is called
- **Then**: Returns next 5 sessions

### 8. Session Event Creation
- **Given**: Existing session ID and valid event data
- **When**: `add_session_event` is called
- **Then**: Creates `SessionEvent` with:
  - Generated UUID `id`
  - Current UTC timestamp
  - Event data stored as JSON-serializable dict
- **And**: Event is associated with the session

### 9. Event Type Validation
- **Given**: Invalid event type (not in allowed set)
- **When**: `add_session_event` is called
- **Then**: Raises `ValueError` listing allowed event types

### 10. Session Status Updates
- **Given**: Existing active session
- **When**: `update_session_status(session_id, "completed")` is called
- **Then**: Session status changes to "completed"
- **And**: `updated_at` timestamp is updated

### 11. Invalid Status Transition
- **Given**: Existing session
- **When**: `update_session_status` is called with invalid status (not "active"/"completed"/"archived")
- **Then**: Raises `ValueError`

### 12. Paper Association
- **Given**: Existing session and Paper domain model
- **When**: `add_paper_to_session` is called
- **Then**: Paper ID is added to session's `papers` list
- **Note**: Paper should be persisted separately; this only creates association

### 13. Report Association
- **Given**: Existing session and Report domain model
- **When**: `add_report_to_session` is called
- **Then**: Report ID is added to session's `reports` list

### 14. Session Papers Retrieval
- **Given**: Session with 3 associated papers
- **When**: `get_session_papers` is called
- **Then**: Returns list of 3 Paper objects (loaded from paper storage)

### 15. Session Reports Retrieval
- **Given**: Session with 2 associated reports
- **When**: `get_session_reports` is called
- **Then**: Returns list of 2 Report objects

## Adapter-Specific Behaviors

### PostgresSessionAdapter
- **Requires**: PostgreSQL database with vector extension
- **Connection**: Uses SQLAlchemy with connection pooling
- **Transactions**: All operations are transactional with rollback on failure
- **Scalability**: Supports concurrent access from multiple threads/processes

### InMemorySessionAdapter (Shadow Adapter)
- **Purpose**: For testing without database dependencies
- **Persistence**: In-memory storage only (lost on restart)
- **Thread Safety**: Not required (single-threaded tests only)
- **Performance**: Sub-millisecond response times

## Error Handling Requirements

1. **Network Errors**: Gracefully handle database connection failures
2. **Data Integrity**: Validate all inputs before database operations
3. **Transaction Safety**: Ensure atomic operations (all or nothing)
4. **Resource Cleanup**: Close database connections properly

## Performance Requirements

1. **Response Time**: < 100ms for all operations (excluding network latency)
2. **Concurrency**: Support at least 10 concurrent sessions
3. **Memory Usage**: Efficient memory usage for large session histories

## Test Data Requirements

All tests must use mock data and should not require:
- Real database credentials
- External API keys
- Network connectivity
- Pre-existing data in databases

Tests should be completely isolated and repeatable.
