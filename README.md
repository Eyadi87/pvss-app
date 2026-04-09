# PVSS — Predictive Virtual Sun Visor System

**The Problem:** Flask looks for templates inside a `templates/` subfolder.  
Your `index.html` was sitting next to `app.py` directly — Flask couldn't find it.

**The Fix:** Move `index.html` into a `templates/` folder.

### Correct Project Structure

```
pvss/
├── app.py
├── requirements.txt
├── Procfile              ← for deployment
└── templates/
    └── index.html        ← MUST be inside templates/
```

---

## Running Locally

```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000
```

---

## 🚀 Deploying to Render (Free, Recommended)

Render is the easiest free option — no credit card needed for hobby apps.

### Step 1 — Push to GitHub
1. Create a free account at https://github.com
2. Create a new repository (e.g. `pvss-app`)
3. Upload all your files keeping the folder structure:
   ```
   pvss/
   ├── app.py
   ├── requirements.txt
   ├── Procfile
   └── templates/
       └── index.html
   ```
   Or use Git from terminal:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/pvss-app.git
   git push -u origin main
   ```

### Step 2 — Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your `pvss-app` repo
4. Fill in these settings:
   - **Name:** pvss-app (anything you like)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Click **"Create Web Service"**
6. Wait ~2 minutes — Render builds and deploys automatically
7. Your app will be live at `https://pvss-app.onrender.com`

> ⚠️ Free Render apps "sleep" after 15 min of inactivity and take ~30s to wake up on the next visit. Upgrade to a paid plan ($7/month) to keep it always-on.

---

## Alternative: Deploy to Railway

1. Go to https://railway.app and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub Repo"**
3. Select your repo — Railway auto-detects Python and deploys
4. Your app gets a public URL instantly

---

## Alternative: Deploy to PythonAnywhere (Beginner-Friendly)

1. Sign up at https://www.pythonanywhere.com (free tier available)
2. Go to **Files** tab → upload `app.py`, `requirements.txt`, and `templates/index.html`
3. Go to **Consoles** → open a Bash console:
   ```bash
   pip install flask gunicorn
   ```
4. Go to **Web** tab → **Add a new web app** → **Flask** → point it to your `app.py`
5. Click **Reload** — your app is live at `https://yourusername.pythonanywhere.com`
