from __future__ import annotations

from pathlib import Path

import pytest

from ai_nfl_gm.data import nflverse


def test_asset_url_for_static_table() -> None:
    url = nflverse.asset_url("contracts")
    assert url.endswith("/contracts/historical_contracts.parquet")
    assert url.startswith("https://github.com/nflverse/nflverse-data/releases/download/")


def test_asset_url_requires_season_for_per_season_tables() -> None:
    with pytest.raises(ValueError, match="per season"):
        nflverse.asset_url("stats_player_reg")
    assert nflverse.asset_url("stats_player_reg", 2024).endswith("stats_player_reg_2024.parquet")


def test_unknown_table() -> None:
    with pytest.raises(KeyError):
        nflverse.asset_url("not_a_table")


def test_cache_path_uses_cache_dir(tmp_path: Path) -> None:
    path = nflverse.cache_path("players", cache_dir=tmp_path)
    assert path == tmp_path / "players.parquet"


@pytest.mark.network
def test_download_contracts_smoke(tmp_path: Path) -> None:
    frame = nflverse.load("contracts", cache_dir=tmp_path, columns=["player", "apy_cap_pct"])
    assert {"player", "apy_cap_pct"} <= set(frame.columns)
    assert len(frame) > 1000
