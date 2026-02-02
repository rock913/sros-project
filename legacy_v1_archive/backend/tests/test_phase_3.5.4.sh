#!/bin/bash
set -e

echo "🧪 Phase 3.5.4 Integration Tests"
echo "================================="

# Test environment
API_URL="http://localhost:8121"
DB_CONTAINER="langgraph-postgres"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Database Indexes
echo ""
echo "Test 1: Database Indexes"
echo "------------------------"

INDEXES=$(docker exec $DB_CONTAINER psql -U postgres -d postgres -t -c "SELECT COUNT(*) FROM pg_indexes WHERE indexname LIKE 'idx_%';")
EXPECTED_MIN=12

if [ "$INDEXES" -ge "$EXPECTED_MIN" ]; then
    echo "Found $INDEXES indexes (expected >= $EXPECTED_MIN)"
    test_result 0
    
    # List key indexes
    echo ""
    echo "Key indexes:"
    docker exec $DB_CONTAINER psql -U postgres -d postgres -t -c "SELECT '  - ' || indexname || ' ON ' || tablename FROM pg_indexes WHERE indexname LIKE 'idx_%' ORDER BY tablename, indexname LIMIT 10;"
else
    echo "Found $INDEXES indexes (expected >= $EXPECTED_MIN)"
    test_result 1
fi

# Test 2: Backend API Health
echo ""
echo "Test 2: Backend API Health"
echo "--------------------------"

HEALTH_RESPONSE=$(curl -s $API_URL/health || echo "ERROR")

if echo "$HEALTH_RESPONSE" | jq -e '.status' > /dev/null 2>&1; then
    STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.status')
    echo "API Status: $STATUS"
    
    if [ "$STATUS" = "healthy" ] || [ "$STATUS" = "degraded" ]; then
        test_result 0
    else
        test_result 1
    fi
else
    echo "API not responding or invalid response"
    test_result 1
fi

# Test 3: API Performance - Papers Endpoint
echo ""
echo "Test 3: API Performance - Papers Endpoint"
echo "------------------------------------------"

# Warm up
curl -s $API_URL/papers?limit=10 > /dev/null 2>&1

# Actual test
START_TIME=$(date +%s%N)
curl -s $API_URL/papers?limit=100 > /dev/null
END_TIME=$(date +%s%N)
ELAPSED=$((($END_TIME - $START_TIME) / 1000000)) # Convert to milliseconds

echo "Response time: ${ELAPSED}ms (target: < 500ms)"

if [ $ELAPSED -lt 500 ]; then
    test_result 0
else
    test_result 1
fi

# Test 4: VS Code Extension Compilation
echo ""
echo "Test 4: VS Code Extension Compilation"
echo "--------------------------------------"

COMPILE_OUTPUT=$(docker exec vscode-dev bash -c "cd /workspaces/gemini-fullstack-langgraph-quickstart/vscode-extension && npm run compile 2>&1")
COMPILE_EXIT=$?

if [ $COMPILE_EXIT -eq 0 ]; then
    echo "Compilation successful"
    
    # Check for deprecation warnings
    if echo "$COMPILE_OUTPUT" | grep -qi "deprecat"; then
        echo -e "${YELLOW}⚠️  Warning: Still has deprecation warnings${NC}"
        echo "$COMPILE_OUTPUT" | grep -i deprecat | head -5
    fi
    
    test_result 0
else
    echo "Compilation failed"
    echo "$COMPILE_OUTPUT" | tail -20
    test_result 1
fi

# Test 5: WebSocket Heartbeat Mechanism
echo ""
echo "Test 5: WebSocket Heartbeat Mechanism"
echo "--------------------------------------"

# Check if heartbeat code exists in app.py
if grep -q "HEARTBEAT_INTERVAL" /mnt/data/hyf/gemini-fullstack-langgraph-quickstart/backend/src/agent/app.py; then
    echo "Heartbeat mechanism implemented in code"
    test_result 0
else
    echo "Heartbeat mechanism not found in code"
    test_result 1
fi

# Test 6: Database Migration Script
echo ""
echo "Test 6: Database Migration Script"
echo "----------------------------------"

MIGRATION_FILE="/mnt/data/hyf/gemini-fullstack-langgraph-quickstart/backend/migrations/001_add_indexes.sql"

if [ -f "$MIGRATION_FILE" ]; then
    echo "Migration script exists: $MIGRATION_FILE"
    
    # Check if it has required indexes
    INDEX_COUNT=$(grep -c "CREATE INDEX" "$MIGRATION_FILE" || echo "0")
    echo "Found $INDEX_COUNT CREATE INDEX statements"
    
    if [ $INDEX_COUNT -ge 10 ]; then
        test_result 0
    else
        test_result 1
    fi
else
    echo "Migration script not found"
    test_result 1
fi

# Test 7: Loading Indicator in Analytics Webview
echo ""
echo "Test 7: Loading Indicator in Analytics Webview"
echo "-----------------------------------------------"

WEBVIEW_FILE="/mnt/data/hyf/gemini-fullstack-langgraph-quickstart/vscode-extension/src/analyticsWebview.ts"

if grep -q "loading-container" "$WEBVIEW_FILE" && grep -q "spinner" "$WEBVIEW_FILE"; then
    echo "Loading indicator implemented in Analytics Webview"
    test_result 0
else
    echo "Loading indicator not found in Analytics Webview"
    test_result 1
fi

# Summary
echo ""
echo "================================="
echo "📊 Test Summary"
echo "================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
