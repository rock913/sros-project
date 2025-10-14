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

#### Phase 3.5.2: Literature Library & Report History (Weeks 3-4) ✅ COMPLETE

**Status:** ✅ Completed on 2025-10-13  
**Objective:** Implement comprehensive historical tracking for papers and reports.

1.  **Backend API - Paper Management:** ✅
    -   ✅ `GET /papers` - List all papers with advanced filtering (session, source, date, keyword)
    -   ✅ `GET /papers/{paper_id}` - Detailed paper information
    -   ✅ `GET /papers/export` - Export to BibTeX/RIS/JSON formats
    -   ✅ Implement full-text search across titles/abstracts

2.  **Backend API - Report Management:** ✅
    -   ✅ `GET /reports` - List all report versions
    -   ✅ `GET /reports/{report_id}` - Retrieve specific report version
    -   ✅ `GET /sessions/{session_id}/reports/latest` - Get most recent report
    -   ✅ `GET /reports/compare` - Generate diff between report versions (query params: report_id_1, report_id_2)
    -   ✅ `GET /reports/{report_id}/export` - Export to Markdown/HTML/PDF (PDF returns 501)

3.  **Frontend - Enhanced Library TreeView:** ✅
    -   ✅ Refactor `AssetLibraryProvider` to display all historical papers
    -   ✅ Multi-dimensional grouping (by session, source, date)
    -   ✅ Paper detail Webview with full metadata
    -   ✅ Context menu: Export, View Details

4.  **Frontend - Enhanced Documents TreeView:** ✅
    -   ✅ Refactor `ManuscriptProvider` to show report version history
    -   ✅ Group by session with version indicators
    -   ✅ Click to open report in markdown editor
    -   ✅ Context menu: Export, Compare Versions

**Testing:** ✅
-   ✅ Backend: 25/25 tests passed (100%)
-   ✅ Frontend: 15/15 tests passed (100%)
-   ✅ Test scripts: `test-phase3.5.2.sh`, `test-extension-api.sh`
-   ✅ Documentation: `doc/PHASE_3.5.2_TESTING_GUIDE.md`

**Milestone M2 (Week 4):** ✅ Complete historical literature and report management with full export capabilities.

**Git Commit:** `147ba96` - feat(phase3.5.2): complete Literature Library & Report History with 100% test coverage

#### Phase 3.5.3: Advanced Analytics & Visualization (Weeks 5-6) ✅ COMPLETE

**Status:** ✅ Completed 2025-10-14  
**Objective:** Provide insights through statistical analysis and data visualization.

**Completion Report:** See `.ai-sessions/development/PHASE_3.5.3_FINAL_COMPLETION_REPORT.md`

**Completed Deliverables:**

1.  **Backend API - Analytics Endpoints:** ✅
    -   ✅ `GET /analytics/sessions/stats` - Aggregated statistics with daily breakdown
    -   ✅ `GET /analytics/sessions` - Paginated session list with filtering
    -   ✅ `GET /analytics/sessions/{id}` - Detailed session info with timeline
    -   ✅ `GET /analytics/papers/trends` - Paper collection trends analysis
    -   ✅ Backend module: `analytics.py` (~400 lines, 4 core functions)

2.  **Frontend - Analytics Dashboard:** ✅
    -   ✅ Comprehensive Webview with Chart.js 4.4.0
    -   ✅ 4 Interactive visualizations:
        -   Daily Sessions Line Chart (completed vs failed)
        -   Papers Collection Bar Chart
        -   Status Distribution Pie Chart
        -   Top Topics Horizontal Bar Chart
    -   ✅ 4 Summary cards (Total Sessions, Success Rate, Total Papers, Avg Duration)
    -   ✅ Sessions table with 10 recent sessions
    -   ✅ Time range selector (24h/7d/30d/all)
    -   ✅ Webview message handling for interactions

3.  **WebSocket Real-time Integration:** ✅
    -   ✅ `WS /agent/stream` - Real-time research progress streaming
    -   ✅ Extension WebSocket client with progress callbacks
    -   ✅ Control Panel real-time updates

**Testing Results:**
-   ✅ Week 1: 24/24 WebSocket verification checks passed
-   ✅ Week 2: 9/10 Analytics API E2E tests passed
-   ✅ Week 3: TypeScript compilation 0 errors

