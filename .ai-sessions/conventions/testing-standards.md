# Testing Standards for AI-Native Development

## Overview
Comprehensive testing standards for the MPA workflow, ensuring quality, reliability, and maintainability of AI-assisted development.

## Testing Philosophy

### 1. Test-Driven Development (TDD)
- Write tests before implementation
- Tests define the contract/interface
- Implementation satisfies test requirements
- Refactor with confidence using test suite

### 2. Hexagonal Architecture Testing
- **Domain Layer**: Pure logic, no I/O
- **Infrastructure Layer**: Adapters with external dependencies
- **Protocols**: Define test scenarios in docstrings
- **MCP Tools**: Integration testing with mock servers

### 3. AI-Native Testing Principles
- Tests must be deterministic (no AI randomness)
- Mock all external AI/LLM calls
- Isolate environment variables
- Tests should run without internet connection

## Test Categories

### 1. Unit Tests
**Scope:** Single function or class
**Location:** `tests/unit/` or `tests/[module]/`
**Coverage:** 100% for new code

```python
# Example unit test
def test_paper_validation():
    paper = Paper(title="Test", authors=["Author"])
    assert validate_paper(paper) == True
```

### 2. Integration Tests
**Scope:** Multiple components working together
**Location:** `tests/integration/`
**Coverage:** Critical paths only

```python
# Example integration test
def test_zotero_adapter_integration():
    adapter = ZoteroAdapter()
    paper = Paper(title="Test", authors=["Author"])
    result = adapter.save_paper(paper)
    assert result.startswith("ZOTERO_")
```

### 3. Protocol Tests
**Scope:** Protocol/interface compliance
**Location:** `tests/protocols/`
**Coverage:** All protocol methods

```python
# Example protocol test
def test_reference_manager_protocol():
    adapter = ZoteroAdapter()
    assert isinstance(adapter, ReferenceManager)
    # Test all protocol methods
```

### 4. MCP Tool Tests
**Scope:** MCP tool functionality
**Location:** `tests/mcp/`
**Coverage:** Tool input/output validation

```python
# Example MCP tool test
def test_arxiv_search_tool():
    tool = ArxivSearchTool()
    result = tool.execute({"query": "machine learning"})
    assert "papers" in result
```

### 5. End-to-End Tests
**Scope:** Complete workflow
**Location:** `tests/e2e/`
**Coverage:** Critical user journeys

```python
# Example E2E test
def test_complete_research_workflow():
    # Start research session
    # Execute searches
    # Process papers
    # Generate report
    # Verify results
```

## Mocking Standards

### 1. External API Mocking
```python
@patch('agent.infrastructure.llm_adapter.completion')
def test_llm_adapter(self, mock_completion):
    mock_completion.return_value = "Mocked response"
    # Test with mocked LLM
```

### 2. Environment Variable Mocking
```python
@patch.dict(os.environ, {"API_KEY": "test-key"})
def test_with_mocked_env(self):
    # Test with mocked environment
```

### 3. Database Mocking
```python
@patch('agent.infrastructure.database_adapter.Session')
def test_database_operations(self, mock_session):
    mock_session.return_value.query.return_value.all.return_value = []
    # Test with mocked database
```

### 4. File System Mocking
```python
@patch('builtins.open', mock_open(read_data='{"test": "data"}'))
def test_file_operations(self):
    # Test with mocked file system
```

### 5. Context Manager Mocking
```python
# For 'with get_db():' patterns
mock_func.return_value.__enter__.return_value = session_mock
```

## Test Structure

### 1. Test Class Organization
```python
class TestZoteroAdapter:
    """Tests for ZoteroAdapter implementing ReferenceManager protocol."""
    
    def setup_method(self):
        """Setup before each test."""
        self.adapter = ZoteroAdapter()
    
    def teardown_method(self):
        """Cleanup after each test."""
        self.adapter.cleanup()
    
    def test_save_paper_valid(self):
        """Test saving a valid paper."""
        # Arrange
        paper = Paper(title="Test", authors=["Author"])
        
        # Act
        result = self.adapter.save_paper(paper)
        
        # Assert
        assert result is not None
        assert isinstance(result, str)
    
    def test_save_paper_invalid(self):
        """Test saving an invalid paper."""
        # Arrange
        paper = Paper(title="", authors=[])  # Invalid
        
        # Act & Assert
        with pytest.raises(ValidationError):
            self.adapter.save_paper(paper)
```

