# standard is 'python3', but you can replace with:
# make install PYTHON=python3.14
PYTHON ?= python3
VENV = .venv
PIP = $(VENV)/bin/pip

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make install     - Create virtual environment and install dependencies"
	@echo "  make lint        - Run Flake8 linter"
	@echo "  make test        - Run Pytest suite"
	@echo "  make check       - Run linter AND tests (Fail-Fast)"
	@echo "  make clean       - Remove virtual environment"

# Install
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Installation abgeschlossen."
	@echo "Aktiviere das venv mit: 'source $(VENV)/bin/activate' (oder fish: 'source .venv/bin/activate.fish')"

check: lint test

lint:
	$(VENV)/bin/flake8 .

test:
	$(VENV)/bin/pytest -c test/pytest.ini

clean:
	rm -rf $(VENV)

.PHONY: install test lint check clean