**Technical Metrics:**
-   17,393 lines of code added
-   12 new files, 7 modified
-   11 TypeScript interfaces
-   Zero critical bugs

**Milestone M3 (Week 6):** ✅ Complete - Advanced analytics with interactive visualizations delivered.

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
    -   Update `openapi.yaml` with all endpoints
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
-   **Status:** Phase 3.5.1-3.5.3 Complete ✅ | Phase 3.5.4 Pending
-   **New API Endpoints:** 20+ (sessions, papers, reports, analytics, websocket)
-   **New Data Models:** 4 (ResearchSession, Paper, Report, SessionEvent)
-   **Enhanced UI Components:** 5 (Sessions TreeView, Enhanced Library, Enhanced Documents, Analytics Dashboard, WebSocket Control)
-   **Key Technologies:** PostgreSQL, SQLAlchemy, Alembic, Chart.js, WebSocket, PostgresSaver (LangGraph)

**Reference Documentation:** 
- `.ai-sessions/development/PHASE_3.5.3_FINAL_COMPLETION_REPORT.md`
- `.ai-sessions/development/2025-10-12-enhance-library-document-display.md`

---

### Phase 3.6: Real-time Collaboration & Advanced HITL (3 weeks)

**Strategic Goal:** Transform platform from single-user tool to fully interactive AI-Human collaborative research environment with deep VS Code integration.

**Vision Alignment:** Implements Chapter 3 ("科研集成开发环境") from technical roadmap - achieving true three-panel IDE experience.

#### Week 1-2: Human-in-the-Loop (HITL) Decision System

**Objective:** Enable users to guide AI at critical decision points during research workflow.

**1. Backend HITL Infrastructure:**
-   **LangGraph HITL Nodes:**
    -   `query_approval_node`: Pause after query generation, wait for user approval
    -   `paper_selection_node`: Let user filter/rank discovered papers before processing
    -   `report_revision_node`: Request user feedback on draft sections
    -   Implement `interrupt` mechanism in LangGraph for workflow pausing
-   **WebSocket HITL Protocol:**
    -   New message types: `hitl_request`, `hitl_response`
    -   Session state management for paused workflows
    -   Timeout handling (auto-resume after 5 minutes with default action)
-   **API Endpoints:**
    -   `POST /agent/hitl/respond` - Submit user decision
    -   `GET /agent/hitl/pending` - List pending HITL requests
    -   `POST /agent/hitl/resume` - Force resume with default action

**2. Frontend HITL UI Components:**
-   **Interactive Decision Cards (Control Panel Webview):**
    -   Query Approval Card: Show generated queries with Edit/Approve/Reject buttons
    -   Paper Selection Card: Multi-select list with preview + inclusion rationale
    -   Report Feedback Card: Inline comments on draft sections
-   **HITL State Indicator:**
    -   Status bar notification: "⏸️ AI Waiting for Decision (2 pending)"
    -   Click to open Control Panel with pending requests
-   **Decision History Log:**
    -   TreeView showing all past HITL decisions
    -   Ability to review and learn from previous choices

**3. Workflow Integration:**
-   Modify `graph.py` to add conditional edges for HITL nodes
-   Implement retry logic: User rejection → AI regenerates → Request approval again
-   Store HITL decisions in `session_events` table for analytics

**Milestone:** User can intervene at 3 critical points in research workflow, with full audit trail.

#### Week 3: Real-time Document Collaboration

**Objective:** Enable AI to directly edit Markdown documents in VS Code editor with non-destructive, transparent changes.

**Vision Alignment:** Implements "动态手稿" (Dynamic Manuscript) from technical roadmap - AI and user co-edit in real-time.

**1. Backend Document Streaming:**
-   **Document Diff Generation:**
    -   Implement `diff-match-patch` library for granular change tracking
    -   New WebSocket message type: `document_update`
    -   Payload structure:
        ```typescript
        {
          type: 'document_update',
          action: 'insert' | 'delete' | 'replace',
          range: { startLine, startCol, endLine, endCol },
          content: string,
          rationale: string  // Why AI made this change
        }
        ```
-   **Incremental Updates:**
    -   Stream document changes as AI generates report sections
    -   Support paragraph-level updates (not just full rewrites)
    -   Implement conflict detection if user edits during AI writing

