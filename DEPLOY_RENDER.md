# Deploy SuburbRank to Render

## 1. Push the code to GitHub
Your repo:
- https://github.com/vghattavi/suburbrank

From the workspace root, the project folder is:
- /data/.openclaw/workspace/suburbrank

If using git locally on the machine:
```bash
cd /data/.openclaw/workspace/suburbrank
git init
git branch -M main
git remote add origin https://github.com/vghattavi/suburbrank.git
git add .
git commit -m "Initial SuburbRank FastAPI MVP"
git push -u origin main
```

If the remote already exists:
```bash
git remote set-url origin https://github.com/vghattavi/suburbrank.git
```

## 2. Create a Render web service
In Render:
- New +
- Web Service
- Connect GitHub repo: vghattavi/suburbrank

## 3. Use these settings
### Runtime
- Python

### Build Command
```bash
pip install --break-system-packages -r suburbrank/app/requirements.txt
```

### Start Command
```bash
PYTHONPATH=/opt/render/project/src python -m uvicorn suburbrank.app.main:app --host 0.0.0.0 --port $PORT
```

## 4. Environment variables
Set:
- ENVIRONMENT=production
- APP_BASE_URL=https://YOUR-RENDER-URL.onrender.com

Optional later:
- DATABASE_URL
- STRIPE_SECRET_KEY
- STRIPE_PRICE_ID
- STRIPE_WEBHOOK_SECRET

## 5. Expected first live routes
- /
- /pricing
- /how-it-works
- /app/dashboard
- /app/suburbs
- /app/reports

## 6. Notes
- Current app uses SQLite by default.
- That is acceptable for a first MVP/demo deployment.
- For a real SaaS launch, move to Postgres next.
- Auth, Stripe paywall, admin pages, and PDF generation are still next-phase work.
