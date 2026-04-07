# SuburbRank Page Map

## Public Pages

### 1. Home (`/`)
Purpose:
- explain what SuburbRank is
- establish modern startup credibility
- drive sign-up

Sections:
- hero
- how it works
- why suburb ranking matters
- sample suburb cards/table preview
- CTA

### 2. Pricing (`/pricing`)
Purpose:
- show $20/month plan
- clarify what is included
- trigger checkout

Sections:
- plan card
- feature list
- FAQ
- subscribe CTA

### 3. How It Works (`/how-it-works`)
Purpose:
- explain suburb scoring in plain English
- show methodology at a high level

Sections:
- data inputs
- ranking model
- weekly reports
- suburb profile details

## Auth Pages
- `/account/login`
- `/account/register`

## Paid App Pages

### 4. Dashboard (`/app/dashboard`)
Purpose:
- give a fast summary of latest rankings and report

Components:
- latest report hero
- top 10 suburb cards/table
- key market stats
- featured suburb
- link to full suburb rankings

### 5. Suburb Rankings (`/app/suburbs`)
Purpose:
- browse top-ranked suburbs

Components:
- search bar
- filters (later if needed)
- sortable ranking table
- latest run badge

### 6. Suburb Profile (`/app/suburbs/{id}`)
Purpose:
- inspect a single suburb in detail

Components:
- suburb header
- score card
- metrics grid
- score breakdown card
- explanation card
- risk flags
- included-in-report indicator

### 7. Reports Library (`/app/reports`)
Purpose:
- show published weekly reports

Components:
- report cards/list
- publication date
- latest report highlight

### 8. Report Detail (`/app/reports/{id}`)
Purpose:
- display a weekly report in-app

Components:
- title + summary
- methodology box
- top 10 ranked suburbs
- featured suburb section
- narrative insights
- download PDF button

## Billing Pages
### 9. Billing Success (`/billing/success`)
Purpose:
- confirm payment and route user into app

### 10. Billing Manage (`/billing/manage`)
Purpose:
- manage Stripe subscription

## Admin Pages

### 11. Admin Home (`/admin`)
Purpose:
- operational summary

### 12. Data Generation (`/admin/data`)
Purpose:
- generate fake suburb datasets

Actions:
- choose suburb count
- generate dataset
- view latest generation timestamp

### 13. Scoring Runs (`/admin/scoring`)
Purpose:
- run ranking engine

Actions:
- trigger scoring
- choose or view weights
- publish scoring run

### 14. Reports Admin (`/admin/reports`)
Purpose:
- create/publish weekly reports from runs

Actions:
- select latest run
- generate report
- publish report
- regenerate PDF

### 15. Settings (`/admin/settings`)
Purpose:
- edit platform defaults

Settings:
- scoring weights
- branding copy snippets
- default fake data generation settings
