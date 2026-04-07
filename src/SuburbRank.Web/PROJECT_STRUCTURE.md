# Intended Project Structure

SuburbRank.sln
- src/SuburbRank.Web
- src/SuburbRank.Core
- src/SuburbRank.Infrastructure
- tests/SuburbRank.Tests

## SuburbRank.Core
Contains:
- domain entities
- value objects
- scoring interfaces
- report interfaces

## SuburbRank.Infrastructure
Contains:
- EF Core db context
- fake data generation
- scoring implementation
- stripe integration
- report generation

## SuburbRank.Web
Contains:
- UI pages/components
- auth wiring
- admin pages
- API/controllers if needed
