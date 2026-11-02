# AI NFL GM

A trade calculator and draft board for the NFL, built by the Carleton AI Society on free
data. We price every player and draft pick in one number, **surplus value** (what a player
produces minus what he costs against the salary cap), and use it to answer the three
questions a general manager faces: what to offer in free agency, whether a trade is fair,
and where a college prospect should go in the draft. The result goes live on
[carletonai.com](https://carletonai.com).

> **Status (Nov 2026):** scaffolding only. The layout, tooling and interfaces are here;
> the models are not. Building them is the project.

## Setup

You need [uv](https://docs.astral.sh/uv/getting-started/installation/); it fetches the right
Python for you.

```bash
git clone https://github.com/carletonai/ai-nfl-gm.git
cd ai-nfl-gm
make setup   # installs everything into .venv and sets up the pre-commit hooks
make check   # lint + tests, the same as CI; if this passes you are ready
```

Everything runs through `uv run`, so there is no virtualenv to activate. On Windows without
`make`, run `uv sync --all-extras`, `uv run pre-commit install` and `uv run pytest` instead.

Then prove the data is real (paste into `uv run python`):

```python
from ai_nfl_gm.data import nflverse

contracts = nflverse.load("contracts")  # downloads once, cached under data/raw/
contracts[["player", "position", "year_signed", "apy_cap_pct"]].head()
```

## Pick a task

The project is five workstreams, one per stage of the pipeline. Pick the one that matches
what you want to learn and say so in `#ai-nfl-gm`.

| Stream | You will build | Good if you like | Code |
| --- | --- | --- | --- |
| Data | clean per-position tables from nflverse and CollegeFootballData (CFBD) | pandas, data cleaning (best first stream) | `src/ai_nfl_gm/data/` |
| Market model | a model of what the league pays a player | regression, scikit-learn | `src/ai_nfl_gm/market/` |
| Prospects | college stats and combine results to NFL value and draft slot | feature engineering, ranking | `src/ai_nfl_gm/prospects/` |
| Valuation engine | aging curves, surplus value, our own draft chart, trade value | statistics, modelling judgment | `src/ai_nfl_gm/valuation/` |
| Product | the trade calculator and draft board | React, APIs | `src/ai_nfl_gm/api/`, `web/` |

Then:

1. Read your stream's section of [docs/workstreams.md](docs/workstreams.md): what to build
   first and which files to open.
2. Find a task. Unwritten functions raise `NotImplementedError` with a `TODO(<stream>)` note,
   so `git grep -n "TODO(" src/` is the backlog.
3. Branch, build, open a PR. [CONTRIBUTING.md](CONTRIBUTING.md) is one page.

## Where to ask

[`#ai-nfl-gm`](https://carletonai.com) on the CAIS Discord. Tag Jeremy for repo access or anything about scope.

## Everything else

The detail lives in [docs/](docs/): how the pipeline fits together, the data sources and
their rules, the term plan, decisions, and a reading list. Read it when you need it, not
before you start.

Code is [MIT](LICENSE). Data comes from [nflverse](https://github.com/nflverse) (which packages
Over The Cap and Pro Football Reference data) and
[CollegeFootballData](https://collegefootballdata.com), under their own terms; see
[docs/data-sources.md](docs/data-sources.md).
