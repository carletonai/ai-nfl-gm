# configs

Sport-level configuration, one YAML file per league under `sports/`.

The code treats the sport as a config (see `ai_nfl_gm.config.load_sport_config`), so
adding the NBA later means adding `sports/nba.yaml` with its own cap rules, position
groups and crosswalk, not editing the models.

`sports/nfl.yaml` is the only file today. Entries marked **verify** in its comments (the cap
table, the lossy position mappings) are starting points that the Data workstream must check
against Over The Cap before they feed a model.

`draft_charts/` holds published reference pick-value charts as small CSVs (`pick,value`).
