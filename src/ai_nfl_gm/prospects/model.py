"""Prospect model: predicted NFL value from college features.

TODO(prospects): start by predicting the consensus slot (the cheapest strong signal),
then look for where production and measurables disagree with it. Evaluate with
Spearman rank correlation against actual slot and against career value.
"""

from __future__ import annotations

import pandas as pd


def rank_correlation(predicted: pd.Series, actual: pd.Series) -> float:
    """Spearman rank correlation between predicted and actual ordering."""
    return float(predicted.corr(actual, method="spearman"))
