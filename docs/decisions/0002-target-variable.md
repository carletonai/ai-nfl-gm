# 0002: Cross-position production label

**Status:** direction accepted, Nov 2, 2026; construction open (Valuation workstream).

## Context

"Price every player" needs one cross-position measure of what a player produced. The
market model's *target* is settled: `apy_cap_pct` from the contracts table, what the
market paid. This decision is about the *production* label used on the other side of
surplus, in the derived draft chart and as the prospect model's outcome.

The research notes laid out the off-the-shelf options and their compromises:

| Option | Pros | Cons | Who uses it |
| --- | --- | --- | --- |
| PFR Approximate Value | Free, every position, decades of coverage, in nflverse `draft_picks` | Crude; driven by counting stats and team success; weak for OL and defense | Chase Stuart's chart, ESPN's chart, Hadley et al. |
| Over The Cap Valuation | Free on the site, in dollars, position-aware | Must be scraped (not allowed); inherits OTC's model | OTC's bargain and surplus posts |
| Madden ratings | Free archives, every position, one 0-99 scale; the NFL's own chart (with CMU) uses years 3-5 | Opinion-based; lags performance; archive inconsistencies | NFL Ops x CMU draft chart |
| Build our own | Transparent; uses every data point we have; explainable per player | Covers QB and skill players well, others barely; the slowest path to a first number | Kevin Cole's Plus/Minus; nflWAR |

## Decision

**Build our own composite.** Jeremy's call (Nov 2, 2026): the project should make informed
decisions from as many data points as are available, assigning value to players from a
multitude of metrics rather than adopting one published number. The composite is the
production label everywhere a label is needed.

The interface is fixed in `ai_nfl_gm.valuation.player_value` (one row per player-season,
one `value` column on a cross-position scale, plus the components it came from). How the
components are combined and scaled is the Valuation workstream's design problem; the
candidate inputs and the open questions are listed in that module's docstring.

## Consequences

- WR first, as everywhere else: the richest free inputs (targets, receiving EPA, NGS
  separation, PFR receiving stats) and a published number (AV) to validate against.
- The composite should be validated two ways before anything downstream trusts it: rank
  agreement with AV, and how well it predicts second-contract APY on held-out seasons.
- Risk named in the research notes: building a label is the slowest path. Mitigation: the
  week-4 gate (WR valuations near Spotrac/OTC) can run on AV as a stand-in component while
  the composite matures, so the market and data streams are not blocked on it.
- Coverage is uneven by design: NGS from 2016, PFR advanced stats from 2018. The composite
  will be richer for recent seasons; document which components each season used.
- Components and weights are themselves data: version them in `configs/` so a value can be
  reproduced and explained later.
