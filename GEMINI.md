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