import json
from statistics import mean

WEIGHTS = {
    "population_growth": 0.18,
    "price_growth_12m": 0.14,
    "rental_yield": 0.14,
    "vacancy_rate": 0.12,
    "listings_trend": 0.10,
    "days_on_market": 0.10,
    "infrastructure_score": 0.12,
    "demand_pressure": 0.05,
    "supply_pressure": 0.05,
}

LOWER_IS_BETTER = {"vacancy_rate", "days_on_market"}


def _normalize(values):
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def score_snapshots(snapshot_rows):
    metric_names = list(WEIGHTS.keys())
    raw = {metric: [row[metric] for row in snapshot_rows] for metric in metric_names}
    normalized = {metric: _normalize(vals) for metric, vals in raw.items()}

    results = []
    for idx, row in enumerate(snapshot_rows):
        contributions = {}
        total = 0.0
        for metric in metric_names:
            value = normalized[metric][idx]
            if metric in LOWER_IS_BETTER:
                value = 1 - value
            contribution = value * WEIGHTS[metric]
            contributions[metric] = round(contribution * 100, 2)
            total += contribution

        score = round(total * 100, 2)
        top_drivers = sorted(contributions.items(), key=lambda x: x[1], reverse=True)[:3]
        summary = build_summary(row, score)
        explanation = build_explanation(row, score, top_drivers)
        risks = build_risk_flags(row)
        results.append(
            {
                "suburb_id": row["suburb_id"],
                "score": score,
                "breakdown_json": json.dumps(contributions),
                "summary_line": summary,
                "explanation": explanation,
                "risk_flags_json": json.dumps(risks),
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    for rank, item in enumerate(results, start=1):
        item["rank"] = rank
    return results


def build_summary(row, score):
    if score >= 85:
        return "High-conviction suburb with strong investor signal alignment."
    if score >= 75:
        return "Well-balanced suburb with attractive investment fundamentals."
    if row["rental_yield"] >= 5.5:
        return "Yield-led suburb with income appeal and improving local conditions."
    return "Mixed but potentially interesting suburb with selective strengths."


def build_explanation(row, score, top_drivers):
    drivers = ", ".join(name.replace("_", " ") for name, _ in top_drivers)
    return (
        f"This suburb scored {score} based on a combination of {drivers}. "
        f"The current profile shows population growth of {row['population_growth']}%, "
        f"rental yield of {row['rental_yield']}%, vacancy rate of {row['vacancy_rate']}%, "
        f"and infrastructure score of {row['infrastructure_score']}/5. "
        f"It ranks well within the NSW universe because its supply-demand balance and overall investor signal profile are competitive."
    )


def build_risk_flags(row):
    flags = []
    if row["vacancy_rate"] > 3.5:
        flags.append("Elevated vacancy may weaken near-term rental pressure.")
    if row["days_on_market"] > 70:
        flags.append("Longer selling times may indicate softer liquidity.")
    if row["price_growth_12m"] < 0:
        flags.append("Negative recent price momentum increases uncertainty.")
    if row["median_price"] > 1800000:
        flags.append("High entry price may reduce accessibility for many investors.")
    return flags
