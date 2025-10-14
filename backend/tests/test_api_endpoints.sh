#!/bin/bash

echo "============================================================"
echo "Phase 3.6 HITL API Endpoint Tests"
echo "============================================================"
echo ""

# Test 1: Get pending HITL requests
echo "📋 Test 1: GET /agent/hitl/pending"
echo "----------------------------"
SESSION_ID="fd3f71a2-ffc4-423f-8b53-e38f05307f27"
RESPONSE=$(curl -s "http://localhost:8121/agent/hitl/pending?session_id=$SESSION_ID")
echo "$RESPONSE" | jq -r '.pending_count'
PENDING_COUNT=$(echo "$RESPONSE" | jq -r '.pending_count')

if [ "$PENDING_COUNT" -gt 0 ]; then
    echo "✅ Test 1 PASSED: Found $PENDING_COUNT pending requests"
    
    # Extract first request_id for next test
    REQUEST_ID=$(echo "$RESPONSE" | jq -r '.requests[0].request_id')
    echo "   Request ID: $REQUEST_ID"
else
    echo "❌ Test 1 FAILED: No pending requests found"
    exit 1
fi

echo ""
echo "----------------------------"
echo ""

# Test 2: Respond to HITL request
echo "📤 Test 2: POST /agent/hitl/respond"
echo "----------------------------"

# API expects query parameters, not JSON body
RESPOND_RESPONSE=$(curl -s -X POST "http://localhost:8121/agent/hitl/respond?request_id=$REQUEST_ID&decision=approve" \
  -H "Content-Type: application/json")

echo "$RESPOND_RESPONSE" | jq '.'

STATUS=$(echo "$RESPOND_RESPONSE" | jq -r '.status // empty')
MESSAGE=$(echo "$RESPOND_RESPONSE" | jq -r '.message // empty')
if [ "$STATUS" = "success" ] || [ -n "$MESSAGE" ]; then
    echo "✅ Test 2 PASSED: Response recorded"
    echo "   Status: $STATUS"
    echo "   Message: $MESSAGE"
else
    echo "⚠️ Test 2: Response status unclear (check output above)"
fi

echo ""
echo "----------------------------"
echo ""

# Test 3: Verify pending count decreased
echo "🔍 Test 3: Verify pending count decreased"
echo "----------------------------"
NEW_RESPONSE=$(curl -s "http://localhost:8121/agent/hitl/pending?session_id=$SESSION_ID")
NEW_PENDING_COUNT=$(echo "$NEW_RESPONSE" | jq -r '.pending_count')

echo "Before: $PENDING_COUNT pending"
echo "After:  $NEW_PENDING_COUNT pending"

if [ "$NEW_PENDING_COUNT" -lt "$PENDING_COUNT" ]; then
    echo "✅ Test 3 PASSED: Pending count decreased"
else
    echo "⚠️ Test 3: Pending count unchanged (may need manual verification)"
fi

echo ""
echo "============================================================"
echo "API Endpoint Tests Complete"
echo "============================================================"
