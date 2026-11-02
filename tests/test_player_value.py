from __future__ import annotations

import pandas as pd
import pytest

from ai_nfl_gm.valuation.player_value import VALUE_TABLE_COLUMNS, composite_value


def test_value_table_contract_names_the_join_keys() -> None:
    assert VALUE_TABLE_COLUMNS[:2] == ["gsis_id", "season"]
    assert "value" in VALUE_TABLE_COLUMNS


def test_composite_value_is_a_placeholder() -> None:
    with pytest.raises(NotImplementedError):
        composite_value(pd.DataFrame(), position_group="WR")
