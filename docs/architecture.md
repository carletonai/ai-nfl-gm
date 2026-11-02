# Architecture

One pipeline, six stages, surplus value in the middle. Everything upstream exists to produce
that one number; everything downstream spends it, as draft-pick currency in trades or as a
rank on the draft board.

```
nflverse ──┐
           ├─▶ data/ ──▶ market/ ──▶ valuation/ (aging, surplus) ──▶ valuation/ (draft chart, trade)
CFBD ──────┘      │                                                          │
                  └─────────────────▶ prospects/ ─────────────────────────────┤
                                                                              ▼
                                                                            api/ ──▶ web page
```

## Stages and their contracts

The tables passed between stages are the interface between workstreams. Each stage says
what it consumes and what it produces; column names follow the source data dictionaries.

| Stage | Package | Consumes | Produces |
| --- | --- | --- | --- |
| 1. Data | `ai_nfl_gm.data` | nflverse parquet (contracts, players, draft picks, combine, stats); CFBD JSON | one row per contract-year (cap hits exploded); one clean player-season table per position; player-ID and position crosswalks |
| 2. Market model | `ai_nfl_gm.market` | signings with prior-season production, age, position | predicted `apy_cap_pct` per signing; held-out error on the last two FA classes |
| 3. Surplus | `ai_nfl_gm.valuation.aging`, `.surplus` | player-seasons, market model, remaining cap hits | projected seasons; surplus (% of cap) per player over controlled years |
| 4. Trade value | `ai_nfl_gm.valuation.draft_chart`, `.trade` | surplus of drafted players over rookie deals; rookie-scale cost | our draft chart (expected surplus by slot, with floor/ceiling); trade evaluation = sum per side |
| 5. Prospects | `ai_nfl_gm.prospects` | CFBD stats, combine, recruiting, age; consensus slot | predicted NFL value and slot per prospect, over/underdrafted flags |
| 6. Product | `ai_nfl_gm.api`, `web/` | outputs of 3, 4, 5 as tables | trade calculator and draft board |

## Design rules

- **Sport is a config.** League rules (cap table, position groups, crosswalk, discounts) live in
  `configs/sports/<sport>.yaml` and are loaded through `ai_nfl_gm.config.load_sport_config`.
  Code reads them; it does not hard-code them.
- **Data access is one layer.** Only `ai_nfl_gm.data` and `scripts/` touch the network or the
  cache. Models take DataFrames.
- **Small data, simple models.** A few hundred deals per position: ridge regression or a
  regularised gradient-boosted model, not deep nets. Every model implements the
  `MarketModel` protocol so the evaluation harness can compare them.
- **One evaluation harness.** `ai_nfl_gm.market.evaluate` owns the held-out split so every
  model is scored on the same deals.
- **Thin API.** Request handlers validate, call into `valuation`, and return. No inference or
  loading in handlers.
- **Notebook to module.** Explore in `notebooks/`; when something is right, move it into
  `src/` with a test.

## Where the frontend lives

The outline calls for a React page on carletonai.com with a small FastAPI backend. The site's
source is the club's `cais-website` repo, so the page may live there and call this API. `web/`
holds that decision and, if the Product workstream prefers, a standalone client. See
[decisions/0001-stack-and-layout.md](decisions/0001-stack-and-layout.md).
