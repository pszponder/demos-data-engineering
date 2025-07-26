# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Builder stage: install uv, create venv, install dependencies
FROM base AS builder

# Install uv (prebuilt binary)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy only dependency files first for better cache usage
COPY --link pyproject.toml ./
COPY --link uv.lock ./

# Create venv and install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    ENV_PATH="/app/.venv/bin:$PATH" && \
    PATH="$ENV_PATH" uv pip install -r pyproject.toml

# Copy application code
COPY --link src/ ./src/
COPY --link main.py ./main.py

# Final stage: minimal image with non-root user
FROM base AS final

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy venv and app code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# Set environment for venv
ENV PATH="/app/.venv/bin:$PATH"

# Set default port if not provided
ENV PORT=8000

USER appuser

# Use PORT environment variable for EXPOSE
EXPOSE $PORT

# Start FastAPI app with uvicorn using PORT environment variable
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port $PORT"
