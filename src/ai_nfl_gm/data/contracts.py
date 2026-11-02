"""Contract table preparation.

The nflverse ``contracts`` table (sourced from Over The Cap) has one row per contract
and nests the per-year cap numbers inside each row. Everything downstream needs one
row per contract-year, so :func:`explode_cap_hits` is the first transformation that
runs. ``apy_cap_pct`` (APY as a share of the cap at signing) is the market model's
target; ``inflated_apy`` is APY adjusted for cap growth.

Column reference: https://nflreadr.nflverse.com/articles/dictionary_contracts.html
"""

from __future__ import annotations

import pandas as pd

#: Columns the market model needs from the contracts table.
CONTRACT_COLUMNS = [
    "player",
    "position",
    "team",
    "is_active",
    "year_signed",
    "years",
    "value",
    "apy",
    "guaranteed",
    "apy_cap_pct",
    "inflated_value",
    "inflated_apy",
    "inflated_guaranteed",
    "player_page",
    "otc_id",
    "gsis_id",
    "date_of_birth",
    "height",
    "weight",
    "college",
    "draft_year",
    "draft_round",
    "draft_overall",
    "draft_team",
    "cols",
]


def explode_cap_hits(contracts: pd.DataFrame) -> pd.DataFrame:
    """Return one row per contract-year with the nested cap numbers as columns.

    TODO(data): the nested ``cols`` column holds per-year ``year``, ``cap_number``,
    ``cash_paid`` and guarantee fields. Explode it, normalise the struct into columns and
    keep a contract id so rows can be grouped back. Write a test on a small fixture first.
    """
    raise NotImplementedError("Data workstream: explode the nested per-year cap hits.")


def veteran_contracts(contracts: pd.DataFrame, first_season: int) -> pd.DataFrame:
    """Veteran (non-rookie) deals signed in ``first_season`` or later.

    TODO(data): rookie deals are identified by ``draft_year == year_signed`` for drafted
    players; undrafted rookies need a rule too. Franchise tags and extensions need a flag.
    """
    raise NotImplementedError("Data workstream: filter to veteran deals since first_season.")
