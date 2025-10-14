# Phase 3.6 Week 3 - Real-time Document Collaboration

**Start Date**: 2025-10-14  
**Duration**: 5-7 days  
**Status**: 🚧 **IN PROGRESS** - Day 1  
**Goal**: Enable AI and user to collaboratively edit research reports in real-time

---

## 📋 Implementation Plan Overview

### Day 1-2: Backend Document Streaming ⏳ IN PROGRESS
- [ ] Document Diff generation (diff-match-patch)
- [ ] WebSocket message protocol extension
- [ ] Conflict detection mechanism
- [ ] Unit tests for document utils

### Day 3-4: Frontend Document Integration
- [ ] VS Code Workspace API integration
- [ ] Change decorations (gutter icons, highlights)
- [ ] Accept/Reject CodeLens UI
- [ ] WebSocket message handling

### Day 5: Conflict Resolution
- [ ] Conflict detection UI
- [ ] Three-way merge implementation
- [ ] Retry mechanism
- [ ] Conflict resolution tests

### Day 6: Undo/Redo & Polish
- [ ] Undo stack integration
- [ ] Performance optimization
- [ ] Error handling
- [ ] Documentation

### Day 7: Testing & Documentation
- [ ] Comprehensive testing
- [ ] Final documentation
- [ ] Git commit & tag

---

## Day 1 Tasks - Backend Document Streaming (Part 1)

**Current Time**: 2025-10-14 Morning  
**Focus**: Document diff generation and streaming infrastructure

### Task 1.1: Install Dependencies ✅

```bash
# Install diff-match-patch for incremental diff generation
docker exec langgraph-api pip install diff-match-patch
```

### Task 1.2: Create Document Utils Module

**File**: `backend/src/agent/document_utils.py`

**Functions to Implement**:
1. `generate_paragraph_diff()` - Compare two text versions, return paragraph-level changes
2. `extract_paragraphs()` - Split Markdown into paragraphs
3. `calculate_line_range()` - Convert paragraph index to line numbers
4. `generate_update_message()` - Create WebSocket message payload

**Test-Driven Approach**:
- Write tests first in `backend/tests/test_document_utils.py`
- Implement functions to pass tests
- Target: >90% code coverage

### Task 1.3: Extend WebSocket Protocol

**File**: `backend/src/agent/app.py`

**New Message Types**:
```python
# Document update message
{
    "type": "document_update",
    "action": "insert" | "replace" | "delete",
    "range": {
        "startLine": 10,
        "startColumn": 0,
        "endLine": 12,
        "endColumn": 0
    },
    "content": "New paragraph content...",
    "rationale": "Adding methodology section based on selected papers"
}

# Conflict notification
{
    "type": "document_conflict",
    "conflictingRange": {...},
    "aiContent": "AI's version",
    "userContent": "User's version",
    "baseContent": "Original version"
}
```

### Task 1.4: Integrate with Synthesis Node

**File**: `backend/src/agent/graph.py` (synthesis_node)

**Strategy**: Stream report generation paragraph-by-paragraph
- Generate first paragraph → Send `document_update`
- Generate second paragraph → Send `document_update`
- Continue until report complete

---

## Success Criteria - Day 1

- [x] diff-match-patch installed and working
- [ ] `document_utils.py` module created with 4 core functions
- [ ] Unit tests written and passing (>90% coverage)
- [ ] WebSocket message protocol documented
- [ ] Basic integration with synthesis_node

---

## Technical Design Decisions

### 1. Granularity: Paragraph-Level Updates

**Rationale**:
- Too fine-grained (sentence): Too many WebSocket messages, UI flicker
- Too coarse (full document): Not incremental, defeats purpose
- **Paragraph**: Natural semantic unit, balances performance and UX

**Implementation**:
```python
# Split by double newline (Markdown paragraph separator)
paragraphs = content.split('\n\n')
```

### 2. Conflict Detection Strategy

**Version Tracking**:
- Use SHA-256 hash of document content
- Track last known version on backend
- On each update, compare hashes
- If mismatch → User edited → Conflict

**Conflict Types**:
1. **Non-overlapping**: User edits paragraph 1, AI edits paragraph 5 → Auto-merge
2. **Overlapping**: Both edit paragraph 3 → Show conflict UI
3. **Concurrent**: User typing while AI sending update → Queue AI update

### 3. Performance Optimization

**Batching**:
- Don't send updates faster than 500ms
- Batch multiple small edits into one message
- Use debounce on frontend to avoid UI thrashing

