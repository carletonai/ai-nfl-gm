from __future__ import annotations

from pathlib import Path

import pytest

from ai_nfl_gm.config import Settings, load_sport_config


def test_nfl_config_loads(nfl) -> None:
    assert nfl.name == "nfl"
    assert nfl.market_model_first_season == 2011
    assert nfl.position_rollout[0] == "WR"
    assert 0 < nfl.future_pick_discount_per_year <= 1


def test_crosswalk_targets_are_defined_groups(nfl) -> None:
    assert set(nfl.position_crosswalk.values()) <= set(nfl.position_groups)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("DE", "EDGE"), ("olb", "EDGE"), ("G", "IOL"), ("FS", "S"), ("WR", "WR"), ("XX", None)],
)
def test_canonical_position(nfl, raw: str, expected: str | None) -> None:
    assert nfl.canonical_position(raw) == expected


def test_salary_cap_table_is_increasing_except_2021(nfl) -> None:
    caps = nfl.salary_cap_musd
    for season in sorted(caps)[1:]:
        if season == 2021:  # the pandemic year cap fell
            assert caps[season] < caps[season - 1]
        else:
            assert caps[season] > caps[season - 1]


def test_unknown_sport_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_sport_config("nba", configs_dir=tmp_path)


def test_settings_defaults_point_at_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AI_NFL_GM_DATA_DIR", raising=False)
    settings = Settings(_env_file=None)
    assert settings.raw_dir.name == "raw"
    assert (settings.configs_dir / "sports" / "nfl.yaml").exists()


def test_env_file_is_read_from_repo_root_not_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ai_nfl_gm.config import REPO_ROOT

    monkeypatch.delenv("CFBD_API_KEY", raising=False)
    monkeypatch.delenv("AI_NFL_GM_CFBD_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)  # e.g. a notebook kernel started under notebooks/
    assert Settings.model_config["env_file"] == REPO_ROOT / ".env"
    env_file = tmp_path / "elsewhere" / ".env"
    env_file.parent.mkdir()
    env_file.write_text("CFBD_API_KEY=from-dotenv\n", encoding="utf-8")
    assert Settings(_env_file=env_file).cfbd_api_key == "from-dotenv"


def test_relative_data_dir_resolves_against_repo_root(monkeypatch: pytest.MonkeyPatch) -> None:
    from ai_nfl_gm.config import REPO_ROOT

    monkeypatch.setenv("AI_NFL_GM_DATA_DIR", "./scratch-data")
    settings = Settings(_env_file=None)
    assert settings.data_dir == (REPO_ROOT / "scratch-data").resolve()
