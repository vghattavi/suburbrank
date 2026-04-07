# Next Implementation Steps

Because dotnet is unavailable in the current runtime, do this next when SDK access exists:

1. Create solution and projects
2. Add Identity + EF Core + PostgreSQL
3. Create domain entities from docs
4. Implement fake suburb generator
5. Implement scoring engine
6. Build dashboard, suburbs list, suburb detail pages
7. Build weekly report pages + PDF generation
8. Add Stripe billing/paywall
9. Deploy to Azure

## Minimal CLI plan
- dotnet new sln -n SuburbRank
- dotnet new blazor -n SuburbRank.Web
- dotnet new classlib -n SuburbRank.Core
- dotnet new classlib -n SuburbRank.Infrastructure
- dotnet new xunit -n SuburbRank.Tests
- dotnet sln add ...

## Packages to add later
- Microsoft.AspNetCore.Identity.EntityFrameworkCore
- Npgsql.EntityFrameworkCore.PostgreSQL
- Stripe.net
- QuestPDF
- Hangfire.AspNetCore
- Hangfire.PostgreSql
