from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.auth import hash_password, verify_password
from app.config import settings
from app.database import SessionLocal
from app.fake_data import seed_database
from app.models import MetricSnapshot, ScoringRun, Suburb, SuburbScore, User, WeeklyReport

app = FastAPI(title="SuburbRank")
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, same_site="lax")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup_event():
    seed_database()


def db_session() -> Session:
    return SessionLocal()


def current_user(request: Request, db: Session):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


def render_template(request: Request, template_name: str, context: dict, status_code: int = 200):
    db = db_session()
    try:
        user = current_user(request, db)
    finally:
        db.close()
    full_context = {"brand": "SuburbRank", "current_user": user, **context}
    return templates.TemplateResponse(request, template_name, full_context, status_code=status_code)


def require_auth(request: Request):
    if request.session.get("user_id"):
        return None
    return RedirectResponse(url="/login", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_template(
        request,
        "home.html",
        {
            "title": "Data-driven suburb rankings for Australian property investors",
        },
    )


@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return render_template(
        request,
        "pricing.html",
        {
            "price": "$20/month",
        },
    )


@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):
    return render_template(request, "how_it_works.html", {})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/app/dashboard", status_code=303)
    return render_template(request, "signup.html", {"error": None, "email": ""})


@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    normalized_email = email.strip().lower()
    db = db_session()
    try:
        existing_user = db.query(User).filter(User.email == normalized_email).first()
        if existing_user:
            return render_template(
                request,
                "signup.html",
                {"error": "That email is already registered.", "email": normalized_email},
                status_code=400,
            )
        if len(password) < 8:
            return render_template(
                request,
                "signup.html",
                {"error": "Password must be at least 8 characters.", "email": normalized_email},
                status_code=400,
            )
        if len(password.encode("utf-8")) > 72:
            return render_template(
                request,
                "signup.html",
                {"error": "Password is too long.", "email": normalized_email},
                status_code=400,
            )
        user = User(email=normalized_email, password_hash=hash_password(password))
        db.add(user)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            return render_template(
                request,
                "signup.html",
                {"error": "Signup is temporarily unavailable.", "email": normalized_email},
                status_code=500,
            )
        db.refresh(user)
        request.session["user_id"] = user.id
        return RedirectResponse(url="/app/dashboard", status_code=303)
    finally:
        db.close()


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/app/dashboard", status_code=303)
    return render_template(request, "login.html", {"error": None, "email": ""})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    normalized_email = email.strip().lower()
    db = db_session()
    try:
        user = db.query(User).filter(User.email == normalized_email, User.is_active == True).first()
        if not user or not verify_password(password, user.password_hash):
            return render_template(
                request,
                "login.html",
                {"error": "Invalid email or password.", "email": normalized_email},
                status_code=400,
            )
        request.session["user_id"] = user.id
        return RedirectResponse(url="/app/dashboard", status_code=303)
    finally:
        db.close()


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.get("/app/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    auth_redirect = require_auth(request)
    if auth_redirect:
        return auth_redirect

    db = db_session()
    try:
        latest_run = db.query(ScoringRun).order_by(ScoringRun.run_date.desc()).first()
        report = None
        dashboard_rows = []
        top_suburb = None

        if latest_run:
            report = (
                db.query(WeeklyReport)
                .filter(WeeklyReport.scoring_run_id == latest_run.id, WeeklyReport.is_published == True)
                .order_by(WeeklyReport.published_at.desc())
                .first()
            )
            score_rows = (
                db.query(SuburbScore, Suburb, MetricSnapshot)
                .join(Suburb, Suburb.id == SuburbScore.suburb_id)
                .join(MetricSnapshot, MetricSnapshot.suburb_id == Suburb.id)
                .filter(SuburbScore.scoring_run_id == latest_run.id)
                .order_by(SuburbScore.rank.asc())
                .all()
            )
            dashboard_rows = [
                {
                    "suburb_id": suburb.id,
                    "rank": score.rank,
                    "name": suburb.name,
                    "postcode": suburb.postcode,
                    "score": round(score.total_score, 1),
                    "demand_supply": round(snapshot.demand_pressure * 7, 1),
                    "rental": round(snapshot.rental_yield * 14, 1),
                    "infrastructure": round(snapshot.infrastructure_score * 17.5, 1),
                    "income": round(snapshot.price_growth_12m * 7, 1),
                    "population": round(snapshot.population_growth * 16, 1),
                    "median_price": round(snapshot.median_price),
                    "yield_percent": round(snapshot.rental_yield, 2),
                    "vacancy_percent": round(snapshot.vacancy_rate, 2),
                    "summary": score.summary_line,
                }
                for score, suburb, snapshot in score_rows
            ]
            if dashboard_rows:
                top_suburb = dashboard_rows[0]

        return render_template(
            request,
            "dashboard.html",
            {
                "table_rows": dashboard_rows,
                "top_suburb": top_suburb,
                "report": report,
                "suburb_count": len(dashboard_rows),
            },
        )
    finally:
        db.close()


@app.get("/app/suburbs", response_class=HTMLResponse)
async def suburbs(request: Request):
    auth_redirect = require_auth(request)
    if auth_redirect:
        return auth_redirect

    db = db_session()
    try:
        latest_run = db.query(ScoringRun).order_by(ScoringRun.run_date.desc()).first()
        rows = []
        if latest_run:
            rows = (
                db.query(SuburbScore, Suburb)
                .join(Suburb, Suburb.id == SuburbScore.suburb_id)
                .filter(SuburbScore.scoring_run_id == latest_run.id)
                .order_by(SuburbScore.rank.asc())
                .all()
            )
        suburbs_view = [
            {
                "suburb_id": suburb.id,
                "name": suburb.name,
                "rank": score.rank,
                "total_score": round(score.total_score, 2),
                "summary_line": score.summary_line,
            }
            for score, suburb in rows
        ]
        return render_template(request, "suburbs.html", {"suburbs": suburbs_view})
    finally:
        db.close()


@app.get("/app/suburbs/{suburb_id}", response_class=HTMLResponse)
async def suburb_detail(request: Request, suburb_id: int):
    auth_redirect = require_auth(request)
    if auth_redirect:
        return auth_redirect

    db = db_session()
    try:
        suburb = db.query(Suburb).filter(Suburb.id == suburb_id).first()
        latest_run = db.query(ScoringRun).order_by(ScoringRun.run_date.desc()).first()
        snapshot = db.query(MetricSnapshot).filter(MetricSnapshot.suburb_id == suburb_id).order_by(MetricSnapshot.as_of_date.desc()).first()
        score = None
        if latest_run:
            score = (
                db.query(SuburbScore)
                .filter(SuburbScore.suburb_id == suburb_id, SuburbScore.scoring_run_id == latest_run.id)
                .first()
            )
        return render_template(
            request,
            "suburb_detail.html",
            {"suburb": suburb, "snapshot": snapshot, "score": score},
        )
    finally:
        db.close()


@app.get("/app/reports", response_class=HTMLResponse)
async def reports(request: Request):
    auth_redirect = require_auth(request)
    if auth_redirect:
        return auth_redirect

    db = db_session()
    try:
        reports = db.query(WeeklyReport).filter(WeeklyReport.is_published == True).order_by(WeeklyReport.published_at.desc()).all()
        return render_template(request, "reports.html", {"reports": reports})
    finally:
        db.close()


@app.get("/app/reports/{slug}", response_class=HTMLResponse)
async def report_detail(request: Request, slug: str):
    auth_redirect = require_auth(request)
    if auth_redirect:
        return auth_redirect

    db = db_session()
    try:
        report = db.query(WeeklyReport).filter(WeeklyReport.slug == slug).first()
        top_rows = []
        if report:
            top_rows = (
                db.query(SuburbScore, Suburb)
                .join(Suburb, Suburb.id == SuburbScore.suburb_id)
                .filter(SuburbScore.scoring_run_id == report.scoring_run_id)
                .order_by(SuburbScore.rank.asc())
                .limit(10)
                .all()
            )
        top_suburbs = [
            {
                "name": suburb.name,
                "total_score": round(score.total_score, 2),
                "summary_line": score.summary_line,
            }
            for score, suburb in top_rows
        ]
        return render_template(
            request,
            "report_detail.html",
            {"report": report, "top_suburbs": top_suburbs},
        )
    finally:
        db.close()
