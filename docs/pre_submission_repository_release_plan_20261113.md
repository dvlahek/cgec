# CGEC submission release and availability checklist — 13 November 2026

## Ground truth (checked via GitHub API and latest Overleaf PDFs)

- GitHub: https://github.com/dvlahek/cgec — **PRIVATE**, branch `main`, no GitHub release.
- **No LICENSE or CITATION.cff**, no registered software/research-artifact DOI.
- Archived original v29 S1 source/receipt; Table 3 v33 run/candidate records; v31 strict OOF label-review source; seed-0 Wine OOF; S5 exact conditional-null receipt; corrected Fig. S6; historical v36b *aggregate* runtime summary.
- Not all individual original timing components/candidates for v36b survive; full original Wine five-seed outputs, nonlinear benchmark raw experiment records and selected path stability originals remain outside the frozen public release package. The archive does not certify one-command regeneration of every manuscript result.
- Latest main PDF `main(20261113-161943).pdf` and supplementary `supplementary(20261113-161943).pdf` pass the previously identified Fig. S6, Section 6.5 and dual-metric p-value corrections, with no unresolved `??`. Availability text still has no public GitHub/DOI. Main abstract count is ~250 words after joining printer hyphenation; do not lengthen.
- **Seven** keywords appear on main page 2, but Applied Intelligence instructions require **four to six**. Drop `training-example explanation` to keep six high-value index terms.
- The Supplementary first page lists only title and author names; Applied Intelligence requests journal title, corresponding author affiliation and email in each supplementary file. Add `Applied Intelligence` and corresponding-author affiliation and `dvlahek@foi.hr`.
- The outdated `paper_reproducibility/REPRODUCIBILITY_LOCK.md` still has October paper title/figure numbering and is not authoritative for November results. Do not present it as an exact map to the current manuscript without updating.
- Full LaTeX sources, style files, bibliography and figures must be uploaded with PDF for journal submission.

## Required *before making repository public*

- [ ] Authors approve public release and code/data licensing rights; select and add an OSI-approved code LICENSE (e.g., BSD-3-Clause or MIT, only if entitled) and appropriate data reuse statements.
- [ ] Review tracked files and Git history for credentials, local personal paths, data-reuse restrictions and third-party code license compatibility. No secret scan is certified yet.
- [ ] Fix outdated title, tables/figures mapping and limitations in reproducibility docs; make a release entry point pointing to current manuscript.
- [ ] State clearly that original individual v3.6b timing JSONLs are unavailable although archived aggregate results match Table S3. Explain the other incomplete raw histories; do not claim `full reproducibility`.
- [ ] Add a `CITATION.cff` with confirmed author order/affiliations, manuscript title and version, avoiding invented ORCID/DOI.
- [ ] Run `python -m pytest` and the evidence validators on the exact release candidate; record run output and SHA-256 manifests.
- [ ] Tag a manuscript-matched commit, for example `v1.0.0-manuscript`, and create a GitHub release. Do not change visibility or create a release without author approval.
- [ ] Make the repository public after rights/security approval, then archive the tagged release in Zenodo, or manually deposit a matching frozen archive. Record the actual Zenodo DOI and cite it. **No DOI exists yet**.
- [ ] Verify the public URL and Zenodo DOI in an unauthenticated browser before updating manuscript's availability statement.

## Two truthful availability formulations

### A. Presently private (if submitting *before* an authorized public release)

```
Data availability. The benchmark datasets were obtained from the Penn Machine Learning Benchmarks (PMLB) collection, with the eight-dataset predictive panel pinned to PMLB commit 7c1f4bdc00136dc2e55c87fa6b8ba6e8af6d1a68, and from the UCI Wine Quality Red dataset. Preserved numerical outputs supporting the reported analyses are available from the corresponding author on reasonable request.

Code availability. The CGEC implementation, evaluation scripts, and verification tools are maintained in an author-controlled research repository. Access can be provided to editors and reviewers on request. A public archived release is planned. Some original intermediate execution records are not retained, as documented in the reproducibility materials.
```

**Only use this formulation if authors genuinely agree to provide access on request and plan public release.** Do not put a private GitHub hyperlink in the article as if it provided public access.

### B. Preferred after verified public GitHub + Zenodo release

```
Data availability. The benchmark data are available from the Penn Machine Learning Benchmarks (PMLB) collection (predictive-panel snapshot at commit 7c1f4bdc00136dc2e55c87fa6b8ba6e8af6d1a68) and the UCI Wine Quality Red dataset. Archived numerical outputs and verification materials supporting the reported analyses are available in the CGEC reproducibility release [ACTUAL ZENODO DOI], with coverage and limitations documented in the accompanying repository.

Code availability. The CGEC implementation, evaluation scripts, and verification tools are available at https://github.com/dvlahek/cgec and in the versioned release archived at [ACTUAL ZENODO DOI].
```

**The DOI placeholder must be replaced only after actual record publication.** Do not claim that every original raw run has been preserved.

## Latest journal instructions

- https://link.springer.com/journal/10489/submission-guidelines
- https://www.springernature.com/gp/open-science/code-policy
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/deposit/create-new-upload/

No GitHub visibility, license, release or DOI changes were made when creating this checklist.
