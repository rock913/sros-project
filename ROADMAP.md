# Project Upgrade Plan: Towards an Automated Research Platform

This project is undergoing a significant upgrade to transform it from a demo into a powerful, VS Code-native automated research platform. The development is divided into three phases.

### Phase 1: Backend Foundation and Core Agent (Complete)

This foundational phase has been completed. We have built a robust, "headless" AI agent that is callable via an API and fully implements the four-stage research workflow described above.

**Key deliverables from this phase:**
-   **Functional FastAPI Server:** The backend is served via FastAPI, with database initialization handled on startup.
-   **PostgreSQL + pgvector DB:** A PostgreSQL database with the `pgvector` extension is integrated for RAG.
-   **Four-Stage LangGraph Agent:** The core agent logic is implemented in `backend/src/agent/graph.py`.
-   **Integrated Tooling:** The agent uses `arxiv`, `unpaywall`, `pyzotero`, and `litellm` to perform its tasks.
-   **Containerized Environment:** The entire backend stack can be run using Docker Compose.

### Phase 2: VS Code Skeleton and Static Display (In Progress)

The next phase focuses on building the user-facing component of the platform: a VS Code extension. The goal is to create a "read-only" view of the research process.

**Detailed Plan:**
1.  **Develop the basic VS Code Extension:**
    -   Set up a new TypeScript project for the extension.
    -   Implement the three-panel layout as described in the technical documentation:
        -   **Left Panel (Research Asset Library):** A TreeView to display research resources (papers, notes).
        -   **Center Panel (Dynamic Manuscript):** The main editor, where the final report will be shown.
        -   **Right Panel (AI Control Panel):** A Webview to show the agent's status and thinking process.
2.  **API Integration (Read-Only):**
    -   The extension will call the backend API to fetch the status and results of a completed research task.
    -   The data will be used to populate the three panels (e.g., list of papers in the asset library, final report in the editor, agent logs in the control panel).
3.  **Static Visualization:**
    -   The primary goal is to prove that the frontend can successfully connect to and display data from the backend. All interactions that trigger new runs will be handled via API tools (like Insomnia or curl) for now.

### Phase 3: Real-time Interaction and Dynamic Collaboration (Future)

The final phase will bring the platform to life by enabling full, real-time, two-way communication between the user and the agent.

**Detailed Plan:**
1.  **WebSocket Integration:**
    -   Implement WebSocket communication between the VS Code extension and the FastAPI backend.
    -   This will allow the agent to stream its "thoughts" and progress to the AI Control Panel in real-time.
2.  **Interactive Controls:**
    -   Build the UI components in the AI Control Panel (using React and the VS Code Webview UI Toolkit) that allow the user to:
        -   Start new research tasks with a natural language prompt.
        -   Observe the agent's progress.
        -   Implement "human-in-the-loop" (HITL) decision points, where the agent pauses and asks for user input before proceeding.
3.  **Dynamic Document Editing:**
    -   The agent will be able to directly edit the Markdown file in the center panel using the VS Code Workspace API. This will allow the agent to collaboratively write the report with the user.
