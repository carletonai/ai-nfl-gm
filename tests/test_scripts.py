from __future__ import annotations

import datetime

from scripts.pull_nflverse import current_nfl_season


def test_current_nfl_season_rolls_over_in_september() -> None:
    assert current_nfl_season(datetime.date(2026, 11, 2)) == 2026
    assert current_nfl_season(datetime.date(2027, 3, 1)) == 2026
    assert current_nfl_season(datetime.date(2027, 9, 10)) == 2027
