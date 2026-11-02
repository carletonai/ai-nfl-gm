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
| 3. Surplus | `ai_nfl_gm.valuation.player_value`, `.aging`, `.surplus` | player-seasons, market model, remaining cap hits | composite player value per player-season (the production label); projected seasons; surplus (% of cap) per player over controlled years |
| 4. Trade value | `ai_nfl_gm.valuation.draft_chart`, `.trade` | surplus of drafted players over rookie deals; rookie-scale cost | our draft chart (expected surplus by slot, with floor/ceiling); trade evaluation = sum per side |
| 5. Prospects | `ai_nfl_gm.prospects` | CFBD stats, combine, recruiting, age; consensus slot | predicted NFL value and slot per prospect, over/underdrafted flags |
| 6. Product | `ai_nfl_gm.api`, `web/` | outputs of 3, 4, 5 as tables | trade calculator and draft board |

## Repository layout

One pipeline, in the order it runs. Each stage is a package under `src/ai_nfl_gm/`.

```
src/ai_nfl_gm/
├── config.py        settings (.env) and the sport config (configs/sports/nfl.yaml)
├── data/            1. pull nflverse + CFBD, ID and position crosswalks, explode cap hits
├── market/          2. what the league pays for production, age, position (+ held-out eval)
├── valuation/       3-4. aging curves, surplus, our draft chart, trade value
├── prospects/       5. college stats + combine -> predicted NFL value vs consensus slot
└── api/             6. FastAPI backend the trade calculator and draft board read
configs/             sports/ league rules as data (cap table, positions, crosswalk); draft_charts/ reference tables
data/                raw / interim / processed caches (gitignored) and shared/ for published tables
notebooks/           exploration; code that survives moves into src/
scripts/             CLI entry points (pull data, later: train, export tables)
tests/               pytest; no network unless marked
models/              trained model files (gitignored)
docs/                this folder
web/                 React page, or a pointer to the cais-website repo; see web/README.md
```

Modules that are not written yet raise `NotImplementedError` with a `TODO(<workstream>)`
note saying what belongs there. `git grep -n "TODO(" src/` is the backlog.

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
