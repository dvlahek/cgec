# Follow-up QA of new Overleaf exports — 13 November 2026, 16:11 filenames

**Reviewed files:** `main(20261113-161107).pdf` (26 pages; SHA-256 `693d03c36bcdf9de9d1442251e3af4ef7a4309836dff9af3bba6cadd013494b9`) and `supplementary(20261113-161107).pdf` (11 pages; SHA-256 `589ffc381be0907bb0f3c2d244640179ff149fd7e38dc4882737b6e1f99bf64f`).

**Corrected since previous Nov-12 review:**
- Supplementary PDF p. 10, Fig. S6 has all six corrected v3.1 figure labels (`ecoli` PR +0.014; `mfeat Zernike` PR +0.140; `SPECTF` PR +0.173; `vehicle` ROC −0.018 / PR −0.020; `yeast` PR +0.007).
- Main PDF p. 14 explicitly reports **unadjusted** `p=0.0386` for each kNN ROC-AUC/PR-AUC comparison, with `p_Holm=0.0771` when two metrics are treated as one family.
- Author affiliations/corresponding email appear on p. 1. Supplementary S4 and Table S3 remain correctly present.

**Two required remaining edits:**
1. **Main PDF p. 14** has literal `Individual reviewed cases are examined in Section ??.` Replace unresolved cross-reference with a valid LaTeX label pointing to **Section 6.5, Explainable training-label review**; compile twice and confirm `??` is absent.
2. **Supplementary PDF p. 10, Fig. S6 caption** still says `with exact two-sided sign-test p = 0.0386 for both metrics` and does not qualify the p-values as unadjusted. Revise to `with unadjusted exact two-sided sign-test p = 0.0386 for each metric (Holm-adjusted p = 0.0771 for the two-metric family)`. This matches the corrected main-text disclosure.

**After those two edits:** re-export PDFs, search for `??` in both, check the Fig. S6 caption and the main p. 14 reference. No further numeric runs are indicated. The final data and code availability statement should still reflect the true archive/public release status at submission. No Overleaf edits were made through GitHub.

---

# Manuscript + Supplementary final QA — 13 November 2026

**Source versions actually reviewed**: main PDF `main(20261112-085144).pdf` (26 pages, SHA-256 `3d687bf0a7b5dc98632f2ec028ce0b1f38ef57a47932f11056bc617f86e72369`), Supplementary PDF `supplementary(20261112-085145).pdf` (11 pages, SHA-256 `6c8bbecd8d1d919db23a2a389abb19b5bf59ffd7fb448d574129b43dacb1aca8`). These **predate** the 13 November 2026 corrected S6 asset and subsequent GitHub data archive; they are **not** known to be the latest Overleaf builds.

**Scope**: Rendered inspection of all pages and high-resolution review of the primary figures and supplementary figures; cross-check of principal printed results against already verified, archived repository evidence. This is not a pixel-identical figure source re-derivation, journal-policy audit, or independent rerun of all models.

## Required before submission

### 1. Replace outdated Supplementary Fig. S6 (PDF page 10)

The reviewed 12-November Supplementary PDF still contains the older plotted values:

| Dataset | Metric | Old visible label | Correct v3.1 label |
| --- | --- | ---: | ---: |
| ecoli | PR-AUC | +0.015 | +0.014 |
| mfeat_zernike | PR-AUC | +0.139 | +0.140 |
| spectf | PR-AUC | +0.179 | +0.173 |
| vehicle | ROC-AUC | -0.019 | -0.018 |
| vehicle | PR-AUC | -0.022 | -0.020 |
| yeast | PR-AUC | +0.008 | +0.007 |

The corrected plot and checked underlying v3.1 numbers are already in the repository:
- [Corrected PDF](../paper_reproducibility/outputs/fig_s6_v31.pdf)
- [Corrected PNG](../paper_reproducibility/outputs/fig_s6_v31.png)
- [Verified plot data](../paper_reproducibility/results/fig_s6_v31_summary.json)
- [Verification receipt](../reproductions/supplement_s6_v31/verification_receipt.json)

**Action:** replace only the Overleaf graphic used for `Figure S6` with the archived corrected PDF, not the original frozen older `fig3_oof_vs_knn.pdf`. Recompile and confirm the six values in the **final exported** Supplementary PDF. No need to regenerate other figures.

### 2. Specify that Fig. S6 and main Table 4's kNN sign-test p-values are unadjusted

Main manuscript PDF p. 14: 10/12 ROC-AUC and 10/12 PR-AUC wins vs OOF kNN, with `p=0.0386` for each metric. Supplementary Figure S6 caption p. 10 repeats the same. The exact two-sided sign-test p-value is `0.03857421875` for **each**. These are unadjusted values.

