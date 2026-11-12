# Reproducibility

## Environment

Python 3.10 or newer. Install the research dependencies and run local tests.

```bash
python -m venv .venv
python -m pip install -e ".[dev,paper]"
python -m pytest
python wine/verify_available_wine_evidence.py
```

Record the exact interpreter, platform, package versions, code commit and dataset revision for any independently published numerical run. The minimum dependency versions in this repository do not constitute an environment lock.

## Source code

The paper-specific classifier is `paper_reproducibility/xai/field_only_cgec.py`. Its training graph, diffusion field, local evidence, exact margin decomposition, feature interventions and deterministic path logic match the paper-oriented implementation archived on source branch `dvlahek/MCGC-new@5b1fc6af4387d934f3f06a395b563db7a5d1efe3`.

The `src/mcgc/` package provides compatibility for the original benchmark scripts. In the paper's predictive experiments, its stochastic walker component is disabled. Scripts under `paper_reproducibility/benchmarks/` and `examples/` are preserved with original version-specific names so their dependencies can be traced.

## Current coverage

| Study component | Source code | Frozen inputs/results | Status |
| --- | --- | --- | --- |
| Paper-specific field-only CGEC | Included | Small self-tests | Code available |
| Wine grouped seed-0 OOF | Included analysis scripts | 1,599 score and intervention records | Checkable |
| Wine 333 independent refit | Included | Fold indices and direct contributions | Checkable; small archived difference |
| Wine five grouped seeds | Analysis code, partial exports | Only seed 0 currently available | Incomplete |
| Nonlinear twelve-seed prediction | Benchmark scripts included | Full original run records and baseline outputs not deposited | Incomplete |
| Real-data eight-dataset panel | Benchmark/tuning scripts included | Full dataset caches and seed-level outputs not deposited | Incomplete |
| PMLB label review | v3.1 strict-OOF source, summary, original locally verified file and tests | Table 4 (24 values), Table 5 (18 means), all 12 denominators, six Holm tests checked | **Verified locally**; original full audit needs repository deposit |
| Path and feature stability | Source scripts included | Only selected numerical summaries included | Incomplete |
| Figures | Generation scripts and selected numerical inputs included | Not every final figure data source supplied | Incomplete |

## Paper version

The archived `paper_reproducibility/results/final_manuscript_results.json` was prepared before the November 2026 manuscript edits and is not the authoritative source for the final Table 4/5 results. Those **42 printed means** match `paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json` exactly. The full v3.1 source JSON has been SHA-256 verified locally and all 12 pooled Table 5 denominators checked; see [label-review audit](label-review-audit.md). The original full file is not yet deposited in Git.

## Required for a full release

- Final manuscript-matched source commit and environment lock
- Complete multi-seed and label-review outputs
- Exact split and grouping manifests for every dataset
- Baseline configuration, PMLB dataset revision and required caches
- One documented command per reported table and figure
- Automated comparison of regenerated outputs against the final results

No complete manuscript reproduction or release DOI is claimed at this stage.
