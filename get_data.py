"""Download the core nflverse tables into data/ as parquet files.

    uv run get_data.py               # player stats from 2011 to the current season
    uv run get_data.py --from 2020   # fewer seasons, faster
    uv run get_data.py --refresh     # download again even if the files exist

nflverse publishes these tables for free on GitHub:
https://github.com/nflverse/nflverse-data/releases
"""

import argparse
import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlretrieve

import pandas as pd

BASE = "https://github.com/nflverse/nflverse-data/releases/download"
DATA = Path(__file__).resolve().parent / "data"

# Output file name -> path on the nflverse release page.
TABLES = {
    "contracts": "contracts/historical_contracts.parquet",
    "players": "players/players.parquet",
    "draft_picks": "draft_picks/draft_picks.parquet",
    "combine": "combine/combine.parquet",
    "trades": "trades/trades.parquet",
}
STATS = "stats_player/stats_player_reg_{season}.parquet"


def current_season() -> int:
    """The NFL season starts in September, so January to August belong to last year."""
    today = datetime.date.today()
    return today.year if today.month >= 9 else today.year - 1


def download(release_path: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part")
    urlretrieve(f"{BASE}/{release_path}", tmp)
    tmp.replace(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the core nflverse tables into data/.")
    parser.add_argument("--from", dest="first", type=int, default=2011, help="first season of player stats")
    parser.add_argument("--refresh", action="store_true", help="download again even if the files exist")
    args = parser.parse_args()

    for name, release_path in TABLES.items():
        out = DATA / f"{name}.parquet"
        if args.refresh or not out.exists():
            print(f"downloading {name} ...")
            download(release_path, out)
        print(f"  {out.relative_to(DATA.parent)}")

    out = DATA / "player_stats.parquet"
    if args.refresh or not out.exists():
        seasons = []
        for season in range(args.first, current_season() + 1):
            part = DATA / "tmp" / f"player_stats_{season}.parquet"
            print(f"downloading player stats {season} ...")
            try:
                download(STATS.format(season=season), part)
            except HTTPError as err:
                print(f"  skipped {season}: {err}")
                continue
            seasons.append(pd.read_parquet(part))
            part.unlink()
        (DATA / "tmp").rmdir()
        pd.concat(seasons, ignore_index=True).to_parquet(out)
    print(f"  {out.relative_to(DATA.parent)}")
    print("done. Open a notebook with: uv run jupyter lab")


if __name__ == "__main__":
    main()
