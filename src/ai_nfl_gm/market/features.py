"""Feature construction for the market model.

Each row is one contract signing. Features are built only from seasons *before*
``year_signed`` so the model never sees the future.

TODO(market): start with WR. Candidate features from nflverse: targets, receptions,
receiving yards, receiving EPA, air yards share, target share, YAC (2016+ NGS adds
separation and cushion). Add age at signing and the position group.
"""

from __future__ import annotations

import pandas as pd


def build_signing_features(
    contracts: pd.DataFrame,
    player_seasons: pd.DataFrame,
    *,
    lookback_seasons: int = 3,
) -> pd.DataFrame:
    """Join each contract to the player's ``lookback_seasons`` prior seasons of stats.

    Returns one row per contract with aggregated production features plus
    ``apy_cap_pct`` as the target column.
    """
    raise NotImplementedError("Market workstream: build pre-signing production features.")
