"""Minimal CollegeFootballData (CFBD) API client.

CFBD needs a free API key (https://collegefootballdata.com/key; about 1,000 calls a
month on the free tier). Set ``CFBD_API_KEY`` in your ``.env``. Use the ``apinext`` base
URL; the legacy API is deprecated.

The whole college pull the prospects workstream needs is roughly 50 calls (player
season stats take only a ``year`` and return everyone), so cache every response under
``data/raw/cfbd/`` and never loop over players.

Only the plumbing is here. Endpoint wrappers belong to the Prospects workstream; add
them as thin methods that return DataFrames.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import httpx
import pandas as pd

from ai_nfl_gm.config import get_settings

log = logging.getLogger(__name__)


class CFBDClient:
    """Thin authenticated wrapper around the CFBD REST API with a file cache."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        cache_dir: Path | None = None,
        timeout: float = 30.0,
    ) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.cfbd_api_key
        if not self.api_key:
            raise RuntimeError(
                "CFBD_API_KEY is not set. Get a free key at https://collegefootballdata.com/key "
                "and put it in .env (see .env.example)."
            )
        self.base_url = (base_url or settings.cfbd_base_url).rstrip("/")
        self.cache_dir = cache_dir or (settings.raw_dir / "cfbd")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
            timeout=timeout,
        )

    def _cache_file(self, path: str, params: dict[str, Any]) -> Path:
        key = "_".join(f"{k}-{v}" for k, v in sorted(params.items())) or "all"
        return self.cache_dir / path.strip("/").replace("/", "_") / f"{key}.json"

    def get(self, path: str, *, refresh: bool = False, **params: Any) -> list[dict[str, Any]]:
        """GET ``path`` with query ``params``; cached on disk so quota is spent once."""
        cache = self._cache_file(path, params)
        if cache.exists() and not refresh:
            return json.loads(cache.read_text(encoding="utf-8"))
        log.info("CFBD GET %s %s", path, params)
        response = self._client.get(path, params=params)
        response.raise_for_status()
        payload = response.json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def get_frame(self, path: str, *, refresh: bool = False, **params: Any) -> pd.DataFrame:
        """Like :meth:`get` but returns a flat DataFrame."""
        return pd.json_normalize(self.get(path, refresh=refresh, **params))

    # --- Endpoint wrappers (Prospects workstream fills these in) -------------------

    def draft_picks(self, year: int) -> pd.DataFrame:
        """NFL draft picks with college athlete id, pre-draft ranking and grade."""
        return self.get_frame("/draft/picks", year=year)

    def player_season_stats(self, year: int) -> pd.DataFrame:
        """Season stats for every player in ``year`` (one call per season)."""
        return self.get_frame("/stats/player/season", year=year)
