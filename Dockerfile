# Use the provided base image with Python 3.13 on Bookworm
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    gcc \
    poppler-utils \
    libsndfile1 \
    ffmpeg \
    libgl1 \
    libportaudio2 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    portaudio19-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libsndfile1-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to disable .pyc file creation and enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_HTTP_TIMEOUT=520
ENV BLIS_ARCH=generic
# Set the working directory

WORKDIR /app

# Copy only dependency-related files first for better caching
COPY pyproject.toml uv.lock README* ./
# Install dependencies *without* installing the project yet
# --frozen means it respects your pinned versions (if you have a lockfile)
RUN pip install --no-cache-dir wheel setuptools
RUN uv lock
RUN uv sync 

# Copy the rest of the application code
COPY core/ ./core/
COPY api/ ./api/
# Install dependencies using the frozen lockfile

# Expose port 80 for the FastAPI application
EXPOSE 80

# Run the FastAPI application using uvicorn (ensure main:app is available)
ENTRYPOINT ["fastapi", "dev","api/main.py", "--host", "0.0.0.0", "--port", "80"]

