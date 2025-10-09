# GEMINI: AI-Assisted Development Framework for Auto-Researcher

This document is the authoritative guide for the AI assistant, providing a comprehensive framework for developing the **Auto-Researcher** project. It ensures the assistant can operate efficiently, autonomously, and in alignment with project standards.

## 1. Project Overview

- **Project Name**: Auto-Researcher
- **Description**: An autonomous AI platform to automate the research lifecycle, from topic discovery to final report generation.
- **Architecture**: Full-stack application with a Python/LangGraph backend and a React/TypeScript frontend.
- **Key Directories**:
    - `backend/`: FastAPI application containing the core agent logic.
    - `frontend/`: React (Vite) application for the user interface.
    - `docker-compose.yml`: Container orchestration for reproducible environments.

## 2. Core Philosophy: Session-Driven Workflow

All development and debugging tasks **must** follow a unified **Session-Driven Workflow**. This methodology treats every task as a "session," creating a real-time, traceable log from start to finish. It ensures that the entire lifecycle of a feature or bug fix—including all attempts, errors, and corrections—is captured in a single, coherent narrative.

The authoritative guide for this process is:
- **Unified Workflow**: `doc/WORKFLOW_STRATEGY.md`

### Session-Driven Workflow at a Glance

The core idea is to unify development and debugging under a single process, managed within the `/.ai-sessions/` directory.

1.  **Initiate a Session**:
    - For **new features**, a session log is created in `/.ai-sessions/development/`. The goal is typically to make a `.feature` file pass.
    - For **standalone bugs** (e.g., a failing E2E test), a session log is created in `/.ai-sessions/debugging/`. The goal is to make a specific test, like `e2e_test.sh`, pass.

2.  **Execute and Record**: The AI follows a plan, recording each step, tool call, and verification result in the session file.

3.  **Enter Debug State (If Needed)**: If any step fails, the AI enters a "debug state" *within the same session file*. It creates a "Debugging Snapshot" to diagnose, attempt a fix, and re-verify. This loop continues until the step succeeds.

4.  **Complete the Session**: The session is complete when the overarching goal (e.g., the acceptance test) is met.

This unified approach eliminates the disconnect between development and debugging, providing a clear, end-to-end history for every task.

## 3. Key Commands & Configuration

All testing and verification **must** be performed using the project's `Makefile`.

### a. Makefile Commands

-   **Run All Backend Tests**:
    ```bash
    make -C backend/ test
    ```
-   **Run a Specific Test File**:
    ```bash
    make -C backend/ test TEST_FILE=tests/path/to/your_test_file.py
    ```
-   **Run End-to-End (E2E) Tests**:
    ```bash
    make test-e2e-docker TOPIC="A relevant research topic"
    ```
-   **Start Development Environment**:
    ```bash
    make dev-docker
    ```

### b. Environment Configuration

The backend agent uses `litellm` and requires environment variables to be set for the desired Large Language Model (LLM) provider.

