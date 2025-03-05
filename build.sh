#!/bin/bash
set -e

# Create and use a new buildx builder instance
docker buildx create --name mybuilder --use || true
docker buildx inspect --bootstrap

# Build the multi-architecture image and push it to Docker Hub
docker buildx build --platform linux/arm64 \
  -t codecraftme/codecraft-core:latest --push .

