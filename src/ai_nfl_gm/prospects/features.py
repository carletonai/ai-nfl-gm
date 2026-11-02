"""Prospect features from CFBD and nflverse combine data.

TODO(prospects): join CFBD draft picks to nflverse ``draft_picks`` on draft year plus
overall pick (CFBD ``year, overall`` to nflverse ``season, pick``), then CFBD player season
stats by CFBD's athlete id, and ``combine`` by name plus draft year. Career value for the
outcome: ``w_av`` (``car_av`` is empty). Features: final two college
seasons of production, age on draft day, recruiting rank, combine measurables, the
consensus pre-draft grade/ranking from CFBD's draft endpoint.
"""

from __future__ import annotations

import pandas as pd


def build_prospect_features(draft_year: int) -> pd.DataFrame:
    """One row per prospect in ``draft_year`` with features and (if known) the actual slot."""
    raise NotImplementedError("Prospects workstream: build the prospect feature table.")
