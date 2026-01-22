# Session: [Development Implementation Title]

**Date:** YYYY-MM-DD
**Developer:** [GitHub Copilot / Aider + Qwen Max]
**Phase:** [Phase Number]
**Status:** [In Progress / Completed / Blocked]
**Goal:** [Clear, specific implementation goal]

## Context
- **Architecture:** [Related architecture documents or sessions]
- **Standard:** [Development standards, e.g., .clinerules, TESTING.md]
- **Tools:** [Tools used, e.g., Aider, pytest, ruff]
- **MPA Role:** [Architect/Builder/Inspector]

## Implementation Plan

### 1. [Task 1]
**Objective:** [What needs to be implemented]
**Approach:** [How it will be implemented]
**Files:** [Files to create/modify]
**Tests:** [Test strategy]

### 2. [Task 2]
**Objective:** [What needs to be implemented]
**Approach:** [How it will be implemented]
**Files:** [Files to create/modify]
**Tests:** [Test strategy]

## Code Changes

### Domain Layer Implementation

```python
# agent/domain/schemas/[schema_name].py
# Pydantic model implementation
```

### Protocol Implementation

```python
# agent/domain/ports/[protocol_name].py
# Protocol with @TestScenarios decorator
```

### Adapter Implementation

```python
# agent/infrastructure/[adapter_name].py
# Adapter implementing protocol
```

### MCP Tool Wrapper

```python
# agent/infrastructure/mcp/tools/[tool_name].py
# MCP tool wrapper
```

## Testing Strategy

### Unit Tests
```python
# Test file: tests/[test_file].py
# Mocking strategy and test cases
```

### Integration Tests
```python
# Integration test scenarios
```

### MCP Tool Tests
```python
# MCP tool validation tests
```

## Aider TDD Command

```bash
aider --model openai/deepseek-chat --yes --no-suggest-shell-commands \
  --file $INTERFACE $SCHEMA $MCP_SCHEMA \
  --read $APP_CONTEXT \
  --add $IMPL $TEST \
  --lint-cmd "ruff check $IMPL $TEST --fix" \
  --test-cmd "pytest $TEST" \
  --message "
Task: Implementation of [feature_name] via TDD.
Rules:
1. Fix Imports First: Ensure all point to agent.domain.
2. TDD: Write tests in \$TEST first. Mock all env vars and API calls.
3. Context: Refer to provided read-only schemas.
"
```

## Execution Log

### Step 1: [Step description]
**Command:** [Command executed]
**Output:** [Command output]
**Result:** [Success/Failure]

### Step 2: [Step description]
**Command:** [Command executed]
**Output:** [Command output]
**Result:** [Success/Failure]

### Step 3: [Step description]
**Command:** [Command executed]
**Output:** [Command output]
**Result:** [Success/Failure]

## Artifacts

### Files Created
- `[file_path_1]`: [Lines added, purpose]
- `[file_path_2]`: [Lines added, purpose]

### Files Modified
- `[file_path_1]`: [Changes: +X -Y lines]
- `[file_path_2]`: [Changes: +X -Y lines]

### Test Results
```
# pytest output
```

### Linter Results
```
# ruff check output
```

## Issues and Solutions

### Issue 1: [Problem description]
**Root Cause:** [What caused the issue]
**Solution:** [How it was fixed]
**Prevention:** [How to prevent in future]

### Issue 2: [Problem description]
**Root Cause:** [What caused the issue]
**Solution:** [How it was fixed]
**Prevention:** [How to prevent in future]

## Verification

### Code Quality
- [ ] All imports use absolute paths (`from agent.domain...`)
- [ ] No I/O in domain layer
- [ ] All protocols have `@TestScenarios`
- [ ] Pydantic V2 methods used (`.model_dump_json()`, `.model_json_schema()`)

### Testing
- [ ] Unit tests pass (100% coverage for new code)
- [ ] Integration tests pass
- [ ] All external dependencies mocked
- [ ] Environment variables isolated in tests

### Documentation
- [ ] Protocol docstrings updated with test scenarios
- [ ] README files updated if needed
- [ ] API documentation updated

## Results

### Success Metrics
- **Code Coverage:** [X]%
- **Lint Score:** [X]/10
- **Performance:** [X]ms average response time
- **Reliability:** [X]% test pass rate

### Deliverables Completed
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### Technical Debt Created
- [ ] [Debt item 1]
- [ ] [Debt item 2]
- [ ] [Debt item 3]

## Next Steps

### Immediate Follow-up
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Code Review Items
- [Review item 1]
- [Review item 2]
- [Review item 3]

### Future Improvements
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

## References
- [Architecture Session]: [Link to architecture session]
- [Protocol Definition]: [Link to protocol file]
- [Test Standards]: [Link to TESTING.md]
- [MPA Workflow]: [Link to conventions/mpa-workflow.md]

---

**Session Completed:** YYYY-MM-DD HH:MM  
**Developer Signature:** [Name/Initials]  
**Architect Review:** [Pending / Reviewed / Approved]  
**Test Status:** [All Passed / Issues Found]