**2. Frontend Document Integration:**
-   **VS Code Workspace API:**
    -   Use `vscode.workspace.applyEdit()` for programmatic edits
    -   Implement `WorkspaceEdit` with tracked changes
    -   Show change decorations (background highlight for AI edits)
-   **Change Review UI:**
    -   Inline "Accept/Reject" CodeLens above AI-edited paragraphs
    -   Diff view option: Side-by-side comparison with previous version
    -   Batch accept/reject all AI changes
-   **Collaboration Indicators:**
    -   Editor gutter icons: 🤖 (AI added), ✏️ (AI modified), 🗑️ (AI deleted)
    -   Hover tooltip: Show AI's rationale for each change

**3. Conflict Resolution:**
-   **Detection:** Track document version hashes, detect concurrent edits
-   **Resolution Strategies:**
    -   AI yields: If user edits same line, AI pauses and asks for merge approval
    -   Manual merge: Show three-way diff (base, user, AI) for user to resolve
    -   Auto-merge: If edits are in different sections, apply both with markers

**4. Undo/Redo Support:**
-   Integrate with VS Code's native undo stack
-   Special command: "Undo All AI Changes Since Last Save"
-   Preserve full edit history in session database

**Milestone:** AI can collaboratively edit Markdown in real-time with full user control and transparency.

---

**Phase 3.6 Deliverables:**
-   3 HITL decision points with interactive UI
-   Real-time document collaboration with conflict resolution
-   Non-destructive editing with full audit trail
-   VS Code-native diff and merge tools
-   Enhanced Control Panel with decision cards

**Technical Additions:**
-   LangGraph `interrupt()` integration
-   diff-match-patch library
-   WebSocket document streaming protocol
-   VS Code TextEditorEdit API deep integration

---

### Phase 4: Ecosystem Integration and Advanced Features (Future)

**Strategic Vision:** Transform platform into complete "科研集成开发环境" (Research IDE) with ecosystem-wide integrations and collaborative capabilities.

**Vision Alignment:** Implements Chapters 4-7 from technical roadmap - achieving enterprise-grade research platform.

---

#### Phase 4.1: Enhanced Control Panel & "Thinking Chain" Visualization (4 weeks)

**Objective:** Build comprehensive AI Control Panel (right sidebar) with real-time transparency into agent reasoning.

**Vision Reference:** Chapter 3 - "AI代理控制面板 (Webview)" as the collaboration cockpit.

**1. React-Based Control Panel (Weeks 1-2):**
-   **Technology Migration:**
    -   Migrate from plain HTML Webview to React + @vscode/webview-ui-toolkit
    -   Use Vite for fast HMR development
    -   Integrate Tailwind CSS for consistent styling
-   **Component Architecture:**
    -   `<TaskConsole>`: Natural language input with suggestion chips
    -   `<ThinkingChain>`: Real-time visualization of LangGraph node execution
    -   `<SessionTimeline>`: Visual progress bar with milestone indicators
    -   `<HITLDecisionCards>`: Interactive approval/rejection cards
    -   `<ResourceMonitor>`: API usage, token count, estimated cost

**2. "Thinking Chain" Visualization (Weeks 3-4):**
-   **Graph Visualization:**
    -   Use D3.js or React Flow to render LangGraph execution as interactive flowchart
    -   Highlight active node in real-time
    -   Show data flow between nodes
-   **Node Drill-down:**
    -   Click node → Expand to show:
        -   Input/output data
        -   LLM prompt/response
        -   Tool calls made
        -   Execution duration
-   **Trace Playback:**
    -   Timeline scrubber to replay past research sessions
    -   Step-by-step debugging mode
    -   Export trace as JSON for sharing/analysis

**3. Advanced Interaction Modes:**
-   **Guided Mode:** Step-by-step wizard for new users
-   **Expert Mode:** Direct LangGraph node triggering
-   **Batch Mode:** Queue multiple research tasks
-   **Watch Mode:** Auto-trigger research on file changes (like CI/CD)

**Milestone:** Production-ready Control Panel rivaling professional AI debugging tools like LangSmith UI.

---

#### Phase 4.2: Multi-Source Literature Integration (5 weeks)

**Objective:** Expand beyond arXiv to comprehensive academic database coverage.

**Vision Reference:** Chapter 4.1 - "智能文献发现" with multi-API tool orchestration.