**Diff Algorithm**:
- Use `diff-match-patch` library (Google's algorithm)
- Time complexity: O(n*d) where d is edit distance
- Acceptable for typical report size (<10,000 words)

---

## Testing Strategy

### Unit Tests (`test_document_utils.py`)

```python
def test_extract_paragraphs():
    text = "Para 1\n\nPara 2\n\nPara 3"
    assert len(extract_paragraphs(text)) == 3

def test_generate_paragraph_diff_insert():
    old = "Para 1\n\nPara 2"
    new = "Para 1\n\nPara 1.5\n\nPara 2"
    diff = generate_paragraph_diff(old, new)
    assert diff['action'] == 'insert'
    assert diff['content'] == 'Para 1.5'

def test_generate_paragraph_diff_replace():
    old = "Para 1\n\nPara 2"
    new = "Para 1\n\nPara 2 Modified"
    diff = generate_paragraph_diff(old, new)
    assert diff['action'] == 'replace'

def test_conflict_detection():
    # Simulate concurrent edit
    base = "Original"
    user = "User edit"
    ai = "AI edit"
    conflict = detect_conflict(base, user, ai)
    assert conflict['is_conflict'] == True
```

### Integration Tests (`test_document_streaming.py`)

```python
async def test_websocket_document_update():
    # Connect to WebSocket
    # Start research session
    # Listen for document_update messages
    # Verify incremental updates received
    pass

async def test_conflict_notification():
    # Start research session
    # Simulate user edit via API
    # AI attempts to edit same section
    # Verify conflict message received
    pass
```

### E2E Tests (`test-document-collaboration.sh`)

```bash
#!/bin/bash
# 1. Start research session
# 2. Monitor WebSocket for document_update messages
# 3. Simulate user editing report file
# 4. Verify conflict detection
# 5. Verify final report correctness
```

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Diff algorithm too slow | Low | Medium | Benchmark with large docs, add timeout |
| WebSocket message loss | Medium | High | Add sequence numbers, client-side buffering |
| Concurrent edit race condition | Medium | High | Use document version hashing, conflict detection |
| VS Code API limitations | Low | Medium | Fallback to readonly display + manual merge |

### Timeline Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Conflict resolution takes >2 days | Medium | Medium | Simplify to basic strategy first, iterate |
| Testing discovers major bugs | Low | High | Comprehensive unit tests before integration |
| Frontend integration complex | Medium | Medium | Start simple (read-only display), add interactivity |

---

## Dependencies

### Python Libraries
- `diff-match-patch` - Text diff algorithm
- `asyncio` - Async WebSocket handling
- `pytest` - Testing framework

### VS Code APIs
- `vscode.workspace.applyEdit()` - Programmatic editing
- `vscode.CodeLens` - Accept/Reject buttons
- `vscode.TextEditorDecorationType` - Visual highlights
- `vscode.commands.executeCommand('vscode.diff')` - Diff viewer

### Existing Infrastructure
- WebSocket endpoint `/agent/stream` (already implemented)
- LangGraph synthesis_node (report generation)
- Frontend WebSocket client (already working)

---

## Deliverables Checklist

### Code
- [ ] `backend/src/agent/document_utils.py` (~200 lines)
- [ ] `backend/tests/test_document_utils.py` (~150 lines)
- [ ] `backend/tests/test_document_streaming.py` (~100 lines)
- [ ] `backend/src/agent/app.py` (WebSocket handler updates)
- [ ] `backend/src/agent/graph.py` (synthesis_node updates)
- [ ] `vscode-extension/src/documentCollaboration.ts` (~300 lines)
- [ ] `vscode-extension/src/codeLensProvider.ts` (~100 lines)

### Tests
- [ ] Unit tests: >90% coverage
- [ ] Integration tests: 5 scenarios
- [ ] E2E test: Full collaboration workflow

### Documentation
- [ ] `PHASE_3.6_WEEK3_IMPLEMENTATION.md` - Technical details
- [ ] `PHASE_3.6_WEEK3_TESTING_REPORT.md` - Test results
- [ ] `PHASE_3.6_COMPLETE.md` - Final completion report
- [ ] API documentation updates
- [ ] User guide with GIF demos

---

## Next Steps (After Day 1)

**Day 2**:
- Complete WebSocket integration
- Test incremental report generation
- Document conflict detection logic

**Day 3-4**:
- Frontend Workspace API integration
- Visual decorations implementation
- Accept/Reject CodeLens

**Day 5**:
- Conflict resolution UI
- Three-way merge
- Retry mechanism

**Day 6**:
- Polish and optimization
- Error handling
- Documentation

**Day 7**:
- Final testing
- Documentation completion
- Git commit and tag

---

**Status**: Ready to start implementation  
**First Task**: Install diff-match-patch and create document_utils.py  
**Expected Completion**: Day 1 EOD - Basic document streaming infrastructure ready

