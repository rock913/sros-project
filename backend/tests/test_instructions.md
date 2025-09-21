# BDD Test Execution Instructions

To run the BDD tests for the backend agent, execute the following command within the `langgraph-api` container (e.g., via `docker-compose exec langgraph-api bash` or directly if you are in the container):

```bash
cd /deps/backend && POSTGRES_URI="postgresql://postgres:postgres@langgraph-postgres:5432/postgres" uv run --with-editable . pytest
```

This command sets the `POSTGRES_URI` environment variable, installs dependencies in editable mode, and then runs `pytest` to execute all tests, including the BDD scenarios defined in `features/agent_workflow.feature` and implemented in `step_defs/test_agent_workflow_steps.py`.
