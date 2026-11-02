from __future__ import annotations

from fastapi.testclient import TestClient

from ai_nfl_gm.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["sport"] == "nfl"


def test_trade_evaluate() -> None:
    payload = {
        "side_a": {
            "team": "A",
            "assets": [
                {"kind": "player", "label": "WR", "surplus_pct": 4.5},
                {"kind": "pick", "label": "2027 4th", "surplus_pct": 1.0, "season": 2027},
            ],
        },
        "side_b": {
            "team": "B",
            "assets": [{"kind": "pick", "label": "Pick 40", "surplus_pct": 5.6}],
        },
        "current_season": 2026,
    }
    response = client.post("/trade/evaluate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["side_b_total_pct"] == 5.6
    assert body["currency_label"] == "% of cap"
    assert body["difference_pct"] < 0
