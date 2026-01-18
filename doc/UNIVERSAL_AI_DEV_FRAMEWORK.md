    # Universal AI-Assisted Development Framework

    **Version**: 1.0  
    **Last Updated**: 2025-10-29

    This document provides a generalized, project-agnostic framework for AI-assisted software development. It can be adapted to any project by customizing the placeholders and examples to your specific technology stack and requirements.

    ---

    ## Table of Contents

    1. [Core Philosophy](#1-core-philosophy)
    2. [Session-Driven Workflow](#2-session-driven-workflow)
    3. [File Organization](#3-file-organization)
    4. [Development Principles](#4-development-principles)
    5. [Testing Strategy](#5-testing-strategy)
    6. [Environment Setup](#6-environment-setup)
    7. [Implementation Guide](#7-implementation-guide)

    ---

    ## 1. Core Philosophy

    ### Everything is a Session

    All development work—whether feature implementation or bug fixing—is treated as a **session**: a traceable, self-contained unit of work from goal definition to completion.

    **Key Benefits:**
    - **Unified Process**: Same workflow for development and debugging
    - **Complete Traceability**: Full history of decisions, attempts, and outcomes
    - **Knowledge Transfer**: Easy onboarding for new team members (human or AI)
    - **Regression Prevention**: Clear record of what changed and why

    ### Principle 0: Contract First

    For any work involving multiple components (e.g., frontend/backend, service-to-service), define the **interface contract** before implementation.

    **Why?**
    - Enables parallel development
    - Prevents integration errors
    - Serves as executable documentation
    - Provides clear acceptance criteria

    **How?**
    - Use OpenAPI/Swagger for REST APIs
    - Use Protocol Buffers for gRPC
    - Use GraphQL schemas for GraphQL APIs
    - Use TypeScript interfaces for internal modules

    ---

    ## 2. Session-Driven Workflow

    ### Session Lifecycle

    Every session follows four standard phases:

    ```
    ┌─────────────────┐
    │ Initialization  │ Define goal, analyze, plan
    └────────┬────────┘
            │
            ▼
    ┌─────────────────┐
    │ Execution       │ Implement steps, verify each
    └────────┬────────┘
            │
            ▼ (if verification fails)
    ┌─────────────────┐
    │ Debug State     │ Diagnose, fix, re-verify
    └────────┬────────┘
            │
            ▼ (when goal achieved)
    ┌─────────────────┐
    │ Completion      │ Final verification, summary
    └─────────────────┘
    ```

    ### Phase 1: Initialization

    **Actions:**
    1. Create session file in appropriate directory
    2. Define **The Goal** (clear, measurable success criteria)
    3. Document current state analysis
    4. Create step-by-step implementation plan
    5. **Define or verify API contract** (if multi-component work)

    **Template:**
    ```markdown
    # Session: [Brief Description]

    **Date**: YYYY-MM-DD HH:mm UTC
    **Category**: [development|debugging]
    **Phase/Milestone**: [e.g., Phase 3.6, Sprint 5]

    ## The Goal

    [Clear, testable objective. Examples:]
    - Make `tests/features/user_authentication.feature` pass
    - Fix failing E2E test in `test_payment_flow.py`
    - Implement API endpoint `/api/v1/users` per OpenAPI spec

    ## Initial Analysis

    ### Current State
    - [What exists now]
    - [Relevant files/components]
    - [Dependencies]

    ### Gap Analysis
    - [What's missing]
    - [What needs to change]

    ## Implementation Plan

    - [ ] **Step 1**: [Action with verification method]
    - [ ] **Step 2**: [Action with verification method]
    - [ ] **Step 3**: [Action with verification method]
    ...

    ## Contract Definition (if applicable)

    **API Endpoint**: `POST /api/v1/resource`
    **Request Schema**: [Link to OpenAPI/schema file]
    **Response Schema**: [Link to OpenAPI/schema file]
    **Contract Status**: ✅ Reviewed | ⏳ Pending Review
    ```

    ### Phase 2: Iterative Execution

    For each step in the plan:

    **Template:**
    ```markdown
    ---
    ### [Step N: Brief Description]

    **Time**: HH:mm UTC

    #### Action
    [Describe what you're doing]

    #### Tool Calls
    ```bash
    # Command used or tool invoked
    make test TEST_FILE=path/to/test.py
    ```

    #### Verification
    ```
    [Command used to verify]
    ```

    **Result**: 
    ```
    [Paste relevant output]
    ```

    **Status**: ✅ Success | ❌ Failed

    [If failed, trigger Debug State below]
    ```

    ### Phase 3: Debug State (Conditional)

    Triggered when verification fails. Stay in this loop until the step succeeds.

    **Template:**
    ```markdown
    #### 🐛 Debugging Snapshot

    ##### Error
    ```
    [Full error message, stack trace, logs]
    ```

    ##### Hypothesis
    [Your theory about the root cause]

    ##### Fix Attempt
    ```bash
    # Commands or code changes made
    ```

    ##### Verification
    ```bash
    # Re-run the failing test
    ```

    **Result**:
    ```
    [Output]
    ```

    **Status**: ✅ Fixed | ❌ Still Failing

    [If still failing, add another Debugging Snapshot]
    ```

    ### Phase 4: Completion

    **Template:**
    ```markdown
    ---
    ## Session Complete

    **End Time**: YYYY-MM-DD HH:mm UTC
    **Duration**: [X hours]

    ### Final Verification
    ```bash
    # Command that proves the goal is met
    ```

    **Result**: ✅ All acceptance criteria met

    ### Summary
    - **Completed**: [List of deliverables]
    - **Modified Files**: [List with brief descriptions]
    - **Key Learnings**: [Any insights for future work]

    ### Next Steps (Optional)
    - [ ] Follow-up task 1
    - [ ] Follow-up task 2

    ### Commit Information (Optional)
    ```bash
    git status
    git diff --stat
    ```

    **Proposed Commit Message**:
    ```
    [type]: [subject]

    [body]

    Closes #[issue-number]
    ```
    ```

    ---

    ## 3. File Organization

    ### Directory Structure

    ```
    <project-root>/
    ├── .ai-sessions/
    │   ├── README.md                    # Index of all sessions
    │   ├── development/                 # Feature development sessions
    │   │   ├── README.md               # Development session index
    │   │   └── YYYY-MM-DD-HHmm-phase-X.Y-category-description.md
    │   └── debugging/                   # Standalone bug fix sessions
    │       ├── README.md               # Debug session index
    │       └── YYYY-MM-DD-HHmm-phase-X.Y-debug-description.md
    ├── docs/
    │   ├── WORKFLOW_STRATEGY.md        # This workflow (project-specific)
    │   └── TESTING.md                  # Testing guide
    ├── [your source code directories]
    └── [your test directories]
    ```

    ### Session File Naming Convention

    **Standard Format**:
    ```
    YYYY-MM-DD-HHmm-phase-X.Y-<category>-<description>.md
    ```

    **Components**:
    1. **DateTime**: `YYYY-MM-DD-HHmm` (ISO 8601, 24-hour, UTC+0)
    2. **Phase/Milestone**: `phase-X.Y` or `sprint-N` or `v1.2.3`
    3. **Category**: One of the standard categories below
    4. **Description**: 1-5 words in kebab-case

    **Standard Categories**:

    | Category | Purpose | Frequency |
    |----------|---------|-----------|
    | `plan` | Implementation/sprint planning | 1-2 per phase |
    | `progress` | Daily/incremental work logs | 1-3 per day |
    | `report` | Milestone completion reports | 1 per milestone |
    | `test` | Test execution & coverage reports | As needed |
    | `debug` | Bug investigation & fixes | As needed |
    | `analysis` | Technical deep-dives, retrospectives | 1-2 per week |
    | `summary` | Phase/sprint summaries | 1 per phase |
    | `reference` | Quick reference guides | 1-2 per phase |

    **Examples**:
    ```
    2025-10-29-0900-sprint-5-progress-day1-auth-module.md
    2025-10-29-1430-v1.2.3-test-e2e-payment-flow.md
    2025-10-29-1600-sprint-5-debug-database-connection.md
    2025-10-30-1000-sprint-5-analysis-performance-bottleneck.md
    ```

    **Session Index** (`.ai-sessions/README.md`):
    ```markdown
    # AI Session Index

    ## Current Phase: [Phase/Sprint Name]

    ### Quick Links
    - [Current Sprint Plan](development/YYYY-MM-DD-sprint-N-plan.md)
    - [Latest Progress](development/YYYY-MM-DD-HHmm-sprint-N-progress-dayX.md)
    - [Active Debugging](debugging/YYYY-MM-DD-HHmm-sprint-N-debug-issue.md)

    ## Sessions by Category

    ### Development
    - [2025-10-29-0900-sprint-5-progress-day1-auth-module.md](development/2025-10-29-0900-sprint-5-progress-day1-auth-module.md)
    - ...

    ### Debugging
    - [2025-10-29-1600-sprint-5-debug-database-connection.md](debugging/2025-10-29-1600-sprint-5-debug-database-connection.md)
    - ...

    ## Sessions by Phase/Sprint

    ### Sprint 5 (2025-10-28 ~ 2025-11-10)
    - Plan: [sprint-5-plan.md](development/2025-10-28-sprint-5-plan.md)
    - Progress: Day 1, Day 2, ...
    - Completion: [pending]
    ```

    ---

    ## 4. Development Principles

    ### A. Tool Parameter Precision

    **Rule**: Always verify tool/function parameter names against documentation before invocation.

    **Why**: Prevents wasted iterations due to typos (e.g., `newContent` vs `new_string`).

    **Practice**:
    1. Check function signature before calling
    2. Use autocomplete/IDE hints
    3. Reference API documentation

    ### B. Snapshot-Driven Development

    **Rule**: Update the session snapshot **immediately after** completing each step.

    **Workflow**:
    1. Identify current step from session file
    2. Execute the step
    3. **Update session file** with results
    4. Only then proceed to next step

    **Why**: 
    - Creates real-time audit trail
    - Prevents loss of context if work is interrupted
    - Enables other developers to pick up exactly where you left off

    ### C. Verification-First Mindset

    **Rule**: Every implementation step must have a corresponding verification command.

    **Examples**:
    ```bash
    # Unit tests
    npm test -- src/utils.test.ts
    pytest tests/unit/test_auth.py

    # Integration tests
    make test-integration

    # E2E tests
    npm run test:e2e
    ./scripts/e2e_test.sh

    # Linting
    npm run lint
    flake8 src/

    # Type checking
    npm run type-check
    mypy src/
    ```

    **Practice**: Define verification command in the plan, execute after implementation.

    ### D. Incremental Commits

    **Rule**: Commit after each successfully completed and verified step.

    **Benefits**:
    - Easy to revert if needed
    - Clear git history
    - Facilitates code review

    **Commit Message Format**:
    ```
    <type>(<scope>): <subject>

    <body>

    <footer>
    ```

    **Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `style`

    ---

    ## 5. Testing Strategy

    ### Test Pyramid

    ```
            ┌───────────┐
            │    E2E    │  (Few, slow, high value)
            ├───────────┤
            │Integration│  (More, medium speed)
            ├───────────┤
            │   Unit    │  (Many, fast, focused)
            └───────────┘
    ```

    ### Testing Checklist

    For every feature or bug fix:

    - [ ] **Unit Tests**: Test individual functions/classes in isolation
    - [ ] **Integration Tests**: Test component interactions
    - [ ] **E2E Tests**: Test complete user workflows
    - [ ] **Regression Tests**: Ensure old features still work
    - [ ] **Golden File/Snapshot Tests**: Compare output against known-good baseline (if applicable)

    ### Golden File Testing (Regression Prevention)

    For complex outputs (e.g., API responses, generated files), use snapshot testing:

    **Workflow**:
    1. Run the feature and capture output
    2. Manually verify the output is correct
    3. Save output as "golden file" in `tests/snapshots/`
    4. Future runs compare against this baseline
    5. Update golden file only when changes are intentional

    **Example**:
    ```bash
    # Generate current output
    ./run_feature.sh > /tmp/current_output.json

    # Compare to golden file
    diff tests/snapshots/expected_output.json /tmp/current_output.json

    # If intentional change, update golden file
    cp /tmp/current_output.json tests/snapshots/expected_output.json
    ```

    ---

    ## 6. Environment Setup

    ### Containerized Development (Recommended)

    **Goal**: Ensure all developers (human and AI) work in identical environments.

    **Tools**:
    - **Docker/Docker Compose**: Define runtime environment
    - **Dev Containers (VS Code)**: Integrated development environment
    - **.devcontainer/**: Configuration for VS Code Dev Containers

    **Benefits**:
    - No "works on my machine" issues
    - Fast onboarding
    - Consistent CI/CD
    - Easy to switch contexts

    **Structure**:
    ```
    .devcontainer/
    ├── devcontainer.json          # Main dev container config
    ├── devcontainer.backend.json  # Backend-specific config
    ├── devcontainer.frontend.json # Frontend-specific config
    └── Dockerfile.dev            # Development image
    ```

    ### Environment Variables

    **Rule**: Never hardcode secrets. Use environment variables.

    **Setup**:
    1. Create `.env.example` with placeholder values
    2. Developer copies to `.env` and fills in real values
    3. Add `.env` to `.gitignore`
    4. Load `.env` in development environment

    **Example `.env.example`**:
    ```bash
    # Database
    DATABASE_URL=postgresql://user:password@localhost:5432/dbname

    # API Keys
    API_KEY_SERVICE_A=your_key_here
    API_KEY_SERVICE_B=your_key_here

    # Environment
    NODE_ENV=development
    DEBUG=true
    ```

    ---

    ## 7. Implementation Guide

    ### Step-by-Step Adoption

    #### Week 1: Setup

    1. **Create `.ai-sessions/` structure**
    ```bash
    mkdir -p .ai-sessions/{development,debugging}
    ```

    2. **Create session index files**
    - `.ai-sessions/README.md`
    - `.ai-sessions/development/README.md`
    - `.ai-sessions/debugging/README.md`

    3. **Create project-specific workflow doc**
    - Copy this template to `docs/WORKFLOW_STRATEGY.md`
    - Customize for your project (stack, tools, conventions)

    4. **Create testing guide**
    - Document all test commands in `docs/TESTING.md`
    - Include setup, execution, and interpretation

    #### Week 2-3: Pilot

    5. **Choose a pilot feature**
    - Select a small, well-defined feature
    - Use it to test the session-driven workflow

    6. **Create first session file**
    - Follow the templates exactly
    - Record every step, even if it seems obvious

    7. **Review and iterate**
    - After completion, review the session file
    - Identify what worked and what needs adjustment

    #### Week 4+: Scale

    8. **Team training**
    - Share completed session examples
    - Conduct walkthrough of the workflow

    9. **Integrate with CI/CD**
    - Add snapshot tests to CI pipeline
    - Require session file for all PRs

    10. **Continuous improvement**
        - Collect feedback
        - Update templates
        - Share learnings

    ---

    ## Customization Checklist

    When adapting this framework to your project, customize:

    - [ ] **Project name and description** in main doc
    - [ ] **Technology stack** (languages, frameworks)
    - [ ] **Phase/milestone naming** (Phase X.Y vs Sprint N vs vX.Y.Z)
    - [ ] **Testing commands** (project-specific test runners)
    - [ ] **Contract format** (OpenAPI vs Protobuf vs GraphQL)
    - [ ] **Directory structure** (match your project layout)
    - [ ] **Environment setup** (Docker vs native vs other)
    - [ ] **Commit message conventions** (match team standards)
    - [ ] **Code review process** (integrate session files into reviews)

    ---

    ## Appendix: Quick Reference

    ### Session File Template (Minimal)

    ```markdown
    # Session: [Title]

    **Goal**: [One sentence objective]
    **Date**: YYYY-MM-DD HH:mm UTC

    ## Plan
    - [ ] Step 1
    - [ ] Step 2

    ---
    ### Step 1: [Description]
    **Action**: [What I'm doing]
    **Verification**: `command here`
    **Status**: ✅ | ❌

    ---
    ## Complete
    **Result**: [Success/Failure with evidence]
    ```

    ### Common Verification Commands

    ```bash
    # Run all tests
    make test

    # Run specific test file
    make test TEST=path/to/test

    # Run E2E tests
    make test-e2e

    # Lint
    make lint

    # Type check
    make type-check

    # Build
    make build

    # Start dev server
    make dev
    ```

    ### Debugging Snapshot Template (Minimal)

    ```markdown
    #### 🐛 Debug Snapshot

    **Error**: [Paste error]
    **Hypothesis**: [Theory]
    **Fix**: [What I changed]
    **Verification**: `command`
    **Status**: ✅ Fixed | ❌ Still failing
    ```

    ---

    ## License

    This framework is released under [MIT License](LICENSE). Feel free to adapt and use in your projects.

    ## Acknowledgments

    This framework is derived from the GEMINI methodology developed for the Auto-Researcher project. It synthesizes best practices from:
    - Test-Driven Development (TDD)
    - Behavior-Driven Development (BDD)
    - Snapshot Testing
    - DevOps observability practices
    - AI-assisted software engineering research

    ---

    **Document Version History**:
    - v1.0 (2025-10-29): Initial generalized framework
