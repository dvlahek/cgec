# Table 3 — read-only v3.3 verification

The final manuscript (12 November 2026, Table 3) reports E-AURC dataset means on eight pre-specified real-data datasets across 12 outer seeds for fixed CGEC, matched-tuned CGEC, kNN, random forest, Label Spreading and RBF-SVM.

## Original outputs located on the experiment workstation

These files were located in `C:\\Articles\\Clanci\\MCGC-new-repo\\paper_reproducibility\\results`, but their bytes have not been uploaded into this repository:

| File | Bytes | Use |
| --- | ---: | --- |
| `v32c_real_data_confirmation.json` | 2,979,336 | Earlier frozen result summary |
| `v32c_real_data_confirmation_runs.jsonl` | 1,535,603 | Original fixed-CGEC and tuned-baseline seed records |
| `v33_tuned_cgec_candidates.jsonl` | 1,294,741 | Matched-tuning candidate records |
| `v33_tuned_cgec_runs.jsonl` | 1,046,187 | Tuned-CGEC per-seed results |
| `v33_tuned_cgec_summary.json` | 740,879 | Full v3.3 dataset and panel summary |

The presence and file sizes above come from the author's local file listing, not from an independent file-content check.

## Run the minimum audit (no training)

Run in the new `cgec` repository from PowerShell:

```powershell
git pull

.\.venv\Scripts\python.exe scripts\verify_table3_v33.py --results-dir "C:\Articles\Clanci\MCGC-new-repo\paper_reproducibility\results"
```

The script:

1. Requires the frozen v3.3 full 8×12 dataset/seed protocol.
2. Cross-checks all 96 per-seed runs in the v3.3 summary with original v3.2c fixed baseline and v3.3 tuned-model checkpoints.
3. Independently computes all 48 Table 3 E-AURC means and compares them with the latest PDF's printed four-decimal values in units of `10^-3`.
4. Checks the five primary dataset-level win/tie/loss summaries and exact two-sided sign-test p-values.
5. Records SHA-256 of all three source files in `validation/table3_v33_verification.json` (local receipt).

The procedure reads existing files only and does not import ML libraries, fit models or download datasets.

## Decision

- If every check passes, the **reported Table 3 numbers and inferential summaries are reproducible from the preserved seed-level records**, without rerunning the benchmark.
- If a check fails, inspect the reported discrepancy before adjusting either the code or manuscript. Do not rerun all seeds reflexively.
- The source checkpoint files are not yet committed to Git. An audit receipt does not replace an archival copy of those exact source files.

The primary fixed-model comparison and tuned secondary analysis must remain distinct, as in the manuscript. Matched-tuned CGEC improvement is not evidence of universal superiority over random forest or RBF-SVM.
