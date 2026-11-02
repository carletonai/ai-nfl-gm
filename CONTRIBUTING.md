# Contributing

Thanks for joining. This page is how we work; the project itself is described in the
[README](README.md) and [docs/](docs/).

## Set up

```bash
make setup   # uv sync --all-extras
make hooks   # pre-commit install
make check   # ruff + pytest, same as CI
```

Everything runs through `uv run`, so you never need to activate the virtualenv. Python 3.11
or newer; `.python-version` pins 3.12 for `uv`.

## Pick work

- Workstreams and their week-4 milestones are in [docs/workstreams.md](docs/workstreams.md).
- Open work is in GitHub Issues (use the *Task* template) and in the code:
  `grep -rn "TODO(" src/ --include="*.py"`.
- Say what you are picking up in `#ai-nfl-gm` so two people do not do the same thing.

## Branches and pull requests

1. Branch from `main`: `<stream>/<short-description>`, e.g. `data/explode-cap-hits`,
   `market/wr-ridge-baseline`, `product/trade-page`.
2. Commit as you go (see commit messages below). Run `make check` before pushing.
3. Open a PR against `main` and fill in the template. Small PRs get reviewed fast; a PR that
   touches one module and adds its test is the ideal size.
4. One approval from another member merges it. Squash-merge unless the history matters.

CI runs ruff (lint and format) and pytest on Python 3.11 and 3.12. A red check blocks merge.

## Commit messages

Conventional commits: `<type>(<scope>): <description>`, imperative, lowercase, no period.

| Type | Use for |
| --- | --- |
| `feat` | new feature, module, endpoint, table |
| `fix` | bug fix |
| `refactor` | restructuring with no behaviour change |
| `test` | tests only |
| `docs` | docs only |
| `chore` | tooling, config, dependencies |
| `perf` | performance |
| `ci` | CI changes |

Scope is the package or workstream: `data`, `market`, `valuation`, `prospects`, `api`, `web`,
`configs`, `docs`. Examples:

```
feat(data): explode per-year cap hits from contracts
fix(market): drop franchise-tag deals from the training set
docs(decisions): record the target-variable choice
```

Do not add AI co-author trailers or override authorship with `--author`.

## Code style

- `ruff` formats and lints (`make format` fixes what it can). Line length 100.
- Type hints on public functions. Docstrings say what a function returns and which
  table it expects, because the tables are the interface between workstreams.
- Pure functions over DataFrames; no module-level data loading. Reading from disk or the
  network happens in `ai_nfl_gm.data` and in `scripts/`, not inside models.
- Log, do not print, inside the package. `print` is fine in `scripts/`.
- Column names follow the source table (`apy_cap_pct`, `gsis_id`) so the data dictionary
  stays the documentation.

## Tests

- `pytest` under `tests/`. Tests run offline by default; anything that downloads is marked
  `@pytest.mark.network` and skipped unless you ask for it (`make test-network`).
- New behaviour comes with a test on a small fixture. Build fixtures by hand or by saving a
  few rows of a real table under `tests/fixtures/` (keep them under a few KB).
- A model PR reports its held-out metric in the description, using
  `ai_nfl_gm.market.evaluate` so numbers are comparable.

## Notebooks

Notebooks are for exploring. Name them `NN_<stream>_<topic>.ipynb` under `notebooks/`,
clear outputs before committing (`jupyter nbconvert --clear-output --inplace`), and when
something in a notebook turns out to be right, move it into `src/` with a test. Notebooks
are not imported by anything.

## Data

- Never commit raw downloads. `data/raw`, `data/interim` and `data/processed` are gitignored
  and pre-commit blocks files over 500 KB. If a derived table must be shared, put it in
  `data/shared/` (tracked), keep it small, and mention it in the PR.
- Secrets go in `.env` (gitignored). `.env.example` lists the names.
- Use the sources only as described in [docs/data-sources.md](docs/data-sources.md).

## Decisions

Anything that changes how everyone works or what the models predict (target variable,
aging-curve method, position taxonomy, hosting) gets a short note in
[docs/decisions/](docs/decisions/): context, decision, consequences. Propose it in a PR so
the discussion is attached to the text.

## Getting help

Ask in `#ai-nfl-gm`. Tag Jeremy for repo access or anything about scope.
