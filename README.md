# AI NFL GM

Price every NFL player and draft pick in one currency, **surplus value**: what a player
produces minus what he costs against the salary cap, as a share of the cap. From that one
number come the three calls a general manager makes: what to offer in free agency, whether a
trade is fair, and where a college prospect should go in the draft. The result is a public
trade calculator and draft board on [carletonai.com](https://carletonai.com), built on free data.

This is the Carleton AI Society term project. NFL first because the data is best there; the
code treats the sport as a config so the NBA can follow.

> **Status (Nov 2026):** scaffolding only. The layout, tooling and interfaces are here;
> the models are not. Pick a workstream below and start filling in the `TODO`s.

## The six lines

| Line | AI NFL GM |
| --- | --- |
| Objective | Price every NFL player and draft pick in surplus value, as a share of the salary cap |
| Data | [nflverse](https://github.com/nflverse/nflverse-data/releases) (stats, contracts, draft history; free) and the [CollegeFootballData](https://collegefootballdata.com) API for prospects |
| Baseline | The contract valuations Spotrac and Over The Cap publish; match them before beating them |
| Metric | Market model: hold out the last two free-agency classes, report error on predicted contract value. Prospect model: rank correlation with actual draft slot and with career value |
| Deliverable | Open trade calculator and draft board on carletonai.com; code here; end-of-term showcase |
| Roles | Five workstreams: Data, Market model, Prospects, Valuation engine, Product |

## Quickstart

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/carletonai/ai-nfl-gm.git
cd ai-nfl-gm
make setup          # uv sync --all-extras: creates .venv with everything
make hooks          # pre-commit hooks (ruff, no large files, no secrets)
cp .env.example .env   # add your CFBD_API_KEY if you work on prospects
make check          # lint + tests; this is what CI runs
make pull-data      # core nflverse tables into data/raw (~20 MB); --seasons FIRST LAST to change the range
make api            # FastAPI dev server at http://127.0.0.1:8000/docs
```

Prefer `uv run <cmd>` over activating the venv; the Makefile is only a list of those commands.
On Windows without `make`, run the commands inside the Makefile directly.

```python
from ai_nfl_gm.data import nflverse

contracts = nflverse.load("contracts")  # cached under data/raw/nflverse/
wr = contracts[contracts["position"] == "WR"]
wr[["player", "year_signed", "apy_cap_pct"]].head()
```

## How the code is laid out

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
docs/                architecture, data sources, workstreams, decisions, reading list
web/                 where the React page goes, or a pointer to the website repo
```

Modules that are not written yet raise `NotImplementedError` with a `TODO(<workstream>)`
note saying what belongs there. `grep -rn "TODO(" src/ --include="*.py"` is the backlog.

## Workstreams

Pick one in the channel and say which. Each has a week-4 milestone that stands on its own.

| Stream | Builds | Week-4 milestone | Code lives in |
| --- | --- | --- | --- |
| Data | nflverse and CFBD pulls, player-ID crosswalk, exploded cap hits, one clean table per position | WR table joined: stats, contract, age, cap hits, 2011 to now | `data/` |
| Market model | Contract value from the previous 2 to 3 seasons of production, age, position | WR model beating the naive baseline on the held-out classes | `market/` |
| Prospects | College production, combine, recruiting rank, age to predicted NFL value and slot | A prospect table for one draft class with predicted vs actual slot | `prospects/` |
| Valuation engine | Aging curves, surplus value, draft-pick values from pick history, the trade ledger | Our own draft chart, checked against Fitzgerald-Spielberger and Jimmy Johnson | `valuation/` |
| Product | The trade calculator and draft board, reading the models' outputs | A page that prices any two WR-and-pick packages against each other | `api/`, `web/` |

Details, including what each stream should read first: [docs/workstreams.md](docs/workstreams.md).

## Term plan

Twelve weeks in three phases. A phase ends when its gate is met, not when the calendar says so.

1. **Weeks 1 to 4, stand up.** Data pulled and joined, WR market model trained, first surplus numbers. Gate: WR valuations within a sensible margin of Spotrac and OTC on the held-out classes.
2. **Weeks 5 to 8, breadth.** EDGE and QB, aging curves, our own draft chart, trade calculator v0. Gate: a calculator that prices real recent trades and we can defend the answers.
3. **Weeks 9 to 12, draft and showcase.** Prospect model on one draft class, draft board, public page, write-up. Gate: live page on carletonai.com and a showcase night.

## Data rules

- **Do not commit raw data.** `data/raw`, `data/interim` and `data/processed` are gitignored, and
  a pre-commit hook blocks files over 500 KB. A derived table that everyone needs (features,
  model outputs) goes in `data/shared/`, small and on purpose, and the PR says so.
- **Use sources through nflverse.** Do not scrape Pro Football Reference or Over The Cap; PFR's
  terms ban automated access. PFF data is paywalled and excluded.
- **Know the blind spots.** Public data is strong for QB, WR, RB and TE, decent for EDGE, thin
  for OL and DB. That is why receivers come first.

Full detail: [docs/data-sources.md](docs/data-sources.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md): branches, conventional commits, PRs, tests, the
notebook-to-module habit. Decisions that affect everyone are recorded in
[docs/decisions/](docs/decisions/). Background reading is in [docs/reading-list.md](docs/reading-list.md).

## Attribution

Data from [nflverse](https://github.com/nflverse) (CC-BY 4.0; FTN charting CC-BY-SA 4.0),
which packages Over The Cap contracts, Pro Football Reference statistics and NFL Next Gen Stats;
college data from [CollegeFootballData.com](https://collegefootballdata.com). The NFL data
belongs to its owners and their terms govern. This is a non-commercial club project.

## License

Code is [MIT](LICENSE). The data is not ours to license: nflverse releases are CC-BY 4.0 (FTN
CC-BY-SA 4.0) and the underlying NFL data belongs to its owners; see Attribution above.
