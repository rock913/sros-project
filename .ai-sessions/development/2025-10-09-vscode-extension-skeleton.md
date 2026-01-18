# Session: VS Code Extension Skeleton (Phase 2)

## Core Goal

The goal of this session is to implement the foundational skeleton for the VS Code extension as outlined in Phase 2 of the `ROADMAP.md`.

**Final Acceptance Criteria:**
- The extension successfully calls the backend API.
- Fetched research data is statically displayed across the three-panel layout (Asset Library, Manuscript, AI Control Panel).

---

## Analysis & Plan

### Analysis

- **Strategy:** The VS Code extension development will be fully containerized, similar to the backend. This requires creating a dedicated Dev Container that can be managed by Docker Compose and used by VS Code's "Remote-Containers" feature.
- **Tooling:** The dev container's Dockerfile must include Node.js, `yo`, and `@vscode/vsce`.
- **Networking:** The extension container must be on the same Docker network as the backend to facilitate API calls via service names (e.g., `http://backend:8000`).

### Revised Plan (Multi-Container Strategy)

1.  **[DONE] [Step 1: Analyze Existing Dev Container Config]**
    *   **Action**: Read the contents of `.devcontainer/devcontainer.json` and `docker-compose-dev.yml` to understand the current backend development setup.
    *   **Verification**: Confirm understanding of how the `backend` service is configured and launched.
    *   **Summary**: The configuration was analyzed and found to be already set up for VS Code extension development.

2.  **[DONE] [Step 2: Create and Integrate Frontend Dev Container]**
    *   **Action**: Create a `vscode-extension/Dockerfile.dev` with Node.js, `yo`, and `@vscode/vsce`.
    *   **Action**: Add a new `vscode-dev` service to `docker-compose-dev.yml` which uses the new Dockerfile and mounts the `vscode-extension` directory.
    *   **Action**: Modify `.devcontainer/devcontainer.json` to ensure it uses Docker Compose and sets `backend` as the default service to attach to.
    *   **Verification**: `docker-compose -f docker-compose-dev.yml build` completes successfully for all services. VS Code can "Reopen in Container" and successfully attach to the `backend` service.
    *   **Summary**: The `Dockerfile.dev` was verified to contain the necessary tools. The `docker-compose-dev.yml` and `devcontainer.json` were also confirmed to be correctly configured.

3.  **[DONE] [Step 3: Scaffold Extension in Dev Container]**
    *   **Action**: Attach a new VS Code window to the `vscode-dev` container. Inside the container's terminal, run `yo code` to scaffold a new TypeScript extension in the `/workspaces/gemini-fullstack-langgraph-quickstart/vscode-extension` directory.
    *   **Verification**: The extension project is created and can be launched in a debug window from this VS Code instance.
    *   **Summary**: The `yo code` command failed to run non-interactively. The extension skeleton was created manually by writing all necessary files (`package.json`, `tsconfig.json`, `src/extension.ts`, etc.).

4.  **[DONE] [Step 4: Implement Three-Panel Layout]**
    *   **Action**: Modify the extension's `package.json` to define the three required view containers and views.
    *   **Verification**: Launching the extension shows the three empty panels in the UI.
    *   **Summary**: The `package.json` was updated with the `contributes` section, defining the activity bar and the three views (Asset Library, Manuscript, AI Control Panel).

5.  **[Step 5: Implement API Communication]**
    *   **Action**: Add a service module within the extension to call the backend at `http://backend:8000`.
    *   **Verification**: Unit tests for the service module pass, confirming it can fetch and parse data.

6.  **[Step 6: Static Data Display]**
    *   **Action**: Populate the three panels with the data fetched from the API.
    *   **Verification**: A manual check confirms that launching the extension correctly displays the static data.
---
