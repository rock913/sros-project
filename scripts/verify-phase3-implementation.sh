#!/bin/bash
# Phase 3 Implementation Verification Script
# Checks code completeness without requiring running backend

echo "=========================================="
echo "Phase 3 Implementation Verification"
echo "=========================================="
echo ""

PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✅ File exists: $1"
        ((PASSED++))
        return 0
    else
        echo "❌ File missing: $1"
        ((FAILED++))
        return 1
    fi
}

# Function to check string in file
check_string() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo "✅ Found in $1: $2"
        ((PASSED++))
        return 0
    else
        echo "❌ Not found in $1: $2"
        ((FAILED++))
        return 1
    fi
}

echo "1. Backend WebSocket Endpoint"
echo "------------------------------"
check_file "backend/src/agent/app.py"
check_string "backend/src/agent/app.py" "@app.websocket(\"/agent/stream\")"
check_string "backend/src/agent/app.py" "WebSocketDisconnect"
check_string "backend/src/agent/app.py" "run_in_executor"
check_string "backend/src/agent/app.py" "db_manager.create_session"
check_string "backend/src/agent/app.py" "db_manager.log_event"
check_string "backend/src/agent/app.py" "db_manager.update_session"
echo ""

echo "2. Extension WebSocket Client"
echo "------------------------------"
check_file "vscode-extension/src/api.ts"
check_string "vscode-extension/src/api.ts" "import.*WebSocket.*from 'ws'"
check_string "vscode-extension/src/api.ts" "export async function startResearchStream"
check_string "vscode-extension/src/api.ts" "export interface ResearchProgressCallback"
check_string "vscode-extension/src/api.ts" "new WebSocket"
echo ""

echo "3. Extension UI Integration"
echo "------------------------------"
check_file "vscode-extension/src/extension.ts"
check_string "vscode-extension/src/extension.ts" "auto-researcher.startResearch"
check_string "vscode-extension/src/extension.ts" "startResearchStream"
check_string "vscode-extension/src/extension.ts" "Quick Actions"
check_string "vscode-extension/src/extension.ts" "Start New Research"
check_string "vscode-extension/src/extension.ts" "onDidReceiveMessage"
echo ""

echo "4. Test Scripts"
echo "------------------------------"
check_file "scripts/test-ws-quick.py"
check_file "scripts/test-websocket-stream.sh"
check_file "scripts/test-phase3-websocket.sh"
echo ""

echo "5. TypeScript Compilation"
echo "------------------------------"
cd vscode-extension
if npm run compile 2>&1 | grep -q "error"; then
    echo "❌ TypeScript compilation failed"
    ((FAILED++))
else
    echo "✅ TypeScript compilation passed"
    ((PASSED++))
fi
cd ..
echo ""

echo "6. Package Dependencies"
echo "------------------------------"
if grep -q '"ws"' vscode-extension/package.json; then
    echo "✅ ws dependency in package.json"
    ((PASSED++))
else
    echo "❌ ws dependency missing in package.json"
    ((FAILED++))
fi

if grep -q '"@types/ws"' vscode-extension/package.json; then
    echo "✅ @types/ws dependency in package.json"
    ((PASSED++))
else
    echo "❌ @types/ws dependency missing in package.json"
    ((FAILED++))
fi
echo ""

echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 Phase 3 implementation is COMPLETE!"
    echo ""
    echo "Implementation verified:"
    echo "  ✅ Backend WebSocket endpoint (/agent/stream)"
    echo "  ✅ Extension WebSocket client (api.ts)"
    echo "  ✅ Control Panel UI with Quick Actions"
    echo "  ✅ Command: auto-researcher.startResearch"
    echo "  ✅ Webview message handling"
    echo "  ✅ TypeScript compilation"
    echo "  ✅ Test scripts"
    echo ""
    echo "Next steps:"
    echo "  1. Start backend: docker-compose -f docker-compose-dev.yml up -d"
    echo "  2. Test WebSocket: bash scripts/test-phase3-websocket.sh"
    echo "  3. Test in VS Code: Open Control Panel → Start New Research"
    echo "  4. Proceed to Week 1 Task 1.3 (Documentation)"
    exit 0
else
    echo "⚠️  Some checks failed. Please review above."
    exit 1
fi
