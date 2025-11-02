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

### Session File Naming Convention (Updated 2025-10-15 14:00)

All session files **must** follow the standardized naming format to ensure chronological traceability:

**Format**: `YYYY-MM-DD-HHmm-phase-X.Y-<category>-<description>.md`

**Components**:
1. **DateTime Prefix**: `YYYY-MM-DD-HHmm` (ISO 8601 format, 24-hour clock, UTC+0)
   - Example: `2025-10-15-1430` = October 15, 2025, 14:30 UTC
2. **Phase Identifier**: `phase-X.Y` (e.g., `phase-3.6`, `phase-4.1`)
3. **Category Tag**: One of: `plan`, `progress`, `report`, `test`, `debug`, `analysis`, `summary`, `reference`
4. **Description**: kebab-case, 1-5 words describing the session focus

**Examples**:
- `2025-10-14-0900-phase-3.6-progress-day1-backend-hitl.md` - Morning progress log for backend HITL development
- `2025-10-14-1430-phase-3.6-test-unit-hitl-nodes.md` - Afternoon unit test report for HITL nodes
- `2025-10-15-1000-phase-3.6-analysis-progress-optimization.md` - Analysis of development progress vs plan
- `2025-10-20-1800-phase-3.6-summary-complete.md` - Final completion summary for Phase 3.6

**Category Definitions**:
| Category | Purpose | Frequency |
|----------|---------|-----------|
| `plan` | Implementation plans | 1-2 per phase |
| `progress` | Daily/incremental progress logs | 1-3 per day |
| `report` | Completion reports | 1 per milestone |
| `test` | Test execution reports | As needed |
| `debug` | Debugging session logs | As needed |
| `analysis` | Strategic/retrospective analysis | 1-2 per week |
| `summary` | Phase/project summaries | 1 per phase |
| `reference` | Quick reference guides | 1-2 per phase |

**Why This Format?**
1. **Chronological Sorting**: Files naturally sort by creation date (`ls` or file browser)
2. **Phase Grouping**: Easy to filter files by `grep "phase-3.6"`
3. **Category Filtering**: Quick search for specific document types (`grep "test"`)
4. **Self-Documenting**: Filename alone provides context (date + phase + purpose)
5. **Git-Friendly**: Avoids special characters, safe for all operating systems

**Legacy Files**: Existing files with old naming formats (e.g., `PHASE_3.6_DAY1_PROGRESS.md`) are preserved as-is to maintain Git history. A mapping index is available in `.ai-sessions/development/README.md`.

**Legacy Files**: Existing files with old naming formats (e.g., `PHASE_3.6_DAY1_PROGRESS.md`) are preserved as-is to maintain Git history. A mapping index is available in `.ai-sessions/development/README.md`.

### Principle 0: API Contract First

For any task involving interaction between the frontend (VS Code extension) and the backend (Python agent), you **must** adhere to the **API Contract First** principle.

1.  **The Goal**: To ensure frontend and backend development are perfectly aligned, enabling parallel work and eliminating integration errors (like the `404 Not Found` error that prompted this update).
2.  **The Contract**: The `openapi.yaml` file is the single source of truth for all API definitions.
3.  **Your Primary Task**: Before writing any implementation code for a feature, your first step is to:
    -   **Check for the contract**: Search for and review the `openapi.yaml` file.
    -   **Define or Update**: Work with the user to define a new API endpoint or update an existing one within `openapi.yaml`.
    -   **Gain Agreement**: Do not proceed until the contract is clear and validated. This contract is your blueprint for the implementation plan.

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

### b. Snapshot-Driven Development

To ensure progress is tracked and the development process is transparent, the AI assistant must follow a strict snapshot-driven workflow when executing a development plan.

