# Project Testing Strategy

This document outlines the comprehensive, multi-layered testing strategy for the Auto-Researcher project. It is designed to be understood and executed by both human developers and AI assistants, aligning with the project's core philosophy of Observation-Driven Development (ODD).

## Core Philosophy

1.  **Observation-Driven Development (ODD):** We prioritize testing the observable *behavior* of the system, not just the final output. This is achieved through snapshot testing at the end-to-end (E2E) level.
2.  **Layered Testing:** Each part of the application (backend, VS Code extension, frontend) has a dedicated, multi-layered testing strategy to ensure correctness at different levels of integration.
3.  **AI-Driven & Documented:** This strategy is the single source of truth for testing. All test commands are standardized to be easily executed by an AI assistant as part of the "Unified Session Workflow."

---

## 1. Backend Testing (`backend/`)

The backend agent's logic is complex and stateful, making E2E behavioral tests the most critical layer.

### 🔹 Unit & Integration Tests

-   **Purpose:** To quickly verify the logic of individual components (tools, database functions, state transitions) in isolation.
-   **Framework:** `pytest`
-   **Command:**
    ```bash
    make test-backend
    ```
-   **Environment:** Must be run inside the **backend** (`langgraph-api`) dev container.

### 🔸 End-to-End (E2E) Behavioral Snapshot Tests

-   **Purpose:** **This is the core of the backend's quality assurance.** It verifies the agent's entire research workflow by comparing the full execution log against a blessed "golden file" snapshot.
-   **Framework:** `bash` script (`e2e_test.sh`) comparing log outputs.
-   **Command:**
    ```bash
    make test-e2e TOPIC="<your-topic>"
    ```
-   **Environment:** Must be run inside the **backend** (`langgraph-api`) dev container.

---

## 2. VS Code Extension Testing (`vscode-extension/`)

The VS Code extension requires testing at both the logic (integration) and UI (E2E) levels.

### 🔹 Unit & Integration Tests (Primary Workflow)

-   **Purpose:** **This is the main feedback loop for extension development.** It tests the extension's logic and its interaction with VS Code APIs *without* relying on a live backend or rendering a real UI. It is fast and reliable.
-   **Frameworks:** `mocha`, `sinon` (for mocking/stubbing `vscode` and `axios` APIs).
-   **Command:**
    ```bash
    npm test
    ```
-   **Environment:** Run inside the `vscode-extension` directory within the **frontend** (`vscode-dev`) dev container.

### 🔸 End-to-End (E2E) UI Snapshot Tests

-   **Purpose:** To verify key user journeys in a real VS Code instance connected to a **live backend**. This aligns with the backend's snapshot philosophy by taking snapshots of UI components (e.g., a Webview's HTML) and comparing them against a blessed version.
-   **Frameworks:** `vscode-test`, `mocha`
-   **Command:**
    ```bash
    npm run test-e2e
    ```
-   **Environment:** Run inside the `vscode-extension` directory within the **frontend** (`vscode-dev`) dev container.

---

## 3. Legacy Frontend Testing (`frontend/`)

As a legacy application, the frontend maintains a standard set of tests.

### 🔹 Unit & Component Tests

-   **Purpose:** To test individual React components in isolation.
-   **Frameworks:** `jest`, `React Testing Library`
-   **Command:**
    ```bash
    npm test
    ```
-   **Environment:** Run inside the `frontend` directory within the **frontend** (`vscode-dev`) dev container.
