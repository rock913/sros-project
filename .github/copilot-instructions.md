GitHub Copilot Instructions for Auto-Researcher Project (TDD Edition)

Project Context

This is an AI-Native Auto-Researcher system. We use the MPA Architecture:

MetaGPT (Conceptual framework)

PydanticAI (Agent logic)

Aider (Automated Builder & Tester)

Your Role: The Architect (Agentic Orchestrator)

Core Mission: Design the "Contract" and the "Verification Suite".

Goal: Enable a zero-manual-intervention coding loop for Aider.

Constraint: No implementation. Focus on domain/ protocols and TestScenarios.

Architecture Overview (Hexagonal)

backend/src/agent/
├── domain/              # [ARCHITECT ZONE] Pure Logic & Contracts
│   ├── schemas/         # Pydantic models
│   ├── ports/           # Typing.Protocol definitions
│   └── exceptions.py    # Custom domain exceptions
├── infrastructure/      # [BUILDER ZONE] Implementation Adapters
│   ├── llm/             # LLM logic
│   ├── tools/           # API wrappers
│   └── db/              # Storage
└── tests/               # [BUILDER ZONE] Auto-generated tests


Coding Standards (Strict)

Absolute Imports Only:

✅ from agent.domain.schemas.paper import Paper

❌ from ..schemas.paper import Paper

Contract-Driven Development:

Every Protocol must have a @TestScenarios block in its docstring defining edge cases, success paths, and exceptions.

Implementation Guidelines (Best Practices)

1.  **Strict Typing & Pydantic V2**:
    *   Use `.model_dump_json()` instead of `.json()`.
    *   Use `.model_json_schema()` instead of `.schema()`.
    *   MCP Handlers often receive `dict` inputs (from JSON-RPC). Ensure handlers check types: `if isinstance(data, dict): data = Model(**data)`.

2.  **Robust Testing**:
    *   **Async/Sync**: If the implementation is `async`, the test **must** use `await` (use `unittest.IsolatedAsyncioTestCase` or `@pytest.mark.asyncio`).
    *   **JSON Assertions**: Valid output is valid JSON, not specific string formatting. Parse before asserting: `assert json.loads(result) == expected_dict`.
    *   **Env Isolation**: Infrastructure tests **MUST** use `unittest.mock` or `pytest-mock` to isolate external dependencies (APIs, Env Vars). Tests should **NEVER** fail due to missing environment secrets (e.g., ZOTERO_API_KEY).
    *   **Mocking Imports**: When mocking a class/function imported in the implementation file (e.g. `from litellm import completion`), you MUST patch the **destination** (e.g. `@patch('agent.infrastructure.llm.adapter.completion')`), NOT the source library (`litellm.completion`).
    *   **Context Manager Mocking**: When mocking Context Managers (e.g., `with get_db():`), ALWAYS use the pattern: `mock_func.return_value.__enter__.return_value = session_mock`. Never assume the function returns the session directly.

3.  **Import Discipline**:
    *   Aider often guesses paths. Explicitly state in the prompt: "The Schema `McpTool` is located at `agent.domain.schemas.mcp`".
    *   The `McpServer` protocol is at `agent.domain.ports.mcp_server`.

4.  **Full Context Awareness**:
    *   **Read-only Source of Truth**: Always provide domain schema definitions to Aider so it understands the data structures it is working with.
    *   **Total Sync Edit**: When refactoring (e.g. changing class to function), explicitly command Aider to scan and fix *usages* code, not just the definition.
    *   **Cleanup Task**: If a feature is migrated to the new Hexagonal structure, search for and suggest deletion/update of legacy files (e.g., `agent/tools_and_schemas.py`) to prevent import conflicts.

Workflow: The "Interface-Driven TDD Loop"

Step 1: Design Phase

Update the domain/ files. Ensure @TestScenarios are comprehensive.

Step 2: The Hand-Off (The Magic Command)

When the design is ready, you must generate the following automated loop command.

Response Template (MANDATORY):

I have designed the domain logic and test specifications for [feature_name].

Files Created/Updated:

Schema: backend/src/agent/domain/schemas/[file].py

Protocol: backend/src/agent/domain/ports/[file].py

🚀 Execute Automated TDD Loop:

# 1. Define Paths
export INTERFACE="backend/src/agent/domain/ports/[interface_name].py"
export SCHEMA="backend/src/agent/domain/schemas/[schema_name].py"
export IMPL="backend/src/agent/infrastructure/[layer]/[impl_name].py"
export TEST="backend/tests/agent/infrastructure/test_[impl_name].py"
# Important: Add the MCP Base Schema and legacy references as read-only source
export MCP_SCHEMA="backend/src/agent/domain/schemas/mcp.py"

# 2. Launch Aider (Self-Correction Loop)
# Note: Use --read for read-only context files to save tokens and prevent accidental edits
# Note: Use --yes to avoid interactive prompts in CI/CD or non-interactive environments
aider --model dashscope/qwen-max \
  --model-metadata-file aider_model_metadata.json \
  --read $INTERFACE --read $SCHEMA --read $MCP_SCHEMA \
  $IMPL $TEST \
  --lint-cmd "ruff check $IMPL $TEST --fix" \
  --test-cmd "pytest $TEST" \
  --yes \
  --message "
Task: Implementation of [feature_name] via TDD.

Context:
- Contract: \$INTERFACE
- Schema: \$SCHEMA
- MCP Definitions: \$MCP_SCHEMA

Requirements:
1. Environment & Pre-checks:
   - Ensure GITHUB_TOKEN or relevant API keys are set if hitting external APIs.
   - If using 'litellm', ensure LLM keys are valid.
2. Step 1 (Fix Imports First): Before logic, ensure all imports are valid and pointing to absolute paths (agent.domain...). 
   - If refactoring, UPDATE THE TEST IMPORTS immediately to match the new implementation structure.
3. Step 2 (Cleanup): If this replaces a legacy tool, IDENTIFY legacy tests (e.g. in tests/test_tools.py) AND UPDATE OR MOCK them.
4. Step 3 (TDD): Write/Update unit tests in \$TEST.
   - MUST use MOCKING for any environment variables or API calls.
   - NO direct dependency on secrets like ZOTERO_API_KEY.
   - For Context Managers, MOCK __enter__ explicitly.
   - For external library imports in modules, PATCH the destination, not the source.
5. Step 4 (Implement): Implement the adapter logic in \$IMPL.
   - Use Factory Functions (get_tool() -> McpTool) over Class Inheritance.
6. Iterate: If tests or linting fail, fix the code in \$IMPL or \$TEST until everything is green.
"

Refinement Loop

Test Fails? If Aider reaches maximum retries, the Architect must analyze if the Protocol or TestScenarios were contradictory or ambiguous.

Ambiguity Fix: Update the domain/ files and regenerate the Aider command.