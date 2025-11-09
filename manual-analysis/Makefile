.PHONY: help venv install install-dev clean chat

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PYTHON_BIN := $(BIN)/python

help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install package in editable mode"
	@echo "  make chat          - Run interactive pattern analysis chat"
	@echo "  make clean         - Remove cache files"
	@echo "  make clean-all     - Remove everything including venv"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
		echo "Virtual environment created at $(VENV)"; \
	else \
		echo "Virtual environment already exists at $(VENV)"; \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "Installation complete!"
	@echo "To activate the venv: source $(VENV)/bin/activate"

install-dev: venv
	@echo "Installing package in editable mode..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	@echo ""
	@echo "Installation complete!"
	@echo "You can now run: make chat"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf $(VENV)
	rm -rf *.egg-info
	rm -rf src/*.egg-info

chat:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install-dev' first."; \
		exit 1; \
	fi
	$(BIN)/chat

