# SuburbRank Launch Plan

## Goal
Get SuburbRank live as fast as possible with the Python stack.

## Stack
- FastAPI
- Jinja2 templates
- SQLAlchemy
- SQLite for local dev
- PostgreSQL in production
- Stripe for subscription billing

## Current implementation status
Implemented in source:
- public pages
- dashboard shell
- suburb rankings
- suburb detail pages
- reports library and detail pages
- fake data seeding
- deterministic scoring engine
- SQLAlchemy models

Not yet implemented in source:
- authentication
- Stripe checkout/paywall wiring
- admin pages
- PDF generation

## Fastest path to launch
### Milestone 1
Get current app running in a proper Python environment.

### Milestone 2
Add auth + Stripe paywall.

### Milestone 3
Add admin generation controls.

### Milestone 4
Deploy to Azure App Service or container.

## Run instructions in a proper Python environment
1. Create a virtual environment
2. Install requirements
3. Run the app with uvicorn
4. Visit:
- /
- /pricing
- /how-it-works
- /app/dashboard
- /app/suburbs
- /app/reports

## Commands
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deploy direction
- Azure App Service for Containers or Python Web App
- environment vars for Stripe and database URL
- switch SQLite to Postgres
