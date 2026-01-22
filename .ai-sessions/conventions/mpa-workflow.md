# MPA (MetaGPT+PydanticAI+Aider) Workflow Standards

## Overview
The MPA workflow is an AI-Native development methodology that divides responsibilities between different AI agents following hexagonal architecture principles.

## Role Definitions

### 1. Architect (GitHub Copilot)
**Responsibilities:**
- Design domain schemas (Pydantic models)
- Define protocols/ports with `@TestScenarios`
- Create architecture blueprints
- Review implementation for architectural compliance
- Document design decisions

**Outputs:**
- `agent/domain/schemas/*.py`
- `agent/domain/ports/*.py`
- Architecture session documents
- Design decision records

### 2. Builder (Aider + Qwen Max)
**Responsibilities:**
- Implement infrastructure adapters
- Write comprehensive tests
- Follow TDD methodology
- Ensure code quality standards
- Integrate with external services

**Outputs:**
- `agent/infrastructure/*.py`
- `tests/*.py`
- Implementation session documents
- Test results and coverage reports

### 3. Inspector (Aider)
**Responsibilities:**
- Run tests and validate implementation
- Check code quality (linting, formatting)
- Verify architectural compliance
- Identify technical debt
- Ensure backward compatibility

**Outputs:**
- Test execution reports
- Code quality reports
- Technical debt assessments
- Verification checklists

## Workflow Process

### Phase 1: Architecture Design (Architect)
1. **Analyze Requirements**
   - Understand feature requirements
   - Identify domain entities
   - Define data flows

2. **Design Domain Layer**
   - Create Pydantic schemas
   - Define protocols with `@TestScenarios`
   - Document design decisions

3. **Create Architecture Blueprint**
   - Session document in `.ai-sessions/architecture/`
   - Include all design decisions and rationale
   - Define success criteria

### Phase 2: Implementation (Builder)
1. **Setup TDD Environment**
   ```bash
   aider --model openai/deepseek-chat --yes --no-suggest-shell-commands \
     --file $INTERFACE $SCHEMA $MCP_SCHEMA \
     --read $APP_CONTEXT \
     --add $IMPL $TEST \
     --lint-cmd "ruff check $IMPL $TEST --fix" \
     --test-cmd "pytest $TEST" \
     --message "Task: Implementation of [feature_name] via TDD..."
   ```

2. **Write Tests First**
   - Mock all external dependencies
   - Isolate environment variables
   - Define test scenarios from protocol docstrings

3. **Implement Adapters**
   - Follow hexagonal architecture
   - Use absolute imports (`from agent.domain...`)
   - No I/O in domain layer

4. **Create MCP Tool Wrappers**
   - Wrap adapters in MCP tools
   - Define proper input/output schemas
   - Add error handling

### Phase 3: Inspection (Inspector)
1. **Run Test Suite**
   ```bash
   pytest tests/ --cov=agent --cov-report=html
   ```

2. **Check Code Quality**
   ```bash
   ruff check agent/ tests/ --fix
   ```

3. **Verify Architecture Compliance**
   - No I/O in domain layer
   - All imports use absolute paths
   - Protocols have `@TestScenarios`
   - Pydantic V2 methods used

4. **Document Results**
   - Update session document
   - Record test coverage
   - Identify technical debt

### Phase 4: Documentation
1. **Update Protocol Docstrings**
   - Include `@TestScenarios`
   - Document usage examples
   - Add error conditions

2. **Update README Files**
   - Feature documentation
   - Usage instructions
   - Configuration guides

3. **Update API Documentation**
   - OpenAPI specifications
   - TypeScript definitions
   - Example requests/responses

## Quality Standards

### Code Standards
1. **Absolute Imports Only**
   ```python
   # ✅ Correct
   from agent.domain.schemas.paper import Paper
   
   # ❌ Incorrect
   from ..schemas.paper import Paper
   ```

2. **No I/O in Domain Layer**
   ```python
   # ✅ Domain layer (pure logic)
   def validate_paper(paper: Paper) -> bool:
       return len(paper.title) > 0
   
   # ❌ Domain layer (I/O)
   def save_paper(paper: Paper) -> None:
       with open("paper.json", "w") as f:
           f.write(paper.model_dump_json())
   ```

