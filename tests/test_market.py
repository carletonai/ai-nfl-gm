from __future__ import annotations

import pytest

from ai_nfl_gm.market.evaluate import evaluate, regression_metrics, split_last_classes
from ai_nfl_gm.market.model import NaiveBaseline


def test_split_holds_out_last_two_seasons(toy_signings) -> None:
    split = split_last_classes(toy_signings)
    assert split.test_seasons == (2023, 2024)
    assert set(split.train["year_signed"]) == {2021, 2022}


def test_split_needs_enough_seasons(toy_signings) -> None:
    with pytest.raises(ValueError):
        split_last_classes(toy_signings[toy_signings["year_signed"] <= 2022], n_classes=2)


def test_naive_baseline_predicts_group_mean(toy_signings) -> None:
    model = NaiveBaseline().fit(toy_signings[["position_group"]], toy_signings["apy_cap_pct"])
    pred = model.predict(toy_signings[["position_group"]])
    wr_mean = toy_signings.loc[toy_signings["position_group"] == "WR", "apy_cap_pct"].mean()
    assert pred[toy_signings["position_group"] == "WR"].eq(wr_mean).all()


def test_evaluate_runs_end_to_end(toy_signings) -> None:
    metrics = evaluate(NaiveBaseline(), toy_signings, feature_columns=["position_group"])
    assert metrics["n"] == 4
    assert metrics["mae"] > 0
    assert metrics["test_seasons"] == [2023, 2024]


def test_regression_metrics_zero_error() -> None:
    import pandas as pd

    y = pd.Series([1.0, 2.0, 3.0])
    assert regression_metrics(y, y)["rmse"] == 0.0
