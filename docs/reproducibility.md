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
| Real-data eight-dataset panel | v32c/v33 scripts, archived full JSON/JSONL and verified receipt | All 48 Table 3 cells, 96 seed units and five sign tests checked; original source files deposited | Verified locally; raw outputs and SHA-256 manifest tracked |
| PMLB label review | v3.1 strict-OOF source, full original JSON, summary, tests | Table 4 (24 values), Table 5 (18 means), all 12 denominators, six Holm tests checked | **Verified locally**; full raw audit and checksum tracked |
| Path and feature stability | Source scripts included | Only selected numerical summaries included | Incomplete |
| Figures and supplementary tables | [Mapped audit](final-figures-supplement-audit.md), v3.1-corrected Fig. S6 PDF/PNG and plot input | S6 corrected GitHub files deposited; v29 S1 original located locally and verifier added; S2 regression test; S3/S5 still missing raw source | Partial; no new fitting required for current verification workflow |

## Paper version

The archived `paper_reproducibility/results/final_manuscript_results.json` was prepared before the November 2026 manuscript edits and is not the authoritative source for the final Table 4/5 results. Those **42 printed means** match `paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json` exactly. The full v3.1 source JSON has been SHA-256 verified locally and all 12 pooled Table 5 denominators checked; see [label-review audit](label-review-audit.md). The full original v3.1 file is now deposited under `paper_reproducibility/results/`, with SHA-256 in `archived_source_manifest.json`.

## Required for a full release

- Final manuscript-matched source commit and environment lock
- Complete multi-seed and label-review outputs
- Exact split and grouping manifests for every dataset
- Baseline configuration, PMLB dataset revision and required caches
- One documented command per reported table and figure
- Automated comparison of regenerated outputs against the final results

No complete manuscript reproduction or release DOI is claimed at this stage.
