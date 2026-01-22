# AI-Native Development Sessions

This directory contains structured session records for the AI-Native development workflow following the MPA (MetaGPT+PydanticAI+Aider) architecture.

## Purpose
- Document architectural decisions and design rationale
- Track development progress and implementation details
- Record debugging sessions and problem-solving processes
- Maintain historical context for future development
- Standardize AI-assisted development workflow

## Directory Structure

```
.ai-sessions/
├── README.md                          # This file
├── architecture/                      # Architectural design sessions
│   ├── template-architecture-session.md
│   └── [date]-[topic]-design.md
├── development/                       # Development implementation sessions
│   ├── phase-4.2/                     # Phase-specific development
│   ├── phase-3.5.4/
│   ├── phase-3.6/
│   └── [other-phases]/
├── debugging/                         # Debugging and troubleshooting sessions
│   ├── template-debugging-session.md
│   └── [date]-[issue]-debug.md
├── templates/                         # Session templates
│   ├── architecture-session-template.md
│   ├── development-session-template.md
│   └── debugging-session-template.md
└── conventions/                       # Development conventions and standards
    ├── mpa-workflow.md
    ├── testing-standards.md
    └── documentation-standards.md
```

## Session Types

### 1. Architecture Sessions
- **Purpose**: High-level design decisions, protocol definitions, schema design
- **Location**: `architecture/`
- **Template**: `templates/architecture-session-template.md`

### 2. Development Sessions
- **Purpose**: Implementation details, code changes, feature development
- **Location**: `development/[phase]/`
- **Template**: `templates/development-session-template.md`

### 3. Debugging Sessions
- **Purpose**: Problem diagnosis, error resolution, troubleshooting
- **Location**: `debugging/`
- **Template**: `templates/debugging-session-template.md`

## Session Documentation Standards

### Required Elements
Each session document must include:

1. **Session Header**
   - Date (YYYY-MM-DD format)
   - Architect/Developer name
   - Phase and status
   - Clear goal statement

2. **Context Section**
   - Related architecture documents
   - Development standards referenced
   - Tools and technologies used

3. **Content Sections**
   - Design decisions (for architecture sessions)
   - Implementation details (for development sessions)
   - Problem analysis (for debugging sessions)

4. **Artifacts**
   - Files created or modified
   - Code snippets
   - Test results

5. **Results and Next Steps**
   - Outcomes and learnings
   - Next actions
   - Follow-up requirements

### Naming Convention
- Architecture: `YYYY-MM-DD-[topic]-design.md`
- Development: `YYYY-MM-DD-[phase]-[topic]-implementation.md`
- Debugging: `YYYY-MM-DD-[issue]-debug.md`

## MPA Workflow Integration

### Role Definitions
- **Architect**: GitHub Copilot - Designs contracts, protocols, schemas
- **Builder**: Aider + Qwen Max - Implements adapters, writes tests
- **Inspector**: Aider - Validates implementation, runs tests

### Workflow Process
1. **Architect Phase**: Design contracts and protocols in domain layer
2. **Builder Phase**: Implement adapters in infrastructure layer
3. **Inspector Phase**: Run tests, validate implementation
4. **Documentation Phase**: Record session, update documentation

## Quality Standards

### Code Quality
- Follow hexagonal architecture principles
- Use absolute imports (`from agent.domain...`)
- Implement comprehensive testing
- Maintain backward compatibility

### Documentation Quality
- Update all related documents
- Include test scenarios in protocol docstrings
- Maintain consistency with .clinerules
- Record decisions and rationale

### Testing Standards
- Mock all external dependencies
- Isolate environment variables
- Achieve >85% test coverage
- Include integration and E2E tests

## Related Documents
- [.clinerules](../.clinerules) - AI-Native development rules
- [ROADMAP.md](../ROADMAP.md) - Project roadmap and phases
- [DEVELOPMENT_STATUS.md](../DEVELOPMENT_STATUS.md) - Current development status
- [TESTING.md](../TESTING.md) - Testing methodology

---

**Last Updated:** 2026-01-22  
**Maintainer:** Project Architect  
**Status:** Active