Suggested *minimal* copy edits:
- Main Table 4 discussion: change `(p = 0.0386 for both metrics)` to `(unadjusted two-sided sign-test p = 0.0386 for each metric)`.
- Figure S6 caption: change `with exact two-sided sign-test p = 0.0386 for both metrics` to `with unadjusted exact two-sided sign-test p = 0.0386 for each metric`.

**Interpretation:** if the two metrics are treated as one multiplicity family, Holm-adjusted p-values are `0.0771484375` each, so the two individual unadjusted p-values should **not** be represented as establishing family-wise significance at 0.05. The 10/12 descriptive directional findings remain correct. Do not change the values or invent a new preregistered test family.

### 3. Recheck the final Code and Data Availability wording just before release

Main PDF p. 23: the statement currently says a permanent release of the *complete* code and frozen benchmark outputs has not yet been deposited and an archival identifier will be supplied later. This remains correct **if** the final public DOI/archive still does not exist. As of 13 November, the working GitHub repository includes more raw evidence (v3.1, v3.2c/v3.3, v2.9 S1, reconstructed v3.6b S3, Wine seed-0) than the older PDF described.

**Action:** align the statement with the actual submission-time release/publication state. Do not call the private working GitHub repo a complete public archival release, and do not promise an existing DOI. The S3 v3.6b JSON was reconstructed from a prior submitted text file, not source-byte-identical with original; its raw candidate/component JSONL checkpoints remain unavailable.

## Verified; no targeted numerical edits recommended

- **Main Table 2 (PDF p. 13):** verified exact two-sided sign-test values from W/T/L: kNN 27/9 `p=0.00393317`, RF 26/10 `p=0.01133098`, LS 28/8 `p=0.00119324`, RBF-SVM 17/19 `p=0.8679394`. The main claim that the first three survive Holm correction over four baselines is consistent.
- **Main Table 3 (p. 13):** the previously locked v3.3 read-only verifier checked all 48 cells / 96 seed-level units. Do not substitute older October summary.
- **Main Table 4 (p. 14) and Table 5 (p. 15):** the previously locked v3.1 source audit checked 24 Table 4 values, 18 recovery means, 12 counts and six Holm tests.
- **Supplementary Table S1 (p. 1):** original 231,765-byte v2.9 JSON and checksum receipt verified 14 means, 36 units, six sign-test checks.
- **Supplementary Table S2 (p. 3):** archived regression/source audit remains consistent with 24 paired dataset×seed units.
- **Supplementary Table S3 (p. 5):** **retain**. Historic v3.6b summary has been recovered and all 11 printed timing medians checked: eight datasets × five seeds, n=40. Individual raw timing checkpoint rows remain unavailable. The label "descriptive" / "not a scaling analysis" is appropriate.
- **Main Fig. 5 (p. 19)** and **Fig. 6 (p. 21):** visual graphics/captions are internally aligned with the six recorded grades, 1,599 wines, class-oriented signs and wine 333's twelve-neighbor case. Wine review S5 uses the correctly conditioned grade-stratum reference.
- **Supplementary Fig. S5 (p. 10):** exact Wine top-80/top-160 conditional upper-tail p-values re-derived from original archived seed-0 OOF scores, checked against the printed `0.273` and `0.511`. No numerical replacement required.
- **Figure count and numbering:** main Figs. 1–6, Supplementary Figs. S1–S7. Cross-references for Supplementary Sections S4 (runtime), S6 (Wine) and S7 (other classifier-inspection figures) are appropriate **when S4 remains present**. Do not apply the earlier abandoned section-removal/renumbering plan.
- Text extraction found no unresolved `??` placeholders. Rendered scans show no critical figure/table content clipping. This does not guarantee compatibility with a future Overleaf build.

## Nonblocking visual note

Main PDF p. 17, Fig. 4 (digits label review): there is a tiny disconnected glyph/dot near the top-left edge of the graphic, above the left-most chart column, visible at high zoom. It is not a scientific-data discrepancy. If the original figure source can be re-exported without changing content, remove the stray fragment; otherwise do not prioritize this above S6 and the statistical disclosure.

## Exact acceptance gate

1. Overleaf Supplementary p. 10 contains all six **corrected Fig. S6 labels**.
2. Main p. 14 and Supplementary Fig. S6 caption use `unadjusted` for the two individual sign tests (or provide a clear multiplicity-family statement).
3. Keep Supplementary Table S3 and existing S4/S5/S6/S7 section numbering.
4. Re-export main and Supplementary PDFs, and spot-check the two places above in **new PDFs**.
5. Confirm data/code availability statement reflects actual released access and deposition.
6. Preserve all frozen sources and experiment receipts without rerunning the experiments.
