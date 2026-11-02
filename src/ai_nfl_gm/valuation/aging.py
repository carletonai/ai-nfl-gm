"""Position aging curves.

Project a player's next seasons from his recent production and age. WR has a
well-behaved curve and goes first.

TODO(valuation): fit per-position curves (delta method or a smooth regression on age)
from the player-season stats table and expose ``project_seasons``. Record the method in
``docs/decisions/``.
"""

from __future__ import annotations

import pandas as pd


def project_seasons(player_seasons: pd.DataFrame, *, horizon: int) -> pd.DataFrame:
    """Return projected production for the next ``horizon`` seasons per player."""
    raise NotImplementedError("Valuation workstream: fit and apply position aging curves.")
