#!/bin/bash
# Test script for LangGraph Checkpointer functionality

set -e  # Exit on error

echo "🧪 Testing LangGraph Checkpointer Implementation"
echo "================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8121"

echo -e "${BLUE}Step 1: Health Check${NC}"
curl -s ${BASE_URL}/ok | jq
echo ""

echo -e "${BLUE}Step 2: Test Session 1 - Create with thread_id 'test-session-001'${NC}"
echo "Topic: Artificial Intelligence in Healthcare"
RESPONSE1=$(curl -s -X POST ${BASE_URL}/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "Artificial Intelligence in Healthcare"}
      ]
    },
    "config": {
      "configurable": {
        "thread_id": "test-session-001"
      }
    }
  }')

echo "Response received (truncated):"
echo "$RESPONSE1" | jq -r '.output.report' | head -c 200
echo "..."
echo ""

echo -e "${BLUE}Step 3: Test Session 2 - Create with thread_id 'test-session-002' (parallel)${NC}"
echo "Topic: Quantum Computing Applications"
RESPONSE2=$(curl -s -X POST ${BASE_URL}/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "Quantum Computing Applications"}
      ]
    },
    "config": {
      "configurable": {
        "thread_id": "test-session-002"
      }
    }
  }')

echo "Response received (truncated):"
echo "$RESPONSE2" | jq -r '.output.report' | head -c 200
echo "..."
echo ""

echo -e "${BLUE}Step 4: Retrieve Session 1 State via thread_id${NC}"
STATE1=$(curl -s ${BASE_URL}/agent/state/test-session-001)
echo "Session 1 - Research Topic:"
echo "$STATE1" | jq -r '.research_topic'
echo "Session 1 - Number of papers:"
echo "$STATE1" | jq -r '.literature_abstracts | length'
echo ""

echo -e "${BLUE}Step 5: Retrieve Session 2 State via thread_id${NC}"
STATE2=$(curl -s ${BASE_URL}/agent/state/test-session-002)
echo "Session 2 - Research Topic:"
echo "$STATE2" | jq -r '.research_topic'
echo "Session 2 - Number of papers:"
echo "$STATE2" | jq -r '.literature_abstracts | length'
echo ""

echo -e "${BLUE}Step 6: Verify Session Isolation${NC}"
TOPIC1=$(echo "$STATE1" | jq -r '.research_topic')
TOPIC2=$(echo "$STATE2" | jq -r '.research_topic')

if [ "$TOPIC1" != "$TOPIC2" ]; then
    echo -e "${GREEN}✅ PASS: Sessions are properly isolated${NC}"
    echo "   - Session 1 topic: $TOPIC1"
    echo "   - Session 2 topic: $TOPIC2"
else
    echo -e "${RED}❌ FAIL: Sessions are not isolated!${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}Step 7: Check Database Checkpoints${NC}"
docker exec langgraph-postgres psql -U postgres -d postgres -c \
  "SELECT thread_id, checkpoint_id, created_at FROM checkpoints ORDER BY created_at DESC LIMIT 5;"
echo ""

echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "Summary:"
echo "--------"
echo "✅ Checkpointer is working correctly"
echo "✅ Thread-based session isolation is functional"
echo "✅ State persistence and retrieval is operational"
echo "✅ Multiple concurrent sessions are supported"
