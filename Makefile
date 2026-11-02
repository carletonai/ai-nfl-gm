# Common tasks. Everything runs through uv so nobody has to activate a venv.
.PHONY: help setup lint format test test-network check api pull-data check-cap-table hooks clean

help:
	@echo "make setup      install the package, all extras and dev tools into .venv, plus the pre-commit hooks"
	@echo "make hooks      (re)install the pre-commit hooks on their own"
	@echo "make lint       ruff check + format check"
	@echo "make format     ruff format + autofix"
	@echo "make test       pytest (offline tests)"
	@echo "make test-network  the tests that download real data"
	@echo "make check      lint + test (what CI runs)"
	@echo "make api        run the FastAPI dev server on http://127.0.0.1:8000"
	@echo "make pull-data  download the core nflverse tables into data/raw"
	@echo "make check-cap-table  cross-check configs/sports/nfl.yaml against Over The Cap data in nflverse"

setup:
	uv sync --all-extras
	uv run pre-commit install

hooks:
	uv run pre-commit install

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check . --fix

test:
	uv run pytest

test-network:
	uv run pytest -m network

check: lint test

api:
	uv run uvicorn ai_nfl_gm.api.main:app --reload

pull-data:
	uv run python scripts/pull_nflverse.py

check-cap-table:
	uv run python scripts/check_cap_table.py

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