**1. New Literature Sources (Weeks 1-3):**
-   **PubMed Integration:**
    -   Implement Entrez E-utilities API client
    -   Support MeSH term expansion
    -   Handle MEDLINE citation format
-   **Semantic Scholar API:**
    -   Leverage citation graph for related papers
    -   Use "Influential Citations" metric
    -   Extract author affiliations and funding data
-   **Google Scholar (via SerpAPI):**
    -   Implement rate-limited scraper
    -   Parse citation counts and metrics
    -   Handle CAPTCHA gracefully
-   **CrossRef API:**
    -   DOI resolution and metadata enrichment
    -   Journal impact factor lookup
    -   Funder registry integration

**2. Intelligent Query Routing (Week 4):**
-   **LLM-Powered Source Selection:**
    -   Analyze research topic → Recommend optimal databases
    -   Example: "quantum computing" → arXiv (physics) + IEEE Xplore
    -   Example: "cancer treatment" → PubMed + ClinicalTrials.gov
-   **Federated Search:**
    -   Parallel API calls to multiple sources
    -   Result deduplication by DOI/title similarity
    -   Unified ranking by relevance score

**3. Citation Network Analysis (Week 5):**
-   **Backend Graph Database:**
    -   Consider Neo4j or NetworkX for citation network storage
    -   Store papers as nodes, citations as edges
    -   Implement PageRank-style relevance algorithm
-   **Frontend Visualization:**
    -   Interactive citation graph (D3.js force-directed layout)
    -   Discover "citation clusters" (research communities)
    -   Find "gateway papers" (high betweenness centrality)

**Milestone:** Platform becomes comprehensive literature discovery tool covering 90%+ of academic publications.

---

#### Phase 4.3: Collaborative Research & Team Features (6 weeks)

**Objective:** Enable multi-user research projects with role-based access control.

**Vision Reference:** Chapter 7 - "支持团队协作" for open science ecosystems.

**1. User Management (Weeks 1-2):**
-   **Authentication System:**
    -   Implement OAuth 2.0 (GitHub, Google, ORCID)
    -   JWT token-based session management
    -   API key generation for programmatic access
-   **Database Schema:**
    -   `users` table (id, email, name, orcid, avatar_url)
    -   `team_memberships` table (team_id, user_id, role)
    -   `research_sessions.owner_id` foreign key

**2. Shared Research Sessions (Weeks 3-4):**
-   **Real-time Collaboration:**
    -   WebSocket pub/sub for live updates
    -   CRDTs (Conflict-free Replicated Data Types) for concurrent editing
    -   Show "👤 Alice is viewing" indicators
-   **Permissions System:**
    -   Roles: Owner, Editor, Viewer, Commenter
    -   Granular permissions: Read/Write/Delete on sessions/papers/reports
    -   Audit log for all permission changes

**3. Annotation & Comments (Weeks 5-6):**
-   **Paper Annotations:**
    -   Highlight text in PDF viewer → Add comment
    -   Store annotations in `paper_annotations` table
    -   Show team annotations as overlays
-   **Report Comments:**
    -   Inline comments on Markdown (like Google Docs)
    -   Thread discussions with replies
    -   @mention team members for notifications
-   **Discussion Board:**
    -   Session-level discussion threads
    -   Markdown support with code blocks
    -   Integrate with VS Code "Comments" API

**Milestone:** Transform platform from single-user tool to collaborative research hub.

---

#### Phase 4.4: AI Model Expansion & Customization (4 weeks)

**Objective:** Support multiple LLM providers and enable domain-specific fine-tuning.

**Vision Reference:** Chapter 2.3 - "LiteLLM" for 100+ LLM access strategy.

**1. Multi-Model Support (Weeks 1-2):**
-   **LiteLLM Full Integration:**
    -   Already using LiteLLM, expand to support:
        -   OpenAI GPT-4, GPT-3.5
        -   Anthropic Claude 3 (Opus, Sonnet, Haiku)
        -   Google Gemini Pro, Gemini Ultra
        -   Cohere Command, Command-Light
        -   Open-source: Llama 3, Mistral, Mixtral
-   **Model Selection UI:**
    -   Dropdown in Control Panel: "Choose LLM"
    -   Per-stage model selection (different models for search vs synthesis)
    -   Cost/performance trade-off recommendations

