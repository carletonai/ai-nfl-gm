"""Download nflverse release parquet files into the local cache.

nflverse publishes its data as parquet assets on GitHub releases, free and without a
key (CC-BY 4.0; FTN charting CC-BY-SA 4.0). This module reads those URLs directly with
pandas instead of depending on the ``nflreadpy`` wrapper, which is still beta and
lacks loaders for PFR advanced stats and ESPN QBR.

Usage::

    from ai_nfl_gm.data import nflverse

    contracts = nflverse.load("contracts")  # cached under data/raw/nflverse/
    stats_2024 = nflverse.load("stats_player_reg", season=2024)

Add a table by adding an entry to :data:`TABLES`; the release page lists every asset:
https://github.com/nflverse/nflverse-data/releases
"""

from __future__ import annotations

import logging
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

from ai_nfl_gm.config import get_settings

log = logging.getLogger(__name__)

RELEASE_BASE = "https://github.com/nflverse/nflverse-data/releases/download"

#: Table name -> ``"<release tag>/<asset file>"``. ``{season}`` is filled from the
#: ``season`` argument for per-season assets.
TABLES: dict[str, str] = {
    # One row per contract; per-year cap hits are nested in `season_history` (explode first).
    "contracts": "contracts/historical_contracts.parquet",
    # One row per player; the ID crosswalk (gsis_id, pfr_id, otc_id, espn_id, ...).
    "players": "players/players.parquet",
    # season, round, pick, team, gsis_id, pfr_player_id, cfb_player_id; career AV columns.
    "draft_picks": "draft_picks/draft_picks.parquet",
    "combine": "combine/combine.parquet",
    "trades": "trades/trades.parquet",
    # Per-season player stats (regular season). Replace `reg` with `week` for weekly rows.
    "stats_player_reg": "stats_player/stats_player_reg_{season}.parquet",
    "rosters": "rosters/roster_{season}.parquet",
    "snap_counts": "snap_counts/snap_counts_{season}.parquet",
    # Pro Football Reference advanced stats (2018+). Only available through nflverse.
    "pfr_advstats_rec": "pfr_advstats/advstats_season_rec.parquet",
    "pfr_advstats_pass": "pfr_advstats/advstats_season_pass.parquet",
    "pfr_advstats_rush": "pfr_advstats/advstats_season_rush.parquet",
    "pfr_advstats_def": "pfr_advstats/advstats_season_def.parquet",
    # Next Gen Stats (2016+).
    "ngs_receiving": "nextgen_stats/ngs_receiving.parquet",
    "ngs_passing": "nextgen_stats/ngs_passing.parquet",
    "ngs_rushing": "nextgen_stats/ngs_rushing.parquet",
}


def asset_url(table: str, season: int | None = None) -> str:
    """Return the release URL for ``table`` (and ``season`` where the asset is per season)."""
    try:
        template = TABLES[table]
    except KeyError as exc:
        raise KeyError(f"Unknown nflverse table {table!r}. Known: {sorted(TABLES)}") from exc
    if "{season}" in template:
        if season is None:
            raise ValueError(f"Table {table!r} is per season; pass season=...")
        template = template.format(season=season)
    return f"{RELEASE_BASE}/{template}"


def cache_path(table: str, season: int | None = None, cache_dir: Path | None = None) -> Path:
    """Where :func:`load` stores the downloaded file."""
    root = cache_dir or (get_settings().raw_dir / "nflverse")
    name = asset_url(table, season).rsplit("/", 1)[-1]
    return root / name


def download(
    table: str,
    season: int | None = None,
    *,
    cache_dir: Path | None = None,
    refresh: bool = False,
) -> Path:
    """Download ``table`` into the cache if missing (or ``refresh``) and return its path."""
    path = cache_path(table, season, cache_dir)
    if path.exists() and not refresh:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    url = asset_url(table, season)
    log.info("downloading %s -> %s", url, path)
    tmp = path.with_suffix(path.suffix + ".part")
    urlretrieve(url, tmp)  # noqa: S310 - fixed https host
    tmp.replace(path)
    return path


def load(
    table: str,
    season: int | None = None,
    *,
    columns: list[str] | None = None,
    cache_dir: Path | None = None,
    refresh: bool = False,
) -> pd.DataFrame:
    """Return ``table`` as a DataFrame, downloading it on first use."""
    path = download(table, season, cache_dir=cache_dir, refresh=refresh)
    return pd.read_parquet(path, columns=columns)
