# -------------------------------
# Base stage
# -------------------------------
FROM python:3.13-bookworm AS base

RUN apt update && apt install ffmpeg libsm6 libxext6 -y

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml /app/


# Copy your application code
COPY api/ /app/api
COPY core /app/core

# Final sync/install after copying application code
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install -r pyproject.toml --no-cache-dir --system

# Make sure the .venv is on PATH

EXPOSE 80

# Use uvicorn to serve FastAPI on port 80
ENTRYPOINT ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "80"]