**The Workflow:**
1.  **Identify the Current Step:** Before starting work, identify the current step from the relevant session snapshot file (e.g., in `/.ai-sessions/development/`).
2.  **Execute the Step:** Perform the actions required to complete the step (e.g., creating files, modifying code).
3.  **Update the Snapshot:** After the step is successfully completed, the assistant **must** first update the session snapshot file. This involves marking the completed step (e.g., with `[DONE]`) and adding a brief summary of the actions taken.
4.  **Proceed:** Only after the snapshot is updated can the assistant propose and begin the next development step.

This ensures a persistent, auditable trail of the development progress for every session.

By adhering to this framework, the AI assistant can effectively contribute to the project, maintaining high standards of code quality, documentation, and process transparency.

## Detailed Strategy

This framework's specific implementation details are defined in `doc/WORKFLOW_STRATEGY.md`. This document is the core behavioral guideline for all AI developers (both human and model) and details:

1.  **File Organization & Naming Conventions**: How to organize and name session files based on work intent (feature development vs. bug fixing).
2.  **Unified Session Workflow**: The four standard phases from initialization, iterative execution, conditionally triggered debugging state, to final completion.
3.  **Debugging Snapshot**: How to structurally record errors, propose hypotheses, attempt fixes, and re-verify when a test fails.

### Development Environment: VS Code Dev Containers

To facilitate the **Session-Driven Workflow**, the project has adopted a fully containerized development environment using **VS Code Dev Containers**. This approach directly supports the core principles of GEMINI by providing a consistent, reproducible, and isolated environment for all development and debugging tasks.

-   **Consistency:** The entire development environment, including all dependencies and tooling, is defined in code (`Dockerfile`, `docker-compose.yml`). This eliminates "works on my machine" problems and ensures that both human and AI developers operate in the exact same context.

-   **Pre-built for Speed:** The development images are pre-built with the VS Code Server installed. This significantly reduces the startup time for new Dev Container sessions, allowing developers to get into a coding session almost instantly. This speed is crucial for maintaining a tight feedback loop during iterative development and debugging.

-   **Separate Contexts for Frontend and Backend:** The project provides two distinct Dev Container configurations (`.devcontainer/devcontainer.json` for frontend and `.devcontainer/devcontainer.json.backend` for backend). This allows developers to work in a context that is tailored to the specific task at hand, with the correct tools and extensions readily available. This separation of concerns aligns with the GEMINI principle of breaking down complex problems into smaller, manageable units of work.

By leveraging Dev Containers, the GEMINI framework ensures that every development "session" is executed in a clean, predictable, and efficient environment, thereby enhancing the reliability and effectiveness of the AI-assisted development process.

## E2E Testing & Regression Snapshots (Golden File Testing)

Our End-to-End (E2E) tests validate the entire research workflow. To prevent regressions, we use an enhanced test script (`e2e_test_enhanced.sh`) that compares the output of a test run against a pre-recorded "Golden File Snapshot".

> **Note on Terminology:** These **Golden File Snapshots** are used for automated regression testing. They are distinct from the **Debugging Snapshots** captured in `.ai-sessions` files, which serve as a narrative log for a specific debugging session as defined in `doc/WORKFLOW_STRATEGY.md`.

### 1. Running the Standard E2E Test

The basic E2E test simply runs the workflow and streams the output.

**Invocation:**
```bash
make test-e2e-docker TOPIC="Your Research Topic"
```

### 2. Running the Enhanced Test with Snapshot Validation

For rigorous, automated regression testing, use the enhanced script. It validates the run's log output against a golden file snapshot.

**How it Works:**

1.  **Execute and Capture:**
    ```bash
    ./backend/examples/e2e_test_enhanced.sh "Your Research Topic"
    ```
    This runs the agent and saves its full, structured log to a temporary file (e.g., `/tmp/e2e_test_run.log`).

2.  **Snapshot Comparison:** The script automatically compares this log to a corresponding "golden" snapshot file located in `backend/tests/features/snapshots/`.

