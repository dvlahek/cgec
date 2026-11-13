# Final figure and Supplementary audit — 13 November 2026

**Basis:** latest manuscript PDFs `main(20261112-085144).pdf` (26 pages) and `supplementary(20261112-085145).pdf` (11 pages), the existing GitHub figure scripts and frozen result summaries. This is a **source/evidence coverage audit**, not a claim that every figure was regenerated pixel-identically. The PDFs were inspected and their figure and table captions enumerated.

## Main manuscript figures

| Figure | Identifiable source / data in this repo | Scope / remaining item |
| --- | --- | --- |
| Fig. 1, schematic | Mathematical methods and classifier code | The exact publication-ready vector source maintained in Overleaf is not deposited |
| Fig. 2, digits decision explanation | `paper_reproducibility/figures/fig_digits_xai.py`, `provenance/digits_query.json` | Code and example provenance present; exact final placed figure source should be archived with Overleaf package |
| Fig. 3, path stability and delete/refit | `fig_path_validation.py`, `results/figure_inputs.json` | Figure can be generated from the frozen aggregate inputs; original run-level path source not yet archived |
| Fig. 4, reviewed digits | CGEC source and example logic; final placed illustration currently in an older author-side figure package | **Final figure asset/source not tracked in the new GitHub repo** |
| Fig. 5, wine chemistry | `wine/source_wine_seed0/` plus independently verified UCI chemistry | Seed-0 numerical evidence available; final plotting source/placed image not tracked |
| Fig. 6, wine 333 | `wine/WINE333_REFIT_AUDIT.json`, original 12 direct contributions, recomputation script | Main numerical claim independently checked; final plotting source/placed image not tracked |

## Supplementary evidence map

| Item | Data/implementation | Assessment | Minimum next step |
| --- | --- | --- | --- |
| Table S1 — one-factor sensitivity | `benchmark_field_core_sensitivity_v29.py`; original `v29_field_core_parameter_sensitivity.json` (231,765 bytes) now located in the old local `results/` directory | **Source file located but its contents not yet audited** | Run [`scripts/verify_supplement_s1_v29.py`](../scripts/verify_supplement_s1_v29.py), then stage original byte-for-byte if all checks pass |
| Table S2 — digits/wine prediction | `results/figure_inputs.json` -> `predictive.real_primary` | Four published mean advantages and W/T/L checked by `tests/test_supplementary_table_s2.py` | Test locally (no training) |
| Table S3 — runtime, 40 units | `benchmark_real_data_runtime_medium_v36b.py` | Original v36b runtime summary/records **not** deposited | Locate `v36b_runtime_summary.json` and candidate/component JSONL before claiming raw reproducibility |
| Fig. S1 — selective-risk differences | `fig_predictive_boundary.py`, `results/figure_inputs.json` | Reconstructible from archived *aggregate* source, not from original seed-level runs | Retain source file and final placed figure; no training required |
| Fig. S2 — spiral path | `fig_spiral_evidence.py`, `provenance/spiral_query.json` | Script can regenerate an illustrative case; final placed figure source absent | Archive publication plot source from original manuscript project |
| Fig. S3 — wine feature magnitudes | `wine/source_wine_seed0/wine_oof_feature_interventions.csv` | Raw seed-0 intervention data available; standalone figure generator not yet tracked | Retain the plotting source or plot-ready aggregation |
| Fig. S4 — wine oriented interventions by grade | Wine seed-0 OOF intervention and grade records | Seed-0 source available; standalone figure generator not yet tracked | Archive exact plotting source |
| Fig. S5 — wine adjacent-review conditional null | Wine OOF scores; PDF reports conditional p=0.273 and 0.511 | **Original conditional hypergeometric calculation and plot data not deposited** | Find original calculation JSON/script, no new OOF fitting |
| **Fig. S6 — PMLB dataset deltas** | Original v3.1 full JSON, `fig_s6_v31_summary.json`, and revised GitHub PDF/PNG | **Verified mismatch fixed in regenerated image:** 6/24 plotted three-decimal labels differed from the old v2.1 summary; sign tests remain 10/12 wins | **Visually approve revised PDF and replace the old Fig. S6 in Overleaf** |
| Fig. S7 — breast-cancer interventions | `fig_bc_interventions.py`, `results/bc_interventions_summary.json`, archived five-seed feature-stability reproduction | Numerical stability result reproduced; plot script exists | Retain final placed figure asset; no fresh seed sweep |

**Figure numbering caution:** the historical source file `fig3_oof_vs_knn.py` corresponds to **Supplementary Fig. S6 in the latest PDF**, not to main Fig. 3 (which is path validation). Preserve that distinction in any new documentation.

## Check S6 using original v3.1 records — NO TRAINING

From the new `cgec` repository root on the experiment workstation:

```powershell
git pull
.\.venv\Scripts\python.exe -m pytest

.\.venv\Scripts\python.exe scripts\verify_supplement_s6_v31.py --raw "C:\Articles\Clanci\MCGC-new-repo\paper_reproducibility\results\v31_strict_oof_scaling_audit.json"
```