3. **Protocols with Test Scenarios**
   ```python
   @TestScenarios([
       TestScenario(
           description="Save paper with valid data",
           given={"paper": Paper(title="Test", authors=["Author"])},
           when="save_paper is called",
           then="returns item key"
       )
   ])
   class ReferenceManager(Protocol):
       def save_paper(self, paper: Paper) -> str: ...
   ```

4. **Pydantic V2 Methods**
   ```python
   # ✅ Correct
   paper.model_dump_json()
   paper.model_json_schema()
   
   # ❌ Incorrect (Pydantic V1)
   paper.json()
   paper.schema()
   ```

### Testing Standards
1. **Mock External Dependencies**
   ```python
   @patch('agent.infrastructure.zotero_adapter.Zotero')
   def test_save_paper(self, mock_zotero):
       # Mock setup
       mock_zotero.return_value.create_item.return_value = {"key": "test123"}
       
       # Test execution
       result = adapter.save_paper(paper)
       
       # Assertions
       self.assertEqual(result, "test123")
   ```

2. **Isolate Environment Variables**
   ```python
   @patch.dict(os.environ, {"ZOTERO_API_KEY": "test-key"})
   def test_adapter_initialization(self):
       # Test with mocked environment
       adapter = ZoteroAdapter()
       self.assertIsNotNone(adapter)
   ```

3. **100% Coverage for New Code**
   ```bash
   # Coverage report
   pytest --cov=agent.infrastructure.zotero_adapter --cov-report=term-missing
   ```

### Documentation Standards
1. **Session Documentation**
   - Follow template structure
   - Include all required sections
   - Record decisions and rationale

2. **Protocol Documentation**
   - Include `@TestScenarios`
   - Document all methods
   - Provide usage examples

3. **API Documentation**
   - OpenAPI spec updated
   - TypeScript definitions generated
   - Example code provided

## Tool Configuration

### Aider Configuration
```yaml
# .aider.conf.yml
model: openai/deepseek-chat
openai-api-base: https://dashscope.aliyuncs.com/compatible-mode/v1
map-tokens: 1024
cache-prompts: true
```

### Testing Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=agent --cov-report=html --cov-report=term-missing"

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "B", "C4", "W", "UP"]
ignore = ["E501", "C901"]
```

### VS Code Configuration
```json
{
  "python.testing.pytestArgs": ["tests"],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true,
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true
}
```

## Success Metrics

### Quality Metrics
- **Test Coverage:** >85% for new code
- **Lint Score:** 0 errors, <5 warnings
- **Architecture Compliance:** 100% (no I/O in domain)
- **Documentation Coverage:** 100% of protocols documented

### Performance Metrics
- **Build Time:** <5 minutes
- **Test Execution:** <2 minutes
- **Code Review:** <1 day turnaround

### Process Metrics
- **Cycle Time:** <3 days per feature
- **Defect Rate:** <1 defect per feature
- **Technical Debt:** <5% of codebase

## Common Pitfalls and Solutions

### Pitfall 1: I/O in Domain Layer
**Solution:** Move I/O to infrastructure adapters

### Pitfall 2: Relative Imports
**Solution:** Always use absolute imports from `agent`

### Pitfall 3: Missing Test Scenarios
**Solution:** Add `@TestScenarios` to all protocols

### Pitfall 4: Pydantic V1 Methods
**Solution:** Use `.model_dump_json()` and `.model_json_schema()`

## References
- [.clinerules](../../.clinerules) - AI-Native development rules
- [TESTING.md](../../TESTING.md) - Testing methodology
- [ROADMAP.md](../../ROADMAP.md) - Project roadmap
- [Architecture Blueprint](../../doc/AI-Native%20自主开发系统架构蓝皮书v1.1.md) - Architecture design

---

**Version:** 1.0  
**Last Updated:** 2026-01-22  
**Maintainer:** Project Architect  
**Status:** Active
