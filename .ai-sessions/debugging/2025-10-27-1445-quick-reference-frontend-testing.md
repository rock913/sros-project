# Quick Reference: Frontend Testing

**Date**: 2025-10-27 14:45 UTC  
**Context**: After fixing backend startup issues  
**Related**: [2025-10-27-1400-debug-langfuse-module-not-found.md](./2025-10-27-1400-debug-langfuse-module-not-found.md)

---

## 🎯 Testing Checklist

### 1. Backend Health Verification ✅

```bash
# Check service status
docker compose ps

# Health check
curl http://localhost:8121/health | jq '.'

# List sessions
curl http://localhost:8121/sessions | jq '. | length'
```

**Expected Results**:
- ✅ All containers running
- ✅ Health status: "healthy" or "degraded" (degraded is OK if only missing optional env vars)
- ✅ Sessions endpoint returns data

---

## 🖥️ Frontend Testing Options

### Option A: VS Code Extension (Recommended)

**Location**: `vscode-extension/`

**Steps**:
1. Open VS Code
2. Press `F5` to launch Extension Development Host
3. In the new VS Code window:
   - Open Command Palette (`Cmd/Ctrl + Shift + P`)
   - Type: "Research Agent"
   - Select: "Research Agent: Open Control Panel"
4. Test the UI:
   - Should see input field for research topic
   - Should see "Start Research" button
   - Should see list of previous sessions

**What to Check**:
- [ ] Input field is visible
- [ ] "Start Research" button works
- [ ] Sessions list loads (should show 50 sessions)
- [ ] Can click on a session to view details
- [ ] WebSocket connection established (check browser console)

---

### Option B: Web Frontend

**Location**: `frontend/`

**Steps**:
```bash
cd frontend
npm install
npm run dev
```

**Access**: http://localhost:5173

**What to Check**:
- [ ] Research topic input field visible
- [ ] Can submit new research request
- [ ] Sessions list displays
- [ ] Real-time updates work (WebSocket)

---

### Option C: Direct API Testing

**Test Basic Flow**:
```bash
# 1. Create a new session
curl -X POST http://localhost:8121/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test-'$(date +%s)'",
    "title": "Test Research Session",
    "user_query": "What are the latest advances in neural networks?",
    "status": "active",
    "metadata": {"source": "manual_test"}
  }' | jq '.'

# 2. Get session details
SESSION_ID="<from above response>"
curl http://localhost:8121/sessions/$SESSION_ID | jq '.'

# 3. Test HITL endpoint
curl http://localhost:8121/hitl/pending | jq '.'

# 4. Test document collaboration endpoint
curl http://localhost:8121/documents/changes/$SESSION_ID | jq '.'
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot connect to backend"

**Check**:
```bash
docker logs langgraph-api --tail 50
curl http://localhost:8121/health
```

**Solution**: Backend might still be starting. Wait 10-20 seconds.

---

### Issue 2: "Input field not visible"

**Possible Causes**:
1. Frontend not built properly
2. WebSocket connection failed
3. API endpoint mismatch

**Debug Steps**:
```bash
# Check browser console (F12)
# Look for errors like:
# - "WebSocket connection failed"
# - "404 Not Found"
# - "CORS error"

# Verify API is accessible
curl http://localhost:8121/sessions
```

---

### Issue 3: "WebSocket connection failed"

**Check**:
```bash
# Test WebSocket endpoint
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  http://localhost:8121/stream/test-thread-id
```

**Solution**: Ensure CORS is properly configured in `backend/src/agent/app.py`

---

## 📊 Expected Behavior (Phase 3.6 + 4.1)

### Features Available:
1. ✅ **Basic Research Flow**
   - Submit research topic
   - Stream real-time progress
   - View final report

2. ✅ **HITL (Human-in-the-Loop)** - Phase 3.6 Week 1-2
   - Query approval prompts
   - Paper selection prompts
   - Report revision prompts

3. ✅ **Session Management** - Phase 3.5.4
   - List all sessions
   - View session details
   - Track session events

4. ✅ **Analytics** - Phase 3.5.3
   - Token usage tracking
   - Cost estimation
   - Performance metrics

5. 🚧 **Document Collaboration** - Phase 3.6 Week 3 (In Progress)
   - Real-time document updates
   - Conflict detection
   - Version tracking

6. 🚧 **LangFuse Integration** - Phase 4.1 (Partially Complete)
   - Trace visualization
   - Performance monitoring
   - HITL decision tracking

---

## 🔧 Debugging Commands

```bash
# View all logs
docker compose logs -f

# View only backend logs
docker logs langgraph-api -f

# View only PostgreSQL logs
docker logs langgraph-postgres -f

# Check Redis
docker exec -it langgraph-redis redis-cli PING

# Check database
docker exec -it langgraph-postgres psql -U postgres -d postgres -c "\dt"

# Restart specific service
docker compose restart langgraph-api

# Rebuild and restart
docker compose build langgraph-api && docker compose up -d langgraph-api
```

---

## 📝 Test Data

**Sample Research Topics** (for testing):
1. "What are the latest advances in transformer architectures?"
2. "How does federated learning preserve privacy?"
3. "What are the applications of graph neural networks in drug discovery?"
4. "Explain the trade-offs between model size and inference speed"

**Sample Session IDs** (from existing data):
```bash
# Get recent sessions
curl http://localhost:8121/sessions?limit=5 | jq '.[].session_id'
```

---

## 🎯 Success Criteria

Frontend test is successful if:
- [ ] Input field is visible and accepts text
- [ ] "Start Research" button triggers backend API
- [ ] Real-time progress updates appear
- [ ] Session list displays historical data
- [ ] WebSocket connection maintains stability
- [ ] HITL prompts appear when required
- [ ] Final report displays correctly

---

## 📚 Related Documentation

- **API Documentation**: http://localhost:8121/docs
- **Project README**: `/README.md`
- **Testing Guide**: `/TESTING.md`
- **GEMINI Framework**: `/GEMINI.md`
- **Phase 3.6 Plans**: `/.ai-sessions/development/PHASE_3.6_*`
- **Phase 4.1 Plans**: `/.ai-sessions/development/2025-10-16-1300-phase-4.2-plan-production-optimization.md`

---

**Next Steps**:
1. Choose a testing option (A, B, or C)
2. Follow the steps above
3. Report any issues or unexpected behavior
4. Update this document with findings

**Last Updated**: 2025-10-27 14:45 UTC