The verifier enforces the archived SHA-256, 12 datasets and 240 dataset-condition-seed units, recomputes the 24 Figure S6 data points and the 10/12 exact sign tests, then compares the printed three-decimal labels with the old figure data. Its output is `validation/fig_s6_v31_summary.json`.

**If labels differ**, generate a corrected replacement figure without training:

```powershell
.\.venv\Scripts\python.exe paper_reproducibility\figures\fig3_oof_vs_knn.py --summary-json validation\fig_s6_v31_summary.json --output-dir validation\s6_v31
```

Then replace **only Supplementary Fig. S6** in Overleaf once the author visually confirms its match to the v3.1 results. Do not silently substitute the plot or rewrite the frozen historical file.

## Confirmed Figure S6 correction (local verifier, 13 November 2026)

The author ran the source-checking verifier on the original 1,469,272-byte full v3.1 OOF JSON and reported **PASS**, 12 datasets, 240 units, 24 compared figure points. Six printed values change:

| Dataset | Metric | Older displayed label | v3.1 correct label |
| --- | --- | ---: | ---: |
| ecoli | PR-AUC | +0.015 | +0.014 |
| mfeat_zernike | PR-AUC | +0.139 | +0.140 |
| spectf | PR-AUC | +0.179 | +0.173 |
| vehicle | ROC-AUC | -0.019 | -0.018 |
| vehicle | PR-AUC | -0.022 | -0.020 |
| yeast | PR-AUC | +0.008 | +0.007 |

Maximum absolute new–old difference across all 24 points: `0.006032602`. See [verification receipt](../reproductions/supplement_s6_v31/verification_receipt.json). A revised figure has since **been regenerated and deposited in GitHub** as `paper_reproducibility/outputs/fig_s6_v31.pdf` and `.png` (commit `86795ac1614c7fe8e969faac2ce8cf8afecea485`). **Visual confirmation and replacement in Overleaf are still pending.** Keep the old frozen summary as historical evidence; do not overwrite it.

## Preserve original audited inputs — NO TRAINING

The original v3.1 label-review audit and v3.2c/v3.3 full files passed local source/result checks and **have now been deposited on GitHub** in commit `88f862f4fed463d2390e633e0ddd4aa75ee8e5cf`. The commands below document how to recheck or restore them if needed; do not create a duplicate commit:

```powershell
.\.venv\Scripts\python.exe scripts\archive_minimum_results.py --source-results-dir "C:\Articles\Clanci\MCGC-new-repo\paper_reproducibility\results"

# If the dry-run reports PASS for all six:
.\.venv\Scripts\python.exe scripts\archive_minimum_results.py --source-results-dir "C:\Articles\Clanci\MCGC-new-repo\paper_reproducibility\results" --apply

git status
```

The script validates four pinned SHA-256 values and checks sizes for the two additional full source files. It refuses to overwrite conflicting files. It does **not** commit or push automatically. Review changes, then commit only these original outputs and the generated `archived_source_manifest.json`.

## Supplementary Table S1 — located original v29 output (13 November 2026)

The author found original files under `C:\Articles\Clanci\MCGC-new-repo\results`:

- `v29_field_core_parameter_sensitivity.json` — **231,765 bytes**; complete output was found but **has not yet passed the read-only source audit**.
- `v29_field_core_parameter_sensitivity.log` — **40,856 bytes**; optional provenance, not a numerical substitute for the full JSON.

The preserved v2.9 benchmark script's output schema contains `datasets`, `pooled_primary`, `protocol`, and 36 dataset×seed records with seven one-factor-at-a-time configurations. An audit tool has been added to independently recalculate all 14 four-decimal Table S1 means, six reported exact sign-test p-values, and the two diffusion-depth prediction-disagreement counts.

Run:

```powershell
git pull --ff-only origin main
.\.venv\Scripts\python.exe scripts\verify_supplement_s1_v29.py --raw "C:\Articles\Clanci\MCGC-new-repo\results\v29_field_core_parameter_sensitivity.json"

# Only after PASS (this stages source + receipt in tracked paths):
.\.venv\Scripts\python.exe scripts\verify_supplement_s1_v29.py --raw "C:\Articles\Clanci\MCGC-new-repo\results\v29_field_core_parameter_sensitivity.json" --stage
git status --short
```

This does not fit any model. Do not mark Table S1 fully audited until the result shows `PASS` for all its values and statistical checks.

## Remaining evidence-first search

Search only existing files; do **not** launch the benchmark scripts:

```powershell
Get-ChildItem "C:\Articles\Clanci\MCGC-new-repo" -Recurse -File |
  Where-Object { $_.Name -match "v29_field_core_parameter_sensitivity|v36b_runtime_(summary|candidates|components)|wine_review|wine_adjacent" } |
  Select-Object FullName,Length
```

**Release gate:** numeric tables 3–5 and seed-0 Wine/feature-stability checks are closed. The revised v3.1 Fig. S6 PDF/PNG and numerical input are already committed, but its *visual approval and Overleaf replacement remain open*. The original S1 v29 result is located locally and awaits the read-only verifier; S3/S5 source evidence and final placed plot sources are still outstanding. The original raw files for Tables 3–5 are archived. Neither this audit nor source copying implies a complete end-to-end experiment rerun.
