# Docker Deployment Guide

This guide explains how to run the RAG chatbot using Docker and Docker Compose.

## 🐳 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- Google API key for Gemini models

## 🚀 Quick Start

### 1. Set Up Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

This will start:
- **FastAPI Backend** → http://localhost:8000
- **Gradio UI** → http://localhost:7860

### 3. Access the Application

- **Gradio UI**: Open http://localhost:7860 in your browser
- **FastAPI Docs**: Open http://localhost:8000/docs
- **API Endpoints**: Available at http://localhost:8000

## 📋 Docker Compose Services

### Services Overview

```yaml
services:
  fastapi:   # Backend API service
    - Port: 8000
    - Auto-reload enabled for development
    
  gradio:    # Web UI service
    - Port: 7860
    - Depends on fastapi service
```

### Shared Resources

- **ChromaDB Volume**: `chroma_data` - Persistent vector database storage
- **Network**: `rag-network` - Internal communication between services

## 🔧 Common Commands

### Start Services
```bash
# Start all services
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Start specific service
docker-compose up fastapi
docker-compose up gradio
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes ChromaDB data)
docker-compose down -v
```

### View Logs
```bash
# View all service logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs fastapi
docker-compose logs gradio
```

### Rebuild Services
```bash
# Rebuild after code changes
docker-compose up --build

# Force rebuild (no cache)
docker-compose build --no-cache
```

### Execute Commands Inside Container
```bash
# Run a command in the fastapi container
docker-compose exec fastapi python -m src.data_loader

# Open a shell in the container
docker-compose exec fastapi /bin/bash

# Test the vector store
docker-compose exec fastapi python -m src.vector_store
```

## 🔍 Service Health Checks

The FastAPI service includes a health check:

```bash
# Check service health
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "message": "RAG Chatbot API is running",
  "vector_store_initialized": true,
  "total_transactions": 5
}
```

## 📊 Volume Management

### ChromaDB Persistence

Data is persisted in a Docker named volume `chroma_data`:

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect ai_project_chroma_data

# Backup volume
docker run --rm -v ai_project_chroma_data:/data -v ${PWD}:/backup ubuntu tar czf /backup/chroma_backup.tar.gz /data
```

### Reset Vector Database

To initialize a fresh vector database:

```bash
# Stop services and remove volume
docker-compose down -v

# Restart services (will recreate vector store)
docker-compose up -d
```

## 🛠️ Development vs Production

### Development Mode (Current Setup)

The docker-compose.yml is configured for development with:
- Auto-reload on code changes
- Source code mounted as volumes
- Logs visible in console

### Production Mode

For production, modify `docker-compose.yml`:

1. **Remove volume mounts** for source code
2. **Disable auto-reload**:
   ```yaml
   command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```
3. **Add resource limits**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 1G
   ```

## 🌐 Environment Variables

All environment variables can be configured in `.env`:

```bash
# Google API
GOOGLE_API_KEY=your_key_here

# Vector Store
VECTOR_DB_PATH=/app/chroma_db
COLLECTION_NAME=transactions

# LLM Configuration
LLM_MODEL=gemini-3-pro-preview
EMBEDDING_MODEL=models/gemini-embedding-001
TEMPERATURE=0
TOP_K_RESULTS=3
```

## 🧪 Testing the Docker Setup

### 1. Test FastAPI
```bash
# Health check
curl http://localhost:8000/health

# Get transactions
curl http://localhost:8000/transactions

# Chat query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Amit'\''s total spending?"}'
```

### 2. Test Gradio UI
- Open http://localhost:7860
- Try sample queries
- Check analytics dashboard

## 📦 Docker Image Size

The built image is optimized:
- Base: Python 3.11 slim
- Size: ~1.5GB (includes all dependencies)
- Layers cached for faster rebuilds

## 🚨 Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process or change port in docker-compose.yml
```

### Issue: API Key Not Working
```bash
# Verify environment variable is set
docker-compose exec fastapi env | grep GOOGLE_API_KEY

# Restart services after updating .env
docker-compose restart
```

### Issue: ChromaDB Permission Errors
```bash
# Fix volume permissions
docker-compose down
docker volume rm ai_project_chroma_data
docker-compose up -d
```

### Issue: Container Fails to Start
```bash
# Check logs
docker-compose logs fastapi

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## 🔐 Security Best Practices

1. **Never commit `.env`** - It's in `.gitignore`
2. **Use secrets management** for production (Docker Swarm secrets, Kubernetes secrets)
3. **Scan images** for vulnerabilities:
   ```bash
   docker scan rag-chatbot-api
   ```
4. **Use non-root user** in production Dockerfile

## 📈 Scaling

To scale services horizontally:

```bash
# Scale Gradio UI to 3 instances
docker-compose up --scale gradio=3

# Note: You'll need a load balancer for multiple instances
```

## 🎯 Next Steps

1. ✅ Services running → Test the API and UI
2. 📊 Monitor logs → `docker-compose logs -f`
3. 🔄 Update code → Changes auto-reload in containers
4. 📦 Deploy → Use production configuration

---

**Need Help?** Check the main [README.md](README.md) for application usage details.
