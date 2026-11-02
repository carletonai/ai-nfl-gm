"""Surplus value: market value of projected production minus remaining cap cost.

Rookie deals come out as large surplus; that is correct and is why draft picks have
value at all. A cut-risk adjustment matters: of the 2,007 contract years handed out in
2011 to 2015 free agency only about 62% were actually served.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SurplusBreakdown:
    """One player's surplus over his remaining controlled years, in % of cap."""

    market_value_pct: float
    cap_cost_pct: float

    @property
    def surplus_pct(self) -> float:
        return self.market_value_pct - self.cap_cost_pct


def player_surplus(
    projected_production,  # noqa: ANN001 - shape decided by the aging/market work
    remaining_cap_hits_pct: list[float],
    *,
    cut_risk: float = 0.0,
) -> SurplusBreakdown:
    """Price projected seasons with the market model and subtract remaining cap hits.

    TODO(valuation): needs the fitted market model and the exploded cap hits. ``cut_risk``
    should discount later years of non-guaranteed money.
    """
    raise NotImplementedError("Valuation workstream: price projections and subtract cap hits.")