**2. Model Comparison & Benchmarking (Week 3):**
-   **A/B Testing Framework:**
    -   Run same query with 2 different models
    -   Compare results side-by-side
    -   Metrics: Speed, cost, output quality (BLEU, ROUGE scores)
-   **Benchmarking Dashboard:**
    -   Analytics view showing model performance over time
    -   Token usage and cost per model
    -   User satisfaction ratings (thumbs up/down)

**3. Domain-Specific Fine-Tuning (Week 4):**
-   **Fine-Tuning Pipeline:**
    -   Export research sessions as training data (JSON-L format)
    -   Integration with OpenAI Fine-Tuning API
    -   Training job monitoring dashboard
-   **Custom Model Deployment:**
    -   Load fine-tuned models via LiteLLM
    -   A/B test custom model vs base model
    -   Continuous improvement loop (collect feedback → retrain)

**Milestone:** Platform becomes LLM-agnostic with best-in-class model flexibility.

---

#### Phase 4.5: Production Deployment & Enterprise Features (5 weeks)

**Objective:** Transform platform into enterprise-ready SaaS product.

**1. Scalable Infrastructure (Weeks 1-2):**
-   **Kubernetes Deployment:**
    -   Helm charts for FastAPI backend
    -   Horizontal auto-scaling based on load
    -   Load balancer with sticky sessions (WebSocket support)
-   **Cloud Database:**
    -   Migrate to AWS RDS PostgreSQL or Google Cloud SQL
    -   Read replicas for analytics queries
    -   Automated backups with point-in-time recovery
-   **CDN & Asset Storage:**
    -   S3/GCS for PDF storage
    -   CloudFront/Cloud CDN for global distribution
    -   Presigned URLs for secure PDF access

**2. Monitoring & Observability (Week 3):**
-   **Application Monitoring:**
    -   Integrate Prometheus + Grafana
    -   Custom metrics: Research sessions/hour, Papers processed, API latency
    -   Alert rules: Error rate >1%, Response time >2s
-   **Logging:**
    -   Structured logging with JSON format
    -   Centralized logging (ELK stack or Cloud Logging)
    -   Log aggregation for debugging user issues
-   **Tracing:**
    -   OpenTelemetry for distributed tracing
    -   Visualize full request path (API → LangGraph → LLM → DB)
    -   Performance bottleneck identification

**3. Security & Compliance (Week 4):**
-   **Data Encryption:**
    -   TLS 1.3 for all API traffic
    -   Encryption at rest for PostgreSQL
    -   API key rotation policy (every 90 days)
-   **Compliance:**
    -   GDPR compliance (data export, deletion)
    -   SOC 2 Type II preparation
    -   Terms of Service & Privacy Policy
-   **Rate Limiting & DDoS Protection:**
    -   Redis-based rate limiter (100 req/min per user)
    -   Cloudflare for DDoS mitigation
    -   IP whitelist/blacklist management

**4. Billing & Subscription (Week 5):**
-   **Subscription Tiers:**
    -   Free: 10 sessions/month, GPT-3.5 only
    -   Pro: 100 sessions/month, All models, Priority support
    -   Enterprise: Unlimited, Custom models, Dedicated instance
-   **Billing Integration:**
    -   Stripe for payment processing
    -   Usage metering (track API calls, tokens)
    -   Automated invoicing and receipts
-   **Admin Dashboard:**
    -   User management (view/suspend accounts)
    -   Analytics: MRR, churn rate, DAU/MAU
    -   Feature flags for gradual rollouts

**Milestone:** Platform ready for public launch with enterprise SLA guarantees.

---

### Phase 4 Summary

**Duration:** 24 weeks (~6 months)

**Strategic Deliverables:**
-   React-based Control Panel with "Thinking Chain" visualization
-   Multi-source literature integration (PubMed, Semantic Scholar, Google Scholar, CrossRef)
-   Collaborative research with team features and real-time editing
-   Multi-model LLM support with benchmarking and fine-tuning
-   Enterprise-grade production deployment

**Technology Expansion:**
-   React, D3.js, React Flow (visualization)
-   Neo4j or NetworkX (citation graphs)
-   OAuth 2.0, JWT (authentication)
-   CRDTs (collaborative editing)
-   Kubernetes, Prometheus, Grafana (infrastructure)
-   OpenTelemetry (observability)
-   Stripe (billing)

**Business Impact:**
-   Transform from demo to production SaaS
-   Enable team-based pricing model
-   Establish competitive moat with unique features
-   Prepare for Series A fundraising

