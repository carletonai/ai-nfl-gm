"""AI NFL GM: price every NFL player and draft pick in surplus value.

Package layout mirrors the pipeline in the project outline:

- :mod:`ai_nfl_gm.data`       pull nflverse and CFBD tables, build the ID and position crosswalks
- :mod:`ai_nfl_gm.market`     what the league pays for production, age and position
- :mod:`ai_nfl_gm.valuation`  aging curves, surplus value, the draft chart, trade value
- :mod:`ai_nfl_gm.prospects`  college production and combine data to predicted NFL value
- :mod:`ai_nfl_gm.api`        the FastAPI backend the trade calculator and draft board read from
"""

__version__ = "0.1.0"
