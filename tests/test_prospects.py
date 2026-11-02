from __future__ import annotations

import pandas as pd
import pytest

from ai_nfl_gm.prospects.model import rank_correlation


def test_rank_correlation_perfect_order() -> None:
    s = pd.Series([1, 2, 3, 4, 5])
    assert rank_correlation(s, s) == pytest.approx(1.0)


def test_rank_correlation_reversed_order() -> None:
    predicted = pd.Series([1, 2, 3, 4, 5])
    actual = pd.Series([5, 4, 3, 2, 1])
    assert rank_correlation(predicted, actual) == pytest.approx(-1.0)