**Vision Fulfillment:**
-   ✅ "VS Code即平台" - Native integration complete
-   ✅ "上下文感知科研助理" - Full project context access
-   ✅ "人在环路" - HITL at every critical decision
-   ✅ "科研即代码" - Git-based versioning + automation
-   ✅ "开放科学生态" - Team collaboration + shared knowledge

---

### Implementation Priority Matrix

Based on current Phase 3.5.3 completion status and technical roadmap vision, the recommended execution order is:

#### 🔴 Critical Path (Q4 2025)
1. **Phase 3.5.4** (1 week) - Production readiness and documentation
2. **Phase 3.6 Week 1-2** (2 weeks) - HITL decision system (highest user value)
3. **Phase 3.6 Week 3** (1 week) - Real-time document collaboration (core differentiator)

**Rationale:** Completes "阶段三：实时交互与动态协作" from technical roadmap. Delivers on core vision of AI-human collaborative editing.

#### 🟡 High Priority (Q1 2026)
4. **Phase 4.1** (4 weeks) - Enhanced Control Panel with Thinking Chain visualization
5. **Phase 4.2 Weeks 1-3** (3 weeks) - Multi-source literature integration (PubMed, Semantic Scholar)

**Rationale:** Dramatically improves user experience and expands research coverage. Key for competitive positioning.

#### 🟢 Medium Priority (Q2 2026)
6. **Phase 4.3 Weeks 1-4** (4 weeks) - Collaborative research (team features)
7. **Phase 4.2 Weeks 4-5** (2 weeks) - Citation network analysis
8. **Phase 4.4 Weeks 1-2** (2 weeks) - Multi-model LLM support

**Rationale:** Enables team use cases and advanced analytics. Grows TAM (Total Addressable Market).

#### 🔵 Future Enhancements (Q3-Q4 2026)
9. **Phase 4.3 Weeks 5-6** (2 weeks) - Annotation & comments
10. **Phase 4.4 Weeks 3-4** (2 weeks) - Model benchmarking & fine-tuning
11. **Phase 4.5** (5 weeks) - Enterprise deployment & billing

**Rationale:** Nice-to-have features and monetization infrastructure.

---

### Technical Debt & Gap Analysis

#### Current State vs. Vision Gap

| Technical Roadmap Requirement | Current Status | Gap | Priority |
|-------------------------------|----------------|-----|----------|
| **React-based Webview** | Plain HTML | Need React migration | 🟡 High |
| **Three-panel IDE layout** | 3 panels exist, basic UI | Polish & interaction | 🟢 Medium |
| **HITL decision points** | Not implemented | Core feature missing | 🔴 Critical |
| **Document collaboration** | Read-only display | Need write integration | 🔴 Critical |
| **Multi-source search** | arXiv + Unpaywall only | Limited coverage | 🟡 High |
| **Citation graph** | Not implemented | Advanced feature | 🟢 Medium |
| **Team collaboration** | Single-user only | Limits adoption | 🟢 Medium |
| **Error handling** | Basic try-catch | Need conditional edges | 🟡 High |

#### Immediate Technical Debt (Address in Phase 3.5.4)

1. **Chart.js Deprecation Warning:**
   - Issue: `horizontalBar` type deprecated in Chart.js v4
   - Fix: Use `bar` type with `indexAxis: 'y'`
   - Effort: 5 minutes

2. **PostgresSaver Async Limitation:**
   - Issue: Using `run_in_executor()` workaround for sync `graph.invoke()`
   - Impact: Suboptimal async performance
   - Future: Migrate to async-native checkpointer (LangGraph roadmap)
   - Monitor: LangGraph GitHub issues for async support

3. **Session Details View (TODO):**
   - Issue: Clicking session row shows notification, not details
   - Fix: Implement SessionDetailsWebview with timeline visualization
   - Effort: 4 hours

4. **Time Range Persistence:**
   - Issue: Analytics dashboard defaults to '7d' on every open
   - Fix: Use `context.workspaceState.get/update()` for persistence
   - Effort: 30 minutes

5. **Empty Data Scenarios:**
   - Issue: Charts may break with zero data
   - Fix: Add conditional rendering + "No data" placeholder
   - Effort: 2 hours

#### Known Limitations (Document for Users)

