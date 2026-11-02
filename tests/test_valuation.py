from __future__ import annotations

import pytest

from ai_nfl_gm.valuation.draft_chart import jimmy_johnson_approx, reference_chart
from ai_nfl_gm.valuation.surplus import SurplusBreakdown
from ai_nfl_gm.valuation.trade import TradeAsset, TradeSide, discount_future_pick, evaluate_trade


def test_jimmy_johnson_table_matches_published_anchors() -> None:
    chart = reference_chart("jimmy_johnson").set_index("pick")["value"]
    assert len(chart) == 224
    assert chart[1] == 3000
    assert chart[32] == 590
    assert chart[64] == 270
    assert chart[100] == 100
    assert chart[224] == pytest.approx(3.0)


def test_jimmy_johnson_table_is_descending_except_source_quirk() -> None:
    # The source page prints 31.8 at pick 152 between 31.0 and 31.2; copied as printed,
    # so that is the one place the table goes up.
    chart = reference_chart("jimmy_johnson")
    increases = chart.loc[chart["value"].diff() > 0, "pick"].tolist()
    assert increases == [152]


def test_unknown_reference_chart() -> None:
    with pytest.raises(KeyError):
        reference_chart("not_a_chart")


def test_jimmy_johnson_approx_anchors_only() -> None:
    assert jimmy_johnson_approx(1) == pytest.approx(3000.0)
    assert jimmy_johnson_approx(32) == pytest.approx(598, abs=1)
    with pytest.raises(ValueError):
        jimmy_johnson_approx(0)


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


def test_evaluate_trade_discounts_future_pick_in_plan_example() -> None:
    """The illustrative trade from the project plan: WR + 2027 4th for pick 40.

    The plan's table shows the undiscounted total (+5.5); applying its stated x0.85 per
    year future-pick discount to the 2027 pick gives 4.5 + 0.85 = 5.35.
    """
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
