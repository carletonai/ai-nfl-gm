# Data sources

Everything the project needs is free. A non-commercial, attributed, open-source club project
is the use these sources exist for. (Practical read, not legal advice.)

## nflverse

Parquet assets on GitHub releases, no key. Most releases are CC-BY 4.0; FTN charting and
participation data from 2023 on are CC-BY-SA 4.0; the fantasy player-id table is GPL-3 (avoid
it); and the `trades` and draft-value tables come from the nflverse/nfldata repo, which has no
licence file, so attribute them and never redistribute them raw.
`ai_nfl_gm.data.nflverse.load(table)` downloads and caches them; add tables to
`nflverse.TABLES` as needed. Release page: https://github.com/nflverse/nflverse-data/releases

| Table (ours) | Asset | What it is | Notes |
| --- | --- | --- | --- |
| `contracts` | `contracts/historical_contracts.parquet` | Every contract, sourced from Over The Cap. `apy_cap_pct` (APY as % of cap at signing) is the market model's target; `inflated_apy` adjusts for cap growth | Per-year cap hits (`cap_number`, `cap_percent`) are nested in `season_history`; contract types (`Drafted`, `UDFA`, `UFA`, `Extension`, `Franchise`, ...) in `contract_history`; **explode first**. Positions use OTC labels (`ED`, `IDL`, `LT`, `RG`) |
| `players` | `players/players.parquet` | One row per player with `gsis_id`, `pfr_id`, `otc_id`, `espn_id`, `pff_id` | The ID crosswalk. Known incomplete |
| `draft_picks` | `draft_picks/draft_picks.parquet` | Season, round, pick (overall), team, `gsis_id`, `pfr_player_id`, `cfb_player_id`, career stats, Approximate Value as `w_av` (weighted) and `dr_av` (with drafting team) | `cfb_player_id` is a Sports-Reference college slug (`joe-burrow-1`), not a CFBD id; `car_av` is empty on every row, use `w_av` |
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

We read the parquet URLs directly rather than through `nflreadpy` (0.1.5, labelled beta). It
does ship `load_pfr_advstats`; what it lacks is ESPN QBR (`espn_data/qbr_season_level.parquet`
on the releases). Reading the files directly keeps every table one line away.

## CollegeFootballData (CFBD)

REST API with a free key (about 1,000 calls/month per account; the academic tier needs a
`.edu` address, which Carleton's `.ca` is not). One key per person: the terms do not allow
pooling keys. Base URL `https://api.collegefootballdata.com`, the official `cfbd` Python
client's default (`apinext` was the v2 preview host; the planning notes' advice to use it is
out of date). Client: `ai_nfl_gm.data.cfbd.CFBDClient`, which caches every response under
`data/raw/cfbd/`.

| Endpoint | What | Quota note |
| --- | --- | --- |
| `/stats/player/season?year=` | Season stats for every player that year | One call per season; coverage 2004+ |
| `/draft/picks?year=` | NFL draft picks with college athlete id, `overall` pick, pre-draft ranking and grade | The consensus-board input. CFBD's `pick` is within the round; join on `overall` |
| recruiting, transfer portal, PPA | Recruiting rank, portal moves, predicted points added | As needed |

The whole college pull is roughly 50 calls. Cache once; never loop over players.
Terms permit commercial use; redistribution of raw data is restricted.

## Join keys

| Join | Key | Caveat |
| --- | --- | --- |
| contracts to players | `otc_id` | Some contracts lack an `otc_id` match; log, do not fuzzy-match |
| players to stats | `gsis_id` | |
| NFL draft to college | `draft_picks.season` + `pick` = CFBD `year` + `overall` | `cfb_player_id` is a Sports-Reference slug and CFBD's athlete id is CFBD's own, so the ids do not join each other; CFBD's `pick` is within-round |
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
