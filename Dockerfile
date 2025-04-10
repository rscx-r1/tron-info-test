FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/

COPY . /app
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

RUN uv venv && uv sync --extra dev

RUN chmod +x run.sh