### 2. Test Data Management
```python
# test_data.py
@pytest.fixture
def sample_paper():
    return Paper(
        title="Test Paper",
        authors=["Author 1", "Author 2"],
        abstract="Test abstract",
        year=2024
    )

@pytest.fixture
def sample_papers():
    return [
        Paper(title=f"Paper {i}", authors=[f"Author {i}"])
        for i in range(5)
    ]
```

### 3. Parameterized Tests
```python
@pytest.mark.parametrize("title,expected", [
    ("Valid Title", True),
    ("", False),
    ("A" * 1000, True),
    ("A" * 1001, False),
])
def test_paper_title_validation(title, expected):
    paper = Paper(title=title, authors=["Author"])
    assert (len(paper.title) > 0) == expected
```

## Test Execution

### 1. Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/mcp/

# Run with coverage
pytest --cov=agent --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_zotero_adapter.py

# Run specific test function
pytest tests/unit/test_zotero_adapter.py::TestZoteroAdapter::test_save_paper_valid
```

### 2. Test Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=agent",
    "--cov-report=html",
    "--cov-report=term-missing",
    "-v"
]

[tool.coverage.run]
source = ["agent"]
omit = [
    "agent/__init__.py",
    "agent/tests/*",
    "agent/*/tests/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\b"
]
```

## Quality Metrics

### 1. Coverage Requirements
- **New Code:** 100% coverage
- **Modified Code:** >90% coverage
- **Legacy Code:** >80% coverage
- **Critical Paths:** 100% coverage

### 2. Performance Requirements
- **Test Execution:** <2 minutes for full suite
- **Individual Test:** <100ms
- **Memory Usage:** <100MB per test
- **Setup/Teardown:** <1 second

### 3. Reliability Requirements
- **Flaky Tests:** 0 tolerance
- **Intermittent Failures:** Must be fixed immediately
- **Test Dependencies:** Must be mocked
- **Environment Dependencies:** Must be isolated

## Common Test Patterns

### 1. Protocol Compliance Testing
```python
def test_protocol_compliance():
    """Test that adapter implements all protocol methods."""
    adapter = ZoteroAdapter()
    protocol = ReferenceManager
    
    # Check all protocol methods exist
    for method_name in protocol.__abstractmethods__:
        assert hasattr(adapter, method_name)
        assert callable(getattr(adapter, method_name))
```

### 2. Error Handling Testing
```python
def test_error_handling():
    """Test error conditions are properly handled."""
    adapter = ZoteroAdapter()
    
    # Test network error
    with patch('requests.post', side_effect=ConnectionError):
        with pytest.raises(AdapterError):
            adapter.save_paper(paper)
    
    # Test API error
    with patch('requests.post', return_value=Mock(status_code=500)):
        with pytest.raises(APIError):
            adapter.save_paper(paper)
```

### 3. Async Testing
```python
@pytest.mark.asyncio
async def test_async_adapter():
    """Test async adapter methods."""
    adapter = AsyncZoteroAdapter()
    result = await adapter.async_save_paper(paper)
    assert result is not None
```

## Test Maintenance

### 1. Test Review Checklist
- [ ] Tests follow naming conventions
- [ ] Tests are independent (no shared state)
- [ ] All external dependencies are mocked
- [ ] Environment variables are isolated
- [ ] Tests clean up after themselves
- [ ] Tests have clear assertions
- [ ] Tests document what they're testing

### 2. Test Refactoring
- Extract common test code into fixtures
- Use parameterized tests for similar scenarios
- Create test data factories
- Move complex setup to helper functions

### 3. Test Documentation
- Each test should have a docstring
- Document test scenarios and edge cases
- Include references to protocol/test scenarios
- Document mocking strategy

## References
- [MPA Workflow](mpa-workflow.md) - Development workflow
- [.clinerules](../../.clinerules) - AI-Native development rules
- [TESTING.md](../../TESTING.md) - Project testing methodology
- [Python Testing with pytest](https://docs.pytest.org/) - pytest documentation

---

**Version:** 1.0  
**Last Updated:** 2026-01-22  
**Maintainer:** Project Architect  
**Status:** Active
