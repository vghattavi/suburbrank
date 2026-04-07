# Core Entities

## ApplicationUser
- Id
- Email
- StripeCustomerId
- StripeSubscriptionId
- SubscriptionStatus
- CurrentPeriodEnd
- CreatedAtUtc

## Suburb
- Id
- Name
- State
- Postcode
- Lga
- Region
- Latitude
- Longitude
- IsActive
- CreatedAtUtc

## MetricSnapshot
- Id
- SuburbId
- AsOfDateUtc
- PopulationGrowth
- MedianPrice
- PriceGrowth12m
- RentalYield
- VacancyRate
- ListingsTrend
- DaysOnMarket
- InfrastructureScore
- DemandPressure
- SupplyPressure
- SourceType

## ScoringRun
- Id
- Name
- RunDateUtc
- Notes
- WeightsJson
- SourceType
- IsPublished
- CreatedAtUtc

## SuburbScore
- Id
- ScoringRunId
- SuburbId
- TotalScore
- Rank
- BreakdownJson
- Explanation
- SummaryLine
- RiskFlagsJson
- CreatedAtUtc

## WeeklyReport
- Id
- Title
- Slug
- ScoringRunId
- PublishedAtUtc
- Summary
- HeroSuburbId
- PdfPath
- IsPublished
- CreatedAtUtc
