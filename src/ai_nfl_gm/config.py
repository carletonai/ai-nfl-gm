"""Runtime settings and sport configuration.

Two kinds of configuration live here:

* :class:`Settings` reads environment variables (and a local ``.env`` file) for things
  that differ per machine: where data is cached, the CFBD API key, log level.
* :class:`SportConfig` is loaded from ``configs/sports/<name>.yaml`` and holds the
  league rules the models depend on. The sport is a config so the NBA can follow.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import AliasChoices, BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# src/ai_nfl_gm/config.py -> repo root. Works for the editable install everyone uses.
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Per-machine settings. Override with environment variables or a ``.env`` file."""

    model_config = SettingsConfigDict(
        env_prefix="AI_NFL_GM_",
        env_file=REPO_ROOT / ".env",  # found from any cwd (notebooks, IDE test runners)
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = Field(default=REPO_ROOT / "data", description="Root of the data cache.")
    configs_dir: Path = Field(default=REPO_ROOT / "configs", description="Sport YAML files.")
    log_level: str = "INFO"

    # Accept the plain name most people will already have in their shell.
    cfbd_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("CFBD_API_KEY", "AI_NFL_GM_CFBD_API_KEY"),
    )
    # The official cfbd Python client (5.33) defaults to this host; apinext was the v2 preview.
    cfbd_base_url: str = "https://api.collegefootballdata.com"

    @field_validator("data_dir", "configs_dir", mode="after")
    @classmethod
    def _anchor_to_repo_root(cls, value: Path) -> Path:
        """Resolve relative paths against the repo root, not the process cwd."""
        return value if value.is_absolute() else (REPO_ROOT / value).resolve()

    @property
    def raw_dir(self) -> Path:
        """Untouched downloads, one file per source table. Gitignored."""
        return self.data_dir / "raw"

    @property
    def interim_dir(self) -> Path:
        """Cleaned and joined tables that are still inputs, not outputs. Gitignored."""
        return self.data_dir / "interim"

    @property
    def processed_dir(self) -> Path:
        """Feature tables and model outputs. Gitignored; publish derived tables deliberately."""
        return self.data_dir / "processed"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide :class:`Settings` (cached)."""
    return Settings()


class SportConfig(BaseModel):
    """League rules loaded from ``configs/sports/<name>.yaml``."""

    name: str
    display_name: str
    currency_label: str = "% of cap"
    market_model_first_season: int
    rookie_contract_years: int
    future_pick_discount_per_year: float
    salary_cap_musd: dict[int, float]
    position_groups: list[str]
    position_crosswalk: dict[str, str]
    position_rollout: list[str]

    def canonical_position(self, raw: str) -> str | None:
        """Map a raw position label (``"DE"``, ``"OLB"``, ``"G"``) to a canonical group.

        Returns ``None`` for labels the crosswalk does not know, so callers can log them
        instead of silently dropping players.
        """
        return self.position_crosswalk.get(raw.strip().upper())


def load_sport_config(name: str = "nfl", configs_dir: Path | None = None) -> SportConfig:
    """Load and validate ``configs/sports/<name>.yaml``."""
    root = configs_dir or get_settings().configs_dir
    path = root / "sports" / f"{name}.yaml"
    with path.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    config = SportConfig.model_validate(raw)
    unknown = set(config.position_crosswalk.values()) - set(config.position_groups)
    if unknown:
        raise ValueError(f"{path}: crosswalk maps to undefined position groups: {sorted(unknown)}")
    return config
