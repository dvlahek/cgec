#!/usr/bin/env python3
"""Check whether Supplementary Fig. S6 reflects the final strict-OOF v3.1 audit.

Read-only with respect to source data. No model fitting, dataset loading or
random-number generation is performed.

Example (Windows PowerShell, from repository root):
  .\\.venv\\Scripts\\python.exe scripts\\verify_supplement_s6_v31.py --raw "C:\\Articles\\Clanci\\MCGC-new-repo\\paper_reproducibility\\results\\v31_strict_oof_scaling_audit.json"

This creates only a new summary under validation/, which can be passed to
paper_reproducibility/figures/fig3_oof_vs_knn.py --summary-json.
"""
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
AUDIT_SUMMARY = ROOT / "paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json"
OLDER_FIGURE = ROOT / "paper_reproducibility/results/fig3_oof_vs_knn_summary.json"
METRICS = ("roc_auc", "pr_auc")
METHODS = ("cgec_oof", "knn_disagreement_oof")
N_SEEDS = 5
N_CONDITIONS = 4


def exact_sign_p(wins, losses):
    n = wins + losses
    if not n:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(wins, losses) + 1)) / 2**n)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--output", default=ROOT / "validation/fig_s6_v31_summary.json", type=Path)
    args = ap.parse_args()

    source = AUDIT_SUMMARY.read_text(encoding="utf-8")
    lock = json.loads(source)
    raw_bytes = args.raw.read_bytes()
    assert len(raw_bytes) == lock["source_bytes"], "Unexpected v3.1 source file length"
    digest = hashlib.sha256(raw_bytes).hexdigest()
    assert digest == lock["source_sha256"], "v3.1 source SHA-256 mismatch"
    full = json.loads(raw_bytes)

    expected_names = list(lock["protocol"]["datasets"])
    all_ok = [r for r in full["records"] if r.get("status") == "ok"]
    assert len(expected_names) == 12
    assert len(all_ok) == 12 * N_CONDITIONS * N_SEEDS, (
        f"Expected 240 complete v3.1 units, got {len(all_ok)}"
    )
    assert set(row["dataset"] for row in all_ok) == set(expected_names)
    assert set(full["analysis"]["dataset_level"][i]["dataset"] for i in range(12)) == set(expected_names)

    rows = []
    for name in expected_names:
        units = [r for r in all_ok if r["dataset"] == name]
        assert len(units) == 20, f"{name}: expected 20 condition-seed units"
        row = {"dataset": name}
        for metric in METRICS:
            cgec = mean(float(r["audit"][METHODS[0]][metric]) for r in units)
            knn = mean(float(r["audit"][METHODS[1]][metric]) for r in units)
            row[metric] = cgec - knn
            dataset_lock = next(x for x in full["analysis"]["dataset_level"] if x["dataset"] == name)
            assert abs(cgec - dataset_lock["methods"][METHODS[0]][metric]) < 1e-12
            assert abs(knn - dataset_lock["methods"][METHODS[1]][metric]) < 1e-12
        rows.append(row)

    for metric in METRICS:
        differences = [r[metric] for r in rows]
        wins = sum(v > 1e-12 for v in differences)
        losses = sum(v < -1e-12 for v in differences)
        ties = 12 - wins - losses
        locked = lock["cgec_vs_knn_dataset_sign_tests"][metric]
        assert (wins, losses, ties) == (locked["wins"], locked["losses"], locked["ties"])
        assert abs(mean(differences) - locked["mean_delta"]) < 1e-12
        assert abs(exact_sign_p(wins, losses) - locked["p"]) < 1e-12
        print(f"v3.1 {metric}: W/T/L={wins}/{ties}/{losses}, p={locked['p']:.9f}, source PASS")

    old = json.loads(OLDER_FIGURE.read_text(encoding="utf-8"))
    by_old = {r["dataset"]: r for r in old["datasets"]}
    assert set(by_old) == set(expected_names)

    changes = []
    for row in rows:
        prior = by_old[row["dataset"]]
        for metric in METRICS:
            former = float(prior[metric])
            current = float(row[metric])
            changed_label = f"{former:+.3f}" != f"{current:+.3f}"
            changes.append({
                "dataset": row["dataset"],
                "metric": metric,
                "older": former,
                "v31": current,
                "delta_v31_minus_older": current - former,
                "printed_3dp_changed": changed_label,
            })
            if changed_label:
                print(f"UPDATED S6 VALUE: {row['dataset']}/{metric}: {former:+.3f} -> {current:+.3f}")

    n_changed = sum(x["printed_3dp_changed"] for x in changes)
    max_abs_change = max(abs(x["delta_v31_minus_older"]) for x in changes)
    result = {
        "description": "Strict fold-local OOF v3.1 dataset-level CGEC minus OOF kNN deltas for Supplementary Fig. S6",
        "source_sha256": digest,
        "sign_test_p": lock["cgec_vs_knn_dataset_sign_tests"]["roc_auc"]["p"],
        "datasets": rows,
        "comparison_to_older_figure": {
            "n_comparisons": len(changes),
            "changed_3dp_labels": n_changed,
            "max_absolute_delta": max_abs_change,
            "details": changes,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"PASS: 12 datasets, 240 original units, 24 figure data points checked")
    print(f"OLDER FIGURE COMPARISON: {n_changed}/24 labels changed at 3 decimal places; max |difference|={max_abs_change:.8g}")
    print("If any displayed values changed, regenerate Fig. S6 from the v3.1 summary.")
    print(f"OUTPUT={args.output.resolve()}")


if __name__ == "__main__":
    main()
