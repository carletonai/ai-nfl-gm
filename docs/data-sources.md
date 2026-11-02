# Data sources

Everything the project needs is free. A non-commercial, attributed, open-source club project
is the use these sources exist for. (Practical read, not legal advice.)

## nflverse

Parquet assets on GitHub releases, no key, nearly all CC-BY 4.0 (FTN charting CC-BY-SA 4.0).
`ai_nfl_gm.data.nflverse.load(table)` downloads and caches them; add tables to
`nflverse.TABLES` as needed. Release page: https://github.com/nflverse/nflverse-data/releases

| Table (ours) | Asset | What it is | Notes |
| --- | --- | --- | --- |
| `contracts` | `contracts/historical_contracts.parquet` | Every contract, sourced from Over The Cap. `apy_cap_pct` (APY as % of cap at signing) is the market model's target; `inflated_apy` adjusts for cap growth | Per-year cap hits are nested in `cols`; **explode first** |
| `players` | `players/players.parquet` | One row per player with `gsis_id`, `pfr_id`, `otc_id`, `espn_id`, `pff_id` | The ID crosswalk. Known incomplete |
| `draft_picks` | `draft_picks/draft_picks.parquet` | Season, round, pick, team, `gsis_id`, `pfr_player_id`, `cfb_player_id`, career AV | Joins NFL to college on draft year + overall pick |
| `combine` | `combine/combine.parquet` | Combine measurables (from PFR) | |
| `trades` | `trades/trades.parquet` | Historical trades | The trade ledger to check the calculator against |
| `stats_player_reg` | `stats_player/stats_player_reg_{season}.parquet` | Season player stats (regular season) | Replace `reg` with `week` for weekly |
| `rosters` | `rosters/roster_{season}.parquet` | Season rosters with positions and birth dates | |
| `snap_counts` | `snap_counts/snap_counts_{season}.parquet` | Snap counts | The only free signal for OL |
| `pfr_advstats_*` | `pfr_advstats/advstats_season_{rec,pass,rush,def}.parquet` | PFR advanced stats, 2018+ | Pressures for EDGE live here |
| `ngs_*` | `nextgen_stats/ngs_{receiving,passing,rushing}.parquet` | Next Gen Stats, 2016+ | Separation, cushion, YAC over expected |

Data dictionaries: [contracts](https://nflreadr.nflverse.com/articles/dictionary_contracts.html),
[players](https://nflreadr.nflverse.com/articles/dictionary_players.html),
[draft picks](https://nflreadr.nflverse.com/articles/dictionary_draft_picks.html).

We read the parquet URLs directly rather than through `nflreadpy`, which is still beta and
lacks loaders for PFR advanced stats and ESPN QBR.

## CollegeFootballData (CFBD)

REST API with a free key (about 1,000 calls/month; an academic tier exists but needs a `.edu`
address). Use the `apinext` base URL; the legacy API is deprecated. Client:
`ai_nfl_gm.data.cfbd.CFBDClient`, which caches every response under `data/raw/cfbd/`.

| Endpoint | What | Quota note |
| --- | --- | --- |
| `/stats/player/season?year=` | Season stats for every player that year | One call per season; coverage 2004+ |
| `/draft/picks?year=` | NFL draft picks with college athlete id, pre-draft ranking and grade | The consensus-board input |
| recruiting, transfer portal, PPA | Recruiting rank, portal moves, predicted points added | As needed |

The whole college pull is roughly 50 calls. Cache once; never loop over players.
Terms permit commercial use; redistribution of raw data is restricted.

## Join keys

| Join | Key | Caveat |
| --- | --- | --- |
| contracts to players | `otc_id` | Some contracts lack an `otc_id` match; log, do not fuzzy-match |
| players to stats | `gsis_id` | |
| NFL draft to college | draft year + overall pick; check with `cfb_player_id` | CFBD's draft endpoint carries its own athlete id |
| position labels | `configs/sports/nfl.yaml` crosswalk | OTC, PFR and rosters disagree (EDGE vs DE/OLB, IDL vs DT); OLB is scheme-dependent |

## What not to do

- **Do not scrape Pro Football Reference or Over The Cap.** PFR's terms ban automated access.
  Use both only through nflverse.
- **PFF** grades and WAR are paywalled and excluded.
- **Do not commit raw dumps.** Training on the data is fine; redistributing it is where terms
  bite. Publish only derived tables.

## Coverage by position

The binding constraint is public data quality by position, not modelling.

| Position group | Quality | Best free signal |
| --- | --- | --- |
| QB | Good | Play-by-play EPA (1999+), Next Gen Stats (2016+), ESPN QBR |
| WR, TE | Good | Targets, EPA, YAC, NGS separation and cushion |
| RB | Good | Rushing EPA, success rate, NGS rush yards over expected |
| EDGE, IDL | Okay | Sacks, pressures from PFR advanced stats (2018+) |
| OL | Poor | Snap counts and PFR Approximate Value only |
| CB, S | Poor | PFR advanced coverage stats (2018+), Approximate Value |

## Other sources worth knowing

- **Over The Cap** and **Spotrac**: the baselines to match; browse, do not scrape.
- **Fitzgerald-Spielberger chart** (OTC) and the **Jimmy Johnson chart**: reference pick charts
  for the calculator (`ai_nfl_gm.valuation.draft_chart`).
- **Grinding the Mocks** / **NFL Mock Draft Database**: consensus expected draft position, the
  prospect "market price".
- **Big Data Bowl 2027** (Kaggle): combine tracking linked to NFL performance; overlaps the
  prospects workstream.
- **nfldata.org**: a normalized public API merging nflverse, PFR and FiveThirtyEight; handy for
  join keys, verify numbers against the primaries.

## Attribution

Credit nflverse, Over The Cap, Pro Football Reference and CollegeFootballData in anything
published (README, write-up, the page).
