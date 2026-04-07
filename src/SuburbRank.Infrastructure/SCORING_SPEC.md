# Scoring Engine Spec

## Inputs
- PopulationGrowth
- PriceGrowth12m
- RentalYield
- VacancyRate
- ListingsTrend
- DaysOnMarket
- InfrastructureScore
- DemandPressure
- SupplyPressure

## Processing rules
1. Normalize numeric metrics per scoring run.
2. Invert lower-is-better metrics:
   - VacancyRate
   - DaysOnMarket
3. Convert negative supply trend into positive tight-supply signal where appropriate.
4. Apply configurable weights.
5. Produce 0-100 score.
6. Rank suburbs descending.
7. Generate score breakdown and top drivers.

## Initial weighting direction
- PopulationGrowth: 0.18
- PriceGrowth12m: 0.14
- RentalYield: 0.14
- VacancyRate: 0.12
- ListingsTrend: 0.10
- DaysOnMarket: 0.10
- InfrastructureScore: 0.12
- DemandPressure: 0.05
- SupplyPressure: 0.05

## Outputs
- Total score
- Rank
- Metric contribution breakdown
- Summary line
- Explanation
- Risk flags
