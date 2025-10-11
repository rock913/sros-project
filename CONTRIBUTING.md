# Contributing to Auto-Researcher

We welcome contributions from everyone. To ensure a smooth and collaborative process, we have a few guidelines that we ask you to follow.

## AI-Assisted Development Workflow

This project is developed with the help of an AI assistant. The assistant's operational framework, including its development and debugging methodology, is defined in the [GEMINI.md](GEMINI.md) file. This ensures the AI's actions are transparent, consistent, and aligned with the project's standards.

While human contributors are not required to follow the AI's exact workflow, understanding it can provide valuable context about how the project evolves.

## Development Environment

You can develop either within a Docker container (recommended) or on your local machine.

### Docker-Based Development (Recommended)

The recommended way to work on this project is using our pre-configured Docker environment. This ensures consistency and avoids issues with local machine setup.

1.  **Prerequisites**: Docker and Docker Compose.
2.  **Start Services**: Run `make dev-docker`. This will build the necessary images and start the frontend, backend, and database services.

### Local Development (Without Docker)

If you prefer to run the services directly on your machine, follow these steps:

**1. Prerequisites:**

*   Node.js and npm (or yarn/pnpm)
*   Python 3.11+

**2. Install Dependencies:**

*   **Backend:** `cd backend && pip install .`
*   **Frontend:** `cd frontend && npm install`

**3. Run Development Servers:**

*   Run `make dev-local` from the root directory to start both frontend and backend servers with hot-reloading.

## Testing

Our test suite is designed to be run in the Docker environment to ensure consistency.

**1. Start the Services:**

Ensure the services are running by executing:
```bash
make dev-docker
```

**2. Run the Test Suites:**

*   **Backend Unit & Integration Tests:**
    This command runs the `pytest` suite, which includes all unit tests and BDD scenarios.
    ```bash
    make test-backend-docker
    ```

*   **End-to-End (E2E) Test:**
    This command simulates a real client interacting with the agent from start to finish. You can override the default topic as shown.
    ```bash
    make test-e2e-docker TOPIC="Your custom research topic"
    ```

By following these guidelines, you help us maintain a high-quality, consistent, and well-documented codebase.