1.  **Create `.env` file**: Copy `.env.example` to `.env` in the project root.
2.  **Set API Keys**: Add the API key for your chosen provider. For example:
    -   **Google Gemini**:
        ```env
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    -   **OpenAI**:
        ```env
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
        ```
3.  **Specify Models (Optional)**: You can override the default models:
    ```env
    GENERATION_MODEL="gemini-1.5-pro"
    EMBEDDING_MODEL="text-embedding-004"
    ```

## 4. Operational Principles

### a. Tool Parameter Precision

The assistant must ensure all tool calls use the correct parameter names as defined in the tool's schema. Repeated, efficiency-impacting errors due to incorrect parameter names (e.g., using `newContent` instead of `new_string`) are to be strictly avoided. Before executing a tool call, parameter names must be double-checked against the provided documentation to ensure correctness.

By adhering to this framework, the AI assistant can effectively contribute to the project, maintaining high standards of code quality, documentation, and process transparency.

## 5. End-to-End (E2E) Testing Framework

This section standardizes how the assistant (and humans) execute, observe, and debug full research flows from a raw topic to a final report. It complements unit/integration tests by validating the multi-stage LangGraph pipeline, external tool orchestration, streaming interface, and persistence layer.

### 5.1 Scope & Goals
E2E tests must verify that for a given research topic:
1. Streaming API (`/agent/stream`) emits structured incremental state chunks.
2. Core state transitions occur in correct order: `generate_initial_queries` → (`execute_searches` fan-out cycles + `reflection_and_refinement` loop) → `automated_resource_management` → `ingest_and_embed_documents` → `retrieve_and_synthesize_report` → final `report`.
3. At least one set of `literature_abstracts` is produced; loop count ≤ configured max (default 3).
4. A final `report` (non-empty) is generated.
5. (Optional) DB receives newly embedded chunks when full-text ingestion occurs.

### 5.2 Interfaces Under Test
- Health: `GET /ok` (readiness check)
- Invoke (non-stream): `POST /agent/invoke` (fast schema / 4xx / 5xx detection)
- Stream (SSE): `POST /agent/stream` with body:
```json
{
    "input": {"messages": [{"role": "user", "content": "<topic>"}]}
}
```

### 5.3 Provided Scripts
| Script | Purpose | When to Use |
|--------|---------|-------------|
| `backend/examples/e2e_test.sh` | Minimal curl-based streaming viewer | Quick manual smoke |
| `backend/examples/e2e_test_enhanced.sh` | Robust test: health check, retries, timeout, key assertions, report extraction, exit codes | CI & reproducible validation |

### 5.4 Enhanced Script Behavior
Exit codes:
- 0: Success (final report captured)
- 2: Usage error
- 3: Health endpoint not ready
- 4: HTTP failure (non-200 or stream error)
- 5: Stream ended without final report / missing mandatory key
- 6: Global timeout exceeded

Key expectations (asserted): `run_id`, `generate_initial_queries`, `execute_searches`, `reflection_and_refinement`, `retrieve_and_synthesize_report`, `report`.

Usage examples:
```bash
bash backend/examples/e2e_test_enhanced.sh "recent development on neuro ai"
bash backend/examples/e2e_test_enhanced.sh "ai in climate change" --timeout 600
```

Artifacts produced:
- Log: `logs/e2e_test_enhanced_<timestamp>.log`
- Extracted report: `logs/e2e_test_enhanced_<timestamp>_report.txt`

### 5.5 Success & Failure Heuristics
| Signal | Interpretation | Action |
|--------|---------------|--------|
| Health fails repeatedly | Service not started / port clash | Inspect container: `docker ps`, `docker logs langgraph-api` |
| Stream ends before `report` | Upstream node error or LLM failure | Search log for last chunked node key |
| Long stall after queries | External search latency / API quota | Reduce queries or set `TEST_MODE=1` |
| No DB ingestion | No DOI or ingestion path triggered | Enable fallback vars or inspect `automated_resource_management` logs |

### 5.6 Configuration & Determinism
Environment knobs (set in `.env` or docker-compose overrides):
- `GENERATION_MODEL`, `EMBEDDING_MODEL`: LLM / embedding choices.
- `TEST_MODE=1`: Disables outbound DOI lookups & some network calls for faster, deterministic loops.
- `ENABLE_TEST_FALLBACK_INGEST=1`: Allows controlled ingestion fallback from abstracts in test mode.
- `MAX_RESEARCH_LOOPS` (code constant): Loop cap (adjust via code patch if needed for perf tests).

### 5.7 DB Validation (Optional Step)
After a successful run (ingestion path triggered):
```sql
-- Example manual check (psql inside postgres container)
SELECT source, COUNT(*) AS chunks FROM documents GROUP BY source ORDER BY COUNT(*) DESC LIMIT 5;
```
Automate by adding a lightweight Python script querying `Document` count delta before/after.

### 5.8 Integration into Session-Driven Workflow
When an E2E run is the goal condition of a development or debugging session:
1. Start a session log under `/.ai-sessions/development/` (new feature) or `/.ai-sessions/debugging/` (failure reproduction).
2. Record: topic used, script variant, git commit, env flags, start timestamp.
3. Embed log artifact path(s) and extracted key timeline (see snapshot template below).
4. If failure: create an inline "Debug Snapshot" subsection (DO NOT start a new session file) describing hypothesis + attempted fix + re-run result.
5. Mark session COMPLETE only when exit code 0 AND `report` length > threshold (e.g., 500 chars) unless otherwise justified.

### 5.9 Snapshot Template
Each E2E session should include an appended structured snapshot (for machine + human parsing):
```
--- E2E SNAPSHOT v1 ---
timestamp_start: 2025-10-03T09:21:07Z
commit: <git-sha>
topic: "recent development on neuro ai"
script: backend/examples/e2e_test_enhanced.sh
env:
    TEST_MODE: "0"
    GENERATION_MODEL: "gemini-1.5-flash"
    EMBEDDING_MODEL: "text-embedding-004"
