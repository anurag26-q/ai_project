# Docker Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: "version attribute is obsolete"
**Symptom:**
```
level=warning msg="docker-compose.yml: the attribute `version` is obsolete"
```

**Solution:** ✅ FIXED
The `version: '3.8'` line has been removed from docker-compose.yml as it's no longer needed in modern Docker Compose.

### Issue 2: "500 Internal Server Error" when building
**Symptom:**
```
unable to get image: request returned 500 Internal Server Error
```

**Possible Causes & Solutions:**

#### 1. Docker Desktop Not Fully Started
```bash
# Wait for Docker Desktop to fully start (check system tray icon)
# Then retry:
docker-compose up --build
```

#### 2. Clean Docker Cache
```bash
# Remove all stopped containers and unused images
docker system prune -a

# Then rebuild
docker-compose up --build
```

#### 3. Reset Docker Compose State
```bash
# Stop and remove everything
docker-compose down -v

# Remove any orphaned containers
docker-compose down --remove-orphans

# Rebuild from scratch
docker-compose up --build
```

#### 4. Check Docker Resources
- Open Docker Desktop Settings
- Ensure adequate resources are allocated:
  - Memory: At least 4GB
  - Disk space: At least 10GB available

### Issue 3: Port Already in Use
**Symptom:**
```
Error: bind: address already in use
```

**Solution:**
```bash
# Find what's using the port (example for port 8000)
netstat -ano | findstr :8000

# Kill the process or change ports in docker-compose.yml
```

### Issue 4: Permission Errors
**Symptom:**
```
Permission denied
```

**Solution:**
```bash
# Run PowerShell as Administrator
# Or ensure Docker Desktop has proper permissions
```

## Quick Fix Commands

### Fresh Start (Recommended for Error Recovery)
```bash
# 1. Stop everything
docker-compose down -v

# 2. Clean Docker system
docker system prune --all --volumes --force

# 3. Rebuild
docker-compose up --build -d

# 4. Check logs
docker-compose logs -f
```

### Check Docker Status
```bash
# Verify Docker is running
docker ps

# Check Docker version
docker --version
docker-compose --version

# View Docker info
docker info
```

### Debugging Container Issues
```bash
# View logs for specific service
docker-compose logs fastapi
docker-compose logs gradio

# Check container status
docker-compose ps

# Restart a specific service
docker-compose restart fastapi
```

## Manual Build Alternative

If docker-compose continues to fail, try building manually:

```bash
# Build the image
docker build -t rag-chatbot .

# Run FastAPI
docker run -d -p 8000:8000 --env-file .env rag-chatbot uvicorn main:app --host 0.0.0.0 --port 8000

# Run Gradio
docker run -d -p 7860:7860 --env-file .env rag-chatbot python run_ui.py
```

## Environment-Specific Issues

### Windows-Specific
- Ensure WSL 2 is enabled if using Docker Desktop
- Check Windows Firewall isn't blocking Docker
- Run PowerShell as Administrator

### Firewall/Antivirus
- Add Docker Desktop to antivirus exceptions
- Ensure ports 8000 and 7860 aren't blocked

## Still Not Working?

### Check Docker Daemon
```bash
# Restart Docker Desktop
# Wait 30 seconds for full initialization
# Try again
```

### Verify .env File
```bash
# Ensure .env exists and has GOOGLE_API_KEY
cat .env
```

### Check Disk Space
```bash
# Ensure at least 2GB free for Docker images
docker system df
```

## Get Help

If issues persist:
1. Check Docker Desktop logs (Settings → Troubleshoot → Get support)
2. Share the full error output
3. Try running without Docker (see README.md for local setup)

## Success Indicators

When working correctly, you should see:
```bash
docker-compose up -d
# Creating network "ai_project_rag-network" ... done
# Creating volume "ai_project_chroma_data" ... done
# Creating rag-chatbot-api ... done
# Creating rag-chatbot-ui  ... done

docker-compose ps
# NAME                 STATUS
# rag-chatbot-api      Up
# rag-chatbot-ui       Up
```

Then access:
- http://localhost:8000/docs
- http://localhost:7860
