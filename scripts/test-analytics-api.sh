#!/bin/bash
# Phase 3.5.3 Analytics API Testing Script

echo "=========================================="
echo "Phase 3.5.3 Analytics API Tests"
echo "=========================================="
echo ""

API_BASE="http://localhost:8121"
PASSED=0
FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -n "Testing: $description... "
    
    response=$(curl -s -w "\n%{http_code}" -X $method "$API_BASE$endpoint")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        ((PASSED++))
        
        # Pretty print JSON if jq is available
        if command -v jq &> /dev/null; then
            echo "$body" | jq '.' | head -20
        else
            echo "$body" | head -5
        fi
        echo ""
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
        ((FAILED++))
        echo "Response: $body"
        echo ""
    fi
}

echo "1. Health Check"
echo "---------------"
test_endpoint "Backend Health" "GET" "/ok"

echo "2. Analytics - Sessions List"
echo "-----------------------------"
test_endpoint "GET" "/analytics/sessions?limit=10&offset=0" "Get sessions list (default)"
test_endpoint "GET" "/analytics/sessions?status=completed&sort_by=created_at&order=desc" "Filter completed sessions"
test_endpoint "GET" "/analytics/sessions?limit=5&sort_by=papers_count&order=desc" "Sort by papers count"

echo "3. Analytics - Session Stats"
echo "-----------------------------"
test_endpoint "GET" "/analytics/sessions/stats?time_range=7d" "Get 7-day stats"
test_endpoint "GET" "/analytics/sessions/stats?time_range=30d" "Get 30-day stats"
test_endpoint "GET" "/analytics/sessions/stats?time_range=all" "Get all-time stats"

echo "4. Analytics - Paper Trends"
echo "----------------------------"
test_endpoint "GET" "/analytics/papers/trends?time_range=7d" "Get 7-day paper trends"
test_endpoint "GET" "/analytics/papers/trends?time_range=30d" "Get 30-day paper trends"

echo "5. Analytics - Session Details"
echo "-------------------------------"
# First get a session ID
echo "Fetching a sample session ID..."
SESSION_ID=$(curl -s "$API_BASE/analytics/sessions?limit=1" | grep -o '"session_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$SESSION_ID" ]; then
    echo "Found session: $SESSION_ID"
    test_endpoint "GET" "/analytics/sessions/$SESSION_ID" "Get session details"
else
    echo "⚠️  No sessions found to test details endpoint"
fi

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All Analytics API tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed. Check output above."
    exit 1
fi
