# SuburbRank MVP Spec

## 1. Product Summary
SuburbRank is a subscription SaaS product for Australian retail property investors. The MVP focuses on NSW and provides suburb rankings, suburb profile pages, and weekly reports.

The initial release uses auto-generated suburb data and an auto-generated scoring system so the app can be built and launched quickly.

## 2. Product Positioning
### Primary message
Data-driven suburb rankings for Australian property investors.

### Supporting message
Forward-looking suburb signals in a clean, modern dashboard.

### Tone
- modern startup
- sharp and credible
- simple, not corporate

## 3. Target User
Retail property investors in Australia.

## 4. MVP Scope
### Included
- Public landing page
- Pricing page
- Login/register
- Subscription paywall
- Dashboard with suburb rankings
- Individual suburb profile pages
- Weekly report page
- Downloadable report
- Admin area to generate fake data and scoring runs
- Auto-generated explanations and score breakdowns

### Excluded for now
- Real data integrations
- Map view
- Watchlists
- Alerts
- Multiple states
- ML/backtesting
- Deep portfolio features

## 5. Key User Flows
### Public visitor
1. Visits homepage
2. Understands product value
3. Clicks pricing / subscribe
4. Registers account
5. Pays subscription
6. Lands in app dashboard

### Paid user
1. Logs in
2. Views suburb ranking dashboard
3. Clicks into suburb profile
4. Views latest weekly report
5. Downloads report PDF

### Admin
1. Logs in
2. Generates fake suburb dataset
3. Runs scoring engine
4. Publishes latest weekly report

## 6. Core App Areas
### Public site
- /
- /pricing
- /how-it-works
- /login
- /register

### Paid app
- /app/dashboard
- /app/suburbs
- /app/suburbs/{id}
- /app/reports
- /app/reports/{id}
- /app/reports/{id}/download

### Admin
- /admin
- /admin/data
- /admin/scoring
- /admin/reports
- /admin/settings

## 7. Core Entities
### ApplicationUser
- Id
- Email
- Password hash / Identity fields
- StripeCustomerId
- StripeSubscriptionId
- SubscriptionStatus
- CurrentPeriodEnd
- CreatedAt

### Suburb
- Id
- Name
- State
- Postcode
- Lga
- Region
- Latitude
- Longitude
- IsActive

### MetricSnapshot
- Id
- SuburbId
- AsOfDate
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

### ScoringRun
- Id
- Name
- RunDate
- Notes
- WeightsJson
- SourceType
- IsPublished

### SuburbScore
- Id
- ScoringRunId
- SuburbId
- TotalScore
- Rank
- BreakdownJson
- Explanation
- SummaryLine
- RiskFlagsJson

### WeeklyReport
- Id
- Title
- Slug
- ScoringRunId
- PublishedAt
- Summary
- HeroSuburbId
- PdfPath
- IsPublished

## 8. Fake Data Generation
The system should generate believable NSW suburb data automatically.

### Requirements
- Generate 100 to 300 NSW suburbs initially
- Use plausible metric ranges
- Ensure some correlation between metrics
- Generate a mix of high-yield, high-growth, balanced, and weak suburbs
- Auto-generate suburb explanations and one-line summaries

### Fake data categories
- Metro growth suburbs
- Yield-focused regional suburbs
- Infrastructure-led emerging suburbs
- Overheated / risky suburbs
- Balanced investor suburbs

## 9. Scoring Engine v1
### Inputs
- Population growth
- Price growth 12m
- Rental yield
- Vacancy rate
- Listings trend
- Days on market
- Infrastructure score
- Derived demand/supply pressure

### Rules
- Normalize all metrics per scoring run
- Invert lower-is-better metrics where needed
- Apply weighted scoring
- Output score 0 to 100
- Rank all suburbs
- Generate explanation + key drivers automatically

### Important
Weights should be configurable internally, even if not fully exposed to users yet.

## 10. Dashboard Requirements
### Dashboard should show
- latest report summary
- top 10 suburbs
- ranked suburb table
- a featured suburb card
- quick stats across the latest run

### Ranked suburbs table
Columns:
- rank
- suburb
- score
- median price
- rental yield
- vacancy rate
- price growth 12m
- summary line

## 11. Suburb Profile Requirements
Each suburb profile should show:
- suburb name and rank
- total score
- key metrics
- score breakdown
- explanation
- top positive drivers
- risk flags
- latest report inclusion status

## 12. Weekly Report Requirements
The weekly report should include:
- title and publication date
- methodology summary
- top 10 suburbs
- narrative summary
- featured suburb
- downloadable PDF version

## 13. Design Direction
### Visual direction
- dark-on-light or dark mode capable modern startup UI
- clean cards
- generous spacing
- strong typography
- crisp tables
- subtle gradients

### Brand feel
- modern startup
- not old-school finance
- not flashy crypto
- trustworthy and polished

## 14. Launch Standard
MVP is launch-ready when:
- a user can register
- a user can subscribe
- a paid user can access dashboard
- the system has generated suburbs and scores
- the user can view suburb profiles
- the user can read the latest report
- the user can download the report