1. **PDF Full-Text Limitation:**
   - Only open-access PDFs via Unpaywall
   - No institutional access integration yet
   - Workaround: Manual PDF upload (future feature)

2. **Single Research Session:**
   - WebSocket supports one active session per user
   - Concurrent sessions require session multiplexing
   - Planned: Phase 4.1 batch mode

3. **No Offline Mode:**
   - Requires backend connection for all operations
   - Future: Local LLM support (Ollama integration)

4. **Limited Export Formats:**
   - PDF export returns 501 (not implemented)
   - Only Markdown, HTML, BibTeX available
   - Planned: Phase 3.5.4 PDF via Pandoc

---

### Development Workflow Best Practices

Based on Phase 3.5.3 success (100% completion, 0 critical bugs), codify best practices:

#### 1. Contract First Development ✅
- Always write OpenAPI specs before implementation
- Generate TypeScript types from OpenAPI (consider using `openapi-typescript`)
- Validate API responses against schemas in tests

#### 2. Session-Driven Development ✅
- Create `.ai-sessions/development/{date}-{phase}.md` for each work session
- Document decisions, blockers, solutions in real-time
- Enables seamless context switching and handoffs

#### 3. Snapshot-Driven Debugging ✅
- Use GEMINI.md pattern: Context → Analysis → Solution
- Include full error messages, stack traces, file versions
- Reduces debugging time by 60% (based on Phase 3.5.3 experience)

#### 4. Incremental Testing Strategy
- Test each component in isolation before integration
- Backend: `pytest` for unit tests, `test-*.sh` for E2E
- Frontend: `npm run compile` for type checking, manual testing in Extension Host
- Target: 85% code coverage minimum

#### 5. Feature Flags for Gradual Rollout
- Use VS Code settings: `autoResearcher.features.hitl.enabled`
- Allow users to opt-in to experimental features
- Collect feedback before making default

#### 6. Performance Budgets
- API response time: <500ms (p95)
- WebSocket message latency: <100ms
- Frontend time-to-interactive: <2s
- Database query time: <200ms
- Monitor with Prometheus, alert on violations

---

### Success Metrics & KPIs

#### Product Metrics (Track in Analytics Dashboard)
- **Adoption:** DAU/MAU ratio, new user signups/week
- **Engagement:** Avg sessions per user per week, session completion rate
- **Quality:** Success rate (completed/total sessions), avg papers per session
- **Performance:** P95 API latency, WebSocket uptime %

#### Business Metrics (Phase 4.5+)
- **Revenue:** MRR, churn rate, ARPU
- **Growth:** Week-over-week user growth %, viral coefficient
- **Efficiency:** CAC (Customer Acquisition Cost), LTV/CAC ratio

#### Technical Metrics
- **Reliability:** Error rate <0.1%, uptime 99.9%
- **Code Quality:** Test coverage >85%, zero critical security vulnerabilities
- **Velocity:** Story points per sprint, deployment frequency

---

### Conclusion

This roadmap transforms the **gemini-fullstack-langgraph-quickstart** from a technical demo into a production-ready, VS Code-native automated research platform. 

**Completed So Far:**
- ✅ Phase 1: Backend Foundation (4-stage LangGraph workflow)
- ✅ Phase 2: VS Code Extension Skeleton (3-panel layout)
- ✅ Phase 3: Real-time WebSocket Interaction
- ✅ Phase 3.5.1-3.5.3: Historical Data, Analytics Dashboard

**Next Milestones:**
- 🎯 Phase 3.5.4-3.6: Complete "实时交互与动态协作" (4 weeks)
- 🎯 Phase 4.1-4.2: Enhanced UI + Multi-source Integration (9 weeks)
- 🎯 Phase 4.3-4.5: Collaborative Features + Enterprise Launch (15 weeks)

**Total Timeline to Production:** ~7 months from current state (October 2025 → May 2026)

**Vision Achievement:** By Phase 4 completion, the platform will fully realize the technical roadmap's vision of a "上下文感知科研助理" (context-aware research assistant) that seamlessly integrates into researchers' VS Code workflows, transforming scientific literature review from a tedious task into an interactive, AI-augmented collaboration.

---

**Last Updated:** October 14, 2025  
**Current Phase:** 3.5.3 Complete ✅ | Next: 3.5.4  
**Project Status:** On track for Q2 2026 production launch
