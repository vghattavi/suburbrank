from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Suburb(Base):
    __tablename__ = "suburbs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str] = mapped_column(String(10), default="NSW")
    postcode: Mapped[str] = mapped_column(String(10), default="")
    lga: Mapped[str] = mapped_column(String(120), default="")
    region: Mapped[str] = mapped_column(String(120), default="")
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    snapshots = relationship("MetricSnapshot", back_populates="suburb", cascade="all, delete-orphan")
    scores = relationship("SuburbScore", back_populates="suburb", cascade="all, delete-orphan")


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    suburb_id: Mapped[int] = mapped_column(ForeignKey("suburbs.id"))
    as_of_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    population_growth: Mapped[float] = mapped_column(Float)
    median_price: Mapped[float] = mapped_column(Float)
    price_growth_12m: Mapped[float] = mapped_column(Float)
    rental_yield: Mapped[float] = mapped_column(Float)
    vacancy_rate: Mapped[float] = mapped_column(Float)
    listings_trend: Mapped[float] = mapped_column(Float)
    days_on_market: Mapped[float] = mapped_column(Float)
    infrastructure_score: Mapped[float] = mapped_column(Float)
    demand_pressure: Mapped[float] = mapped_column(Float)
    supply_pressure: Mapped[float] = mapped_column(Float)
    source_type: Mapped[str] = mapped_column(String(50), default="generated")

    suburb = relationship("Suburb", back_populates="snapshots")


class ScoringRun(Base):
    __tablename__ = "scoring_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    notes: Mapped[str] = mapped_column(Text, default="")
    run_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    weights_json: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(50), default="generated")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    scores = relationship("SuburbScore", back_populates="run", cascade="all, delete-orphan")


class SuburbScore(Base):
    __tablename__ = "suburb_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scoring_run_id: Mapped[int] = mapped_column(ForeignKey("scoring_runs.id"))
    suburb_id: Mapped[int] = mapped_column(ForeignKey("suburbs.id"))
    total_score: Mapped[float] = mapped_column(Float)
    rank: Mapped[int] = mapped_column(Integer)
    breakdown_json: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str] = mapped_column(Text)
    summary_line: Mapped[str] = mapped_column(Text)
    risk_flags_json: Mapped[str] = mapped_column(Text, default="[]")

    run = relationship("ScoringRun", back_populates="scores")
    suburb = relationship("Suburb", back_populates="scores")


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    scoring_run_id: Mapped[int] = mapped_column(ForeignKey("scoring_runs.id"))
    summary: Mapped[str] = mapped_column(Text)
    pdf_path: Mapped[str] = mapped_column(String(255), default="")
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
