.PHONY: help install install-dev clean test lint format type-check build upload-test upload release run-setup run-status run-reset shell update-deps lock-deps check-deps security-check clean-cache clean-all

# Default target
help:
	@echo "Claude Setup - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make shell           Activate pipenv shell"
	@echo ""
	@echo "Development:"
	@echo "  make lint            Run code linting (flake8)"
	@echo "  make format          Format code with black"
	@echo "  make type-check      Run type checking (mypy)"
	@echo "  make test            Run test suite"
	@echo "  make test-verbose    Run tests with verbose output"
	@echo "  make test-coverage   Run tests with coverage report"
	@echo "  make check           Run all checks (lint, type-check, test)"
	@echo ""
	@echo "Running the CLI:"
	@echo "  make run-setup       Run interactive setup wizard"
	@echo "  make run-status      Show current configuration"
	@echo "  make run-reset       Reset configuration"
	@echo ""
	@echo "Dependencies:"
	@echo "  make update-deps     Update all dependencies"
	@echo "  make lock-deps       Lock current dependencies"
	@echo "  make check-deps      Check for outdated dependencies"
	@echo "  make security-check  Check for security vulnerabilities"
	@echo ""
	@echo "Building & Publishing:"
	@echo "  make build           Build distribution packages"
	@echo "  make upload-test     Upload to TestPyPI"
	@echo "  make upload          Upload to PyPI"
	@echo "  make release         Full release (test, build, upload)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove build artifacts"
	@echo "  make clean-cache     Remove Python cache files"
	@echo "  make clean-all       Remove all generated files"

# Installation targets
install:
	pipenv install

install-dev:
	pipenv install --dev
	pipenv install -e .

# Development environment
shell:
	pipenv shell

# Code quality targets
lint:
	@echo "Running flake8..."
	pipenv run flake8 src/ --max-line-length=100 --extend-ignore=E203,W503

format:
	@echo "Formatting code with black..."
	pipenv run black src/ --line-length=100

type-check:
	@echo "Running mypy type checking..."
	pipenv run mypy src/ --ignore-missing-imports

# Testing targets
test:
	@echo "Running test suite..."
	pipenv run pytest

test-verbose:
	@echo "Running test suite (verbose)..."
	pipenv run pytest -vv

test-coverage:
	@echo "Running test suite with coverage..."
	pipenv run pytest --cov=src/claude_setup --cov-report=html --cov-report=term

# Combined checks
check: lint type-check test
	@echo "All checks passed!"

# Running the CLI
run-setup:
	pipenv run claude-setup setup

run-status:
	pipenv run claude-setup status

run-reset:
	pipenv run claude-setup reset

# Dependency management
update-deps:
	pipenv update

lock-deps:
	pipenv lock

check-deps:
	pipenv check

security-check:
	pipenv check --categories security

# Building and publishing
build: clean
	@echo "Building distribution packages..."
	pipenv run python -m build

upload-test: build
	@echo "Uploading to TestPyPI..."
	pipenv run twine upload --repository testpypi dist/*

upload: build
	@echo "Uploading to PyPI..."
	pipenv run twine upload dist/*

release: check build
	@echo "Ready for release!"
	@echo "Run 'make upload-test' to test on TestPyPI first"
	@echo "Then run 'make upload' to publish to PyPI"

# Cleanup targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage

clean-all: clean clean-cache
	rm -rf Pipfile.lock
	rm -rf .claude/settings.local.json

# Development helpers
.PHONY: dev-install-tools
dev-install-tools:
	@echo "Installing development tools..."
	pipenv install --dev black flake8 mypy pytest pytest-cov pytest-mock build twine

# Git helpers
.PHONY: pre-commit
pre-commit: format lint type-check test
	@echo "Pre-commit checks passed!"

# Docker support (future enhancement)
.PHONY: docker-build docker-run
docker-build:
	@echo "Docker support not yet implemented"

docker-run:
	@echo "Docker support not yet implemented"