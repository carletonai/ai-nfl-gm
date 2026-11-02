"""Market model interface and the naive baseline every real model must beat.

The data is small (a few hundred usable deals per position), so the plan is ridge
regression or a regularised gradient-boosted model, not deep nets. Any model that
implements :class:`MarketModel` can be swapped into the evaluation harness.
"""

from __future__ import annotations

from typing import Protocol

import pandas as pd

TARGET = "apy_cap_pct"


class MarketModel(Protocol):
    """What the evaluation harness and the surplus engine expect from a market model."""

    def fit(self, X: pd.DataFrame, y: pd.Series) -> MarketModel:  # noqa: N803 - sklearn style
        """Fit on signing features ``X`` and target ``y`` (``apy_cap_pct``)."""
        ...

    def predict(self, X: pd.DataFrame) -> pd.Series:  # noqa: N803
        """Predicted ``apy_cap_pct`` for each row of ``X``."""
        ...


class NaiveBaseline:
    """Predict the mean target of the player's position group.

    This is the baseline the week-4 milestone refers to: "a WR market model beating a
    naive baseline on the held-out classes".
    """

    def __init__(self, group_column: str = "position_group") -> None:
        self.group_column = group_column
        self.group_means_: pd.Series | None = None
        self.global_mean_: float | None = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> NaiveBaseline:  # noqa: N803
        self.group_means_ = y.groupby(X[self.group_column]).mean()
        self.global_mean_ = float(y.mean())
        return self

    def predict(self, X: pd.DataFrame) -> pd.Series:  # noqa: N803
        if self.group_means_ is None or self.global_mean_ is None:
            raise RuntimeError("Call fit() before predict().")
        predictions = X[self.group_column].map(self.group_means_).fillna(self.global_mean_)
        return predictions.rename(TARGET)
