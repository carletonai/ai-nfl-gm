"""Composite player value: the production label every other model regresses onto.

Direction set by Jeremy on Nov 2, 2026 (see ``docs/decisions/0002-target-variable.md``):
rather than adopt one off-the-shelf number (PFR Approximate Value, Madden ratings), build
our own composite from as many public signals as the data allows, so player values rest on
many data points and are explainable. The exact construction is the Valuation
workstream's design problem; this module fixes the interface so the market model, the
surplus engine, the draft chart and the prospect model can all consume one column.

Output contract: one row per player-season with ``gsis_id``, ``season``,
``position_group`` and ``value`` on a single cross-position scale (higher is better),
plus the component columns it was built from so a number can always be explained.

Candidate inputs, all free through nflverse (see ``docs/data-sources.md``):

* every position: PFR Approximate Value (``draft_picks`` carries career AV; season AV
  needs the PFR tables), snap counts, games started, Pro Bowl / All-Pro flags
* QB: passing EPA per play and total, CPOE, success rate, ESPN QBR, NGS passing
* WR / TE: targets, receiving EPA, target share, air-yards share, YAC over expected,
  NGS separation and cushion (2016+), PFR receiving advanced stats (2018+)
* RB: rushing EPA, success rate, NGS rush yards over expected
* EDGE / IDL: sacks, pressures and pass-rush win rate from PFR advanced stats (2018+)
* OL / LB / CB / S: thin; PFR coverage stats (2018+), snap counts, AV as the fallback

Open design questions for the workstream (record answers in the decision file):

* How to put position-specific components on one scale: standardise within position
  and season, then weight by what the market pays each position? Or regress onto wins
  (EPA to points to wins) so the scale is "wins" and the stretch goal falls out?
* What anchors the weights: AV, second-contract APY, or a wins model? Each choice has a
  known bias (AV favours volume; APY learns what GMs pay, not what wins).
* How far back the composite can go given 2016+ NGS and 2018+ PFR coverage.

TODO(valuation): design the composite for WR first (best free inputs), validate it against
AV and against second-contract APY on held-out seasons, then extend to EDGE and QB.
"""

from __future__ import annotations

import pandas as pd

#: Columns every row of the composite table must carry.
VALUE_TABLE_COLUMNS = ["gsis_id", "season", "position_group", "value"]


def composite_value(player_seasons: pd.DataFrame, *, position_group: str) -> pd.DataFrame:
    """Return the composite value table for one position group.

    ``player_seasons`` is the Data workstream's clean per-position table (one row per
    player-season with the candidate inputs above). The result has
    :data:`VALUE_TABLE_COLUMNS` plus one column per component used.
    """
    raise NotImplementedError("Valuation workstream: build the composite player-value score.")
