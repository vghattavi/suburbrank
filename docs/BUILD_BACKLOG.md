# SuburbRank Build Backlog

## Phase 1 — App Foundation
1. Create Blazor app structure
2. Add Identity-based auth
3. Add application user extension fields for subscription state
4. Add DB context and core entities
5. Add database migrations

## Phase 2 — Billing Foundation
6. Add Stripe config and billing service
7. Add checkout endpoint
8. Add webhook endpoint
9. Add paid-user authorization policy
10. Add pricing page wired to checkout

## Phase 3 — Fake Data + Scoring Core
11. Create suburb entity and fake NSW suburb generator
12. Create metric snapshot generator with realistic ranges
13. Create scoring run entity
14. Create deterministic scoring engine
15. Create score breakdown generator
16. Create explanation generator
17. Seed first published run automatically or via admin

## Phase 4 — User-Facing App
18. Build dashboard page
19. Build suburb rankings page
20. Build suburb profile page
21. Build reports library page
22. Build report detail page
23. Build report download/PDF generation

## Phase 5 — Admin Tools
24. Build admin layout/navigation
25. Build fake data generation page
26. Build scoring run page
27. Build report generation/publishing page
28. Build settings page for scoring weights

## Phase 6 — Product Polish
29. Add modern startup styling system
30. Add hero landing page copy and visuals
31. Add report preview on public site
32. Improve loading/empty states
33. Add seeded demo data for a strong first impression

## Phase 7 — Launch Readiness
34. Add environment config for Azure
35. Add production Stripe settings wiring
36. Add logging/error handling
37. Add basic legal/disclaimer copy
38. Add deploy checklist

## Immediate Build Order Recommendation
Start in this exact order:
1. foundation entities
2. fake data generator
3. scoring engine
4. dashboard + rankings + suburb detail
5. report generation
6. billing/paywall
7. public site polish

## Note
The most important thing is to get the app experience real and convincing. Fake data is acceptable for now, but the product should feel coherent and premium.
