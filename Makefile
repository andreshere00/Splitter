# OS detection: define uv install command.
ifeq ($(OS),Windows_NT)
	UV_INSTALL_CMD = powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
else
	UV_INSTALL_CMD = curl -LsSf https://astral.sh/uv/install.sh | sh
endif

# Load environment variables from .env if it exists.
ifneq (,$(wildcard .env))
	include .env
	export
endif

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make docs             - Run the documentation server."
	@echo "  make install          - Install application dependencies using uv."
	@echo "  make install-uv       - Install uv CLI (OS-specific)."
	@echo "  make run              - Execute the application using uv."
	@echo "  make serve            - Serve the FastAPI application."
	@echo "  make docker-api-build - Build the API dockerized application."
	@echo "  make docker-api-run   - Run the API dockerized application."
	@echo "  make test             - Run tests using uv and pytest."
	@echo "  make shell            - Run a uv shell."
	@echo "  make pre-commit       - Install pre-commit hooks."
	@echo "  make format           - Run pyupgrade, isort, black and flake8 for code style."
	@echo "  make clean            - Clean output, cache and log files."
	@echo "  make clean-cache      - Clean cache files."
	@echo "  make clean-data       - Clean output data files."
	@echo "  make clean-log        - Clean log files."
	@echo "  make remove-data      - Remove data presented in the output folder."

.PHONY: install
install:
	@echo "Installing application dependencies and pre-commit hooks..."
	uv sync && uv run pre-commit install && uv run pre-commit install --hook-type commit-msg

.PHONY: install-uv
install-uv:
	@echo "Installing uv CLI (OS-specific)..."
	$(UV_INSTALL_CMD)

.PHONY: test
test:
	@echo "Running tests using uv and pytest..."
	uv run pytest

.PHONY: clean
clean:
	@echo "Cleaning output, cache, and log files..."
	@find . -type d \( -name '*log*' -o -name '*cache*' \) -exec rm -rf {} + && rm -rf data/output/* data/test/output/* *.DS_store*

.PHONY: clean-log
clean-log:
	@echo "Cleaning log files..."
	@find . -type d -name '*log*' -exec rm -rf {} +

.PHONY: clean-cache
clean-cache:
	@echo "Cleaning cache files..."
	@find . -type d -name '*cache*' -exec rm -rf {} +

.PHONY: clean-data
clean-data:
	@echo "Cleaning output data files..."
	@rm -rf data/output/* data/test/output/*

.PHONY: remove-data
remove-data:
	@echo "Removing data presented in output folder..."
	@rm -rf data/output/* data/test/output/*

.PHONY: run
run:
	@echo "Running the application with default parameters..."
	uv run python src/application/cli.py

.PHONY: serve
serve:
	@echo "Running the FastAPI application..."
	uv run uvicorn src.application.api.app:app --reload

.PHONY: docker-api-build
docker-api-build:
	@echo "Building the API dockerized application..."
	docker build -t splitter_api -f Dockerfile.api .

.PHONY: docker-api-run
docker-api-run:
	@echo "Running the API dockerized application..."
	docker run -p 8080:8080 --env-file .env splitter_api

.PHONY: format
format:
	@echo "Running pyupgrade..."
	uv run pyupgrade --exit-zero
	@echo "Running isort..."
	uv run isort .
	@echo "Running black..."
	uv run black .
	@echo "Running flake8..."
	uv run flake8 --max-line-length=101 --ignore=E203,W291 src/

.PHONY: docs
docs:
	@echo "Running the Documentation server..."
	uv run mkdocs serve

.PHONY: pre-commit
pre-commit:
	@echo "Installing pre-commit hooks..."
	uv run pre-commit

.PHONY: shell
shell:
	@echo "Starting a uv shell..."
	uv run shell
