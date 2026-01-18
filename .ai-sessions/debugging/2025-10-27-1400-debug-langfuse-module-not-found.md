# Debug Session: Module Import & Lifespan Errors

**Date**: 2025-10-27  
**Time**: 14:00 - 14:45 UTC  
**Category**: debug  
**Status**: ✅ RESOLVED

---

## 📋 Problem Statement

### Initial Error
```
ModuleNotFoundError: No module named 'langfuse'
```

### Secondary Error (After langfuse fix)
```
ValueError: Cannot merge lifespans with on_startup or on_shutdown: [<function on_startup at 0x7fc9011c2ca0>] []
```

**Symptoms**:
1. Frontend shows no input field
2. Backend container fails to start with module import errors
3. After adding langfuse, lifespan conflict error appeared

---

## 🔍 Debugging Snapshot #1: Langfuse Module Missing

**Time**: 14:00 - 14:10  
**Hypothesis**: `langfuse` package not in `backend/pyproject.toml` dependencies

**Investigation**:
```bash
# Error traceback showed:
# File "/deps/backend/src/agent/hitl_nodes.py", line 24, in <module>
#   from langfuse import Langfuse
# ModuleNotFoundError: No module named 'langfuse'
```

**Root Cause**: Phase 4.1 LangFuse integration added imports but didn't update `pyproject.toml`

**Files Using Langfuse**:
1. `backend/src/agent/hitl_nodes.py` - Line 24
2. `backend/src/agent/app.py` - Line 17
3. `backend/src/agent/document_utils.py` - Line 20
4. `backend/src/agent/graph.py` - Line 758

**Fix Applied**:
```toml
# backend/pyproject.toml
[project]
dependencies = [
    # ... existing deps ...
    "langfuse>=2.0.0",  # ✅ Added for Phase 4.1 observability
]
```

**Verification**:
```bash
docker compose build langgraph-api  # ✅ Build successful
```

---

## 🔍 Debugging Snapshot #2: LangChain Text Splitter Import Error

**Time**: 14:10 - 14:15  
**Hypothesis**: `langchain.text_splitter` module moved to separate package

**Investigation**:
```bash
# New error after langfuse fix:
# ModuleNotFoundError: No module named 'langchain.text_splitter'
```

**Root Cause**: LangChain refactored text splitters into `langchain-text-splitters` package

**Fix Applied**:
```toml
# backend/pyproject.toml
[project]
dependencies = [
    # ... existing deps ...
    "langchain-text-splitters>=0.2.0",  # ✅ Added for RecursiveCharacterTextSplitter
]
```

**Verification**:
```bash
docker compose build langgraph-api  # ✅ Build successful
```

---

## 🔍 Debugging Snapshot #3: FastAPI Lifespan Conflict

**Time**: 14:15 - 14:40  
**Hypothesis**: Old `@app.on_event("startup")` conflicts with LangGraph API's lifespan

**Investigation**:
```bash
# Error after rebuilding:
# ValueError: Cannot merge lifespans with on_startup or on_shutdown
```

**Root Cause**: 
- FastAPI's new version doesn't support mixing `@app.on_event()` with `lifespan` context managers
- LangGraph API server uses `lifespan` internally
- Our `backend/src/agent/app.py` was using deprecated `@app.on_event("startup")`

**Fix Applied**:
```python
# backend/src/agent/app.py

# 1. Added import
from contextlib import asynccontextmanager

# 2. Created lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    print("--- Initializing database ---")
    init_db()
    db_manager.init_db()  # Initialize session management tables
    print("--- Database initialized ---")
    yield
    # Cleanup code can go here if needed
    print("--- Shutting down ---")

# 3. Updated FastAPI app initialization
app = FastAPI(
    title="Autonomous Research Agent API",
    description="An API for an autonomous research agent powered by LangGraph and Gemini.",
    version="1.0.0",
    lifespan=lifespan,  # ✅ Added lifespan parameter
)

# 4. Removed old on_event decorator
# ❌ REMOVED:
# @app.on_event("startup")
# async def on_startup():
#     ...
```

**Verification**:
```bash
# Rebuild and restart
docker compose build langgraph-api  # ✅ Build successful
docker compose up -d langgraph-api  # ✅ Started successfully

# Check logs
docker logs langgraph-api --tail 40
# ✅ No errors
# ✅ "--- Initializing database ---"
# ✅ "--- Database initialized ---"
# ✅ "Uvicorn running on http://0.0.0.0:8000"

# Health check
curl http://localhost:8121/health
# ✅ Status: "degraded" (only missing UNPAYWALL_EMAIL env var)
# ✅ Database: "healthy"
# ✅ LangGraph: "healthy"

# API test
curl http://localhost:8121/sessions
# ✅ Returns 50 sessions
```

---

## 📊 Summary

### Issues Resolved
1. ✅ **ModuleNotFoundError: langfuse** - Added `langfuse>=2.0.0` to dependencies
2. ✅ **ModuleNotFoundError: langchain.text_splitter** - Added `langchain-text-splitters>=0.2.0`
3. ✅ **ValueError: Cannot merge lifespans** - Migrated from `@app.on_event()` to `lifespan` context manager

### Files Modified
1. `backend/pyproject.toml` - Added 2 dependencies
2. `backend/src/agent/app.py` - Migrated to lifespan pattern

### Time Breakdown
- **Debugging**: 15 minutes
- **Fixing**: 20 minutes
- **Verification**: 10 minutes
- **Total**: 45 minutes

### Next Steps
- [ ] Test frontend input field visibility
- [ ] Run E2E tests to ensure full functionality
- [ ] Update `.env` to fix UNPAYWALL_EMAIL warning (already exists, needs container restart)
- [ ] Document the lifespan migration pattern in TESTING.md

---

## 📚 Lessons Learned

1. **Dependency Management**: When adding new features (Phase 4.1 LangFuse), always update `pyproject.toml` immediately
2. **FastAPI Migration**: Modern FastAPI (>=0.109.0) requires `lifespan` context managers instead of `@app.on_event()`
3. **LangChain Evolution**: LangChain is actively refactoring - always check for moved modules
4. **Docker Build Cache**: After dependency changes, full rebuild is required (`docker compose build`)

---

## 🔗 References

- **FastAPI Lifespan Events**: https://fastapi.tiangolo.com/advanced/events/
- **LangFuse Documentation**: https://langfuse.com/docs
- **LangChain Text Splitters**: https://python.langchain.com/docs/modules/data_connection/document_transformers/

---

**Session Complete**: 2025-10-27 14:45 UTC
