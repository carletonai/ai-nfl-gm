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

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/carletonai/ai-nfl-gm.git
cd ai-nfl-gm
make setup   # installs everything into .venv and sets up the pre-commit hooks
make check   # lint + tests, the same as CI; if this passes you are ready
```

Everything runs through `uv run`, so there is no virtualenv to activate. On Windows without
`make`, open the `Makefile` and run the commands inside it directly.

Then prove the data is real:

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
| Data | clean per-position tables from nflverse and CFBD | pandas, data cleaning (best first stream) | `src/ai_nfl_gm/data/` |
| Market model | a model of what the league pays a player | regression, scikit-learn | `src/ai_nfl_gm/market/` |
| Prospects | college stats and combine results to NFL value and draft slot | feature engineering, ranking | `src/ai_nfl_gm/prospects/` |
| Valuation engine | aging curves, surplus value, our own draft chart, trade value | statistics, modelling judgment | `src/ai_nfl_gm/valuation/` |
| Product | the trade calculator and draft board | React, APIs | `src/ai_nfl_gm/api/`, `web/` |

Then:

1. Read your stream's section of [docs/workstreams.md](docs/workstreams.md): what to build
   first and which files to open.
2. Find a task. Unwritten functions raise `NotImplementedError` with a `TODO(<stream>)` note,
   so `grep -rn "TODO(" src/` is the backlog. Open issues are the other list.
3. Branch, build, open a PR. [CONTRIBUTING.md](CONTRIBUTING.md) is one page.

## Where to ask

`#ai-nfl-gm` on the CAIS Discord. Tag Jeremy for repo access or anything about scope.

## Everything else

The detail lives in [docs/](docs/): how the pipeline fits together, the data sources and
their rules, the term plan, decisions, and a reading list. Read it when you need it, not
before you start.

Code is [MIT](LICENSE). Data comes from [nflverse](https://github.com/nflverse) (mostly
CC-BY 4.0) and [CollegeFootballData](https://collegefootballdata.com) and stays under their
terms; [docs/data-sources.md](docs/data-sources.md) has the details and the attribution.
