SHELL := /bin/bash
COMPOSE := docker compose
COMPOSE_FILE := docker-compose.yml
ENV_FILE := .env
.PHONY: all build-core run-dev test deploy stop clean logs ps help
all: help
build-core:
	@echo "→ Building all Docker images..."
	$(COMPOSE) -f $(COMPOSE_FILE) build --parallel
	@echo "✓ Build complete"
run-dev:
	@if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); echo "✓ Created .env from .env.example — please review it"; fi
	@echo "→ Starting Foresight Engine (dev mode)..."
	$(COMPOSE) -f $(COMPOSE_FILE) up -d
	@echo "✓ All services started"
	@echo "  Frontend:   http://localhost"
	@echo "  Backend:    http://localhost:8000"
	@echo "  API Docs:   http://localhost:8000/docs"
	@echo "  Metrics:    http://localhost:8000/metrics"
test:
	@echo "→ Running Python backend tests..."
	cd backend && python -m pytest --cov=app --cov-report=term-missing -v
	@echo "→ Running Celery worker tests..."
	cd celery-worker && python -m pytest -v
	@echo "→ Running Go agent-collector tests..."
	cd agent-collector && go test -v -race ./...
	@echo "✓ All tests passed"
test-backend:
	@echo "→ Running backend tests only..."
	cd backend && python -m pytest --cov=app --cov-report=term-missing -v
test-go:
	@echo "→ Running Go tests only..."
	cd agent-collector && go test -v -race ./...
test-celery:
	@echo "→ Running Celery tests only..."
	cd celery-worker && python -m pytest -v
lint:
	@echo "→ Linting Python (ruff)..."
	cd backend && ruff check .
	cd celery-worker && ruff check .
	@echo "→ Linting Go (golangci-lint)..."
	cd agent-collector && golangci-lint run ./...
	@echo "✓ Linting passed"
deploy:
	@echo "→ Deploying to production..."
	$(COMPOSE) -f $(COMPOSE_FILE) pull
	$(COMPOSE) -f $(COMPOSE_FILE) up -d --remove-orphans
	docker image prune -f
	@echo "✓ Deployment complete"
stop:
	@echo "→ Stopping all services..."
	$(COMPOSE) -f $(COMPOSE_FILE) down
	@echo "✓ Services stopped"
clean:
	@echo "→ Removing containers, volumes, and images..."
	$(COMPOSE) -f $(COMPOSE_FILE) down -v --rmi local
	@echo "✓ Cleanup complete"
logs:
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f
logs-backend:
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f backend
logs-agent:
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f agent-collector
logs-celery:
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f celery-worker
ps:
	$(COMPOSE) -f $(COMPOSE_FILE) ps
shell-backend:
	$(COMPOSE) -f $(COMPOSE_FILE) exec backend /bin/bash
shell-db:
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}
shell-redis:
	$(COMPOSE) -f $(COMPOSE_FILE) exec redis redis-cli -a $${REDIS_PASSWORD}
migrate:
	$(COMPOSE) -f $(COMPOSE_FILE) exec backend alembic upgrade head
migrate-create:
	$(COMPOSE) -f $(COMPOSE_FILE) exec backend alembic revision --autogenerate -m "$(name)"
help:
	@echo "Foresight Engine — Available targets:"
	@echo "  make build-core      Build all Docker images"
	@echo "  make run-dev         Start all services in dev mode"
	@echo "  make test            Run all tests (Python + Go)"
	@echo "  make test-backend    Run backend tests only"
	@echo "  make test-go         Run Go tests only"
	@echo "  make test-celery     Run Celery worker tests only"
	@echo "  make lint            Run all linters"
	@echo "  make deploy          Pull latest images and redeploy"
	@echo "  make stop            Stop all services"
	@echo "  make clean           Remove all containers, volumes, images"
	@echo "  make logs            Follow all service logs"
	@echo "  make logs-backend    Follow backend logs"
	@echo "  make ps              Show running services"
	@echo "  make shell-backend   Open shell in backend container"
	@echo "  make shell-db        Open psql shell"
	@echo "  make shell-redis     Open redis-cli shell"
	@echo "  make migrate         Run DB migrations"
	@echo "  make migrate-create  Create new migration (name=<msg>)"
