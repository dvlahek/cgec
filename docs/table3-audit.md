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

The file sizes above came from the author's local file listing. A subsequent locally executed verifier checked the full three input files, recorded their SHA-256 checksums and reported PASS. The original source bytes remain on the workstation, not in this GitHub repository.

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

## Verified local result — 13 November 2026

The author supplied [the read-only audit receipt](../reproductions/table3_v33/verification_receipt.json), which reports `PASS` for **48 reported E-AURC cells**, **96 dataset×seed experimental units**, and all five primary dataset-level comparisons. Exact two-sided sign-test probabilities computed independently from the receipt's 8-dataset win/loss counts match its values.

| Compared models | W/T/L (tuned CGEC favorable) | Exact two-sided p |
| --- | ---: | ---: |
| tuned vs fixed CGEC | 7/0/1 | 0.0703125 |
| tuned vs kNN | 6/0/2 | 0.2890625 |
| tuned vs random forest | 1/0/7 | 0.0703125 |
| tuned vs Label Spreading | 8/0/0 | 0.0078125 |
| tuned vs RBF-SVM | 4/0/4 | 1.0 |

The equal-dataset mean fixed-minus-tuned E-AURC improvement was `0.004548503410246824`. These are **unadjusted** sign-test values; the 7/1 tuned-versus-fixed comparison does not cross the two-sided 0.05 threshold.

Original source checksums recorded by the submitted verification:

| Input | SHA-256 |
| --- | --- |
| v33 summary | `a99547042f7845a90811894b801f32d16a671c98610aa1a1bcdc00e8e650f96b` |
| v32c fixed records | `7f26f3d4028a119a8b83d71faad05fbc031ae37d9002695be56c6a5fe0a67a76` |
| v33 tuned records | `cc367789512d3b1bc2c3c77a8e5fee35309de8bfd0afdedd583893f27c08a91f` |

The receipt records the outcome of a local verification and was inspected for internal consistency. **The raw inputs have not been separately read in this ChatGPT session or deposited in Git.** No fresh seed computation was undertaken here.

## Decision

- **Local verification passed.** The reported Table 3 numbers and inferential summaries were reconstructed from the preserved seed-level records without rerunning the benchmark.
- **Archival follow-up:** the original source checkpoint files are not yet committed to Git. The receipt and checksums do not replace the underlying data, which should be deposited unchanged when preparing a complete release.

The primary fixed-model comparison and tuned secondary analysis must remain distinct, as in the manuscript. Matched-tuned CGEC improvement is not evidence of universal superiority over random forest or RBF-SVM.
