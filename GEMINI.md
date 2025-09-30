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

## 2. Core Philosophy: Snapshot-Driven Development

All development and debugging tasks **must** follow a **Snapshot-Driven** methodology. This creates a real-time, traceable log of the entire process, ensuring transparency and seamless collaboration. The authoritative guides for these processes are:
- **Development**: `doc/DEVELOPMENT_STRATEGY.md`
- **Debugging**: `doc/DEBUGGING_STRATEGY.md`

### a. Development Workflow: `DEVELOPMENT_SESSION.md`

The goal is to **build a new feature**.

1.  **Initialize**: Create `DEVELOPMENT_SESSION.md`.
    - **Goal**: Define the user story and specify the acceptance test (`*.feature` file) that must pass.
    - **Analysis**: Explore the codebase (`glob`, `read_file`, `search_file_content`) to assess impact.
    - **Plan**: Decompose the work into a clear, step-by-step plan.

2.  **Iterate (TDD Cycle)**: For each step in the plan:
    - **Log Action**: Record the `[Step N: <description>]` in the session file.
    - **Write Test**: Create a failing unit or integration test.
    - **Log Tool Call**: Record the exact `replace` or `write_file` call used to implement the code.
    - **Verify**: Run the relevant test to confirm the step's success. Log the command and result.
    - **Status**: Mark the step as `✅ Success` or `❌ Failed`.

3.  **Final Verification**: Once all steps are complete, run the final acceptance test to prove the feature is done.

### b. Debugging Workflow: `logs/debugging/*.md`

The goal is to **fix a known bug**. This is triggered when a `Verification` step fails.

1.  **Initialize**: Create `logs/debugging/YYYY-MM-DD-feature-name.md`.
2.  **Reproduce & Snapshot**: Record the full error message, logs, and stack trace.
3.  **Diagnose & Hypothesize**: State a clear hypothesis about the root cause.
4.  **Log Analysis and Plan**: Before attempting a fix, log a detailed analysis of the test failures and a clear, step-by-step plan for the fix in the session file.
5.  **Attempt Fix**: Log the `replace` or `write_file` call used to apply the fix.
6.  **Verify**: Rerun the failing test to confirm the fix. If it fails again, repeat the loop.
7.  **Conclude**: Summarize the root cause and final solution.

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