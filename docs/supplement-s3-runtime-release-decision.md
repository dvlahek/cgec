# Decision record — unsupported Supplementary Table S3 runtime measurements

**Status:** Proposed editorial change; **not yet applied to Overleaf manuscript sources**.

**Evidence reviewed:** CGEC main PDF dated 12 November 2026, Supplementary PDF dated 12 November 2026, repository source and experiment output tree, author-side filename and small-text-content searches on `C:\Articles\Clanci\MCGC-new-repo`.

## Decision and scientific justification

**Prefer removing the standalone runtime subsection and Table S3 for the current manuscript release rather than rerunning a 40-unit timing suite.** The experiment script `paper_reproducibility/benchmarks/benchmark_real_data_runtime_medium_v36b.py` and protocol code exist, but no original `v36b_runtime_summary.json` or runtime candidates/components logs were found. A search for the published values `3.143` and `7.821` found only unrelated `original_margin` values in an explanation-stability file. Those are not timing evidence.

Table S3 reports descriptive hardware-dependent wall-clock results: tuned CGEC 3.143 s and random forest 7.821 s end-to-end; tuned CGEC 34.45 ms and random forest 141.75 ms final fit+prediction, plus four other rows. Without the original 40 dataset×seed timing records, there is currently no evidence to independently verify these medians. Re-running them on a new software/hardware environment is a **new timing experiment**, not verification of the historical time observations.

Removing only this descriptive experiment does **not** affect the manuscript's established predictive E-AURC comparisons, graph-evidence method, representative-path analysis, label review or Wine case study. The main manuscript uses S3 runtime only in **one Discussion sentence** (in the currently reviewed PDF), and separately refers to the supplementary Wine protocol as Section S6. Other main references to Supplementary S2.x and S3 describe different experiments and remain intact.

## Surgical Overleaf edits — when authors accept this editorial choice

In `supplementary.tex`:

1. Delete the entire section presently headed **S4 Runtime evaluation**, including its 40-unit timing protocol, **Table S3**, its footnote and descriptive comparison paragraph, stopping **before** the next section heading, currently **S5 Additional representative-path visualization**. Remove no other tables or figures.
2. Change the headings **S5 Additional representative-path visualization** to **S4 Additional representative-path visualization**, and **S6 Exploratory red-wine case-study protocol** to **S5 Exploratory red-wine case-study protocol**. If section numbers are automatically generated, do not hard-code replacements; LaTeX will handle numbering.
3. In the Supplementary introduction, remove the phrase **“runtime measurements,”** from the list of supplementary contents. Preserve all other listed study components.
4. Continue calling the other tables **Table S1** and **Table S2**. Do **not** renumber Fig. S1–S7 (figure numbering is independent of section numbering).
5. Search all Supplementary source for explicit references to S4/S5/S6 and the removed Table S3. Adjust only section cross-references that actually changed.

In `main.tex`:

1. In the Discussion, remove the sentence: **“Controlled single-threaded runtimes (Supplementary Section S4) do not establish large-scale throughput.”**
2. Preserve the surrounding caveat: **“Scalability remains limited by the dense O(n²) affinity representation; sparse graph construction and diffusion are needed for larger data.”** This is a structural complexity argument rather than a benchmark result.
3. In the Wine discussion paragraph, change the parenthetic citation **“(Supplementary Section S6)”** to **“(Supplementary Section S5)”** for the exact conditional adjacency p-values 0.273 and 0.511. Use a fresh compilation and resolve any automatic cross-references.

The current main PDF contains no other occurrence of the word `runtime` and only one citation of `Supplementary Section S4` (Discussion). It cites `Supplementary Section S6` once for Wine. These counts apply to the 12-Nov-2026 PDF, **not** to any later Overleaf edits.

## Acceptance checks

- Recompile `main.tex` and `supplementary.tex`; verify section headings and numbering.
- No mentions of Table S3, 40-unit runtime, tuned CGEC 3.143 s, random forest 7.821 s, or hardware-specific final-model time remain in submitted text.
- Figure S6 must be the **already archived corrected v3.1** version, replacing its outdated figure in Overleaf.
- Preserve the historical v3.6b timing script/protocol in Git as documented research code; do not delete it merely because this manuscript version omits unverified results.
- Do not claim all complete end-to-end experiments are reproducible: continue the separate original-results / environment lock and final figure-source release checklist.

## Alternative if the runtime comparison is scientifically necessary

Keep Table S3 **only with new source evidence**: either recover the original 40-unit runtime outputs and compare them to all printed values, or run a new, frozen timing study with environment/hardware manifest, full 40-unit raw timing records, single-thread controls, and three-repeat final-model timers, then update the table and description to the new observed values. This would constitute additional work and should not be represented as reproducing lost 2026-11-12 timing runs.
