"""Request and response shapes for the API. Keep these in sync with the web client."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ai_nfl_gm.valuation.trade import AssetKind


class TradeAssetIn(BaseModel):
    kind: AssetKind
    label: str = Field(examples=["WR, 2 years left", "2027 4th round pick"])
    surplus_pct: float = Field(description="Surplus value in % of cap.")
    season: int | None = Field(default=None, description="Draft season, for picks.")


class TradeSideIn(BaseModel):
    team: str
    assets: list[TradeAssetIn]


class TradeRequest(BaseModel):
    side_a: TradeSideIn
    side_b: TradeSideIn
    current_season: int = Field(examples=[2026])
    discount_per_year: float | None = Field(
        default=None,
        gt=0,
        le=1,
        description="Future-pick discount per season out, in (0, 1]; defaults to the sport config.",
    )


class TradeResponse(BaseModel):
    side_a_total_pct: float
    side_b_total_pct: float
    difference_pct: float
    currency_label: str


class HealthResponse(BaseModel):
    status: str
    version: str
    sport: str
