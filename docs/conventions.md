# Conventions

How we write code, tests and commits. [CONTRIBUTING.md](../CONTRIBUTING.md) is the short
version; this is the detail behind it.

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

## Branches and pull requests

- Branch from `main`: `<stream>/<short-description>`.
- Commit as you go and run `make check` before pushing.
- CI runs ruff (lint and format) and pytest on Python 3.11 and 3.12. A red check blocks merge.
- One approval from another member merges it. Squash-merge unless the history matters.

## Code style

- `ruff` formats and lints (`make format` fixes what it can). Line length 100.
- Type hints on public functions. Docstrings say what a function returns and which table
  it expects, because the tables are the interface between workstreams.
- Pure functions over DataFrames; no module-level data loading. Reading from disk or the
  network happens in `ai_nfl_gm.data` and in `scripts/`, not inside models.
- Log, do not print, inside the package. `print` is fine in `scripts/`.
- Column names follow the source table (`apy_cap_pct`, `gsis_id`) so the data dictionary
  stays the documentation.
- Unwritten functions raise `NotImplementedError` with a `TODO(<workstream>)` note saying
  what belongs there; keep that habit so `grep -rn "TODO(" src/` stays the backlog.

## Tests

- `pytest` under `tests/`. Tests run offline by default; anything that downloads is marked
  `@pytest.mark.network` and skipped unless you ask for it (`make test-network`).
- New behaviour comes with a test on a small fixture. Build fixtures by hand or by saving a
  few rows of a real table under `tests/fixtures/` (keep them under a few KB).
- A model PR reports its held-out metric in the description, using
  `ai_nfl_gm.market.evaluate` so numbers are comparable.

## Notebooks

Explore in `notebooks/`; when something turns out to be right, move it into `src/` with a
test. Naming and output-clearing rules are in [notebooks/README.md](../notebooks/README.md).

## Data

- Never commit raw downloads. `data/raw`, `data/interim` and `data/processed` are
  gitignored and pre-commit blocks files over 500 KB. If a derived table must be shared, put
  it in `data/shared/` (tracked), keep it small, and mention it in the PR.
  [data/README.md](../data/README.md) says what goes in each folder.
- Secrets go in `.env` (gitignored). `.env.example` lists the names.
- Use the sources only as described in [data-sources.md](data-sources.md).

## Decisions

Anything that changes how everyone works or what the models predict (target variable,
aging-curve method, position taxonomy, hosting) gets a short note in
[decisions/](decisions/): context, decision, consequences. Propose it in a PR so the
discussion is attached to the text.
