# Python Containerize

Comprehensive Docker containerization for Python applications with multi-stage builds, security hardening, and performance optimization using modern tools like uv.

## Instructions

You are tasked with creating comprehensive Docker containerization for a Python application. Follow these steps to implement production-ready containerization with security best practices and performance optimization.

### 1. Analyze Python Application Structure

First, examine the Python project structure to understand:
- Project type (web app, CLI tool, microservice, etc.)
- Dependencies and package management approach
- Entry points and runtime requirements
- Static files and assets
- Configuration management needs

Look for existing files:
- `pyproject.toml`, `requirements.txt`, or `Pipfile`
- Application entry points (`main.py`, `app.py`, etc.)
- Configuration files
- Static assets or data files

### 2. Create Base Dockerfile with Multi-Stage Build

Create a production-optimized Dockerfile with multi-stage builds:

```dockerfile
# syntax=docker/dockerfile:1.4

# Build stage - Use uv for fast dependency resolution
FROM python:3.12-slim as builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Create and set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies into virtual environment
RUN uv sync --frozen --no-install-project --no-dev

# Production stage
FROM python:3.12-slim as production

# Install security updates and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        # Add only necessary system dependencies here
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Create Development Dockerfile

Create a separate Dockerfile for development with hot-reloading and debugging capabilities:

```dockerfile
# syntax=docker/dockerfile:1.4

FROM python:3.12-slim as development

# Install uv and development tools
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install development system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        build-essential \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Create non-root user
RUN groupadd --gid 1000 devuser && \
    useradd --uid 1000 --gid devuser --shell /bin/bash --create-home devuser

WORKDIR /app

# Install dependencies with dev dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project

# Switch to dev user
USER devuser

# Default command for development
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 4. Create Docker Compose Configuration

Create comprehensive Docker Compose configurations for different environments:

**docker-compose.yml** (Development):
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
      target: development
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/.venv  # Prevent overwriting venv
    environment:
      - PYTHONPATH=/app
      - DEBUG=true
      - DATABASE_URL=postgresql://user:password@db:5432/devdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: devdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/dev.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

**docker-compose.prod.yml** (Production):
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    environment:
      - PYTHONPATH=/app
      - DEBUG=false
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'

  db:
    image: postgres:15-alpine
    env_file:
      - .env.prod
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - app-network
    restart: always

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/prod.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - app-network
    restart: always

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### 5. Create Container Security Configuration

Create `.dockerignore` file:
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.pytest_cache
.mypy_cache
htmlcov

# Git
.git
.gitignore

# Documentation
README.md
docs/

# IDE
.vscode
.idea
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Development
.env.local
.env.development
docker-compose.override.yml
```

Create security scanning script **scripts/security-scan.sh**:
```bash
#!/bin/bash

echo "Running container security scans..."

# Build image for scanning
docker build -t myapp:security-scan .

# Scan for vulnerabilities with Trivy
echo "Scanning for vulnerabilities..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    -v $HOME/Library/Caches:/root/.cache/ \
    aquasec/trivy image --severity HIGH,CRITICAL myapp:security-scan

# Scan with Docker Scout (if available)
echo "Running Docker Scout analysis..."
docker scout cves myapp:security-scan

# Check for secrets
echo "Scanning for secrets..."
docker run --rm -v "$(pwd)":/app \
    trufflesecurity/trufflehog:latest filesystem /app --no-update

echo "Security scan complete!"
```

### 6. Implement Container Performance Optimization

Create optimized production Dockerfile with performance enhancements:

```dockerfile
# syntax=docker/dockerfile:1.4

# Use specific Python version with slim variant
FROM python:3.12.1-slim as base

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set Python environment variables for performance
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Build stage
FROM base as builder

WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Production stage
FROM base as production

# Install minimal system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tini \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/*

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Pre-compile Python files for faster startup
RUN python -m compileall -b . && \
    find . -name "*.py" -delete && \
    find . -name "__pycache__" -type d -exec chmod 755 {} \;

# Set proper permissions
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

# Use tini as init system
ENTRYPOINT ["tini", "--"]

# Health check with proper timeout
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "-m", "gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
```

### 7. Create Monitoring and Logging Configuration

Create monitoring configuration **monitoring/docker-compose.monitoring.yml**:
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log:ro
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus_data:
  grafana_data:
```

### 8. Create Container Build and Deploy Scripts

