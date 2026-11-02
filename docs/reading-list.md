# Reading list

Curated from the project's research notes (Nov 2026). Read the two "start here" items, then
whatever your workstream needs.

## Start here

- **[Unexpected Points](https://www.unexpectedpoints.com)** (Kevin Cole). Offseason
  team-building, draft grades from consensus boards plus surplus value, Plus/Minus for pricing
  non-QBs. The project in blog form.
- **The draft-value-chart literature, in order:** Massey & Thaler, *The Loser's Curse* (2013)
  (history in the [perthirtysix essay](https://perthirtysix.com/essay/nfl-draft-expected-value-curve))
  → [PFF: Revisiting the Loser's Curse](https://www.pff.com/news/nfl-revisiting-the-losers-curse-the-surplus-value-of-draft-picks)
  → [Brill & Wyner, CMSAC 2024](https://www.stat.cmu.edu/cmsac/conference/2024/assets/pdf/Brill24.pdf)
  ([code](https://github.com/snoopryan123/NFL_draft_chart_Ryan))
  → [NFL Ops x CMU: Building an NFL draft value chart](https://operations.nfl.com/updates/football-ops/building-an-nfl-draft-value-chart/).
- **Book:** Eager & Erickson, *Football Analytics with Python & R* (O'Reilly, 2023). Hands-on
  nflverse, EPA, regression. Onboarding for members new to football data.

## Pick value and the trade calculator (Valuation engine)

Every empirical chart since 2005 reaches the same conclusion: the Jimmy Johnson chart
overprices the top of the draft, and surplus peaks around the late first / early second round.

- [Brill & Wyner (2024)](https://www.stat.cmu.edu/cmsac/conference/2024/assets/pdf/Brill24.pdf): expected-performance and surplus curves; the real trade market follows neither. Fork the repo as a baseline.
- [NFL Ops x CMU](https://operations.nfl.com/updates/football-ops/building-an-nfl-draft-value-chart/): Madden years 3-5 as outcome; floor/expected/ceiling quantiles per pick.
- [The Open Trade Project](https://www.preprints.org/manuscript/202603.1149/v1) (2026): Rich Hill chart as prior, residuals from real trades, confidence intervals; grade a trade as a percentile.
- [Hadley et al. 2025](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1628223/full): how badly late picks are undervalued; a trade-up premium.
- [Fitzgerald-Spielberger chart](https://overthecap.com/?p=15949) (OTC): picks valued by second-contract money, grouped into ranges.
- [OTC: Chase Stuart's AV chart vs rookie guarantees](https://overthecap.com/?p=7346): cost curves and performance curves diverge.
- [ESPN: ranking the 2022 in-draft trades](https://www.espn.com.au/nfl/story/_/id/33861237/nfl-draft-2022-ranking-best-draft-trades-why-eagles-not-traded-no-13): what the calculator's output should say about a trade.
- [Jimmy Johnson chart table](https://www.fftoday.com/nfl/nfl_draftpick_value.htm): ship as the "what teams actually use" comparison.
- [Grandhisiri, arXiv 2025](https://arxiv.org/html/2504.07291v1): a loss-function framing for trade fairness (optional).

## Free-agent value and team-building (Market model, Valuation engine)

The cap market is roughly efficient for veterans; the exploitable inefficiency is rookie
contracts, so the FA model and the draft model are the same problem from two ends.

- [Mulholland & Jensen 2019](https://ideas.repec.org/a/eee/intfor/v35y2019i2p767-775.html): which positions reward elite investment; positional-value priors.
- [Wiley 2025, "Buying Wins"](https://openworks.wooster.edu/independentstudy/11517): cap allocation 2019-2023; a fully worked undergrad version of the same idea.
- Over The Cap methodology: [Expected Contract Value](https://overthecap.com/?p=11437), [cap cost vs value from the 2024 draft](https://overthecap.com/the-salary-cap-costs-and-value-added-from-the-2024-nfl-draft).
- [Caponomics](https://overthecap.com/?p=14199) (Zack Moore): positional spending of cap-era champions.
- [Sumer Sports, The Zone](https://sumersports.com/the-zone/tech): a front-office analytics vendor writing in public.
- [The Ringer on contract length vs years served](https://www.theringer.com/platform/amp/nfl/2019/3/15/18266458/free-agent-contracts-guaranteed-money-how-long-do-deals-last): only 62% of 2011-2015 FA contract years were served; the cut-risk adjustment.

## Draft board and prospects (Prospects)

The cheapest strong signal for where a prospect goes is the aggregated mock-draft market;
predict that first, then look for where college and combine data disagree with it.

- [Grinding the Mocks](https://grindingthemocks.substack.com) (Benjamin Robinson): Expected Draft Position from aggregated mocks; the market price per prospect.
- [NFL Mock Draft Database](https://www.nflmockdraftdatabase.com): consensus big boards; a second source.
- [FantasyPros mock-accuracy methodology](https://www.fantasypros.com/nfl-mock-draft-accuracy-methodology): how to score a board; which positions mocks miss most.
- [ProSportsDraftData](https://ginsburg1.r-universe.dev/ProSportsDraftData) (R): historical pre-draft rankings from ESPN, NFL.com, The Ringer, Walter Football.
- **[Big Data Bowl 2027](https://www.kaggle.com/c/nfl-big-data-bowl-2027)**: combine sensor tracking linked to NFL performance, with a student track and NFL mentorship. Announced Oct 8, 2026; prior editions closed mid-December to early January, so confirm the deadline on Kaggle now. Finalists present at the 2027 Combine.

## Data

- [nflverse-data releases](https://github.com/nflverse/nflverse-data/releases) and the [contracts](https://nflreadr.nflverse.com/articles/dictionary_contracts.html), [players](https://nflreadr.nflverse.com/articles/dictionary_players.html) and [draft picks](https://nflreadr.nflverse.com/articles/dictionary_draft_picks.html) dictionaries.
- [nflreadpy](https://pypi.org/project/nflreadpy/) (Python port, beta) and [nflreadpy issue #6](https://github.com/nflverse/nflreadpy/issues/6) on what is missing.
- [CFBD](https://collegefootballdata.com/), [terms](https://collegefootballdata.com/terms), [usage and access](https://apinext.collegefootballdata.com/usage-and-access), [data availability](https://apinext.collegefootballdata.com/data-availability).
- [CMU capstone: QB contract value from nflreadr contracts](https://stat.cmu.edu/capstoneresearch/460files/team2.pdf): a prior academic use of the same tables.
- [Open Source Football](https://opensourcefootball.com): the community the nflverse stack comes from.
