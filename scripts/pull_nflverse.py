"""Download the core nflverse tables into data/raw/nflverse.

Run with ``make pull-data`` or ``uv run python scripts/pull_nflverse.py --seasons 2011 2025``.
Downloads are cached; pass ``--refresh`` to re-download.
"""

from __future__ import annotations

import argparse
import logging

from ai_nfl_gm.config import get_settings
from ai_nfl_gm.data import nflverse

STATIC_TABLES = ["contracts", "players", "draft_picks", "combine", "trades"]
PER_SEASON_TABLES = ["stats_player_reg"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seasons",
        nargs=2,
        type=int,
        metavar=("FIRST", "LAST"),
        default=(2011, 2025),
        help="inclusive season range for per-season tables",
    )
    parser.add_argument("--refresh", action="store_true", help="re-download cached files")
    args = parser.parse_args()

    logging.basicConfig(level=get_settings().log_level, format="%(levelname)s %(message)s")

    for table in STATIC_TABLES:
        path = nflverse.download(table, refresh=args.refresh)
        print(f"{table:20s} {path}")
    first, last = args.seasons
    for season in range(first, last + 1):
        for table in PER_SEASON_TABLES:
            path = nflverse.download(table, season, refresh=args.refresh)
            print(f"{table}_{season:<9d} {path}")


if __name__ == "__main__":
    main()
