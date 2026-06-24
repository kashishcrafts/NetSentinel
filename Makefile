.PHONY: help setup up down build test lint format type-check docker-build docker-push deploy clean seed-db logs backend-shell frontend-shell

help:
	@echo "NetSentinel Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              Install all dependencies"
	@echo "  make seed-db            Seed database with sample data"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up                 Start all services (docker-compose)"
	@echo "  make down               Stop all services"
	@echo "  make build              Build Docker images"
	@echo "  make logs               View docker-compose logs"
	@echo "  make clean              Stop and remove all containers/volumes"
	@echo ""
	@echo "Development:"
	@echo "  make backend-dev        Start backend dev server"
	@echo "  make frontend-dev       Start frontend dev server"
	@echo "  make backend-shell      Open backend container shell"
	@echo "  make frontend-shell     Open frontend container shell"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test               Run all tests"
	@echo "  make test-backend       Run backend tests"
	@echo "  make test-frontend      Run frontend tests"
	@echo "  make test-coverage      Run tests with coverage"
	@echo "  make lint               Run linters"
	@echo "  make format             Format code (black, isort)"
	@echo "  make type-check         Run type checking (mypy)"
	@echo ""
	@echo "Deployment:"
	@echo "  make docker-build       Build production Docker images"
	@echo "  make docker-push        Push images to registry"
	@echo "  make deploy             Deploy to production (requires setup)"
	@echo ""

# Setup & Installation
setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	cd frontend && npm install

seed-db:
	@echo "Seeding database..."
	docker-compose exec backend python scripts/seed_data.py

# Docker Commands
up:
	@echo "Starting services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	sleep 30
	@echo "Services started!"
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost:8001"
	@echo "API Docs: http://localhost:8001/docs"

down:
	@echo "Stopping services..."
	docker-compose down

build:
	@echo "Building Docker images..."
	docker-compose build

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	cd frontend && npm run clean 2>/dev/null || true

# Development
backend-dev:
	cd backend && uvicorn main:app --reload --port 8001 --host 0.0.0.0

frontend-dev:
	cd frontend && npm run dev

backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

# Testing & Quality
test: test-backend

test-backend:
	@echo "Running backend tests..."
	pytest backend/tests -v

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm run test

test-coverage:
	@echo "Running tests with coverage..."
	pytest backend/tests --cov=backend --cov-report=html --cov-report=term

lint:
	@echo "Running linters..."
	flake8 backend --max-line-length=120
	cd frontend && npm run lint

format:
	@echo "Formatting code..."
	black backend --line-length=120
	isort backend
	cd frontend && npm run format

type-check:
	@echo "Type checking..."
	mypy backend --ignore-missing-imports

# Deployment
docker-build:
	@echo "Building production images..."
	docker build -f Dockerfile.backend -t netsentinel:backend-latest .
	docker build -f Dockerfile.frontend -t netsentinel:frontend-latest .

docker-push:
	@echo "Pushing images to registry..."
	@echo "Set DOCKER_REGISTRY environment variable"
	docker tag netsentinel:backend-latest $(DOCKER_REGISTRY)/netsentinel-backend:latest
	docker tag netsentinel:frontend-latest $(DOCKER_REGISTRY)/netsentinel-frontend:latest
	docker push $(DOCKER_REGISTRY)/netsentinel-backend:latest
	docker push $(DOCKER_REGISTRY)/netsentinel-frontend:latest

deploy: docker-build docker-push
	@echo "Deployment commands prepared"
	@echo "Run on production server:"
	@echo "  docker-compose pull && docker-compose up -d"

# Database
db-migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

db-rollback:
	@echo "Rolling back last migration..."
	cd backend && alembic downgrade -1

# Utilities
version:
	@echo "NetSentinel v2.0.0"

check-health:
	@echo "Checking service health..."
	curl -s http://localhost:8001/health | jq .
	curl -s http://localhost/health | jq .

api-docs:
	@echo "Opening API documentation..."
	open http://localhost:8001/docs || xdg-open http://localhost:8001/docs || echo "Visit http://localhost:8001/docs"

frontend:
	@echo "Opening frontend..."
	open http://localhost || xdg-open http://localhost || echo "Visit http://localhost"

install-hooks:
	@echo "Installing git hooks..."
	@echo "#!/bin/bash" > .git/hooks/pre-commit
	@echo "make lint && make type-check" >> .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

.DEFAULT_GOAL := help


install:
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

db-init:
	python init_db.py
	@echo "✓ Database initialized"

db-reset:
	python -c "from backend.core.database import engine, Base; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
	python init_db.py
	@echo "✓ Database reset"

run:
	python run.py

dev:
	cd backend && python -m uvicorn main:app --reload

test:
	pytest -v

lint:
	flake8 backend/
	mypy backend/
	@echo "✓ Linting complete"

format:
	black backend/
	isort backend/
	@echo "✓ Formatting complete"

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.mypy_cache' -delete
	@echo "✓ Cleanup complete"

docs:
	@echo "Documentation available at:"
	@echo "- ./DOCUMENTATION.md"
	@echo "- ./API_EXAMPLES.md"
	@echo "- ./QUICK_START.md"
