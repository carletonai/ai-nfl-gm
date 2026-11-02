"""FastAPI application.

Endpoints are thin: validate the request, call into ``ai_nfl_gm.valuation`` and return
the result. Model inference and data loading stay out of request handlers.
"""

from __future__ import annotations

from fastapi import FastAPI

from ai_nfl_gm import __version__
from ai_nfl_gm.api.schemas import HealthResponse, TradeRequest, TradeResponse
from ai_nfl_gm.config import load_sport_config
from ai_nfl_gm.valuation.trade import TradeAsset, TradeSide, evaluate_trade

app = FastAPI(
    title="AI NFL GM",
    version=__version__,
    description="Surplus-value pricing for NFL players and draft picks.",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    sport = load_sport_config()
    return HealthResponse(status="ok", version=__version__, sport=sport.name)


@app.post("/trade/evaluate", response_model=TradeResponse)
def trade_evaluate(request: TradeRequest) -> TradeResponse:
    """Sum surplus on each side of a proposed trade.

    Surplus numbers are supplied by the caller for now.

    TODO(product): once the valuation engine ships, look players and picks up by id from
    the surplus table instead of taking numbers in the request, and add the draft-board
    endpoint (``GET /draft/board?season=``) the page reads.
    """
    sport = load_sport_config()
    discount = (
        sport.future_pick_discount_per_year
        if request.discount_per_year is None
        else request.discount_per_year
    )

    def to_side(side_in) -> TradeSide:  # noqa: ANN001
        return TradeSide(
            team=side_in.team,
            assets=[TradeAsset(**asset.model_dump()) for asset in side_in.assets],
        )

    result = evaluate_trade(
        to_side(request.side_a),
        to_side(request.side_b),
        current_season=request.current_season,
        discount_per_year=discount,
    )
    return TradeResponse(
        side_a_total_pct=result.side_a_total_pct,
        side_b_total_pct=result.side_b_total_pct,
        difference_pct=result.difference_pct,
        currency_label=sport.currency_label,
    )
