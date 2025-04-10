linter_fix:
	uv run ruff check --fix . && uv run ruff check --fix --select I . && uv run ruff format .