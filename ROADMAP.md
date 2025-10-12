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

The next phase focuses on building the user-facing component of the platform: a VS Code extension. The goal is to create a "read-only" view of the research process, with the entire development workflow being containerized.

**Detailed Plan:**
1.  **Containerized Development Environment:**
    -   Create a dedicated Dockerfile and Dev Container configuration (`.devcontainer/devcontainer.json`) for the extension.
    -   This environment will pre-install all necessary dependencies (Node.js, `yo`, `vsce`) for a consistent, one-click setup.
    -   Integrate this new service into the main `docker-compose-dev.yml` to ensure seamless networking with the backend.
2.  **Develop the basic VS Code Extension (inside the container):**
    -   Set up a new TypeScript project for the extension under a new `vscode-extension` directory.
    -   Implement the three-panel layout as described in the technical documentation:
        -   **Left Panel (Research Asset Library):** A TreeView to display research resources (papers, notes).
        -   **Center Panel (Dynamic Manuscript):** The main editor, where the final report will be shown.
        -   **Right Panel (AI Control Panel):** A Webview to show the agent's status and thinking process.
3.  **API Integration (Read-Only):**
    -   The extension will call the backend API (via its Docker service name, e.g., `http://backend:8000`) to fetch the status and results of a completed research task.
    -   The data will be used to populate the three panels.
4.  **Static Visualization:**
    -   The primary goal is to prove that the frontend can successfully connect to and display data from the backend. All interactions that trigger new runs will be handled via API tools for now.

### Phase 3: Real-time Interaction and Dynamic Collaboration (Complete)

This phase brought the platform to life by enabling full, real-time, two-way communication between the user and the agent.

**Completed Deliverables:**
1.  **WebSocket Integration:**
    -   ✅ Implemented WebSocket communication between the VS Code extension and the FastAPI backend.
    -   ✅ Agent streams its "thoughts" and progress to the AI Control Panel in real-time.
2.  **Interactive Controls:**
    -   ✅ Built UI components in the AI Control Panel (using React and the VS Code Webview UI Toolkit) that allow the user to:
        -   Start new research tasks with a natural language prompt.
        -   Observe the agent's progress.
        -   Implement "human-in-the-loop" (HITL) decision points, where the agent pauses and asks for user input before proceeding.
3.  **Dynamic Document Editing:**
    -   ✅ The agent can directly edit the Markdown file in the center panel using the VS Code Workspace API, allowing collaborative report writing with the user.

### Phase 3.5: Historical Data Management and Advanced Analytics (In Progress)

Building on the foundation established in Phases 1-3, this phase focuses on transforming the platform from a single-task tool into a comprehensive research knowledge base with full historical tracking and advanced analytics.

**Strategic Goal:** Enable researchers to manage, track, and analyze their entire research journey across multiple sessions, papers, and reports.

**Detailed Plan (7 weeks):**

#### Phase 3.5.1: Database Foundation & Session Management (Weeks 1-2)
**Objective:** Establish persistent storage for research sessions and historical data.

1.  **Database Schema Design:**
    -   Design PostgreSQL schema for 4 core entities: `ResearchSession`, `Paper`, `Report`, `SessionEvent`
    -   Create Alembic migration scripts for schema versioning
    -   Implement database indexing strategy for performance

2.  **Backend API - Session Management:**
    -   `GET /sessions` - List all research sessions with filtering (status, date range)
    -   `GET /sessions/{session_id}` - Retrieve detailed session information
    -   `POST /sessions` - Create new research session
    -   `DELETE /sessions/{session_id}` - Archive/delete session
    -   `GET /sessions/{session_id}/events` - Session timeline/event log

3.  **LangGraph Integration:**
    -   Integrate `PostgresSaver` checkpointer with LangGraph
    -   Auto-create session records on `POST /agent/invoke`
    -   Auto-persist papers during literature discovery
    -   Auto-create report versions during synthesis
    -   Record critical events (query generation, search execution, report generation)

4.  **Frontend - Sessions TreeView:**
    -   Create `SessionsProvider` to display all research sessions
    -   Implement session switching/navigation
    -   Add context menu: View Details, Delete, Export

**Milestone M1 (Week 2):** Complete session management infrastructure with full CRUD operations and persistent storage.

#### Phase 3.5.2: Literature Library & Report History (Weeks 3-4)
**Objective:** Implement comprehensive historical tracking for papers and reports.

1.  **Backend API - Paper Management:**
    -   `GET /papers` - List all papers with advanced filtering (session, source, date, keyword)
    -   `GET /papers/{paper_id}` - Detailed paper information
    -   `GET /papers/export` - Export to BibTeX/RIS/JSON formats
    -   Implement full-text search across titles/abstracts

