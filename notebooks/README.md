# notebooks

Exploration lives here; nothing imports from this folder.

- `make setup` already installs JupyterLab; start it with `uv run jupyter lab`. (If you synced
  without extras, add them with `uv sync --inexact --extra notebooks` so the `ml` packages stay.)
- Name notebooks `NN_<stream>_<topic>.ipynb`, e.g. `01_data_contracts_explore.ipynb`.
- Clear outputs before committing: `uv run jupyter nbconvert --clear-output --inplace <nb>`.
- Load data through the package, not by hand:

  ```python
  from ai_nfl_gm.data import nflverse
  contracts = nflverse.load("contracts")
  ```

- When something in a notebook turns out to be right, move it into `src/ai_nfl_gm/` with a
  test. The notebook can stay as the record of how you got there.
