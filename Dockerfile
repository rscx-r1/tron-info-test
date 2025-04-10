FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/

COPY . /app

WORKDIR  /app

ARG ENV

RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"

RUN chmod +x run.sh