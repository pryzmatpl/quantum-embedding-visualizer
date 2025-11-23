# Docker Setup Guide

This guide explains how to run the Quantum Embedding Visualization API using Docker.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the container**:
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode**:
   ```bash
   docker-compose up -d
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

5. **Access the application**:
   - API: http://localhost:8000
   - UI: http://localhost:8000/ui
   - API Docs: http://localhost:8000/docs

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t quantum-embedding-api .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name quantum-embedding-api \
     -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     quantum-embedding-api
   ```

3. **View logs**:
   ```bash
   docker logs -f quantum-embedding-api
   ```

4. **Stop the container**:
   ```bash
   docker stop quantum-embedding-api
   docker rm quantum-embedding-api
   ```

## Configuration

### Environment Variables

You can set environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - EMBEDDINGS_CACHE_DIR=/app/data
```

### Volumes

The `docker-compose.yml` includes volume mounts for:
- `./data:/app/data` - Persistent storage for embeddings cache
- `./static:/app/static` - Static files (for development)

### Ports

Default port is `8000`. To change it, modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"  # Host:Container
```

## Development

For development with hot-reload, you can override the command:

```yaml
command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Or run directly:
```bash
docker-compose run --rm -p 8000:8000 quantum-embedding-api \
  uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Troubleshooting

### Container won't start

1. **Check logs**:
   ```bash
   docker-compose logs quantum-embedding-api
   ```

2. **Check if port is already in use**:
   ```bash
   lsof -i :8000  # Linux/Mac
   netstat -ano | findstr :8000  # Windows
   ```

3. **Rebuild from scratch**:
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up
   ```

### GloVe download issues

The first run will download GloVe vectors (~400MB). This happens automatically when the service starts. If it fails:

1. Check internet connection
2. Check Docker logs for errors
3. The download is cached, so subsequent runs will be faster

### Permission issues

If you encounter permission issues with volumes:

```bash
# Linux/Mac
sudo chown -R $USER:$USER ./data

# Or run with user mapping
docker-compose run --rm --user $(id -u):$(id -g) quantum-embedding-api
```

## Production Deployment

For production, consider:

1. **Use a reverse proxy** (nginx, Traefik) in front of the API
2. **Set proper CORS origins** in `app.py`
3. **Use environment variables** for sensitive configuration
4. **Enable HTTPS** via reverse proxy
5. **Set resource limits** in docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
   ```

## Health Checks

The container includes a health check that verifies the API is responding:

```bash
# Check health status
docker ps  # Look for "healthy" status

# Manual health check
curl http://localhost:8000/api/health
```

