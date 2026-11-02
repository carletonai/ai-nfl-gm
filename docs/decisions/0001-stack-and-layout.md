# 0001: Stack and repository layout

**Status:** accepted, Nov 2026.

## Context

The project outline (Oct 28, 2026) names the tools: Python, pandas, nflreadpy/nflverse, the
CFBD API, SQLite or Parquet cache, scikit-learn, LightGBM or XGBoost, statsmodels, a React
page with a small FastAPI backend, Git and GitHub PRs. The data feasibility check added two
constraints: read nflverse parquet directly because the Python wrapper is beta, and never
commit raw data.

## Decision

- **Python 3.11+**, pinned to 3.12 for development, managed with **uv** (lockfile committed).
  One `pyproject.toml`; modelling libraries in an `ml` extra and notebook tooling in a
  `notebooks` extra. `make setup` installs everything; the split exists so a lean `uv sync`
  (an API deploy, say) can skip them.
- **pandas + pyarrow** reading nflverse release parquet directly, cached under `data/raw/`
  (gitignored). Parquet, not SQLite, for the cache: zero setup and it is what nflverse ships.
- **src layout**, one package `ai_nfl_gm` with a subpackage per pipeline stage
  (`data`, `market`, `valuation`, `prospects`, `api`). Stage boundaries are DataFrames.
- **Sport as config**: `configs/sports/nfl.yaml` loaded through pydantic; the NBA is a
  sibling file.
- **ruff** for lint and format, **pytest** for tests, **pre-commit** for hygiene (including a
  500 KB file-size cap), **GitHub Actions** running the same `make check` on 3.11 and 3.12.
- **FastAPI** backend in this repo. The **React page** likely lives in the club's
  `cais-website` repo, which is the source of carletonai.com, and calls this API; `web/`
  records that and can host a standalone client if the Product stream prefers.
- **Conventional commits**, PR template, issue templates for tasks and bugs.

## Consequences

- Contributors need `uv` installed; nothing else.
- `nflreadpy` is not a dependency. If its loaders catch up, swapping is one module.
- Deploying the API is undecided; it is a small service and can be revisited in phase 3.
- No `LICENSE` yet: the maintainers choose one (MIT suggested) and add it.
