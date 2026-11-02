# Workstreams

Five streams, each with a week-4 milestone that stands on its own if the others slip. Pick
one in `#ai-nfl-gm` and say which.

## Data

**Builds:** nflverse and CFBD pulls cached locally; player-ID crosswalk; unpacked year-by-year
cap hits; one clean table per position.

**Week-4 milestone:** a WR table joined across stats, contract, age and cap hits, 2011 to now.

**Start here:** `src/ai_nfl_gm/data/` (`nflverse.py` works; `contracts.py` and `crosswalk.py`
have the TODOs), `configs/sports/nfl.yaml` (the position crosswalk), `docs/data-sources.md`.
`make pull-data` downloads the core tables.

**First tasks:** explode the nested `cols` cap hits; decide the rookie/veteran flag; measure
how many contracts fail to join to `players` and why; verify the cap table in the sport config
against Over The Cap.

**Good for:** pandas, SQL, data cleaning; the best first stream for new members.

## Market model

**Builds:** contract value (`apy_cap_pct`) from the previous 2 to 3 seasons of production, age
and position; held-out error on the last two free-agency classes.

**Week-4 milestone:** a WR model beating `NaiveBaseline` on the held-out classes.

**Start here:** `src/ai_nfl_gm/market/` (`model.py` has the protocol and baseline, `evaluate.py`
the split and metrics, `features.py` the TODO). Install the `ml` extra.

**First tasks:** WR features from targets, receptions, yards, receiving EPA, target share,
plus age at signing; ridge regression first, then a regularised gradient-boosted model; report
MAE in % of cap on the held-out classes and compare with Spotrac/OTC numbers for the same
players.

**Good for:** regression, scikit-learn, gradient boosting.

## Prospects

**Builds:** college production, combine, recruiting rank and age to predicted NFL value and
draft slot.

**Week-4 milestone:** a prospect table for one draft class with predicted vs actual slot.

**Start here:** `src/ai_nfl_gm/prospects/`, `src/ai_nfl_gm/data/cfbd.py`. Needs a free CFBD key
in `.env`.

**First tasks:** pull one draft class from CFBD (draft picks with pre-draft grade, final two
college seasons of stats); join to nflverse `draft_picks` and `combine`; predict the consensus
slot first, then look for where production disagrees with it. Keep an eye on Big Data Bowl
2027 (see the reading list).

**Good for:** feature engineering, ranking metrics.

## Valuation engine

**Builds:** aging curves, surplus value, draft-pick values from pick history, the trade ledger.

**Week-4 milestone:** our own draft chart, checked against Fitzgerald-Spielberger and Jimmy
Johnson.

**Start here:** `src/ai_nfl_gm/valuation/` (`trade.py` and `draft_chart.py` have working
arithmetic and reference curves; `aging.py` and `surplus.py` have the TODOs).

**First tasks:** WR aging curve from player-seasons; surplus of drafted players over their
rookie deal by slot (needs the market model or, as a stand-in, second-contract APY); group
nearby picks and report floor/expected/ceiling; price the trades in nflverse `trades` and see
whether the answers are defensible.

**Good for:** statistics, modelling judgment.

## Product

**Builds:** the trade calculator and draft board on carletonai.com, reading the models'
outputs.

**Week-4 milestone:** a page that prices any two WR-and-pick packages against each other.

**Start here:** `src/ai_nfl_gm/api/` (`make api`, then http://127.0.0.1:8000/docs), `web/README.md`.

**First tasks:** decide where the page lives (this repo or `cais-website`); a trade form
that posts to `/trade/evaluate` and shows both sides with the Jimmy Johnson comparison;
team-context sliders and future-pick discount as inputs; later the draft board.

**Good for:** React or plain web, APIs.

## Cross-cutting

- **Target variable.** The FA price, the pick curve and the prospect projection all regress
  onto one cross-position value measure. Decide it in week 1 and record it in
  `docs/decisions/0002-target-variable.md`.
- **Position taxonomy.** Every raw label goes through the crosswalk in the sport config.
- **Scope.** The WR pipeline shipping is the milestone, not "the framework".
