# 🚀 Render Quick Start Guide

**Deploy your RAG chatbot to Render in 5 minutes!**

## Prerequisites

- ✅ GitHub/GitLab account with your code pushed
- ✅ [Render account](https://dashboard.render.com/register) (free)
- ✅ Google API key for Gemini

---

## 🎯 Deployment Steps

### 1. Push to Git (if not already done)

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create Blueprint on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your repository
4. Click **"Apply"**

### 3. Set Environment Variables

**For FastAPI service:**
1. Go to `rag-chatbot-api` service
2. Click **"Environment"** tab
3. Set `GOOGLE_API_KEY` to your API key
4. Click **"Save Changes"**

**For Streamlit service:**
1. Go to `rag-chatbot-streamlit` service
2. Click **"Environment"** tab
3. Set `GOOGLE_API_KEY` to your API key
4. Click **"Save Changes"**

### 4. Wait for Deployment ⏳

Both services will build and deploy automatically (5-10 minutes).

### 5. Access Your App! 🎉

- **Streamlit UI**: `https://rag-chatbot-streamlit.onrender.com`
- **FastAPI Docs**: `https://rag-chatbot-api.onrender.com/docs`

---

## ✅ Verify Deployment

Test your FastAPI health endpoint:

```bash
curl https://rag-chatbot-api.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "service": "RAG Chatbot API", "version": "1.0.0"}
```

Open Streamlit UI and ask: **"What is Amit's total spending?"**

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Service won't start | Check logs in Render dashboard |
| API key error | Verify `GOOGLE_API_KEY` is set correctly |
| Streamlit can't connect | Update `FASTAPI_URL` to your FastAPI service URL |
| Slow first request | Free tier spins down after 15 min (upgrade to paid plan) |

---

## 📚 Full Documentation

For detailed instructions, troubleshooting, and advanced configuration:

👉 **See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**

---

## 💰 Pricing

- **Free Tier**: $0/month (services spin down after 15 min)
- **Starter**: $7/month per service (always running)
- **Standard**: $25/month per service (2 GB RAM)

---

**Need help?** Check the [full deployment guide](RENDER_DEPLOYMENT.md) or [Render docs](https://render.com/docs).
