from __future__ import annotations

import pandas as pd

from ai_nfl_gm.data.crosswalk import canonical_positions


def test_canonical_positions_maps_and_flags_unknown(nfl, caplog) -> None:
    raw = pd.Series(["DE", "olb ", "WR", "ZZ", None])
    mapped = canonical_positions(raw, nfl)
    assert mapped.tolist()[:3] == ["EDGE", "EDGE", "WR"]
    assert pd.isna(mapped.iloc[3]) and pd.isna(mapped.iloc[4])
    assert "ZZ" in caplog.text
