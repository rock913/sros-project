#!/bin/bash

# WebSocket Test Script for Research Progress Fix
# This script simulates the frontend WebSocket connection to test the fix

echo "🧪 Testing WebSocket Research Streaming..."
echo "=========================================="
echo ""

# Use websocat if available, otherwise provide instructions
if command -v websocat &> /dev/null; then
    echo "📡 Connecting to WebSocket endpoint..."
    echo '{"messages": [{"role": "user", "content": "recent advance on ai"}]}' | \
    websocat -n1 ws://localhost:8121/agent/stream
else
    echo "⚠️  websocat not found. Install it with:"
    echo "   Ubuntu/Debian: sudo apt install websocat"
    echo "   macOS: brew install websocat"
    echo ""
    echo "Alternative: Test from VS Code Extension Development Host"
    echo "1. Press F5 to launch Extension"
    echo "2. Open Analytics Dashboard"
    echo "3. Enter topic: 'recent advance on ai'"
    echo "4. Click 'Start Research'"
    echo ""
    echo "Expected behavior:"
    echo "✅ Progress updates beyond 20%"
    echo "✅ Shows HITL pause notification"
    echo "✅ Continues after approval"
fi
