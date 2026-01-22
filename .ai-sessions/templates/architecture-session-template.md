# Session: [Architecture Design Title]

**Date:** YYYY-MM-DD
**Architect:** [GitHub Copilot / Developer Name]
**Phase:** [Phase Number]
**Status:** [In Progress / Completed / Blocked]
**Goal:** [Clear, specific goal statement]

## Context
- **Blueprint:** [Related architecture documents, e.g., doc/AI-Native 自主开发系统架构蓝皮书v1.1.md]
- **Standard:** [Development standards referenced, e.g., GEMINI.md, .clinerules]
- **Tools:** [Tools and technologies used, e.g., GitHub Copilot, Aider + Qwen Max]

## Design Decisions

### 1. [Design Decision 1]
**Problem:** [What problem are we solving?]
**Options Considered:**
- Option A: [Description]
- Option B: [Description]
**Decision:** [Chosen option]
**Rationale:** [Why this option was chosen]
**Trade-offs:** [What we're giving up]

### 2. [Design Decision 2]
**Problem:** [What problem are we solving?]
**Options Considered:**
- Option A: [Description]
- Option B: [Description]
**Decision:** [Chosen option]
**Rationale:** [Why this option was chosen]
**Trade-offs:** [What we're giving up]

## Architecture Components

### Domain Layer
```python
# agent/domain/schemas/[schema_name].py
# Pydantic models and data structures
```

### Protocols/Ports
```python
# agent/domain/ports/[protocol_name].py
# Interface definitions with @TestScenarios
```

### Infrastructure Layer
```python
# agent/infrastructure/[adapter_name].py
# Adapter implementations
```

## Integration Points

### Dependencies
- [Dependency 1]: [Purpose]
- [Dependency 2]: [Purpose]

### Data Flow
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Error Handling
- [Error scenario 1]: [Handling strategy]
- [Error scenario 2]: [Handling strategy]

## Artifacts

### Files Created
- `[file_path_1]`: [Purpose]
- `[file_path_2]`: [Purpose]

### Files Modified
- `[file_path_1]`: [Changes made]
- `[file_path_2]`: [Changes made]

### Code Snippets
```python
# Key implementation code
```

## Test Scenarios

### Unit Tests
```python
# Test cases for domain logic
```

### Integration Tests
```python
# Test cases for adapter integration
```

### Performance Tests
- [Performance metric 1]: [Target value]
- [Performance metric 2]: [Target value]

## Results

### Success Criteria Met
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Issues Encountered
1. [Issue 1]: [Solution]
2. [Issue 2]: [Solution]

### Learnings
- [Learning 1]
- [Learning 2]
- [Learning 3]

## Next Steps

### Immediate Actions (Next 24 hours)
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Short-term (Next week)
- [Task 1]
- [Task 2]
- [Task 3]

### Long-term (Future phases)
- [Future consideration 1]
- [Future consideration 2]

## References
- [Reference 1]: [Link or description]
- [Reference 2]: [Link or description]
- [Reference 3]: [Link or description]

---

**Session Completed:** YYYY-MM-DD HH:MM  
**Architect Signature:** [Name/Initials]  
**Review Status:** [Pending / Reviewed / Approved]