3.  **Validation:** If the output from the current run differs from the snapshot, the test fails. This is critical for detecting unintended changes in the agent's behavior.

### 3. Creating and Updating Golden File Snapshots

When you add a feature or intentionally change the agent's behavior, you must update the corresponding snapshot.

**Workflow:**

1.  **Run the enhanced test:**
    ```bash
    ./backend/examples/e2e_test_enhanced.sh "The topic for your test case"
    ```
    The test will likely fail if the snapshot exists and the output has changed. This is expected.

2.  **Inspect the new output:** Manually review the temporary log file (the path is specified in the script's output, e.g., `/tmp/e2e_test_run.log`) to ensure the new output is correct and reflects the intended changes.

3.  **Create or Update the Snapshot:**
    - If the snapshot directory doesn't exist, create it:
      ```bash
      mkdir -p backend/tests/features/snapshots
      ```
    - Copy the temporary log to become the new golden snapshot. **It's crucial to name the snapshot file descriptively based on the test case.**
      ```bash
      cp /tmp/e2e_test_run.log backend/tests/features/snapshots/neuro_ai_development.log
      ```

4.  **Commit:** Commit the new or updated snapshot file along with your code changes. This locks in the new behavior as the standard for future test runs.

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

## Holistic Testing Strategy

The end-to-end behavioral test described above is the cornerstone of our Observation-Driven Development philosophy. However, it is part of a broader, multi-layered testing strategy that covers the entire project.

The canonical guide for all testing procedures, including unit, integration, and E2E tests for the backend, VS Code extension, and frontend, is documented in the root `TESTING.md` file.

**All developers and AI assistants must refer to `TESTING.md` as the single source of truth for how to verify code changes.**

## Example Debugging Scenario

To make this process concrete, the assistant and developers **must** follow the "Session-Driven Workflow" by creating and maintaining a log file within the `/.ai-sessions/` directory for any non-trivial debugging task.

This log serves as a "black box recorder" for the debugging process, capturing hypotheses, attempts, and results.

**Live examples of this process can be found at:**
- **[.ai-sessions/debugging/debug_e2e_http_500_error.md](/.ai-sessions/debugging/debug_e2e_http_500_error.md)** - Documents the resolution of an `HTTP 500` error in E2E tests
- **[.ai-sessions/development/2025-10-12-debug-frontend-backend-sync.md](/.ai-sessions/development/2025-10-12-debug-frontend-backend-sync.md)** - Documents fixing frontend-backend synchronization and API documentation issues
- **[.ai-sessions/development/2025-10-12-enhance-library-document-display.md](/.ai-sessions/development/2025-10-12-enhance-library-document-display.md)** - Comprehensive planning for historical data management feature (Phase 3.5)

These files document the step-by-step resolution of real issues and feature planning. By following and updating these logs, the assistant creates a traceable, shareable history of the development session, which is invaluable for team collaboration and future reference.

**Workflow for the Assistant:**
1.  **Identify the Issue/Task:** A test fails, or a new feature is requested.
2.  **Create a Session Log:** Create a new file in `/.ai-sessions/debugging/` (for bugs) or `/.ai-sessions/development/` (for features) named `<date>-<issue_summary>.md`.
3.  **Document the Initial State (Snapshot #1):** Record the command, the error, or the feature requirements, and the relevant logs.
4.  **Formulate a Hypothesis/Plan:** State a clear hypothesis about the cause (for bugs) or a detailed implementation plan (for features).
5.  **Attempt a Fix/Implementation:** Apply changes to the code.
6.  **Verify and Document:** Re-run tests or verify the implementation, and document the outcome in a new "Snapshot" section in the same file.
7.  **Iterate:** Continue this cycle of "Hypothesize -> Fix -> Verify" (for bugs) or "Plan -> Implement -> Verify" (for features) until the goal is achieved.
8.  **Commit:** The final session log is committed along with the code changes, providing full context for the work done.
