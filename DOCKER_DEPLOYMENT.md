# Docker Deployment Guide - Agent Hercules

## Quick Start (Local Testing)

### Option 1: Using Docker Compose (Easiest)
```bash
docker-compose up
```
Visit: http://localhost:8501

### Option 2: Using Docker Commands
```bash
# Build image
docker build -t gym-manager .

# Run container
docker run -p 8501:8501 gym-manager
```

---

## Deploy to Render.com (5 Minutes) ⭐ RECOMMENDED

### Step 1: Push Docker files to GitHub
```bash
git add Dockerfile .dockerignore docker-compose.yml
git commit -m "Add Docker support for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `gym-manager-hercules`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Instance Type**: `Free` (or `Starter` for better performance)
6. Click **"Create Web Service"**

### Step 3: Wait for Deployment
- Build time: 3-5 minutes
- Your app will be live at: `https://gym-manager-hercules.onrender.com`

### Step 4: Seed Database (First Time Only)
Once deployed, run this via Render Shell:
```bash
python database/seed_data.py
```

---

## Deploy to Railway.app (3 Minutes) - FASTEST

### Step 1: Push to GitHub (if not done)
```bash
git add Dockerfile .dockerignore docker-compose.yml
git commit -m "Add Docker support"
git push origin main
```

### Step 2: Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway auto-detects Docker
7. Click **"Deploy"**

### Step 3: Get URL
- Deployment time: 2-3 minutes
- URL appears in project settings
- Example: `https://your-app.railway.app`

---

## Deploy to DigitalOcean (Production)

### Step 1: Push to GitHub
```bash
git push origin main
```

### Step 2: Create App
1. Go to https://cloud.digitalocean.com/apps
2. Click **"Create App"**
3. Connect GitHub repository
4. DigitalOcean detects Dockerfile automatically
5. Configure:
   - **Name**: `agent-hercules`
   - **Plan**: Basic ($5/month)
   - **Region**: Choose closest
6. Click **"Next"** → **"Create Resources"**

### Step 3: Configure Environment
- Port: `8501`
- Health Check: `/_stcore/health`

### Step 4: Deploy
- Build time: 5-7 minutes
- Professional URL with SSL included

---

## Environment Variables (Optional)

For production, you can add these:

```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

---

## Troubleshooting

### Build fails with "no space left"
- Use Render or Railway (better free tier)

### Container crashes on startup
- Check logs: `docker logs <container-id>`
- Verify requirements.txt is correct

### Database not persisting
- On Render: Add a persistent disk
- On Railway: Use volume mounts

### Can't access from browser
- Check firewall settings
- Verify port 8501 is exposed
- Check health endpoint: `/your-url/_stcore/health`

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Build Time |
|----------|-----------|-----------|------------|
| Render.com | ✅ 750hrs/month | $7/month | 3-5 min |
| Railway.app | $5 credit | $5-20/month | 2-3 min |
| DigitalOcean | ❌ | $5/month | 5-7 min |
| AWS ECS | ❌ | Variable | 10+ min |

---

## Production Checklist

- [ ] Docker files created
- [ ] Pushed to GitHub
- [ ] Platform selected (Render/Railway/DO)
- [ ] Deployment successful
- [ ] Database seeded
- [ ] Test login works
- [ ] Test file upload
- [ ] Test message generation
- [ ] Custom domain configured (optional)

---

## Updating Your App

### Method 1: Auto-deploy (Recommended)
Just push to GitHub:
```bash
git add .
git commit -m "Update feature X"
git push origin main
```
Render/Railway will auto-deploy in 2-3 minutes.

### Method 2: Manual
Rebuild Docker image:
```bash
docker-compose down
docker-compose up --build
```

---

## Support

- Render Docs: https://render.com/docs/docker
- Railway Docs: https://docs.railway.app/deploy/dockerfiles
- DigitalOcean Docs: https://docs.digitalocean.com/products/app-platform/

---

**Recommended: Start with Render.com free tier, upgrade to DigitalOcean when you have 10+ paying customers.**
