"""Draft pick values.

Two kinds of chart live here:

* **Reference charts** teams and analysts already use (Jimmy Johnson; later
  Fitzgerald-Spielberger from Over The Cap). These ship as comparisons in the
  calculator, not as our answer.
* **Our derived chart**: the average surplus that players taken at each slot delivered
  over their rookie deal (market value of production minus the fixed rookie-scale cost).
  Every empirical chart since Massey & Thaler (2013) finds surplus peaks around the late
  first / early second round, far flatter than the Johnson chart.
"""

from __future__ import annotations

import math

import pandas as pd

#: Picks in a modern seven-round draft before compensatory picks.
PICKS_PER_DRAFT = 224


def jimmy_johnson_approx(pick: int) -> float:
    """Smooth approximation of the Jimmy Johnson chart: ``3000 * exp(-0.052 * (pick - 1))``.

    Pick 1 is 3000 points. The published table is step-wise; this curve is close enough
    for a sanity check. TODO(valuation): add the exact published table as a CSV fixture.
    """
    if pick < 1:
        raise ValueError("pick must be >= 1")
    return 3000.0 * math.exp(-0.052 * (pick - 1))


def reference_chart(name: str = "jimmy_johnson", n_picks: int = PICKS_PER_DRAFT) -> pd.DataFrame:
    """Return a reference chart as ``pick, value`` rows."""
    if name != "jimmy_johnson":
        raise NotImplementedError(f"Reference chart {name!r} not added yet.")
    picks = range(1, n_picks + 1)
    return pd.DataFrame({"pick": list(picks), "value": [jimmy_johnson_approx(p) for p in picks]})


def derive_surplus_chart(rookie_outcomes: pd.DataFrame) -> pd.DataFrame:
    """Average rookie-contract surplus by pick slot, smoothed across neighbouring picks.

    TODO(valuation): ``rookie_outcomes`` is one row per drafted player with his overall
    pick, market value of production over the rookie deal and rookie-scale cost. Group
    nearby picks into ranges (as Fitzgerald-Spielberger do) to strip out bust variance,
    and report floor/expected/ceiling quantiles rather than a single point.
    """
    raise NotImplementedError("Valuation workstream: derive the surplus-based draft chart.")
