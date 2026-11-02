"""Cross-check the salary-cap table in the sport config against Over The Cap data.

Every nflverse contract carries ``apy`` (dollars) and ``apy_cap_pct`` (APY as a share of
the cap in the signing season), both from Over The Cap, so ``apy / apy_cap_pct`` is the
league cap that season as OTC used it. The median over every sizeable deal signed in a
season is a robust estimate of the cap to within rounding (a few tenths of a million).

Run with ``uv run python scripts/check_cap_table.py`` after ``make pull-data`` (or let it
download the contracts table). It prints the config value, the implied value and the gap,
and exits non-zero if any season is off by more than ``--tolerance`` (default 1%).
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

from ai_nfl_gm.config import load_sport_config
from ai_nfl_gm.data import nflverse

#: Deals below this share of the cap are ignored: apy_cap_pct is rounded, and on a small
#: deal that rounding swamps the signal.
MIN_CAP_PCT = 0.05


def implied_cap_by_season(contracts: pd.DataFrame) -> pd.DataFrame:
    """Median implied cap (in $M) per signing season, with the deal count and spread."""
    deals = contracts.loc[
        contracts["apy_cap_pct"].ge(MIN_CAP_PCT) & contracts["apy"].gt(0),
        ["year_signed", "apy", "apy_cap_pct"],
    ].copy()
    deals["implied_cap_musd"] = deals["apy"] / deals["apy_cap_pct"]
    grouped = deals.groupby("year_signed")["implied_cap_musd"]
    return pd.DataFrame(
        {
            "deals": grouped.size(),
            "implied_cap_musd": grouped.median(),
            "q25": grouped.quantile(0.25),
            "q75": grouped.quantile(0.75),
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sport", default="nfl")
    parser.add_argument("--tolerance", type=float, default=0.01, help="relative gap allowed")
    args = parser.parse_args()

    sport = load_sport_config(args.sport)
    contracts = nflverse.load("contracts", columns=["year_signed", "apy", "apy_cap_pct"])
    implied = implied_cap_by_season(contracts)

    print(
        f"{'season':>6} {'config':>9} {'implied':>9} {'gap':>7} {'deals':>6}  (implied = median apy / apy_cap_pct, $M)"
    )
    worst = 0.0
    for season, config_cap in sorted(sport.salary_cap_musd.items()):
        if season not in implied.index:
            print(f"{season:>6} {config_cap:>9.3f} {'n/a':>9}")
            continue
        est = float(implied.loc[season, "implied_cap_musd"])
        gap = (config_cap - est) / est
        worst = max(worst, abs(gap))
        flag = "  <-- check" if abs(gap) > args.tolerance else ""
        print(
            f"{season:>6} {config_cap:>9.3f} {est:>9.2f} {gap:>+7.2%} {int(implied.loc[season, 'deals']):>6}{flag}"
        )
    missing = [
        int(s)
        for s in implied.index
        if s >= sport.market_model_first_season and s not in sport.salary_cap_musd
    ]
    if missing:
        print(f"seasons in the data but not in the config: {missing}")
    if worst > args.tolerance:
        print(f"largest gap {worst:.2%} exceeds tolerance {args.tolerance:.0%}", file=sys.stderr)
        return 1
    print(f"all seasons within {args.tolerance:.0%} of the implied cap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
