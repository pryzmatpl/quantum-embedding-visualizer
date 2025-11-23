# Setup Guide - Virtual Environment and Docker

This guide covers both virtual environment and Docker setup options.

## Option 1: Virtual Environment (Local Development)

### Linux/Mac

1. **Run the setup script**:
   ```bash
   ./setup_venv.sh
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Start the API**:
   ```bash
   python app.py
   ```

### Windows

1. **Run the PowerShell script**:
   ```powershell
   .\setup_venv.ps1
   ```

2. **Activate the virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Start the API**:
   ```powershell
   python app.py
   ```

### Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
python app.py
```

## Option 2: Docker (Recommended for Production)

### Quick Start

```bash
# Build and start
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Access the Application

- **API**: http://localhost:8000
- **UI**: http://localhost:8000/ui
- **API Docs**: http://localhost:8000/docs

See [DOCKER.md](DOCKER.md) for detailed Docker documentation.

## Comparison

| Feature | Virtual Environment | Docker |
|---------|---------------------|--------|
| Setup Time | Fast | Medium (first build) |
| Isolation | Limited | Complete |
| Portability | Requires Python | Works anywhere |
| Production Ready | No | Yes |
| Resource Usage | Lower | Higher |
| Best For | Development | Production/Deployment |

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python3: command not found`
- **Solution**: Install Python 3.8+ from python.org or your package manager

**Problem**: `pip: command not found`
- **Solution**: Install pip: `python -m ensurepip --upgrade`

**Problem**: Permission denied on setup script
- **Solution**: `chmod +x setup_venv.sh` (Linux/Mac)

### Docker Issues

**Problem**: Port 8000 already in use
- **Solution**: Change port in `docker-compose.yml` or stop the conflicting service

**Problem**: Docker build fails
- **Solution**: Check internet connection, ensure Docker is running, try `docker-compose build --no-cache`

**Problem**: Container exits immediately
- **Solution**: Check logs with `docker-compose logs`

## Next Steps

After setup:

1. **Test the API**:
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Open the UI**:
   Navigate to http://localhost:8000/ui in your browser

3. **Try an embedding**:
   ```bash
   curl -X POST http://localhost:8000/api/embedding \
     -H "Content-Type: application/json" \
     -d '{"word": "quantum"}'
   ```

## Notes

- **First Run**: The first time you run the application, GloVe vectors (~400MB) will be downloaded automatically
- **Cache**: Embeddings are cached in memory and optionally on disk
- **Performance**: Docker may be slightly slower due to containerization overhead
- **Development**: Use virtual environment for development, Docker for deployment

