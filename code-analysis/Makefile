.PHONY: help venv install clean test analyze tree

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
ANALYZE := $(BIN)/analyze

help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make install       - Create venv and install package in editable mode"
	@echo "  make clean         - Remove cloned repositories and cache"
	@echo "  make clean-all     - Remove everything including venv"
	@echo "  make analyze URL=<repo-url> - Analyze a repository"
	@echo "  make tree DIR=<path> - Generate tree for local directory"
	@echo "  make test          - Run analysis on a small test repository"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
		echo "Virtual environment created at $(VENV)"; \
	else \
		echo "Virtual environment already exists at $(VENV)"; \
	fi

install: venv
	@echo "Installing package in editable mode..."
	$(PIP) install -e .

clean:
	rm -rf target_repo
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf $(VENV)
	rm -rf *.egg-info

analyze:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@if [ -z "$(URL)" ]; then \
		echo "Error: URL parameter required. Usage: make analyze URL=<repo-url>"; \
		exit 1; \
	fi
	$(ANALYZE) analyze $(URL)

tree:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@if [ -z "$(DIR)" ]; then \
		echo "Error: DIR parameter required. Usage: make tree DIR=<path>"; \
		exit 1; \
	fi
	$(ANALYZE) tree $(DIR)

test:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(ANALYZE) analyze https://github.com/psf/requests.git

