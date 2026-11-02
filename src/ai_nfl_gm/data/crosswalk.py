"""Player-ID and position crosswalks.

Two joins hold the whole project together and both are known to be imperfect:

* **Contracts to stats.** The nflverse ``players`` table carries ``gsis_id`` beside
  ``otc_id``, ``pfr_id``, ``espn_id`` and ``pff_id``. Join ``contracts.otc_id`` to
  ``players.otc_id``, then ``players.gsis_id`` to the stats tables. No fuzzy matching;
  log the misses instead.
* **College to NFL.** ``draft_picks`` carries ``cfb_player_id`` and ``pfr_player_id``;
  CFBD's draft endpoint carries its own college athlete id. Join on draft year plus
  overall pick as the primary key and use the ids as a check.

Position labels disagree across OTC, PFR and rosters, so every raw label goes through
:func:`canonical_positions` before grouping.
"""

from __future__ import annotations

import logging

import pandas as pd

from ai_nfl_gm.config import SportConfig

log = logging.getLogger(__name__)


def canonical_positions(raw: pd.Series, sport: SportConfig) -> pd.Series:
    """Map raw position labels onto the sport's canonical position groups.

    Unknown labels become ``NA`` and are logged once so the crosswalk can be extended.
    """
    mapped = raw.astype("string").str.strip().str.upper().map(sport.position_crosswalk)
    unknown = sorted(raw[mapped.isna() & raw.notna()].astype(str).unique())
    if unknown:
        log.warning("positions missing from %s crosswalk: %s", sport.name, unknown)
    return mapped


def build_player_id_crosswalk(players: pd.DataFrame) -> pd.DataFrame:
    """Return one row per player with every external id nflverse knows.

    TODO(data): decide how to handle players with several ``gsis_id`` rows and players
    whose ``otc_id`` is missing (the feasibility check says the crosswalk is incomplete).
    """
    id_columns = [c for c in players.columns if c.endswith("_id")]
    return players[["display_name", *id_columns]].drop_duplicates()
