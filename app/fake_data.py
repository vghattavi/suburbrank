import json
import random
from datetime import datetime
from .database import SessionLocal, engine, Base
from .models import MetricSnapshot, ScoringRun, Suburb, SuburbScore, WeeklyReport
from .scoring import WEIGHTS, score_snapshots

NSW_SUBURBS = [
    ("Maitland", "2320", "Maitland", "Hunter"),
    ("Orange", "2800", "Orange", "Central West"),
    ("Dubbo", "2830", "Dubbo", "Orana"),
    ("Wagga Wagga", "2650", "Wagga Wagga", "Riverina"),
    ("Tamworth", "2340", "Tamworth", "New England"),
    ("Bathurst", "2795", "Bathurst", "Central West"),
    ("Newcastle", "2300", "Newcastle", "Hunter"),
    ("Charlestown", "2290", "Lake Macquarie", "Hunter"),
    ("Kotara", "2289", "Newcastle", "Hunter"),
    ("Merewether", "2291", "Newcastle", "Hunter"),
    ("Parramatta", "2150", "Parramatta", "Sydney"),
    ("Penrith", "2750", "Penrith", "Sydney"),
    ("Liverpool", "2170", "Liverpool", "Sydney"),
    ("Campbelltown", "2560", "Campbelltown", "Sydney"),
    ("Blacktown", "2148", "Blacktown", "Sydney"),
    ("Castle Hill", "2154", "The Hills", "Sydney"),
    ("Rouse Hill", "2155", "The Hills", "Sydney"),
    ("Marsden Park", "2765", "Blacktown", "Sydney"),
    ("Kellyville", "2155", "The Hills", "Sydney"),
    ("Oran Park", "2570", "Camden", "Sydney"),
    ("Goulburn", "2580", "Goulburn Mulwaree", "Southern Tablelands"),
    ("Nowra", "2541", "Shoalhaven", "South Coast"),
    ("Wollongong", "2500", "Wollongong", "Illawarra"),
    ("Kiama", "2533", "Kiama", "South Coast"),
    ("Albury", "2640", "Albury", "Murray"),
    ("Lismore", "2480", "Lismore", "Northern Rivers"),
    ("Ballina", "2478", "Ballina", "Northern Rivers"),
    ("Coffs Harbour", "2450", "Coffs Harbour", "Mid North Coast"),
    ("Port Macquarie", "2444", "Port Macquarie-Hastings", "Mid North Coast"),
    ("Forster", "2428", "Mid-Coast", "Mid North Coast"),
]


def rand(a, b, digits=2):
    return round(random.uniform(a, b), digits)


def build_profile(name, region):
    profile = random.choice(["metro_growth", "regional_yield", "balanced", "infrastructure", "risky"])
    if profile == "metro_growth":
        return {
            "population_growth": rand(2.0, 6.2),
            "median_price": rand(850000, 1800000, 0),
            "price_growth_12m": rand(5.0, 14.0),
            "rental_yield": rand(2.8, 4.8),
            "vacancy_rate": rand(0.6, 2.0),
            "listings_trend": rand(-20.0, 5.0),
            "days_on_market": rand(18, 45, 0),
            "infrastructure_score": rand(3.0, 5.0),
        }
    if profile == "regional_yield":
        return {
            "population_growth": rand(0.8, 3.8),
            "median_price": rand(380000, 760000, 0),
            "price_growth_12m": rand(2.0, 10.0),
            "rental_yield": rand(4.8, 7.2),
            "vacancy_rate": rand(0.7, 2.6),
            "listings_trend": rand(-12.0, 10.0),
            "days_on_market": rand(25, 60, 0),
            "infrastructure_score": rand(2.0, 4.0),
        }
    if profile == "infrastructure":
        return {
            "population_growth": rand(1.8, 5.5),
            "median_price": rand(550000, 1200000, 0),
            "price_growth_12m": rand(4.0, 12.0),
            "rental_yield": rand(3.4, 5.8),
            "vacancy_rate": rand(0.8, 2.4),
            "listings_trend": rand(-15.0, 8.0),
            "days_on_market": rand(20, 52, 0),
            "infrastructure_score": rand(4.0, 5.0),
        }
    if profile == "risky":
        return {
            "population_growth": rand(-0.8, 2.2),
            "median_price": rand(650000, 2200000, 0),
            "price_growth_12m": rand(-6.0, 6.0),
            "rental_yield": rand(2.2, 4.4),
            "vacancy_rate": rand(2.8, 5.5),
            "listings_trend": rand(5.0, 28.0),
            "days_on_market": rand(55, 110, 0),
            "infrastructure_score": rand(1.0, 3.0),
        }
    return {
        "population_growth": rand(1.2, 4.2),
        "median_price": rand(500000, 1100000, 0),
        "price_growth_12m": rand(3.0, 9.5),
        "rental_yield": rand(3.5, 5.5),
        "vacancy_rate": rand(0.9, 2.8),
        "listings_trend": rand(-10.0, 8.0),
        "days_on_market": rand(24, 58, 0),
        "infrastructure_score": rand(2.0, 4.0),
    }


def derive_pressures(data):
    demand_pressure = round((data["population_growth"] * 0.6) + ((6 - data["vacancy_rate"]) * 0.8), 2)
    supply_pressure = round(((30 - data["listings_trend"]) * 0.2) + ((100 - data["days_on_market"]) * 0.03), 2)
    data["demand_pressure"] = demand_pressure
    data["supply_pressure"] = supply_pressure
    return data


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Suburb).count() > 0:
            return {"status": "already_seeded"}

        suburbs = []
        rows = []
        for name, postcode, lga, region in NSW_SUBURBS:
            suburb = Suburb(name=name, postcode=postcode, lga=lga, region=region, state="NSW")
            db.add(suburb)
            db.flush()
            suburbs.append(suburb)

            data = build_profile(name, region)
            data = derive_pressures(data)
            snapshot = MetricSnapshot(suburb_id=suburb.id, **data)
            db.add(snapshot)

            row = {"suburb_id": suburb.id, **data}
            rows.append(row)

        run = ScoringRun(
            name="Initial NSW Generated Run",
            notes="Auto-generated fake data run for MVP.",
            weights_json=json.dumps(WEIGHTS),
            source_type="generated",
            is_published=True,
        )
        db.add(run)
        db.flush()

        scored = score_snapshots(rows)
        for item in scored:
            score = SuburbScore(
                scoring_run_id=run.id,
                suburb_id=item["suburb_id"],
                total_score=item["score"],
                rank=item["rank"],
                breakdown_json=item["breakdown_json"],
                explanation=item["explanation"],
                summary_line=item["summary_line"],
                risk_flags_json=item["risk_flags_json"],
            )
            db.add(score)

        report = WeeklyReport(
            title="Top 10 NSW Suburbs — Launch Edition",
            slug="top-10-nsw-suburbs-launch-edition",
            scoring_run_id=run.id,
            summary="A launch-edition weekly report highlighting the strongest suburb signals in the generated NSW ranking universe.",
            is_published=True,
        )
        db.add(report)
        db.commit()
        return {"status": "seeded", "suburbs": len(NSW_SUBURBS)}
    finally:
        db.close()


if __name__ == "__main__":
    print(seed_database())
