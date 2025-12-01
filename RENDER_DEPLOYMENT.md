# 🚀 Deploying RAG Chatbot to Render

This guide walks you through deploying your RAG-powered chatbot to [Render](https://render.com), a modern cloud platform that makes deployment simple and scalable.

## 📋 Prerequisites

Before you begin, ensure you have:

1. ✅ A [Render account](https://dashboard.render.com/register) (free tier available)
2. ✅ Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. ✅ A Google API key for Gemini models
4. ✅ Git installed locally

## 🎯 Deployment Options

You have **two deployment options**:

### Option A: Blueprint (Recommended) ⭐
Deploy both services (FastAPI + Streamlit) automatically using `render.yaml`

### Option B: Manual Setup
Create and configure each service individually through the Render dashboard

---

## 🚀 Option A: Blueprint Deployment (Recommended)

This is the **easiest and fastest** way to deploy your entire application.

### Step 1: Push Your Code to Git

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Prepare for Render deployment"

# Add your remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### Step 2: Create a New Blueprint on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your Git repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

### Step 3: Configure Environment Variables

After the blueprint is created, you need to set your **Google API Key**:

1. Go to your **FastAPI service** (`rag-chatbot-api`)
2. Navigate to **"Environment"** tab
3. Find `GOOGLE_API_KEY` and click **"Edit"**
4. Paste your Google API key
5. Click **"Save Changes"**

6. Repeat for **Streamlit service** (`rag-chatbot-streamlit`):
   - Go to the Streamlit service
   - Set `GOOGLE_API_KEY` in the Environment tab

### Step 4: Deploy! 🎉

Render will automatically:
- ✅ Build your Docker images
- ✅ Deploy both services
- ✅ Create persistent storage for ChromaDB
- ✅ Set up health checks
- ✅ Provide public URLs

**Your services will be available at:**
- **FastAPI**: `https://rag-chatbot-api.onrender.com`
- **Streamlit UI**: `https://rag-chatbot-streamlit.onrender.com`

---

## 🛠️ Option B: Manual Deployment

If you prefer to set up services individually:

### Deploy FastAPI Backend

1. **Create Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Web Service"**
   - Connect your Git repository
   - Select the repository and branch

2. **Configure Service**
   - **Name**: `rag-chatbot-api`
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Instance Type**: `Free` (or choose paid plan)

3. **Add Environment Variables**
   ```
   GOOGLE_API_KEY=your-google-api-key-here
   VECTOR_DB_PATH=/app/chroma_db
   COLLECTION_NAME=transactions
   LLM_MODEL=models/gemini-2.5-flash
   EMBEDDING_MODEL=models/text-embedding-004
   TEMPERATURE=0
   TOP_K_RESULTS=3
   PORT=8000
   ```

4. **Add Persistent Disk**
   - Click **"Add Disk"**
   - **Name**: `chroma-data`
   - **Mount Path**: `/app/chroma_db`
   - **Size**: `1 GB`

5. **Set Health Check**
   - **Health Check Path**: `/health`

6. **Deploy**
   - Click **"Create Web Service"**

### Deploy Streamlit Frontend

1. **Create Another Web Service**
   - Click **"New +"** → **"Web Service"**
   - Connect the same repository

2. **Configure Service**
   - **Name**: `rag-chatbot-streamlit`
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `./Dockerfile.streamlit`
   - **Instance Type**: `Free`

3. **Add Environment Variables**
   ```
   GOOGLE_API_KEY=your-google-api-key-here
   FASTAPI_URL=https://rag-chatbot-api.onrender.com
   ```
   
   > Replace `https://rag-chatbot-api.onrender.com` with your actual FastAPI service URL

4. **Deploy**
   - Click **"Create Web Service"**

---

## 🔧 Configuration Files Explained

### `render.yaml` (Blueprint Configuration)

This file defines your entire infrastructure as code:

```yaml
services:
  - type: web
    name: rag-chatbot-api
    runtime: docker
    # ... FastAPI configuration
  
  - type: web
    name: rag-chatbot-streamlit
    runtime: docker
    # ... Streamlit configuration
```

**Benefits:**
- ✅ Version-controlled infrastructure
- ✅ Reproducible deployments
- ✅ Easy to update and redeploy
- ✅ Automatic service linking

### `build.sh` (Build Script)

Optional build script for non-Docker deployments:

```bash
#!/usr/bin/env bash
pip install -r requirements.txt
mkdir -p /app/chroma_db
```

---

## 🌍 Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | `AIza...` |

### Optional Variables (with defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `VECTOR_DB_PATH` | `/app/chroma_db` | ChromaDB storage path |
| `COLLECTION_NAME` | `transactions` | Vector collection name |
| `LLM_MODEL` | `models/gemini-2.5-flash` | Gemini model for chat |
| `EMBEDDING_MODEL` | `models/text-embedding-004` | Embedding model |
| `TEMPERATURE` | `0` | LLM temperature (0-1) |
| `TOP_K_RESULTS` | `3` | Number of retrieved docs |
| `PORT` | `8000` | FastAPI port |

---

## 📊 Monitoring Your Deployment

### Check Service Status

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your service
3. View **"Logs"** tab for real-time logs
4. Check **"Metrics"** for performance data

### Health Checks

Your FastAPI service has an automatic health check at `/health`:

```bash
curl https://rag-chatbot-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "RAG Chatbot API",
  "version": "1.0.0"
}
```

### View Logs

```bash
# In Render Dashboard
Services → [Your Service] → Logs
```

---

## 🐛 Troubleshooting

### Issue: Service Won't Start

**Symptoms:**
- Service shows "Deploy failed"
- Logs show errors during startup

**Solutions:**

1. **Check Environment Variables**
   ```bash
   # Verify GOOGLE_API_KEY is set correctly
   # Go to: Service → Environment → Check all variables
   ```

2. **Check Build Logs**
   - Look for dependency installation errors
   - Ensure all packages in `requirements.txt` are compatible

3. **Verify Dockerfile**
   ```bash
   # Test locally first
   docker build -t test-app .
   docker run -p 8000:8000 test-app
   ```

### Issue: ChromaDB Data Not Persisting

**Symptoms:**
- Vector store resets on each deployment
- Need to re-ingest data frequently

**Solutions:**

1. **Verify Persistent Disk**
   - Go to: Service → Settings → Disks
   - Ensure disk is mounted at `/app/chroma_db`
   - Size should be at least 1 GB

2. **Check Environment Variable**
   ```bash
   VECTOR_DB_PATH=/app/chroma_db  # Must match disk mount path
   ```

### Issue: Streamlit Can't Connect to FastAPI

**Symptoms:**
- Streamlit UI shows "API connection failed"
- Health check fails

**Solutions:**

1. **Update FASTAPI_URL**
   ```bash
   # In Streamlit service environment
   FASTAPI_URL=https://rag-chatbot-api.onrender.com
   ```
   
   Replace with your actual FastAPI service URL

2. **Check CORS Settings**
   - Ensure `main.py` allows Streamlit origin
   - Update `allow_origins` if needed

3. **Verify Both Services Are Running**
   - Check both services are "Live" in dashboard
   - Test FastAPI health endpoint directly

### Issue: Slow Cold Starts

**Symptoms:**
- First request takes 30+ seconds
- Service "spins down" when idle

**Explanation:**
- Render's free tier spins down services after 15 minutes of inactivity
- First request after spin-down takes time to restart

**Solutions:**

1. **Upgrade to Paid Plan** (Recommended for production)
   - Paid plans keep services always running
   - No cold starts

2. **Keep Service Warm** (Free tier workaround)
   - Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your service every 5 minutes
   - Add health check URL: `https://rag-chatbot-api.onrender.com/health`

### Issue: Out of Memory Errors

**Symptoms:**
- Service crashes with OOM errors
- Logs show memory-related errors

**Solutions:**

1. **Optimize ChromaDB Settings**
   - Reduce `TOP_K_RESULTS` to lower memory usage
   - Clear old embeddings if not needed

2. **Upgrade Instance Type**
   - Free tier: 512 MB RAM
   - Starter: 1 GB RAM
   - Standard: 2+ GB RAM

### Issue: API Key Authentication Errors

**Symptoms:**
- `AuthenticationError` from Google Gemini
- 401/403 errors in logs

**Solutions:**

1. **Verify API Key**
   ```bash
   # Test your API key locally first
   curl -H "x-goog-api-key: YOUR_API_KEY" \
     https://generativelanguage.googleapis.com/v1beta/models
   ```

2. **Check Environment Variable**
   - Ensure no extra spaces or quotes
   - Re-enter the key in Render dashboard

3. **Enable Gemini API**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Ensure Gemini API is enabled for your project

---

## 🔄 Updating Your Deployment

### Automatic Deployments

Render automatically redeploys when you push to your connected branch:

```bash
git add .
git commit -m "Update feature X"
git push origin main
```

Render will:
1. Detect the push
2. Rebuild your Docker image
3. Deploy the new version
4. Run health checks
5. Switch traffic to new version

### Manual Deployments

You can also trigger manual deployments:

1. Go to Render Dashboard
2. Select your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Rollback to Previous Version

If something goes wrong:

1. Go to **"Events"** tab
2. Find the last successful deployment
3. Click **"Rollback"**

---

## 💰 Cost Estimation

### Free Tier
- ✅ 750 hours/month per service
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Services spin down after 15 min inactivity
- ⚠️ 512 MB RAM

**Cost:** $0/month

### Starter Plan ($7/month per service)
- ✅ Always running (no cold starts)
- ✅ 1 GB RAM
- ✅ Better performance

**Cost:** $14/month (2 services)

### Standard Plan ($25/month per service)
- ✅ 2 GB RAM
- ✅ Priority support
- ✅ Advanced metrics

**Cost:** $50/month (2 services)

---

## 🔐 Security Best Practices

### 1. Never Commit API Keys

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

### 2. Use Environment Variables

Always set sensitive data via Render's environment variables, never hardcode.

### 3. Enable HTTPS

Render provides free SSL certificates automatically.

### 4. Restrict CORS Origins

Update `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rag-chatbot-streamlit.onrender.com"
    ],  # Specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Use Secrets for API Keys

In `render.yaml`, mark sensitive variables:

```yaml
envVars:
  - key: GOOGLE_API_KEY
    sync: false  # This marks it as a secret
```

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Docker Guide](https://render.com/docs/docker)
- [Render Persistent Disks](https://render.com/docs/disks)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Google Gemini API Docs](https://ai.google.dev/docs)

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] Code is pushed to Git repository
- [ ] `render.yaml` is in project root
- [ ] `.env` is in `.gitignore`
- [ ] Google API key is ready
- [ ] `requirements.txt` is up to date
- [ ] Dockerfile builds successfully locally
- [ ] Health check endpoint works (`/health`)
- [ ] CORS settings are configured

After deployment:

- [ ] Both services show "Live" status
- [ ] FastAPI `/health` endpoint responds
- [ ] Streamlit UI loads successfully
- [ ] Can query the chatbot
- [ ] ChromaDB data persists across deployments
- [ ] Logs show no errors

---

## 🎉 Success!

Your RAG chatbot is now live on Render! 

**Next Steps:**
1. Test all functionality
2. Set up monitoring/alerting
3. Configure custom domain (optional)
4. Enable auto-scaling (paid plans)

**Need Help?**
- Check [Render Community](https://community.render.com/)
- Review [Troubleshooting](#-troubleshooting) section above
- Contact Render support

---

**Built with ❤️ using FastAPI, LangChain, ChromaDB, Streamlit, and Google Gemini**

**Deployed on Render 🚀**
