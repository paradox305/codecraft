FROM python:3.10-bookworm 

RUN apt update && apt install ffmpeg libsm6 libxext6 -y

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml /app/

# Final sync/install after copying application code
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install -r pyproject.toml --no-cache-dir --system

# Copy your application code
COPY api/ /app/api
COPY core /app/core

EXPOSE 80

# Use uvicorn to serve FastAPI on port 80
CMD ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "80"]
