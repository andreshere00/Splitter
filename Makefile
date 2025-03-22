.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install          - Install application dependencies using uv."
	@echo "  make test             - Run tests using uv and pytest."
	@echo "  make clean            - Clean output, cache and log files."
	@echo "  make clean-log        - Clean log files."
	@echo "  make clean-cache      - Clean cache files."
	@echo "  make clean-data       - Clean output data files."
	@echo "  make run              - Execute the application using uv."
	@echo "  make format           - Run pyupgrade, isort, black and flake8 for code style."
	@echo "  make shell            - Run a uv shell."
	@echo "  make docs             - Run the documentation server."
	@echo "  make pre-commit       - Install pre-commit hooks."
	@echo "  make serve            - Serve the FastAPI application."
	@echo "  make env              - Export .env file to the package management tool."
	@echo "  make remove-data      - Remove data presented in that folder."
	@echo "  make docker-api-build - Build the API dockerized application."
	@echo "  make docker-api-run   - Run the API dockerized application."

.PHONY: install
install:
	export UV_ENV_FILE=.env & uv sync & uv run pre-commit install & uv run pre-commit install --hook-type commit-msg

.PHONY: env
env:
	export UV_ENV_FILE=.env

.PHONY: test
test:
	uv run pytest

.PHONY: clean
clean:
	@echo "Cleaning log, output and cache files..."
	@find . -type d \( -name '*log*' -o -name '*cache*' \) -exec rm -rf {} + & \
	rm -rf data/output/* data/test/output/* *.DS_store*

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
	@echo "Remove data presented in that folder."
	@rm -rf data/output/* data/test/output/*

.PHONY: run
run:
	@echo "Running the application with default parameters..."
	uv run python src/application/cli.py

.PHONY: serve
serve:
	@echo "Running the FastAPI application"
	uv run uvicorn src.application.api.app:app --reload

.PHONY: docker-api-build
docker-api-build:
	@echo "Building the API dockerized application"
	docker build -t splitter_api -f Dockerfile.api .

.PHONY: docker-api-run
docker-api-run:
	@echo "Running the API dockerized application"
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
	uv run flake8 --max-line-length=101 --ignore=E203 src/

.PHONY: docs
docs:
	@echo "Running the Documentation server."
	uv run mkdocs serve

.PHONY: pre-commit
pre-commit:
	uv run pre-commit
