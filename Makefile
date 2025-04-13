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
help: ## Show this help message.
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: docs
docs: ## Run the documentation server.
	@echo "Running the Documentation server..."
	uv run mkdocs serve

.PHONY: install
install: ## Install application dependencies and pre-commit hooks.
	@echo "Installing application dependencies and pre-commit hooks..."
	uv sync && uv run pre-commit install && uv run pre-commit install --hook-type commit-msg

.PHONY: install-uv
install-uv: ## Install uv CLI (OS-specific).
	@echo "Installing uv CLI (OS-specific)..."
	$(UV_INSTALL_CMD)

.PHONY: run
run: ## Execute the application using uv.
	@echo "Running the application with default parameters..."
	uv run python src/application/cli.py

.PHONY: serve
serve: ## Serve the FastAPI application.
	@echo "Running the FastAPI application..."
	uv run uvicorn src.application.api.app:app --reload

.PHONY: docker-api-build
docker-api-build: ## Build the API dockerized application.
	@echo "Building the API dockerized application..."
	docker build -t splitter_api -f Dockerfile.api .

.PHONY: docker-api-run
docker-api-run: ## Run the API dockerized application.
	@echo "Running the API dockerized application..."
	docker run -p 8080:8080 --env-file .env splitter_api

.PHONY: test
test: ## Run tests using uv and pytest.
	@echo "Running tests using uv and pytest..."
	uv run coverage report -m && uv run pytest 

.PHONY: shell
shell: ## Run a uv shell.
	@echo "Starting a uv shell..."
	uv run shell

.PHONY: pre-commit
pre-commit: ## Install pre-commit hooks.
	@echo "Installing pre-commit hooks..."
	uv run pre-commit

.PHONY: format
format: ## Run pyupgrade, isort, black, and flake8 for code style.
	@echo "Running pyupgrade..."
	uv run pyupgrade --exit-zero
	@echo "Running isort..."
	uv run isort .
	@echo "Running black..."
	uv run black .
	@echo "Running flake8..."
	uv run flake8 --max-line-length=101 --ignore=E203,W291 src/

# Clean commands

.PHONY: clean
clean: ## Clean output, cache, and log files.
	@echo "Cleaning output, cache, and log files..."
	@find . -type d \( -name 'logs/*' -o -name '*cache*' \) -exec rm -rf {} + && rm -rf data/output/* data/test/output/* *.DS_store*

.PHONY: clean-log
clean-log: ## Clean log files.
	@echo "Cleaning log files..."
	@find . -type d -name '*log*' -exec rm -rf {} +

.PHONY: clean-cache
clean-cache: ## Clean cache files.
	@echo "Cleaning cache files..."
	@find . -type d -name '*cache*' -exec rm -rf {} +

.PHONY: clean-data
clean-data: ## Clean output data files.
	@echo "Cleaning output data files..."
	@rm -rf data/output/* data/test/output/*

.PHONY: remove-data
remove-data: ## Remove data presented in the output folder.
	@echo "Removing data presented in output folder..."
	@rm -rf data/output/* data/test/output/*
