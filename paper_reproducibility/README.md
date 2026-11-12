# CGEC experimental source

This directory contains the field-only graph-evidence classifier, manuscript-facing experiments and source scripts for the associated figures.

## Method

The implementation in [xai/field_only_cgec.py](xai/field_only_cgec.py) constructs a locally scaled training graph, propagates class indicators, forms class-versus-rival contrasts and scores held-out queries using normalized neighbor affinities. Representative paths are computed after prediction. Stochastic walkers do not enter the paper's class score.

The original scripts and numerical summaries were copied from the paper reproducibility branch of `dvlahek/MCGC-new` at commit `5b1fc6af4387d934f3f06a395b563db7a5d1efe3`. They are retained under their original filenames for traceability.

## Layout

- `xai/` contains the field-only model and explanation interface.
- `benchmarks/` contains selective-risk, feature/path, real-data and runtime evaluation scripts.
- `figures/` contains publication-figure generators.
- `results/` contains archived summary records, which must be cross-checked against the final manuscript.
- `provenance/` contains query record selections for illustrative experiments.

## Scope

The source contains additional experimental scripts with earlier version numbers. Some expect cached PMLB datasets, baseline outputs or input files that are not currently present in this repository. These dependencies are not evidence that the full benchmark suite can yet be rerun unchanged. Follow the final manuscript's experimental configurations and deposit the remaining frozen inputs before creating a reproducibility release.

See the top-level README and docs/reproducibility.md for available and missing evidence.
