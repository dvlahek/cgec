# Source provenance

The CGEC manuscript-oriented code in `paper_reproducibility/`, the accompanying six baseline and label-review scripts in `examples/`, and the compatibility package in `src/mcgc/` were transferred from:

- Repository: `dvlahek/MCGC-new`
- Source branch: `paper/reproducibility-xai-20261025`
- Source revision: `5b1fc6af4387d934f3f06a395b563db7a5d1efe3`

The original file paths and script names are retained except that `benchmark_field_only_final_predictive_v30.py` resolves its v26 baseline dependency from the repository-root `examples/` directory. No scientific coefficients or benchmark outputs were altered during this transfer.

The red-wine seed-0 CSV files and the independent wine-333 contributions were copied from the numerical evidence archive developed for the case-study revision. File checksums are in `DATA_MANIFEST.sha256`.

Some results recorded in the October numerical lock are not identical to the final November manuscript, and several large raw experiment outputs were not found in the archival source branch. This repository therefore documents both what is available and what remains to be deposited before a final release.
