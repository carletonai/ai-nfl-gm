"""Held-out evaluation for the market model.

The outline's metric: hold out the last two free-agency classes (by ``year_signed``)
and report error on predicted contract value. Keeping the split here, not inside each
model, means every model is compared on the same deals.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ai_nfl_gm.market.model import TARGET, MarketModel


@dataclass(frozen=True)
class HoldoutSplit:
    train: pd.DataFrame
    test: pd.DataFrame
    test_seasons: tuple[int, ...]


def split_last_classes(
    signings: pd.DataFrame, *, n_classes: int = 2, season_column: str = "year_signed"
) -> HoldoutSplit:
    """Hold out the most recent ``n_classes`` signing seasons."""
    seasons = sorted(signings[season_column].dropna().unique())
    if len(seasons) <= n_classes:
        raise ValueError(f"Need more than {n_classes} seasons to hold {n_classes} out.")
    held_out = tuple(int(s) for s in seasons[-n_classes:])
    mask = signings[season_column].isin(held_out)
    return HoldoutSplit(train=signings[~mask], test=signings[mask], test_seasons=held_out)


def regression_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    """MAE, RMSE and median absolute error, all in the target's units (% of cap)."""
    err = y_true.to_numpy(dtype=float) - y_pred.to_numpy(dtype=float)
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "median_ae": float(np.median(np.abs(err))),
        "n": int(err.size),
    }


def evaluate(
    model: MarketModel, signings: pd.DataFrame, feature_columns: list[str]
) -> dict[str, float]:
    """Fit ``model`` on the training classes and score it on the held-out classes."""
    split = split_last_classes(signings)
    model.fit(split.train[feature_columns], split.train[TARGET])
    predictions = model.predict(split.test[feature_columns])
    metrics = regression_metrics(split.test[TARGET], predictions)
    metrics["test_seasons"] = list(split.test_seasons)  # type: ignore[assignment]
    return metrics
