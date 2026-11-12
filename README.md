# Contrastive Graph-Evidence Classifier (CGEC)

Research code and numerical evidence for the manuscript **Graph-Evidence Classification for Intrinsic Explanation and Training-Label Review**.

CGEC is a graph-based classifier that propagates class labels over a locally scaled training graph, uses class-versus-rival evidence for inductive predictions, and provides inspectable neighbor contributions, feature interventions and out-of-fold training-label review.

## Repository status

The current repository provides a reproducible subset of the red-wine case study: grouped seed-0 out-of-fold exports, grade-oriented intervention analysis, and an independent fold refit for the illustrated wine. The complete multi-seed benchmark suite is **not yet included**. This distinction is reflected in the documentation and must be maintained in any paper availability statement.

## Getting started

Python 3.10 or later is recommended.

```bash
git clone https://github.com/dvlahek/cgec.git
cd cgec
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
python wine/verify_available_wine_evidence.py
```

The Wine consistency checks run on archived outputs. Recomputing the chemistry associations and the independent wine-333 model refit additionally requires the original `winequality-red.csv` from the [UCI Wine Quality dataset](https://archive.ics.uci.edu/dataset/186/wine+quality).

```bash
python wine/recompute_wine333_from_cgec.py --wine /path/to/winequality-red.csv
python wine/recompute_wine_pair_value_strata.py --uci-csv /path/to/winequality-red.csv
```

## Project layout

| Path | Description |
| --- | --- |
| `wine/` | Archived seed-0 exports, scripts, statistics and wine-333 evidence |
| `tests/` | Automated checks for data alignment and neighbor additivity |
| `docs/wine.md` | Experimental protocol and scope of the Wine results |
| `docs/reproducibility.md` | Reproduction instructions and outstanding materials |
| `paper/` | Manuscript source status and citation guidance |

## Publication materials

The entire five-seed Wine study, twelve-seed predictive evaluations, label-review benchmark suite, matching configuration files and environment lock must be added and checked before a full paper reproduction claim is made. This repository should not be confused with the earlier [MCGC walker prototype](https://github.com/dvlahek/MCGC-new).

## Reference

Cortez, P., Cerdeira, A., Almeida, F., Matos, T., and Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems*, 47(4), 547–553.

No software license has been declared yet.