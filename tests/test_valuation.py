from __future__ import annotations

import pytest

from ai_nfl_gm.valuation.draft_chart import jimmy_johnson_approx, reference_chart
from ai_nfl_gm.valuation.surplus import SurplusBreakdown
from ai_nfl_gm.valuation.trade import TradeAsset, TradeSide, discount_future_pick, evaluate_trade


def test_jimmy_johnson_pick_one_is_3000() -> None:
    assert jimmy_johnson_approx(1) == pytest.approx(3000.0)
    assert jimmy_johnson_approx(32) < jimmy_johnson_approx(1) / 4


def test_reference_chart_is_monotone_decreasing() -> None:
    chart = reference_chart()
    assert len(chart) == 224
    assert chart["value"].is_monotonic_decreasing


def test_surplus_breakdown() -> None:
    assert SurplusBreakdown(market_value_pct=6.5, cap_cost_pct=2.0).surplus_pct == pytest.approx(
        4.5
    )


def test_future_pick_discount() -> None:
    assert discount_future_pick(
        1.0, pick_season=2027, current_season=2026, discount_per_year=0.85
    ) == pytest.approx(0.85)
    assert discount_future_pick(
        1.0, pick_season=2026, current_season=2026, discount_per_year=0.85
    ) == pytest.approx(1.0)


def test_evaluate_trade_matches_outline_example() -> None:
    """The illustrative trade from the project plan: WR + 2027 4th for pick 40."""
    team_a = TradeSide(
        "A",
        [
            TradeAsset("player", "WR, 2 years left", 4.5),
            TradeAsset("pick", "2027 4th", 1.0, season=2027),
        ],
    )
    team_b = TradeSide("B", [TradeAsset("pick", "Pick 40", 5.6, season=2026)])
    result = evaluate_trade(team_a, team_b, current_season=2026, discount_per_year=0.85)
    assert result.side_a_total_pct == pytest.approx(4.5 + 0.85)
    assert result.side_b_total_pct == pytest.approx(5.6)
    assert result.difference_pct < 0
