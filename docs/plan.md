# Project plan

The Carleton AI Society term project for Fall 2026. NFL first because the data is best
there; the code treats the sport as a config so the NBA can follow.

## The six lines

| Line | AI NFL GM |
| --- | --- |
| Objective | Price every NFL player and draft pick in surplus value, as a share of the salary cap |
| Data | [nflverse](https://github.com/nflverse/nflverse-data/releases) (stats, contracts, draft history; free) and the [CollegeFootballData](https://collegefootballdata.com) API for prospects |
| Baseline | The contract valuations Spotrac and Over The Cap publish; match them before beating them |
| Metric | Market model: hold out the last two free-agency classes, report error on predicted contract value. Prospect model: rank correlation with actual draft slot and with career value |
| Deliverable | Open trade calculator and draft board on carletonai.com; code here; end-of-term showcase |
| Roles | Five workstreams: Data, Market model, Prospects, Valuation engine, Product (see [workstreams.md](workstreams.md)) |

## Term plan

Twelve weeks in three phases. A phase ends when its gate is met, not when the calendar
says so.

1. **Weeks 1 to 4, stand up.** Data pulled and joined, WR market model trained, first
   surplus numbers. Gate: WR valuations within a sensible margin of Spotrac and OTC on the
   held-out classes.
2. **Weeks 5 to 8, breadth.** EDGE and QB, aging curves, our own draft chart, trade
   calculator v0. Gate: a calculator that prices real recent trades and we can defend the
   answers.
3. **Weeks 9 to 12, draft and showcase.** Prospect model on one draft class, draft board,
   public page, write-up. Gate: live page on carletonai.com and a showcase night.

## Why receivers first

Public data is strong for QB, WR, RB and TE, decent for EDGE, thin for OL and DB (the
table in [data-sources.md](data-sources.md#coverage-by-position)). The WR pipeline shipping
end to end is the milestone, not "the framework"; EDGE and QB follow in phase 2.
