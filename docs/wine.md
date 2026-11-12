# Red-wine case study

## Data and row identities

The original UCI Wine Quality red-wine table has 1,599 observations, 11 physicochemical measurements and recorded quality grades 3–8. Obtain `winequality-red.csv` directly from the [UCI dataset](https://archive.ics.uci.edu/dataset/186/wine+quality). Retain the original record order, feature names and semicolon delimiter.

The archived `wine/source_wine_seed0/` files contain grouped five-fold out-of-fold (OOF) scores and fixed winner–runner feature interventions for seed 0. Identical chemical vectors were assigned to the same training fold. The supplied exports preserve zero-based original row indices.

## Method

The independent fold-refit implementation uses 12 neighbors, diffusion parameter 0.85, 40 diffusion steps and training-fold standardization. The review score for wine 333 (one-based UCI record) compares model class 5 against the recorded class 6 on the fold-4 model. Each contribution is the query affinity multiplied by the class-5 minus class-6 training-field contrast.

The twelve contributions sum exactly to the independently refitted margin, approximately 1.184213. The archived original OOF margin is approximately 1.184193. The difference is less than 2×10⁻⁵ but the results are not bitwise identical. The independent refit and the archived model export must not be represented as identical executions.

The signed intervention is `J_k = I_k * sign(winner_grade - runner_grade)`. Correlations and low/high measurement groups are descriptive and refer to the model-selected grade pair, not direct sensory effects.

## Reproduce

### Download the original UCI Wine data (PowerShell)

The original `winequality-red.csv` is not tracked by this repository. The analysis scripts require it at `wine/winequality-red.csv` when using the example commands below. From the repository root, run:

```powershell
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv" -OutFile "wine/winequality-red.csv"
Test-Path "wine/winequality-red.csv"
```

The file contains 1,599 observations plus a header row. Keep its original order and semicolon-separated format.

```bash
python wine/verify_available_wine_evidence.py
python wine/recompute_wine333_from_cgec.py --wine /path/to/winequality-red.csv --out-dir /path/to/output
python wine/recompute_wine_pair_value_strata.py --uci-csv /path/to/winequality-red.csv
```

The original CSV is not redistributed in this repository. The full five-seed OOF archive is not yet included; conclusions requiring that archive are not covered by these checks.
