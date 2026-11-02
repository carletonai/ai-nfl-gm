# 0002: Cross-position target variable

**Status:** open. Decide in week 1; the market model, the pick curve and the prospect
projection all regress onto it.

## Context

"Price every player" needs one cross-position measure of player value. Every free option is
a compromise; the paid one (PFF) is the industry standard and is excluded.

| Option | Pros | Cons | Who uses it |
| --- | --- | --- | --- |
| PFR Approximate Value | Free, every position, decades of coverage, in nflverse `draft_picks` | Crude; driven by counting stats and team success; weak for OL and defense | Chase Stuart's chart, ESPN's chart, Hadley et al. |
| Over The Cap Valuation | Free on the site, in dollars, position-aware | Must be scraped (not allowed); inherits OTC's model | OTC's bargain and surplus posts |
| Madden ratings | Free archives, every position, one 0-99 scale; the NFL's own chart (with CMU) uses years 3-5 | Opinion-based; lags performance; archive inconsistencies | NFL Ops x CMU draft chart |
| Build our own | Transparent; good for a write-up | Covers QB and skill players well, others barely; a semester of work | Kevin Cole's Plus/Minus; nflWAR |

For the **market model** the target is settled: `apy_cap_pct` from the contracts table. This
decision is about the *production* side used in surplus, the pick curve and prospects.

## Proposal

AV or Madden for the cross-position curve, with a position-specific EPA-based model layered
on top for QB and skill players where the data supports it. Record the choice and its known
blind spots here so later results are read with them in mind.

## Decision

_Not yet taken._
