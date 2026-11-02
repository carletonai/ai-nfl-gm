# Contributing

Short version: branch from `main`, make `make check` pass, open a PR, get one review.

## Workflow

1. **Branch** from `main`, named `<stream>/<topic>`: `git switch -c data/explode-cap-hits`
   (or `market/wr-ridge-baseline`, `product/trade-page`). No push access? Fork and open the
   PR from your fork.
2. **Commit** in conventional-commit style, imperative and lowercase:
   `feat(data): explode per-year cap hits` (the type and scope lists are in
   [docs/conventions.md](docs/conventions.md)).
3. **Check** with `make check` (ruff and pytest, exactly what CI runs). `make format` fixes
   most lint for you.
4. **Open a PR** against `main` and fill in the template. One module plus its test is the
   ideal size; small PRs get reviewed fast.
5. **One approval** from another member merges it (squash).

## Three rules

- **No raw data in git.** `data/raw`, `data/interim` and `data/processed` are gitignored and
  pre-commit blocks files over 500 KB. A small derived table everyone needs goes in
  `data/shared/`, and the PR says so.
- **Tests run offline.** New behaviour comes with a small test. Anything that downloads is
  marked `@pytest.mark.network` and skipped by default.
- **Get data only through nflverse and the CFBD API.** Do not scrape Pro Football Reference or
  Over The Cap.

Code style, notebooks, how decisions get recorded and the rest:
[docs/conventions.md](docs/conventions.md).

## Help

Ask in `#ai-nfl-gm`. Tag Jeremy for repo access or anything about scope.