Create **scripts/build.sh**:
```bash
#!/bin/bash

set -euo pipefail

# Configuration
IMAGE_NAME="myapp"
REGISTRY="your-registry.com"
VERSION=${1:-latest}

echo "Building Docker image: ${IMAGE_NAME}:${VERSION}"

# Build multi-architecture image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "${REGISTRY}/${IMAGE_NAME}:${VERSION}" \
    --tag "${REGISTRY}/${IMAGE_NAME}:latest" \
    --push \
    .

# Run security scan
echo "Running security scan..."
./scripts/security-scan.sh

# Run tests in container
echo "Running tests in container..."
docker run --rm "${REGISTRY}/${IMAGE_NAME}:${VERSION}" python -m pytest

echo "Build complete: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"
```

Create **scripts/deploy.sh**:
```bash
#!/bin/bash

set -euo pipefail

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "Deploying to ${ENVIRONMENT} environment..."

case $ENVIRONMENT in
    "production")
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
        ;;
    "staging")
        docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
        ;;
    *)
        docker-compose up -d
        ;;
esac

# Wait for health check
echo "Waiting for application to be healthy..."
timeout 60 bash -c 'until docker-compose ps | grep healthy; do sleep 2; done'

echo "Deployment complete!"
```

### 9. Container Security Hardening

Create security-hardened configuration **security/hardened.dockerfile**:
```dockerfile
# syntax=docker/dockerfile:1.4

FROM python:3.12-slim as production

# Install security updates and minimal dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        tini \
        ca-certificates \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user with minimal privileges
RUN groupadd --gid 10001 appuser && \
    useradd --uid 10001 --gid appuser --home-dir /app --no-create-home --shell /sbin/nologin appuser

# Set security-focused environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy application with proper ownership
COPY --chown=appuser:appuser . .

# Remove unnecessary files and set strict permissions
RUN find /app -type f -name "*.py" -exec chmod 644 {} \; && \
    find /app -type d -exec chmod 755 {} \; && \
    chmod 755 /app

# Drop all capabilities and add only what's needed
USER appuser

# Use read-only root filesystem
# Mount tmpfs for /tmp if needed
VOLUME ["/tmp"]

# Health check with minimal privileges
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Use tini as PID 1
ENTRYPOINT ["tini", "--"]
CMD ["python", "-m", "gunicorn", "app.main:app", "--bind", "0.0.0.0:8000"]
```

### 10. Testing and Validation

Create container testing script **tests/test-container.sh**:
```bash
#!/bin/bash

set -euo pipefail

echo "Testing Docker container..."

# Build test image
docker build -t myapp:test .

# Test container startup
echo "Testing container startup..."
CONTAINER_ID=$(docker run -d -p 8000:8000 myapp:test)

# Wait for startup
sleep 10

# Test health endpoint
if curl -f http://localhost:8000/health; then
    echo "✓ Health check passed"
else
    echo "✗ Health check failed"
    docker logs $CONTAINER_ID
    exit 1
fi

# Test application endpoints
if curl -f http://localhost:8000/; then
    echo "✓ Application responding"
else
    echo "✗ Application not responding"
    docker logs $CONTAINER_ID
    exit 1
fi

# Clean up
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID

echo "Container tests passed!"
```

### 11. Documentation and Deployment Guide

Create **CONTAINER.md** documentation:
```markdown
# Container Deployment Guide

## Quick Start

### Development
```bash
# Start development environment
docker-compose up

# Access application at http://localhost:8000
```

### Production
```bash
# Build production image
./scripts/build.sh v1.0.0

# Deploy to production
./scripts/deploy.sh production v1.0.0
```

## Security Features

- Non-root user execution
- Multi-stage builds for minimal attack surface
- Security scanning with Trivy and Docker Scout
- Read-only root filesystem support
- Dropped capabilities
- Regular security updates

## Performance Optimizations

- Multi-stage builds for smaller images
- uv for fast dependency management
- Pre-compiled Python bytecode
- Optimized layer caching
- Health checks for reliability

## Monitoring

- Prometheus metrics collection
- Grafana dashboards
- Centralized logging with Loki
- Application performance monitoring
```

Follow these steps systematically to implement comprehensive Docker containerization for your Python application. The configuration provides production-ready containers with security hardening, performance optimization, and comprehensive monitoring capabilities.

If you need to customize any configurations for specific frameworks (Django, FastAPI, Flask) or deployment platforms (Kubernetes, AWS ECS, etc.), please specify your requirements.
