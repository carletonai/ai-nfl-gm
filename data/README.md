# data

Local cache. Everything in `raw/`, `interim/` and `processed/` is gitignored; only the
`.gitkeep` files are tracked.

| Folder | Holds | Written by |
| --- | --- | --- |
| `raw/` | Untouched downloads, one file per source table (`raw/nflverse/*.parquet`, `raw/cfbd/**.json`) | `ai_nfl_gm.data.nflverse`, `ai_nfl_gm.data.cfbd`, `make pull-data` |
| `interim/` | Cleaned and joined tables that are inputs to models (exploded cap hits, position tables) | Data workstream |
| `processed/` | Feature tables and model outputs (surplus table, draft chart, prospect board) | Market, Valuation, Prospects |

**Do not commit raw data.** Redistribution is where licence terms bite; training is not. If a
derived table must be shared, keep it small, put it under `processed/` on purpose, and say so
in the PR. The pre-commit hook blocks files over 500 KB.

Point the cache elsewhere with `AI_NFL_GM_DATA_DIR` in `.env`.
