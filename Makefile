# ==============================================================================
# VARIABLES
# ==============================================================================

# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Default research topic for the E2E test
TOPIC ?= "The impact of AI on climate change"

# ==============================================================================
# HELP
# ==============================================================================

.PHONY: help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "------------------ Docker Environment (Recommended) ------------------"
	@echo "  dev-docker         Build and start all services using Docker Compose."
	@echo "  stop-docker        Stop all running Docker Compose services."
	@echo "  test-backend-docker Run backend unit and integration tests inside Docker."
	@echo "  test-e2e-docker    Run the full E2E test case inside Docker."
	@echo "                     Override topic with 'make test-e2e-docker TOPIC=\"Your Topic\"'"
	@echo ""
	@echo "------------------ Local Development (No Docker) -------------------"
	@echo "  dev-local          Start frontend and backend servers locally (requires local setup)."
	@echo "  dev-frontend       Start only the frontend development server locally."
	@echo "  dev-backend        Start only the backend development server locally."
	@echo ""
	@echo "------------------ Utility Scripts ---------------------------------"
	@echo "  list-models        List available Gemini models from the API."
	@echo ""


# ==============================================================================
# DOCKER-BASED WORKFLOW
# ==============================================================================

.PHONY: dev-docker stop-docker test-backend-docker test-e2e-docker

dev-docker:
	@echo "Building and starting services with Docker Compose..."
	@docker-compose -f docker-compose-dev.yml up --build -d

stop-docker:
	@echo "Stopping Docker Compose services..."
	@docker-compose -f docker-compose-dev.yml down

test-backend-docker:
	@echo "Running backend tests inside Docker..."
	@docker-compose exec backend bash -c "uv pip install -e '.[dev]' && pytest"

test-e2e-docker:
	@echo "Running E2E test with topic: $(TOPIC)..."
	@docker-compose exec backend bash -c "uv run python examples/e2e_test_case.py '$(TOPIC)'"


# ==============================================================================
# LOCAL DEVELOPMENT WORKFLOW
# ==============================================================================

.PHONY: dev-local dev-frontend dev-backend

dev-local:
	@echo "Starting both frontend and backend development servers locally..."
	@make dev-frontend & make dev-backend

dev-frontend:
	@echo "Starting frontend development server (local)..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server (local)..."
	@cd backend && langgraph dev


# ==============================================================================
# UTILITY SCRIPTS
# ==============================================================================

.PHONY: list-models

list-models:
	@echo "Listing available models..."
	@./scripts/list-models.sh