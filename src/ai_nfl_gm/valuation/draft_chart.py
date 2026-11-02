"""Draft pick values.

Two kinds of chart live here:

* **Reference charts** teams and analysts already use. The Jimmy Johnson table ships as
  ``configs/draft_charts/jimmy_johnson.csv`` and is the "what teams actually use"
  comparison in the calculator, not our answer. Fitzgerald-Spielberger (Over The Cap)
  is the next one to add.
* **Our derived chart**: the average surplus that players taken at each slot delivered
  over their rookie deal (market value of production minus the fixed rookie-scale cost).
  Every empirical chart since Massey & Thaler (2013) finds surplus peaks around the late
  first / early second round, far flatter than the Johnson chart.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from ai_nfl_gm.config import get_settings

#: Picks in a seven-round draft before compensatory picks.
PICKS_PER_DRAFT = 224

#: Reference chart name -> CSV file under ``configs/draft_charts/`` (``pick,value`` rows).
REFERENCE_CHARTS = {
    "jimmy_johnson": "jimmy_johnson.csv",
}


def reference_chart(name: str = "jimmy_johnson", configs_dir: Path | None = None) -> pd.DataFrame:
    """Return a published reference chart as ``pick, value`` rows, ascending by pick."""
    try:
        filename = REFERENCE_CHARTS[name]
    except KeyError as exc:
        raise KeyError(
            f"Unknown reference chart {name!r}. Known: {sorted(REFERENCE_CHARTS)}"
        ) from exc
    root = configs_dir or get_settings().configs_dir
    chart = pd.read_csv(root / "draft_charts" / filename, comment="#")
    return chart.sort_values("pick", ignore_index=True)


def jimmy_johnson_approx(pick: int) -> float:
    """Smooth stand-in for the Johnson chart: ``3000 * exp(-0.052 * (pick - 1))``.

    This is MetricGate's exponential approximation. It matches the published table only
    at pick 1 and around pick 32; it runs about 40% high through the first half of round
    one and falls 2x to 100x too low from round three on. Use :func:`reference_chart`
    for anything a user sees; keep this only where a closed form is convenient.
    """
    if pick < 1:
        raise ValueError("pick must be >= 1")
    return 3000.0 * math.exp(-0.052 * (pick - 1))


def derive_surplus_chart(rookie_outcomes: pd.DataFrame) -> pd.DataFrame:
    """Average rookie-contract surplus by pick slot, smoothed across neighbouring picks.

    TODO(valuation): ``rookie_outcomes`` is one row per drafted player with his overall
    pick, market value of production over the rookie deal and rookie-scale cost. Group
    nearby picks into ranges (as Fitzgerald-Spielberger do) to strip out bust variance,
    and report floor/expected/ceiling quantiles rather than a single point.
    """
    raise NotImplementedError("Valuation workstream: derive the surplus-based draft chart.")
