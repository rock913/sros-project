#!/bin/bash

# Reset DB for testing - clean slate approach
# This ensures tests start with a clean database state

echo "🧹 Resetting database for clean test slate..."

# Wait for DB to be ready
echo "⏳ Waiting for database..."
sleep 2

# Execute TRUNCATE with CASCADE to handle foreign keys
docker exec langgraph-postgres psql -U postgres -d postgres -c "
TRUNCATE TABLE
  sessions,
  papers,
  reports
  CASCADE;
"

if [ $? -eq 0 ]; then
    echo "✅ Database reset completed"
else
    echo "❌ Database reset failed"
    exit 1
fi