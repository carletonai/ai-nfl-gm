# configs

Sport-level configuration, one YAML file per league under `sports/`.

The code treats the sport as a config (see `ai_nfl_gm.config.load_sport_config`), so
adding the NBA later means adding `sports/nba.yaml` with its own cap rules, position
groups and crosswalk, not editing the models.

`sports/nfl.yaml` is the only file today. The cap table is verified against Over The Cap's
figures in nflverse and the league's announcements (sources in the file; `make check-cap-table`
re-runs the nflverse check). Entries marked **verify** in its comments (the lossy position
mappings such as OLB) are defaults the Data workstream must confirm before they feed a model.

`draft_charts/` holds published reference pick-value charts as small CSVs (`pick,value`).
