# notebooks

Exploration lives here; nothing imports from this folder.

- Install the extra: `uv sync --extra notebooks`, then `uv run jupyter lab`.
- Name notebooks `NN_<stream>_<topic>.ipynb`, e.g. `01_data_contracts_explore.ipynb`.
- Clear outputs before committing: `uv run jupyter nbconvert --clear-output --inplace <nb>`.
- Load data through the package, not by hand:

  ```python
  from ai_nfl_gm.data import nflverse
  contracts = nflverse.load("contracts")
  ```

- When something in a notebook turns out to be right, move it into `src/ai_nfl_gm/` with a
  test. The notebook can stay as the record of how you got there.
