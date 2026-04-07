# App Architecture

## Layers
### 1. Presentation
- FastAPI routes
- Jinja2 templates
- static CSS

### 2. Domain / application logic
- fake data generation
- scoring engine
- report assembly

### 3. Persistence
- SQLAlchemy models
- SQLite locally
- PostgreSQL later

## Route groups
### Public
- /
- /pricing
- /how-it-works

### Protected app (eventual)
- /app/dashboard
- /app/suburbs
- /app/suburbs/{id}
- /app/reports
- /app/reports/{slug}

### Admin (eventual)
- /admin/data
- /admin/scoring
- /admin/reports

### Billing (eventual)
- /billing/checkout
- /billing/success
- /billing/manage
- /stripe/webhook
