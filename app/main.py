from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.fake_data import seed_database
from app.models import MetricSnapshot, ScoringRun, Suburb, SuburbScore, WeeklyReport

app = FastAPI(title="SuburbRank")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup_event():
    seed_database()


def db_session() -> Session:
    return SessionLocal()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "brand": "SuburbRank",
            "title": "Data-driven suburb rankings for Australian property investors",
        },
    )


@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return templates.TemplateResponse(
        request,
        "pricing.html",
        {
            "brand": "SuburbRank",
            "price": "$20/month",
        },
    )


@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):
    return templates.TemplateResponse(request, "how_it_works.html", {"brand": "SuburbRank"})


@app.get("/app/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
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

        return templates.TemplateResponse(
            request,
            "dashboard.html",
            {
                "brand": "SuburbRank",
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
        return templates.TemplateResponse(request, "suburbs.html", {"brand": "SuburbRank", "suburbs": suburbs_view})
    finally:
        db.close()


@app.get("/app/suburbs/{suburb_id}", response_class=HTMLResponse)
async def suburb_detail(request: Request, suburb_id: int):
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
        return templates.TemplateResponse(
            request,
            "suburb_detail.html",
            {"brand": "SuburbRank", "suburb": suburb, "snapshot": snapshot, "score": score},
        )
    finally:
        db.close()


@app.get("/app/reports", response_class=HTMLResponse)
async def reports(request: Request):
    db = db_session()
    try:
        reports = db.query(WeeklyReport).filter(WeeklyReport.is_published == True).order_by(WeeklyReport.published_at.desc()).all()
        return templates.TemplateResponse(request, "reports.html", {"brand": "SuburbRank", "reports": reports})
    finally:
        db.close()


@app.get("/app/reports/{slug}", response_class=HTMLResponse)
async def report_detail(request: Request, slug: str):
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
        return templates.TemplateResponse(
            request,
            "report_detail.html",
            {"brand": "SuburbRank", "report": report, "top_suburbs": top_suburbs},
        )
    finally:
        db.close()
