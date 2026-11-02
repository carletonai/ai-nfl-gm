"""Contract table preparation.

The nflverse ``contracts`` table (sourced from Over The Cap) has one row per contract,
53k rows, 26 columns. Two columns are nested lists of structs and everything downstream
needs them flattened, so this is the first transformation that runs:

* ``season_history``: one struct per season of the deal with ``year``, ``team``,
  ``base_salary``, ``prorated_bonus``, ``option_bonus``, ``roster_bonus``,
  ``guaranteed_salary``, ``cap_number``, ``cap_percent``, ``cash_paid`` (plus workout,
  per-game roster and other bonuses, often null). ``cap_percent`` is the per-year cap hit
  as a share of that season's cap, which is what the surplus engine subtracts.
* ``contract_history``: the player's contracts with ``contract_type`` (``Drafted``,
  ``UDFA``, ``ERFA``, ``RFA``, ``UFA``, ``SFA``, ``Extension``, ``Franchise``,
  ``Transition``, ``Practice``, ``Other``), ``status`` (``Active``, ``Extended``,
  ``Expired``, ``Terminated``, ...), ``year_signed``, ``yrs``, ``total``, ``apy``,
  ``guarantees``, ``amount_earned``, ``percent_earned``, ``effective_apy``.

``apy_cap_pct`` (APY as a share of the cap at signing) is the market model's target;
``inflated_apy`` is APY adjusted for cap growth. Positions use Over The Cap's labels
(``ED``, ``IDL``, ``LT``, ``RG``, ...); run them through the sport config crosswalk.

Column reference: https://nflreadr.nflverse.com/articles/dictionary_contracts.html
Known quirks seen in the Nov 2026 release: a few rows have ``year_signed == 0``; about
7% of rows have no ``gsis_id`` (every row has an ``otc_id``).
"""

from __future__ import annotations

import pandas as pd

#: Every column in the contracts table, in release order.
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
    "height",
    "weight",
    "college",
    "draft_year",
    "draft_round",
    "draft_overall",
    "draft_team",
    "date_of_birth",
    "season_history",
    "contract_history",
]

#: Fields inside each ``season_history`` struct.
SEASON_HISTORY_FIELDS = [
    "year",
    "team",
    "base_salary",
    "prorated_bonus",
    "option_bonus",
    "roster_bonus",
    "guaranteed_salary",
    "cap_number",
    "cap_percent",
    "cash_paid",
    "workout_bonus",
    "per_game_roster_bonus",
    "other_bonus",
]

#: ``contract_history.contract_type`` values that are rookie deals.
ROOKIE_CONTRACT_TYPES = ("Drafted", "UDFA")


def explode_cap_hits(contracts: pd.DataFrame) -> pd.DataFrame:
    """Return one row per contract-year with the ``season_history`` struct as columns.

    TODO(data): ``contracts.explode("season_history")`` then ``pd.json_normalize`` (or
    ``pd.DataFrame(list_of_dicts)``) on the struct, prefix nothing, cast ``year`` to int,
    and keep ``otc_id`` + ``year_signed`` as the contract key so rows group back. Decide
    what to do with rows whose ``season_history`` is null or whose ``year_signed`` is 0.
    Write a test on a five-row fixture under ``tests/fixtures/`` first.
    """
    raise NotImplementedError("Data workstream: explode the nested season_history cap hits.")


def veteran_contracts(contracts: pd.DataFrame, first_season: int) -> pd.DataFrame:
    """Veteran (non-rookie) deals signed in ``first_season`` or later.

    TODO(data): the row-level table has no contract-type column, so the flag has to come
    from ``contract_history`` (``contract_type`` not in :data:`ROOKIE_CONTRACT_TYPES`),
    with ``draft_year == year_signed`` as a fallback. Confirm whether
    ``contract_history`` repeats the whole player history on each of his rows, and how
    to match the row to its own entry (``year_signed`` + ``yrs`` + ``apy``). Decide
    separately how to treat ``Franchise`` and ``Transition`` tags and ``Extension`` deals
    (the market model wants open-market prices; extensions are not quite that).
    """
    raise NotImplementedError("Data workstream: filter to veteran deals since first_season.")
