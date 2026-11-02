"""Trade evaluation: a trade is a sum of surplus on each side.

The arithmetic here is deliberately simple; the hard part is the surplus numbers
that feed it. The project plan names three adjustments that keep the calculator
honest. One is implemented:

* future picks are discounted per season out (``discount_per_year``; the sport config
  default is 0.85, the "one round later" rule of thumb).

Two are not yet:

TODO(valuation): team context should shift the exchange rate (a contender weights this
year's surplus; a cap-strapped team weights cheap years). Agree the shape of a
``year_weights`` input with the Product stream, which owns the sliders.
TODO(valuation): a traded player carries extension and franchise-tag rights; add a small
bonus on top of his contract years.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AssetKind = Literal["player", "pick"]


@dataclass(frozen=True)
class TradeAsset:
    """One thing changing hands, valued in % of cap of surplus."""

    kind: AssetKind
    label: str
    surplus_pct: float
    #: Draft season for picks; the number of seasons out is what gets discounted.
    season: int | None = None


@dataclass(frozen=True)
class TradeSide:
    team: str
    assets: list[TradeAsset] = field(default_factory=list)


@dataclass(frozen=True)
class TradeEvaluation:
    side_a_total_pct: float
    side_b_total_pct: float

    @property
    def difference_pct(self) -> float:
        """Positive means side A gives up more surplus than side B."""
        return self.side_a_total_pct - self.side_b_total_pct


def discount_future_pick(
    surplus_pct: float, *, pick_season: int, current_season: int, discount_per_year: float
) -> float:
    """Discount a future pick's surplus by ``discount_per_year`` for each season out."""
    years_out = max(pick_season - current_season, 0)
    return surplus_pct * discount_per_year**years_out


def side_total(side: TradeSide, *, current_season: int, discount_per_year: float) -> float:
    total = 0.0
    for asset in side.assets:
        value = asset.surplus_pct
        if asset.kind == "pick" and asset.season is not None:
            value = discount_future_pick(
                value,
                pick_season=asset.season,
                current_season=current_season,
                discount_per_year=discount_per_year,
            )
        total += value
    return total


def evaluate_trade(
    side_a: TradeSide,
    side_b: TradeSide,
    *,
    current_season: int,
    discount_per_year: float,
) -> TradeEvaluation:
    """Sum surplus on each side, discounting future picks."""
    return TradeEvaluation(
        side_a_total_pct=side_total(
            side_a, current_season=current_season, discount_per_year=discount_per_year
        ),
        side_b_total_pct=side_total(
            side_b, current_season=current_season, discount_per_year=discount_per_year
        ),
    )
