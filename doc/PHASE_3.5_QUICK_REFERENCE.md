# Phase 3.5 Quick Reference Guide

**Historical Data Management & Advanced Analytics**

---

## 📊 Overview

Phase 3.5 transforms Auto-Researcher from a single-task tool into a comprehensive research knowledge management system with full historical tracking, version control, and analytics.

**Duration:** 7 weeks (4 sub-phases)  
**New Endpoints:** 16 API endpoints  
**New Models:** 4 data entities  
**Enhanced Views:** 4 UI components  

---

## 🗂️ Data Architecture

### Core Entities

```
ResearchSession (研究会话)
├── session_id: UUID
├── research_topic: string
├── status: pending | in_progress | completed | failed
├── created_at, updated_at, completed_at: datetime
└── metadata: {total_papers, total_queries, loop_count, is_sufficient}

Paper (文献)
├── paper_id: UUID
├── session_id: UUID (FK)
├── title, authors[], abstract, summary: string
├── doi, url, arxiv_id: string (nullable)
├── published_date, collected_at: datetime
├── source: arxiv | pubmed | semantic_scholar | manual
├── tags[], relevance_score: array, float

Report (报告)
├── report_id: UUID
├── session_id: UUID (FK)
├── version: integer
├── content: string (Markdown)
├── word_count, paper_count: integer
├── generated_at: datetime
└── metadata: {structure, citations[]}

SessionEvent (会话事件)
├── event_id: UUID
├── session_id: UUID (FK)
├── event_type: session_created | query_generated | search_executed | 
│                paper_collected | report_generated | session_completed
├── timestamp: datetime
└── details: object (dynamic)
```

---

## 🛠️ API Endpoints (16 Total)

### Session Management (5 endpoints)
```http
POST   /sessions                       # Create new session
GET    /sessions                       # List sessions (filterable)
GET    /sessions/{session_id}          # Get session details
DELETE /sessions/{session_id}          # Delete/archive session
GET    /sessions/{session_id}/events   # Get session timeline
```

### Paper Management (3 endpoints)
```http
GET    /papers                         # List all papers (advanced filters)
GET    /papers/{paper_id}              # Get paper details
GET    /papers/export                  # Export to BibTeX/RIS/JSON
```

### Report Management (5 endpoints)
```http
GET    /reports                        # List all reports
GET    /reports/{report_id}            # Get report details
GET    /sessions/{id}/reports/latest   # Get latest report for session
GET    /reports/{id1}/compare/{id2}    # Compare two versions
GET    /reports/{report_id}/export     # Export to MD/HTML/PDF
```

### Statistics & Analytics (4 endpoints)
```http
GET    /stats/global                   # Overall statistics
GET    /stats/trends                   # Time-series activity data
GET    /stats/keywords                 # Keyword frequency analysis
GET    /stats/authors                  # Author network data
```

---

## 🎨 Frontend Components

### 1. Sessions TreeView (新增)
**Purpose:** Display and manage all research sessions

**Features:**
- Hierarchical view: Session → Papers/Reports/Events
- Filtering: by status, date range
- Context menu: View Details, Delete, Export
- Session switching/navigation

**Data Source:** `GET /sessions`

---

### 2. Enhanced Library TreeView (重构)
**Purpose:** Historical literature management

**Current → Enhanced:**
- ❌ Single session → ✅ Multi-session aggregation
- ❌ Basic list → ✅ Multi-dimensional grouping (session/source/date/author)
- ❌ Limited metadata → ✅ Full metadata + tags + relevance
- ❌ No export → ✅ Export to BibTeX/RIS/JSON

**Features:**
- Advanced filtering and search
- Paper detail webview (full metadata)
- Context menu: Export, View Details, Open URL, Copy Citation

**Data Source:** `GET /papers`

---

### 3. Enhanced Documents TreeView (重构)
**Purpose:** Report version history management

**Current → Enhanced:**
- ❌ Single report → ✅ All historical reports
- ❌ No versioning → ✅ Version tracking with metadata
- ❌ Plain text → ✅ Structured Markdown rendering
- ❌ No comparison → ✅ Version diff comparison

**Features:**
- Grouped by session with version indicators
- Report detail webview (Markdown + syntax highlighting)
- Context menu: Export, Compare Versions, View Session

**Data Source:** `GET /reports`

---

### 4. Analytics Dashboard (新增)
**Purpose:** Research insights and trend visualization

**Visualizations:**
- 📈 Research activity timeline (line chart)
- 📊 Paper source distribution (pie chart)
- ☁️ Keyword cloud (word frequency)
- 🕸️ Author network graph (future: D3.js)

**Metrics:**
- Total papers, reports, sessions
- Average papers per session
- Research velocity (papers/week)
- Top keywords and authors

**Data Source:** `GET /stats/*`

---

## 📅 Implementation Timeline

### Week 1-2: Phase 3.5.1 - Database Foundation ⏳
**Focus:** Data persistence infrastructure

- PostgreSQL schema design (4 tables)
- SQLAlchemy models + CRUD layer
- Session management API (5 endpoints)
- LangGraph PostgresSaver integration
- Auto-persistence during research workflow

