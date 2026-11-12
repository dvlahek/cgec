# Reproduced feature-intervention stability

The uploaded local Windows run completed all five seeds (0–4) on the breast-cancer dataset, 171 test queries per seed and all 10 distinct seed-pair comparisons. The experimental model is field-only CGEC with `K=12`, `alpha=0.85`, `nD=40`, `use_walkers=False` and stratified 70/30 outer splits (`random_state=7000+seed`).

The included JSON was parsed and reserialized with UTF-8 line endings. The log was converted from Windows UTF-16 to UTF-8, omitting the local absolute output path.

**Original uploaded files**

- JSON SHA-256 `22fa4354bbcafe26f25fabc91d291e14d26cb77716a73c95063b34786a88c610`
- UTF-16 log SHA-256 `f4c53eeb851aa7e82bb3e6f036f17dc547f0b78afbff49bfbf39ccc41a610ed6`

The archived `paper_reproducibility/results/final_manuscript_results.json` records the same statistics to the reported precision. All ten pairwise statistics were independently averaged and the per-seed reference-sensitivity means checked.

| Metric | New result | Existing lock |
| --- | ---: | ---: |
| mean pairwise spearman | 0.724493882 | 0.724493882 |
| median pairwise spearman | 0.726807564 | 0.726807564 |
| mean top5 jaccard | 0.571428571 | 0.571428571 |
| aggregate mean vs median spearman | 0.948387097 | 0.948387097 |
| aggregate top5 jaccard | 0.666666667 | 0.666666700 |
| aggregate top10 jaccard | 0.818181818 | 0.818181800 |

**Scope:** Verified regeneration of the feature-intervention stability summary. This is not a fresh execution of the other predictive or label-review benchmark suites. The original log does not include an executable Git SHA or frozen package versions; those should be captured for any later run.
