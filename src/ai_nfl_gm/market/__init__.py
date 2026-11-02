"""Market model workstream: what the league pays for production, age and position.

Target: ``apy_cap_pct`` from the contracts table (APY as a share of the cap at
signing). Features: the previous two to three seasons of production, age at signing,
position. Training set: every veteran deal since 2011.

Evaluation: hold out the last two free-agency classes and report error on predicted
contract value. Week-4 milestone: a WR model that beats :class:`NaiveBaseline`.
"""
