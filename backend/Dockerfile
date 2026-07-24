FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_DEV=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local
WORKDIR /backend

COPY pyproject.toml uv.lock ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync --locked

COPY alembic.ini ./
COPY migrations ./migrations
COPY src ./src

RUN groupadd --system --gid 1001 app \
    && useradd --system --uid 1001 --gid app --no-log-init app \
    && chown -R app:app /backend
USER app

EXPOSE 8000
