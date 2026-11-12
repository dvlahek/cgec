# Label-review audit — manuscript revision 12 November 2026

## Finding

The current manuscript's Table 4 and Table 5 numerical **mean** values are backed by the **strict fold-local OOF preprocessing audit v3.1**, not by the older `final_manuscript_results.json` dated 28 October 2026.

Authoritative compact source: [`v31_strict_oof_scaling_audit_summary.json`](../paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json).

Source procedure: [`benchmark_reviewer_oof_scaling_v31.py`](../paper_reproducibility/benchmarks/benchmark_reviewer_oof_scaling_v31.py).

The v3.1 source uses the outer 70/30 split, corrupts labels only in its outer training partition and fits all preprocessing within each OOF training fold. The CGEC estimator already performed fold-local standardization. The revised baseline handling removes cross-fold preprocessing leakage for LR, kNN, Label Spreading and LR-derived Cleanlab/rival-margin controls.

## Cross-check against the submitted PDF

PDF: `main(20261112-085144).pdf`, Table 4 on page 14 and Table 5 on page 15.

| Item | Independently checked against v3.1 compact source | Result |
| --- | --- | --- |
| Table 4, 6 methods × 4 reported metrics | 24 of 24 | Exact match at printed precision |
| Table 5, 6 methods × 3 mean recovery metrics | 18 of 18 | Exact match at printed precision |
| CGEC–kNN dataset-level ROC-AUC and PR-AUC | Both 10 wins, 2 losses | Exact two-sided p = 0.03857421875 each |
| Six primary Table 5 top-budget tests | Four 8/0, two 6/2 | Raw and Holm values match the v3.1 summary |
| Table 5 pooled corrupted-case denominators | 12 integers in manuscript; **not present in v3.1 compact source** | Requires full original JSON |

At the printed precision the six Table 5 recovery vectors are:

| Method | All corrupted | Top 5% | Top 10% |
| --- | ---: | ---: | ---: |
| CGEC | 0.7612 | 0.8931 | 0.8686 |
| RF confidence | 0.7712 | 0.7617 | 0.7585 |
| LR confidence | 0.7544 | 0.7428 | 0.7455 |
| LR rival margin | 0.7544 | 0.8732 | 0.8416 |
| kNN disagreement | 0.7531 | 0.7538 | 0.7612 |
| Label Spreading | 0.7421 | 0.7308 | 0.7354 |

**Important statistical qualification:** The 10/12 sign-test p-value `0.0386` is *unadjusted*. If the two outcomes ROC-AUC and PR-AUC are treated as one Holm family, the adjusted p-value for each is `0.0771484375`. The manuscript and Supplementary should clearly define the comparison family and not imply adjusted significance for these two endpoints.

The six specified Table 5 top-budget comparisons use Holm across six tests: four adjusted p-values `0.046875` and two adjusted p-values `0.578125`, consistent with the manuscript.

## Exact missing source artifact

The full archived audit is named:

`paper_reproducibility/results/v31_strict_oof_scaling_audit.json`

- Expected original length: **1,469,272 bytes**
- Expected SHA-256: **`530f9599d945dd895cc2d155b81020e7488a58dcd7369c36c8d362fb7cbc692e`**

Its name, length and checksum are recorded in the v3.1 summary. **The full file is not present in this repository.** Without it, the 12 `n_corr` denominators in Table 5 and independent recomputation of all original unit-level aggregates cannot be certified.

Locate the original file on the experiment machine. From PowerShell:

```powershell
Get-ChildItem "C:\Articles\Clanci\MCGC-new-repo" -Recurse -File -Filter "v31_strict_oof_scaling_audit.json" |
  Select-Object FullName,Length

# Check the discovered file, substituting its true full path:
Get-FileHash "FULL_PATH_TO\v31_strict_oof_scaling_audit.json" -Algorithm SHA256

# No training: check exact full source and all 12 printed Table 5 denominators
.\.venv\Scripts\python.exe scripts\verify_v31_full_artifact.py --raw "FULL_PATH_TO\v31_strict_oof_scaling_audit.json"
```

The verifier checks SHA-256, all 12 pooled denominators, and recomputes each equal-dataset mean from the unit-level counts. It does **not** train any model.

## Release decision

- **Matched:** Table 4 reported means; Table 5 reported means; exact sign-test and six-test Holm arithmetic.
- **Pending raw evidence:** all 12 Table 5 pooled denominators and the underlying dataset-condition-seed records.
- **No full rerun needed if the original JSON can be located and passes checksum validation.**

Keep October `final_manuscript_results.json` as historical evidence; it is not the authoritative Table 4/5 source for the November manuscript.
