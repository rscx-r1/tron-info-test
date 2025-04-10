linter_fix:
	uv run ruff check --fix . && uv run ruff check --fix --select I . && uv run ruff format .
test:
	docker compose -f docker-compose.yml --profile test run --rm app-test
test_down:
	docker compose -f docker-compose.yml --profile test down --volumes