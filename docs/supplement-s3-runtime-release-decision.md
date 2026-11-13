# Supplementary Table S3 — historical runtime summary recovered

**Decision (13 November 2026): Keep Supplementary Table S3.** Do not remove the runtime subsection from Overleaf.

## What was recovered

The earlier proposal to remove S3 was based on searching Windows directories that did not contain the original experiment archive. The author correctly recalled that a lengthy runtime experiment had been completed and output had been submitted in a previous conversation.

The Project's previously supplied file **`v36b_runtime_summary.json`** was recovered through indexed conversation/Project file content. It is a complete, valid JSON document with v3.6b metadata, eight data sets, five fixed seeds (0, 2, 5, 8, 11), 40 units, single-thread configuration, 36 CGEC tuning candidates, and full per-dataset **aggregate** timing statistics. The JSON was retrieved as text, parsed and reserialized for GitHub as:

`paper_reproducibility/results/v36b_runtime_summary_recovered.json`

**Provenance limitation:** the original raw-byte materialization path was unavailable, so bytewise identity and the original source SHA-256 cannot be established. The archive copy is a recoverable text reconstruction of the former JSON, not a byte-for-byte original. The detailed `v36b_runtime_components.jsonl` and `v36b_runtime_candidates.jsonl` files were not recovered.

## Verified Supplementary Table S3

| Method | End-to-end median (s) | Final fit+predict median (ms) |
| --- | ---: | ---: |
| Fixed CGEC | not applicable | 35.48 |
| Tuned CGEC | 3.143 | 34.45 |
| Scaled tuned kNN | 0.0439 | 1.14 |
| Tuned random forest | 7.821 | 141.75 |
| Scaled tuned Label Spreading | 0.1147 | 2.39 |
| Tuned RBF-SVM | 0.0846 | 3.19 |

All **11 published numerical cells** agree with the recovered source after rounding. Each of six methods has `n=40` in both relevant panel summaries, with `n=5` within each of the eight data sets. The metadata records Python 3.12.2, NumPy 2.5.4, scikit-learn 1.9.1, Windows 11, logical CPUs 12, single-thread numerical settings, random forest `n_jobs=1`, and `time.perf_counter`.

Check from the current repository without performing any timed run:

```powershell
git pull --ff-only origin main
.\.venv\Scripts\python.exe scripts\verify_supplement_s3_v36b.py
.\.venv\Scripts\python.exe -m pytest
```

This is sufficient to restore the **historical descriptive aggregate evidence** supporting the existing Table S3. Do not claim full reproduction of the 40 actual timing measurements or the original 240/1,440 checkpoint rows: those require the missing raw JSONL checkpoint files.

## Editorial action

- **Keep** the existing Supplementary S4 Runtime evaluation section and Table S3 without renumbering other sections.
- **Keep** the Discussion caveat that measured single-threaded runtime does not demonstrate scaling throughput.
- **Do not** change the Wine cross-reference from Supplementary S6 to S5; such a renumbering was previously suggested only if S4 were deleted.
- The previous omission recommendation is **withdrawn and superseded by this evidence recovery**.
- The final corrected Fig. S6 still requires placement and visual approval in Overleaf.

If original JSONL timing checkpoint files reappear in backup, archive them separately and verify their medians against this recovered summary. No new model training is required for this current audit.
