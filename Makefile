# Makefile for Quantum Embedding Visualization

.PHONY: help venv docker-build docker-up docker-down docker-logs docker-shell clean

help:
	@echo "Quantum Embedding Visualization - Makefile Commands"
	@echo ""
	@echo "Virtual Environment:"
	@echo "  make venv          - Set up virtual environment"
	@echo "  make run           - Run the application (requires venv)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker container"
	@echo "  make docker-down   - Stop Docker container"
	@echo "  make docker-logs   - View Docker logs"
	@echo "  make docker-shell  - Open shell in Docker container"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         - Clean up generated files"

venv:
	@echo "Setting up virtual environment..."
	@bash setup_venv.sh

run:
	@echo "Starting API server..."
	@source venv/bin/activate && python app.py

docker-build:
	@echo "Building Docker image..."
	@docker-compose build

docker-up:
	@echo "Starting Docker container..."
	@docker-compose up -d

docker-down:
	@echo "Stopping Docker container..."
	@docker-compose down

docker-logs:
	@echo "Viewing Docker logs..."
	@docker-compose logs -f

docker-shell:
	@echo "Opening shell in Docker container..."
	@docker-compose exec quantum-embedding-api /bin/bash

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__ *.pyc *.pyo
	@rm -rf .pytest_cache .coverage htmlcov
	@rm -rf *.log
	@echo "Done!"

