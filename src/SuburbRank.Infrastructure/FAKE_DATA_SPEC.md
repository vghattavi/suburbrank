# Fake Data Generation Spec

## Goal
Generate a believable NSW suburb universe for MVP demos and product development.

## Seed size
- initial default: 150 suburbs
- configurable: 100 to 300

## Profiles to generate
- Metro growth
- Regional yield
- Infrastructure-led emerging
- Balanced investor suburb
- Risky / overheated suburb

## Fields to generate
- suburb metadata
- metric snapshot values
- score
- summary line
- explanation
- risk flags

## Example metric ranges
- PopulationGrowth: -1.5 to 6.5
- MedianPrice: 350000 to 2800000
- PriceGrowth12m: -8 to 18
- RentalYield: 2.1 to 7.8
- VacancyRate: 0.4 to 5.8
- ListingsTrend: -25 to 35
- DaysOnMarket: 14 to 120
- InfrastructureScore: 1 to 5

## Correlation rules
- high growth suburbs tend to have lower vacancy and lower days on market
- high-yield suburbs often have lower median prices
- overheated suburbs may have strong momentum but weak yield and elevated risk flags
- infrastructure-led suburbs should skew toward stronger future-facing explanation text