2.  **Backend API - Report Management:**
    -   `GET /reports` - List all report versions
    -   `GET /reports/{report_id}` - Retrieve specific report version
    -   `GET /sessions/{session_id}/reports/latest` - Get most recent report
    -   `GET /reports/{id1}/compare/{id2}` - Generate diff between report versions
    -   `GET /reports/{report_id}/export` - Export to Markdown/HTML/PDF

3.  **Frontend - Enhanced Library TreeView:**
    -   Refactor `AssetLibraryProvider` to display all historical papers
    -   Multi-dimensional grouping (by session, source, date, author)
    -   Paper detail Webview with full metadata
    -   Context menu: Export, View Details, Open URL, Copy Citation

4.  **Frontend - Enhanced Documents TreeView:**
    -   Refactor `ManuscriptProvider` to show report version history
    -   Group by session with version indicators
    -   Report detail Webview with Markdown rendering
    -   Context menu: Export, Compare Versions, View Session

**Milestone M2 (Week 4):** Complete historical literature and report management with full export capabilities.

#### Phase 3.5.3: Advanced Analytics & Visualization (Weeks 5-6)
**Objective:** Provide insights through statistical analysis and data visualization.

1.  **Backend API - Statistics & Analytics:**
    -   `GET /stats/global` - Overall statistics (total papers, reports, sessions)
    -   `GET /stats/trends` - Time-series data (daily/weekly activity)
    -   `GET /stats/keywords` - Keyword extraction and frequency analysis
    -   `GET /stats/authors` - Author collaboration network data
    -   Background aggregation jobs for performance

2.  **Frontend - Analytics Dashboard:**
    -   Create comprehensive analytics Webview
    -   Integrate Chart.js for interactive visualizations:
        -   Research activity timeline (line chart)
        -   Paper source distribution (pie chart)
        -   Keyword cloud visualization
        -   Author network graph (future: D3.js)
    -   Real-time metric updates
    -   Export analytics reports

3.  **Frontend - Enhanced Sessions TreeView:**
    -   Expandable tree showing session → papers/reports/events
    -   Timeline visualization within session details
    -   Session comparison feature
    -   Batch operations (export multiple sessions)

**Milestone M3 (Week 6):** Complete advanced analytics with interactive visualizations and comprehensive insights.

#### Phase 3.5.4: Optimization & Production Readiness (Week 7)
**Objective:** Performance tuning, UX refinement, and complete documentation.

1.  **Performance Optimization:**
    -   Database query optimization with proper indexing
    -   API response caching (Redis integration)
    -   Frontend lazy loading and virtual scrolling
    -   Pagination for large datasets
    -   Load testing and benchmarking

2.  **User Experience Enhancements:**
    -   Loading indicators for all async operations
    -   Comprehensive error handling with user-friendly messages
    -   Keyboard shortcuts for common actions
    -   Search/filter across all views
    -   Responsive UI layout adjustments

3.  **Documentation & Testing:**
    -   Update `openapi.yaml` with all 16 new endpoints
    -   Complete `API_DOCUMENTATION.md` update
    -   VS Code Extension user guide
    -   Comprehensive unit tests (target: >85% coverage)
    -   Integration tests for all API endpoints
    -   End-to-end tests for complete workflows

4.  **Deployment Preparation:**
    -   Database migration scripts with rollback support
    -   Environment configuration documentation
    -   Docker Compose updates for production
    -   Monitoring and logging setup

**Milestone M4 (Week 7):** Production-ready system with complete documentation and test coverage >85%.

---

**Phase 3.5 Summary:**
-   **Duration:** 7 weeks (1.5 months)
-   **New API Endpoints:** 16 (sessions, papers, reports, statistics)
-   **New Data Models:** 4 (ResearchSession, Paper, Report, SessionEvent)
-   **Enhanced UI Components:** 4 (Sessions TreeView, Enhanced Library, Enhanced Documents, Analytics Dashboard)
-   **Key Technologies:** PostgreSQL, SQLAlchemy, Alembic, Chart.js, PostgresSaver (LangGraph)

**Reference Documentation:** `.ai-sessions/development/2025-10-12-enhance-library-document-display.md`

### Phase 4: Ecosystem Integration and Advanced Features (Future)

The final phase will expand the platform's capabilities beyond isolated research tasks.

**Planned Features:**
1.  **Multi-Source Literature Integration:**
    -   PubMed, Semantic Scholar, Google Scholar connectors
    -   Automated citation tracking
    -   Reference network visualization

2.  **Collaborative Research:**
    -   Shared research sessions
    -   Team comments and annotations
    -   Role-based access control

3.  **AI Model Expansion:**
    -   Support for multiple LLM providers
    -   Model comparison and benchmarking
    -   Custom fine-tuned models for domain-specific research
