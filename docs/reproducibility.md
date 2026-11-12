# Reproducibility

## Environment

Install from the project root.

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
python -m pytest
```

Record the Python interpreter, operating system, source commit and all package versions when regenerating numerical results. Dependency minimums in `pyproject.toml` are not an environment lock.

## Available checks

| Analysis | Available evidence | Status |
| --- | --- | --- |
| Wine seed-0 OOF row identity | 1,599 scores and intervention rows | Checked |
| Grade-oriented Wine associations | Frozen interventions plus original UCI file | Recomputable |
| Wine 333 evidence margin | Original fold mapping and independent field refit | Recomputable, not bitwise identical to archive |
| Wine five grouped seeds | Only seed 0 is provided | Not complete |
| Nonlinear twelve-seed benchmark | Full frozen numerical records are not provided | Not complete |
| Eight-dataset real-data panel | Full frozen numerical records are not provided | Not complete |
| PMLB label-review benchmark | Complete condition/seed exports are not provided | Not complete |
| Path and feature stability | All underlying original run records are not provided | Not complete |

## Preparing a paper release

A complete publication artifact should include the original CGEC model implementation, all benchmark and label-review scripts, exact dataset revision identifiers, group/split manifests, the full five-/twelve-seed outputs, exact environment versions, and commands to regenerate each table and figure.

Until these materials have been checked, the repository represents a partial case-study reproduction, not the entire paper.