result:
    exit_code: 0
    duration_seconds: 312
    observed_keys:
        - run_id
        - generate_initial_queries
        - execute_searches
        - reflection_and_refinement
        - retrieve_and_synthesize_report
        - report
    research_loop_count: 2
    report_chars: 6842
artifacts:
    log: logs/e2e_test_enhanced_20251003_092107.log
    report: logs/e2e_test_enhanced_20251003_092107_report.txt
notes: |
    Loop 1 produced 3 abstracts; reflection requested additional queries (9 follow-ups). Ingestion path triggered, 1 DOI retrieved.
--- END SNAPSHOT ---
```

Assistants must parse this block (YAML-like) for automated meta-analysis (e.g., comparing loop counts across sessions).

### 5.10 CI Integration (Planned)
Recommended GitHub Actions step:
1. Spin up `docker-compose -f docker-compose-dev.yml up -d`.
2. Run enhanced script with deterministic topic (e.g., `neuro ai test summarization` + `TEST_MODE=1`).
3. Upload `logs/e2e_test_enhanced_*` as artifacts.
4. Parse report length + required keys; fail job if missing.

## 6. Snapshot-Based Observability and Live Debugging

The Session-Driven Workflow relies on layering runtime evidence into durable, structured snapshots:
- **Execution Snapshots**: E2E snapshot (above) + per-node timing (future enhancement: include timestamps for first & last occurrence of each node key).
- **Debug Snapshots**: Triggered only inside a failing session; must contain: failing condition, hypothesis, applied patch/command, re-run reference, delta outcome.
- **Data Provenance Snapshots** (future): Summarize ingested documents (DOI list + chunk counts) to track knowledge base growth per session.

Assistant RULES:
1. Never overwrite existing snapshot blocks; always append.
2. Always include `commit` and `topic` when snapshotting E2E runs.
3. If exit code ≠ 0, include `failure_stage` (e.g., `health`, `invoke`, `stream`, `assertion`).
4. Avoid sensitive API keys in snapshots.

This ensures longitudinal traceability of research agent evolution and supports automated regression detection.

### 6.1 Live Debugging Workflow in Practice

To make this process concrete, the assistant and developers **must** follow the "Session-Driven Workflow" by creating and maintaining a log file within the `/.ai-sessions/` directory for any non-trivial debugging task.

This log serves as a "black box recorder" for the debugging process, capturing hypotheses, attempts, and results.

**A live example of this process can be found at:**
- **[.ai-sessions/debug_e2e_http_500_error.md](/.ai-sessions/debug_e2e_http_500_error.md)**

This file documents the step-by-step resolution of a real `HTTP 500` error in the E2E test. By following and updating this log, the assistant creates a traceable, shareable history of the debugging session, which is invaluable for team collaboration and future reference.

**Workflow for the Assistant:**
1.  **Identify the Issue:** A test fails (e.g., an E2E test).
2.  **Create a Debugging Log:** Create a new file in `/.ai-sessions/debugging/` named `debug_<issue_summary>.md`.
3.  **Document the Initial State (Snapshot #1):** Record the command, the error, and the relevant logs.
4.  **Formulate a Hypothesis:** State a clear hypothesis about the cause of the error.
5.  **Attempt a Fix:** Apply a change to the code.
6.  **Verify and Document:** Re-run the test and document the outcome in a new "Snapshot" section in the same file.
7.  **Iterate:** Continue this cycle of "Hypothesize -> Fix -> Verify" until the issue is resolved.
8.  **Commit:** The final debugging log is committed along with the code changes, providing full context for the fix.
