"""Shared fixtures. Tests never touch the network unless marked ``network``."""

from __future__ import annotations

import pandas as pd
import pytest

from ai_nfl_gm.config import SportConfig, load_sport_config


@pytest.fixture(scope="session")
def nfl() -> SportConfig:
    return load_sport_config("nfl")


@pytest.fixture
def toy_signings() -> pd.DataFrame:
    """A handful of fake signings across four seasons for the market-model harness."""
    return pd.DataFrame(
        {
            "year_signed": [2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024],
            "position_group": ["WR", "EDGE", "WR", "EDGE", "WR", "EDGE", "WR", "EDGE"],
            "apy_cap_pct": [0.08, 0.10, 0.09, 0.11, 0.10, 0.12, 0.11, 0.13],
        }
    )
