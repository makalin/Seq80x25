# Seq80x25 Makefile

.PHONY: help install install-dev run test clean lint format check-deps

# Default target
help:
	@echo "Seq80x25 - Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the sequencer"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean up generated files"
	@echo "  check-deps   - Check for dependency updates"
	@echo "  package      - Create distribution package"
	@echo "  install-pkg  - Install package in development mode"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# Run the sequencer
run:
	python seq80x25.py

# Run tests
test:
	pytest tests/ -v --cov=seq80x25

# Run linting
lint:
	flake8 seq80x25.py
	mypy seq80x25.py

# Format code
format:
	black seq80x25.py
	black tests/

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ .eggs/

# Check for dependency updates
check-deps:
	pip list --outdated

# Create distribution package
package: clean
	python setup.py sdist bdist_wheel

# Install package in development mode
install-pkg:
	pip install -e .

# Run all checks
check: lint test

# Quick start (install and run)
quickstart: install run

# Development setup
dev-setup: install-dev format lint test

# Test all tools and utilities
tools: patterns export effects projects cli
	@echo "✓ All tools tested successfully"

# Run demo script
demo:
	python demo.py

# Test pattern library
patterns:
	python patterns.py

# Test export tools
export:
	python export_tools.py

# Test audio effects
effects:
	python audio_effects.py

# Test project manager
projects:
	python project_manager.py

# Test command-line interface
cli:
	python cli_tool.py --help

# Generate sample audio files
samples: demo
	@echo "✓ Sample audio files generated in samples/ directory"

# Show project info
info:
	@echo "Seq80x25 - Retro Music Sequencer"
	@echo "Python version: $(shell python --version)"
	@echo "Dependencies:"
	@pip list | grep -E "(textual|pygame|numpy)"
	@echo ""
	@echo "Available tools:"
	@echo "  - Pattern Library (patterns.py)"
	@echo "  - Export Tools (export_tools.py)"
	@echo "  - Audio Effects (audio_effects.py)"
	@echo "  - Project Manager (project_manager.py)"
	@echo "  - CLI Tool (cli_tool.py)"
