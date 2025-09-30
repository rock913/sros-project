# Core Development Workflow (AI-Assisted)

This document outlines the standardized development workflow for this project. All contributors, **including AI assistants**, must strictly adhere to these guidelines. Our goal is to create a consistent, high-quality codebase by following a Document-Test-Driven Development (DTDD) model.

## 1. Development Philosophy: Document-Test-Driven Development (DTDD)

The DTDD workflow mandates the following sequence for all new features or significant refactors:

1.  **Define the Contract (Doc-First)**: Before writing any implementation code, define the public API for the new functionality. This is done using language-specific features like TypeScript `interfaces` or Python `abstract base classes`. This contract must be thoroughly documented.
2.  **Write the Tests (Test-as-Specification)**: Based on the contract, write a comprehensive suite of tests that cover all success and failure scenarios described in the documentation. These tests should fail initially.
3.  **Implement the Code (Implement-to-Pass)**: Write the implementation code with the sole purpose of making the tests pass.

This approach ensures that we have a clear specification, a safety net for refactoring, and high-quality documentation from the start.

## 2. Coding Standards & Conventions

### a. General

*   **Language**: The frontend is written in TypeScript, and the backend is in Python.
*   **Naming**: Use clear, descriptive names for variables, functions, and classes. Follow standard conventions for each language (e.g., `camelCase` for functions/variables and `PascalCase` for classes in TypeScript; `snake_case` for functions/variables and `PascalCase` for classes in Python).

### b. Backend (Python)

*   **Linting & Formatting**: We use `ruff` for linting and formatting. All code must be compliant with the rules defined in `backend/pyproject.toml`.
*   **Type Checking**: We use `mypy` for static type checking. All new code must include type hints.
*   **Docstrings**: All public modules, classes, and functions must have Google-style docstrings, as enforced by `pydocstyle`.
*   **Code Contracts**: Use Python's `abc` module to define abstract base classes for new services or components.

### c. Frontend (TypeScript)

*   **Linting**: We use `eslint` with `typescript-eslint`. All code must adhere to the rules in `frontend/eslint.config.js`.
*   **Type Checking**: The `tsconfig.json` is configured with `strict: true`. Avoid using `any` and provide explicit types wherever possible.
*   **Code Contracts**: Use TypeScript `interfaces` to define the shape of objects and the public API of classes.
*   **Component Style**: Follow the existing patterns for React components found in `frontend/src/components/`.

## 3. Commit Message Format

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This is essential for automated versioning and changelog generation.

The format is: `<type>[optional scope]: <description>`

*   **`feat`**: A new feature
*   **`fix`**: A bug fix
*   **`docs`**: Documentation only changes
*   **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
*   **`refactor`**: A code change that neither fixes a bug nor adds a feature
*   **`test`**: Adding missing tests or correcting existing tests
*   **`chore`**: Changes to the build process or auxiliary tools

Example: `feat(agent): add support for new data source`

## 4. AI Assistant Interaction

To ensure the AI assistant is an effective collaborator, always start a new development session with the following prompt:

> "Hello Gemini. In this session, we will strictly follow the development workflow defined in `.ai-conventions/01_workflow.md`. Please ensure all your suggestions and code generations adhere to this document."

This sets the context and ensures the AI's output aligns with our project standards.
