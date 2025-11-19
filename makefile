.PHONY: init run update

run: 
	uv run main.py

test:
	uv run pytest

check:
	uv run pyre check
	uv run ruff check

format:
	uv run ruff format
