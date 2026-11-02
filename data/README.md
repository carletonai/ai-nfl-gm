# data

Local cache plus one tracked folder. Everything in `raw/`, `interim/` and `processed/` is
gitignored; `shared/` is tracked for small derived tables everyone needs.

| Folder | Holds | Written by |
| --- | --- | --- |
| `raw/` | Untouched downloads, one file per source table (`raw/nflverse/*.parquet`, `raw/cfbd/**.json`) | `ai_nfl_gm.data.nflverse`, `ai_nfl_gm.data.cfbd`, `make pull-data` |
| `interim/` | Cleaned and joined tables that are inputs to models (exploded cap hits, position tables) | Data workstream |
| `processed/` | Feature tables and model outputs (surplus table, draft chart, prospect board) | Market, Valuation, Prospects |
| `shared/` | Tracked. Small derived tables other streams or the page need (under 500 KB each) | Any stream, deliberately, named in the PR |

**Do not commit raw data.** Redistribution is where licence terms bite; training is not. If a
derived table must be shared, keep it small, put it in `shared/`, and say so in the PR. The
pre-commit hook blocks files over 500 KB.

Point the cache elsewhere with `AI_NFL_GM_DATA_DIR` in `.env`.
