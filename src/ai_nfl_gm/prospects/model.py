"""Prospect model: predicted NFL value from college features.

TODO(prospects): start by predicting the consensus slot (the cheapest strong signal),
then look for where production and measurables disagree with it. Evaluate with
Spearman rank correlation against actual slot and against career value.
"""

from __future__ import annotations

import pandas as pd


def rank_correlation(predicted: pd.Series, actual: pd.Series) -> float:
    """Spearman rank correlation between predicted and actual ordering.

    Computed as the Pearson correlation of the ranks (average ranks for ties), which is
    Spearman's rho without pulling in scipy, so it works on a core-only install.
    """
    return float(predicted.rank().corr(actual.rank()))
