FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency metadata first for better layer caching.
COPY pyproject.toml uv.lock ./

# Install locked runtime dependencies.
RUN uv sync \
    --frozen \
    --no-dev \
    --no-install-project

# Copy the application.
COPY app ./app

EXPOSE 8000

CMD ["/app/.venv/bin/python", "-m", "app.server"]