**Deliverable:** M1 - Session management operational

---

### Week 3-4: Phase 3.5.2 - Literature & Reports ⏳
**Focus:** Historical data display

- Paper management API (3 endpoints)
- Report management API (5 endpoints)
- Enhanced Library TreeView
- Enhanced Documents TreeView
- Export functionality (multiple formats)

**Deliverable:** M2 - Complete historical data display

---

### Week 5-6: Phase 3.5.3 - Analytics ⏳
**Focus:** Advanced features and insights

- Statistics API (4 endpoints)
- Analytics Dashboard webview
- Chart.js integration
- Report version comparison
- Session timeline visualization

**Deliverable:** M3 - Analytics operational

---

### Week 7: Phase 3.5.4 - Production Ready ⏳
**Focus:** Optimization and polish

- Performance tuning (DB indexing, caching)
- UX improvements (loading states, error handling)
- Complete documentation update
- Test coverage > 85%
- E2E testing

**Deliverable:** M4 - Production-ready system

---

## 🧪 Testing Strategy

### Backend Testing
```bash
# Unit tests for data models
pytest backend/tests/test_models.py

# API endpoint tests
pytest backend/tests/test_sessions_api.py
pytest backend/tests/test_papers_api.py
pytest backend/tests/test_reports_api.py
pytest backend/tests/test_stats_api.py

# Integration tests
pytest backend/tests/test_integration.py

# Target: >85% coverage
pytest --cov=backend/src --cov-report=html
```

### Frontend Testing
```bash
# TreeView provider tests
npm test -- SessionsProvider.test.ts
npm test -- AssetLibraryProvider.test.ts
npm test -- ManuscriptProvider.test.ts

# API client tests
npm test -- api.test.ts

# Webview tests
npm test -- AnalyticsDashboard.test.ts

# Target: >80% coverage
npm test -- --coverage
```

### E2E Testing
```bash
# Complete workflow with historical data
make test-e2e-docker TOPIC="Multi-session research test"

# Verify session persistence
# Verify paper collection across sessions
# Verify report versioning
# Verify analytics accuracy
```

---

## 📦 Dependencies

### Backend (New)
```toml
# pyproject.toml additions
sqlalchemy = "^2.0.0"
alembic = "^1.12.0"
langgraph-checkpoint-postgres = "^1.0.0"
bibtexparser = "^1.4.0"
weasyprint = "^60.0"  # For PDF export
redis = "^5.0.0"  # For caching (Phase 3.5.4)
```

### Frontend (New)
```json
// package.json additions
{
  "chart.js": "^4.4.0",
  "react-chartjs-2": "^5.2.0",
  "marked": "^11.0.0",
  "highlight.js": "^11.9.0",
  "diff2html": "^3.4.0"
}
```

---

## 🗄️ Database Schema

### Migration Commands
```bash
# Initialize Alembic
cd backend
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Add Phase 3.5 tables"

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Key Indexes
```sql
-- Sessions
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);

-- Papers
CREATE INDEX idx_papers_session_id ON papers(session_id);
CREATE INDEX idx_papers_source ON papers(source);
CREATE INDEX idx_papers_collected_at ON papers(collected_at);
CREATE INDEX idx_papers_title_fts ON papers USING gin(to_tsvector('english', title));

-- Reports
CREATE INDEX idx_reports_session_id ON reports(session_id);
CREATE INDEX idx_reports_generated_at ON reports(generated_at);

-- Events
CREATE INDEX idx_events_session_id ON session_events(session_id);
CREATE INDEX idx_events_timestamp ON session_events(timestamp);
```

---

## 🔗 Documentation References

- **Roadmap:** [ROADMAP.md](../ROADMAP.md#phase-35-historical-data-management-and-advanced-analytics-in-progress)
- **Progress Tracking:** [DEVELOPMENT_STATUS.md](../DEVELOPMENT_STATUS.md#phase-35-historical-data-management--in-planning)
- **Detailed Planning:** [.ai-sessions/development/2025-10-12-enhance-library-document-display.md](../.ai-sessions/development/2025-10-12-enhance-library-document-display.md)
- **API Contract:** [openapi.yaml](../openapi.yaml) (will be updated in Phase 3.5.4)
- **Development Workflow:** [doc/WORKFLOW_STRATEGY.md](../doc/WORKFLOW_STRATEGY.md)

---

## 🚀 Getting Started (When Ready)

### 1. Review and Confirm
- Read full planning document
- Review API endpoint specifications
- Validate UI/UX requirements

### 2. Create Feature Branch
```bash
git checkout -b feature/phase-3.5-historical-data-management
```

### 3. Start Phase 3.5.1
- Follow DEVELOPMENT_STATUS.md checklist
- Create session log: `.ai-sessions/development/2025-10-XX-phase-3.5.1-database-foundation.md`
- Begin with database schema design

### 4. Continuous Integration
- Update DEVELOPMENT_STATUS.md weekly
- Mark completed tasks with ✅
- Document issues and solutions in session logs

---

**Status:** 📋 Planning complete, awaiting implementation approval

**Next Action:** User confirmation to begin Phase 3.5.1 implementation
