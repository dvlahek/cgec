# Contrastive Graph-Evidence Classifier

Source code and numerical evidence for *Graph-Evidence Classification for Intrinsic Explanation and Training-Label Review*.

CGEC uses a locally scaled training graph and class-contrast diffusion fields for inductive prediction. The same fitted evidence supports exact training-neighbor contributions, deterministic representative graph paths, paired feature interventions and out-of-fold label review.

## Project layout

| Path | Contents |
| --- | --- |
| [`paper_reproducibility/xai/`](paper_reproducibility/xai/) | Paper-specific field-only CGEC estimator and query explanations |
| [`paper_reproducibility/benchmarks/`](paper_reproducibility/benchmarks/) | Prediction, feature/path validation, real-data and runtime experiments |
| [`paper_reproducibility/figures/`](paper_reproducibility/figures/) | Source scripts for figure construction |
| [`paper_reproducibility/results/`](paper_reproducibility/results/) | Archived numerical summaries and supporting inputs |
| [`examples/`](examples/) | Baseline comparisons and label-review evaluation scripts |
| [`src/mcgc/`](src/mcgc/) | Compatibility code required by earlier experimental scripts |
| [`wine/`](wine/) | Frozen grouped seed-0 Wine exports and independent analysis |
| [`docs/`](docs/) | Reproduction instructions and current evidence coverage |

The published method uses **`FieldOnlyCGEC`**, not the stochastic-walker prediction mechanism from the earlier MCGC prototype. Historical benchmark scripts depend on the MCGC package with walkers disabled. The paper classifier is implemented in `paper_reproducibility/xai/field_only_cgec.py`.

## Installation

Use Python 3.10 or later from the repository root.

```bash
git clone https://github.com/dvlahek/cgec.git
cd cgec
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[dev,paper]"
python -m pytest
python wine/verify_available_wine_evidence.py
```

For the chemical measurements, use the unmodified original UCI table. Do not reorder its records.

### Download the original UCI Wine data (PowerShell)

The original `winequality-red.csv` is not tracked by this repository. The analysis scripts require it at `wine/winequality-red.csv` when using the example commands below. From the repository root, run:

```powershell
Invoke-WebRequest -Uri "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv" -OutFile "wine/winequality-red.csv"
Test-Path "wine/winequality-red.csv"
```

The file contains 1,599 observations plus a header row. Keep its original order and semicolon-separated format.

```bash
python wine/verify_wine_direction.py --uci-csv /path/to/winequality-red.csv
python wine/recompute_wine_pair_value_strata.py --uci-csv /path/to/winequality-red.csv
python wine/recompute_wine333_from_cgec.py --wine /path/to/winequality-red.csv
```

## Reproduction and provenance

The repository includes the original paper-oriented CGEC source and selected archived numerical artifacts from the source branch of `dvlahek/MCGC-new` (commit `5b1fc6af4387d934f3f06a395b563db7a5d1efe3`) as well as verified seed-0 Wine files. They do not yet form a complete frozen recreation of every experiment in the latest manuscript. Some original baseline and multi-seed results, dataset caches and environment details remain to be deposited. The October results lock predates the November manuscript revision and must not be treated as a full independent re-run.

The strict-OOF corrected Supplementary Fig. S6 and its source data are also archived in `paper_reproducibility/outputs/` and `paper_reproducibility/results/`. The original v29 Table S1 sensitivity JSON and audit receipt have been validated and committed. Supplementary Fig. S5's exact conditional Wine null can be reconstructed from archived seed-0 OOF records using [`scripts/verify_wine_s5_conditional_null.py`](scripts/verify_wine_s5_conditional_null.py) without fitting.

See the [minimum reproducibility plan](docs/minimum-reproducibility.md), [final figures and Supplementary audit](docs/final-figures-supplement-audit.md), [Table 3 verification instructions](docs/table3-audit.md), [Table 4/5 label-review audit](docs/label-review-audit.md), [current evidence coverage](docs/reproducibility.md), and [Wine case-study protocol](docs/wine.md). No publication release, DOI or complete-reproduction claim has yet been assigned.

## Citation

The manuscript title is *Graph-Evidence Classification for Intrinsic Explanation and Training-Label Review*. Please use the final publication citation after acceptance. The Wine data originate from Cortez et al. (2009), *Decision Support Systems*, 47(4), 547–553.

The repository has no declared software license until the authors select one.

## Historical runtime timing source

Supplementary Table S3's v3.6b aggregated wall-clock summary was retrieved from a previously supplied Project file and preserved at [`paper_reproducibility/results/v36b_runtime_summary_recovered.json`](paper_reproducibility/results/v36b_runtime_summary_recovered.json). All 11 printed timing medians agree. Source-byte identity and the original candidate/component checkpoint JSONL files are unavailable; the restored summary is **not** evidence of an independent timing rerun. See [verification script](scripts/verify_supplement_s3_v36b.py) and [runtime decision record](docs/supplement-s3-runtime-release-decision.md).
