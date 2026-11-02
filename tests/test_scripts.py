from __future__ import annotations

import datetime

import pytest
from scripts.pull_nflverse import current_nfl_season


def test_current_nfl_season_rolls_over_in_september() -> None:
    assert current_nfl_season(datetime.date(2026, 11, 2)) == 2026
    assert current_nfl_season(datetime.date(2027, 3, 1)) == 2026
    assert current_nfl_season(datetime.date(2027, 9, 10)) == 2027


def test_implied_cap_by_season_uses_sizeable_deals_only() -> None:
    import pandas as pd
    from scripts.check_cap_table import implied_cap_by_season

    contracts = pd.DataFrame(
        {
            "year_signed": [2024, 2024, 2024, 2025],
            "apy": [25.54, 12.77, 1.0, 27.92],
            "apy_cap_pct": [0.10, 0.05, 0.004, 0.10],  # the 0.4% deal is ignored
        }
    )
    implied = implied_cap_by_season(contracts)
    assert implied.loc[2024, "deals"] == 2
    assert implied.loc[2024, "implied_cap_musd"] == pytest.approx(255.4)
    assert implied.loc[2025, "implied_cap_musd"] == pytest.approx(279.2)
