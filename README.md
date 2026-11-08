# AI NFL GM

A Carleton AI Society project. We want to price every NFL player and draft pick in one
number, **surplus value**: what a player produces minus what he costs against the salary cap.
From that we build a trade calculator and a draft board for
[carletonai.com](https://carletonai.com). All the data is free.

We have not started building yet. For now the job is to get the data on your laptop and look
around.

## Get the data

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (it brings its own
Python), then:

```bash
git clone https://github.com/carletonai/ai-nfl-gm.git
cd ai-nfl-gm
uv run get_data.py   # about 20 MB into data/, takes a minute or two
uv run jupyter lab   # start a notebook
```

In the notebook:

```python
import pandas as pd

contracts = pd.read_parquet("data/contracts.parquet")
contracts[["player", "position", "year_signed", "apy_cap_pct"]].head()
```

## What's in `data/`

| File | What it is |
| --- | --- |
| `contracts` | Every contract Over The Cap tracks. `apy_cap_pct` is the yearly value as a share of the cap |
| `players` | One row per player, with the IDs that join the other tables (`gsis_id`, `pfr_id`, ...) |
| `draft_picks` | Every pick since 1980: team, slot, college, career value (`w_av`) |
| `combine` | Combine results since 2000: 40 time, bench, vertical, ... |
| `trades` | Trades since 2002 |
| `player_stats` | Regular-season stats per player per season, 2011 to now |

Two things that trip people up: each contract's year-by-year cap hits sit inside its
`season_history` column, and `car_av` in `draft_picks` is empty, so use `w_av`.

## Questions

Ask in `#ai-nfl-gm` on the CAIS Discord, or ask Jeremy.

---

Code is [MIT](LICENSE). The data comes from [nflverse](https://github.com/nflverse), which
packages Over The Cap and Pro Football Reference data. Credit them, and keep the downloaded
files out of git (`data/` is ignored already).
