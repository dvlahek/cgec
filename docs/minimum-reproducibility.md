# Minimum reproducibility plan

Applies to the manuscript **Graph-Evidence Classification for Intrinsic Explanation and Training-Label Review**, PDF revision dated 12 November 2026.

The aim is to verify the reported numerical evidence with **as little new computation as possible**. An archived run is acceptable evidence if the source data, model revision, split, parameters and numerical output can be identified. A one-seed smoke test checks that code executes; it does **not** reproduce a twelve-seed statistical claim.

## 1. Preserve the working environment

From the repository root on the machine used for the Wine verification:

```powershell
New-Item -ItemType Directory -Force validation | Out-Null
git rev-parse HEAD | Set-Content validation\source_commit.txt
.\.venv\Scripts\python.exe --version | Set-Content validation\python_version.txt
.\.venv\Scripts\python.exe -m pip freeze | Set-Content validation\environment.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe wine\verify_available_wine_evidence.py
```

Keep `validation/` as a local audit folder; do not commit the environment snapshot or rerun output as a replacement for the original experimental data. The official UCI CSV is obtained separately and is ignored by Git.

## 2. Evidence map

| Manuscript item | Available evidence | Minimum next action | Current evidence status |
| --- | --- | --- | --- |
| Method and Table 1 | Paper-specific `FieldOnlyCGEC`, configuration in `paper_reproducibility/results/final_manuscript_results.json` | Keep the already passing unit tests and inspect code-to-equation correspondence | Model smoke tests passed; not a full benchmark reproduction |
| Table 2 — nonlinear E-AURC | `final_manuscript_results.json` and `figure_inputs.json` | Check four means, win/tie/loss counts and exact sign tests against the final manuscript | Archived aggregate values agree with the PDF |
| Table 3 — eight real datasets, fixed and tuned CGEC | Benchmark sources under `paper_reproducibility/benchmarks/` | **Recover the final dataset-by-seed or dataset-mean numerical outputs** and trace them to the reported values | Full final source artifact not yet in this repository |
| Tables 4 and 5 — label review and rival recovery | v3.1 strict-OOF summary and locally SHA-256-verified full audit | Preserve the original audit file and, for a complete public artifact, deposit it unchanged | **All 24 Table 4 means, 18 Table 5 means, 12 denominators and six Holm tests checked; full raw audit currently local-only** |
| Figure 3 — path stability and delete/refit | `figure_inputs.json` and original experiment scripts | Match stored aggregates and exact directional tests to the figure and Section 6 | Archived aggregates agree with the PDF |
| Section 6.4 — feature interventions | `final_manuscript_results.json`, `reproductions/feature_stability_v30/` and feature-stability script | No further run needed; preserve validated local output and source context | **Reproduced on seeds 0–4; statistics match at reported precision** |
| Wine Section 7, Figures 5–6 and Table 6 | `wine/source_wine_seed0/`, frozen strata, wine-333 contributions, original UCI data | No additional seed-0 run needed; preserve user-verified logs | Seed-0 correlations, strata and independent refit reproduced |
| Supplementary material | Supporting source and summaries | Verify each nontrivial numeric claim against a named file before final release | Coverage is partial; record unresolved source gaps |

**Important:** Matching an archived aggregate against the manuscript is a *consistency check*, not an independent repeat of the underlying experiment.

A complete local feature-stability re-execution was received on 12 November 2026 and deposited under [`reproductions/feature_stability_v30/`](../reproductions/feature_stability_v30/). Its 5 seeds and 10 pairwise comparisons reproduce the reference summaries. No additional feature-stability execution is required.

## 3. Resolved table-version discrepancy and locally verified source

The archived `paper_reproducibility/results/final_manuscript_results.json` is dated **28 October 2026** and was produced for an earlier manuscript version. Comparing its four-decimal values with the PDF dated **12 November 2026** shows:

- Table 4: **15 of 24** numerical cells differ.
- Table 5: **28 of 30** numerical cells differ, including some sample counts.

Examples:

| Metric | October archive | November manuscript |
| --- | ---: | ---: |
| Table 4, CGEC P@5% | 0.6914 | 0.6918 |
| Table 4, CGEC P@10% | 0.6343 | 0.6340 |
| Table 5, CGEC top-5% recovery | 0.8934 | 0.8931 |
| Table 5, CGEC corrupted samples in top 5% | 6,168 | 6,173 |

The apparent version discrepancy is **resolved for reported mean values**: the later [`v31_strict_oof_scaling_audit_summary.json`](../paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json) exactly matches the November PDF on **all 24 Table 4 values and all 18 Table 5 mean recovery values**. Its strict fold-local preprocessing protocol explains the small differences from the October archive. The v3.1 summary also matches the six Table 5 Holm-adjusted tests. The **12 pooled `n_corr` denominators have now been checked from the original full audit on the local Windows machine** using [`scripts/verify_v31_full_artifact.py`](../scripts/verify_v31_full_artifact.py). The script confirmed SHA-256 `530f9599d945dd895cc2d155b81020e7488a58dcd7369c36c8d362fb7cbc692e`, size 1,469,272 bytes, all 12 counts and the eight-dataset mean recovery rates. The full raw file is **not yet committed**; preserve it unchanged before an archival release. See [`docs/label-review-audit.md`](label-review-audit.md).

For CGEC vs OOF kNN label-review comparisons, the unadjusted exact two-sided sign-test value for 10 wins from 12 datasets is approximately 0.0386. If ROC-AUC and PR-AUC constitute one Holm family of two, the adjusted value is approximately 0.0771. The article and supplement must state the adopted correction consistently.

## 4. Smallest acceptable new computation

No new full seed sweep is required **if existing numerical records can be recovered and verified**.

1. **Required, no full training:** run the smoke tests and frozen Wine evidence check (commands above). The Wine UCI seed-0 calculations and wine-333 refit were already executed and matched in November.
2. **Required, no full training:** obtain the final numeric source for Table 3. For Tables 4–5, the v3.1 summary, all 42 printed means, and all 12 Table 5 denominators have been reconciled; preserve/deposit the original full v3.1 JSON before claiming complete archival coverage.
3. **Optional targeted smoke test:** execute only one predeclared small nonlinear dataset/seed or one label-review dataset/condition/seed to demonstrate end-to-end operation, with output to `validation/`. This is for execution provenance only. Do not extrapolate single-seed numbers to published multi-seed estimates.
4. **Conditional rerun:** if the correct source records for a major result cannot be recovered, rerun the **affected experiment family** or qualify/remove that unsupported claim. A single seed cannot substitute for missing evidence behind an aggregate.

The existing `benchmark_*_v29.py` / `v30.py` command-line entry points iterate over their frozen sets when run normally. Do not use their default invocation for the optional single-unit smoke test.

## 5. Evidence and release gate

For each final figure/table, keep the following in a manuscript-to-artifact manifest:

- final PDF table/figure and values,
- source script and Git commit,
- data source and revision,
- original output file and file checksum,
- run protocol and inferential unit,
- audit outcome: **matched**, **version mismatch** or **source missing**.

A complete paper-reproducibility claim is justified only when **all essential reported comparisons** have traceable, matching evidence. Publication-ready means not necessarily rerunning every seed now, but preserving the existing empirical basis. Until then, state the repository's limits accurately, and do not call an incomplete artifact a fully reproducible release.
