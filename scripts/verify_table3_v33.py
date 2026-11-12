#!/usr/bin/env python3
"""Audit Table 3 from saved v3.2c/v3.3 results. No model fitting.

Run from the CGEC repository root:

  python scripts/verify_table3_v33.py --results-dir "C:\\Articles\\Clanci\\MCGC-new-repo\\paper_reproducibility\\results"

The published E-AURC table uses units of 1e-3 and four decimal places.
A match means an independently recomputed cell rounds to the printed value.
"""
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
from statistics import mean

# PDF revision 2026-11-12, Table 3, 8 rows x 6 columns, units 1e-3.
COLS = (
    "cgec",
    "cgec_tuned",
    "scaled_tuned_knn_confidence",
    "tuned_random_forest_confidence",
    "scaled_tuned_label_spreading_confidence",
    "tuned_rbf_svm_confidence",
)
ROWS = {
    "credit_approval_australia": (77.2384, 71.1973, 64.3947, 39.9889, 72.2518, 46.1088),
    "credit_approval_germany": (97.2145, 93.8344, 103.1391, 88.5545, 104.8276, 83.4604),
    "dermatology": (2.1450, 1.9079, 3.9751, 1.1500, 4.3538, 1.4153),
    "haberman": (129.0093, 134.2210, 150.7042, 119.3139, 145.0622, 144.8318),
    "heart_disease_cleveland": (45.4653, 45.2434, 50.1797, 37.9299, 48.3953, 60.8670),
    "ionosphere": (71.9241, 42.9719, 56.4080, 9.7335, 53.0920, 13.7507),
    "penguins": (0.0595, 0.0338, 0.0848, 0.7921, 0.0763, 0.0762),
    "segmentation": (6.6294, 3.8878, 3.7949, 0.5759, 4.8831, 7.1651),
}
SEEDS = set(range(12))
TOL_PRINTED = 0.00005001  # 4 decimal places in table's 1e-3 units


def checksame(actual, expected, label, tol=1e-12):
    assert abs(float(actual) - float(expected)) <= tol, (
        f"{label}: calculated={actual} expected={expected}"
    )


def read_checkpoint(path):
    records = {}
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        key = (row["dataset"], int(row["seed"]))
        # Appended files may contain repeated checkpoints after resume; require agreement.
        if key in records:
            assert records[key]["run"] == row["run"], f"conflicting checkpoint at {path}:{no}, {key}"
        records[key] = row
    return records


def sign_p(wins, losses):
    n = wins + losses
    if not n:
        return None
    k = min(wins, losses)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", required=True, type=Path)
    ap.add_argument("--receipt", type=Path, default=Path("validation/table3_v33_verification.json"))
    args = ap.parse_args()
    paths = {
        "summary": args.results_dir / "v33_tuned_cgec_summary.json",
        "fixed": args.results_dir / "v32c_real_data_confirmation_runs.jsonl",
        "tuned": args.results_dir / "v33_tuned_cgec_runs.jsonl",
    }
    for label, path in paths.items():
        assert path.is_file(), f"Missing {label}: {path}"
    hashes = {k: hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}
    doc = json.loads(paths["summary"].read_text(encoding="utf-8"))
    protocol = doc["protocol"]
    assert protocol["version"] == "v3.3"
    assert protocol["primary_result_remains_fixed_cgec"] is True
    assert protocol["status"] == "complete eight-dataset matched-tuning audit"
    assert set(protocol["dataset_panel"]) == set(ROWS)
    assert set(protocol["seeds"]) == SEEDS
    assert set(doc["datasets"]) == set(ROWS)

    fixed, tuned = read_checkpoint(paths["fixed"]), read_checkpoint(paths["tuned"])
    needed = {(dataset, seed) for dataset in ROWS for seed in SEEDS}
    assert needed.issubset(fixed), f"Missing fixed units: {sorted(needed - fixed)[:4]}"
    assert needed.issubset(tuned), f"Missing tuned units: {sorted(needed - tuned)[:4]}"

    computed = {}
    for dataset, printed in ROWS.items():
        bundle = doc["datasets"][dataset]
        runs = bundle["runs"]
        assert len(runs) == 12, (dataset, "expected 12 runs")
        run_ids = {int(run["seed"]) for run in runs}
        assert run_ids == SEEDS, (dataset, "missing/duplicate seed")

        for run in runs:
            seed = int(run["seed"])
            key = dataset, seed
            old, new = fixed[key]["run"], tuned[key]["run"]
            assert run["n_train"] == old["n_train"] == new["n_train"]
            assert run["n_test"] == old["n_test"] == new["n_test"]
            for method in COLS:
                from_checkpoint = (
                    new["tuned_cgec"] if method == "cgec_tuned"
                    else old["models"][method]
                )
                checksame(
                    run["models"][method]["eaurc"],
                    from_checkpoint["eaurc"],
                    f"{dataset}/{seed}/{method} checkpoint",
                )

        calc = {}
        for method, reference in zip(COLS, printed):
            eaurc = mean(float(run["models"][method]["eaurc"]) for run in runs)
            checksame(
                eaurc,
                bundle["mean_metrics_across_seeds"][method]["eaurc"],
                f"{dataset}/{method} mean",
            )
            table_units = 1000 * eaurc
            assert abs(table_units - reference) <= TOL_PRINTED, (
                f"TABLE 3 MISMATCH {dataset}/{method}: "
                f"recomputed {table_units:.7f} vs PDF {reference:.4f}"
            )
            calc[method] = eaurc
        computed[dataset] = calc
        print(f"PASS {dataset:27s} 6/6 cells, 12 seeds")

    expected_primary = {
        "tuned_vs_fixed": (7, 0, 1),
        "scaled_tuned_knn_confidence": (6, 0, 2),
        "tuned_random_forest_confidence": (1, 0, 7),
        "scaled_tuned_label_spreading_confidence": (8, 0, 0),
        "tuned_rbf_svm_confidence": (4, 0, 4),
    }
    primary = doc["panel_summary"]["dataset_level_primary"]
    diffs = [computed[d]["cgec"] - computed[d]["cgec_tuned"] for d in ROWS]
    delta = mean(diffs)
    assert abs(delta - 0.004549) < 0.0000006, delta

    for label, (wins, ties, losses) in expected_primary.items():
        if label == "tuned_vs_fixed":
            ds = diffs
            archived = primary["tuned_vs_fixed"]
        else:
            ds = [computed[d][label] - computed[d]["cgec_tuned"] for d in ROWS]
            archived = primary["tuned_vs_baselines"][label]
        actual_wins = sum(x > 1e-12 for x in ds)
        actual_ties = sum(abs(x) <= 1e-12 for x in ds)
        actual_losses = sum(x < -1e-12 for x in ds)
        assert (actual_wins, actual_ties, actual_losses) == (wins, ties, losses), label
        assert (archived["wins"], archived["ties"], archived["losses"]) == (
            wins, ties, losses
        ), label
        checksame(mean(ds), archived["mean"], f"panel/{label} mean")
        checksame(
            sign_p(wins, losses),
            archived["sign_test_p_two_sided"],
            f"panel/{label} exact p",
        )
        print(f"PASS {label:37s} W/T/L={wins}/{ties}/{losses}, p={sign_p(wins,losses):.8f}")
    assert abs(mean([computed[d]["scaled_tuned_label_spreading_confidence"] - computed[d]["cgec_tuned"] for d in ROWS]) - .004956) < .0000006
    print(f"PASS ALL: 48 Table 3 values, 96 paired seed units, five primary comparisons")

    receipt = {
        "outcome": "PASS",
        "manuscript": "Table 3, PDF dated 2026-11-12",
        "method": "read-only verification, no training",
        "table_values_checked": 48,
        "paired_dataset_seed_units": 96,
        "files_sha256": hashes,
        "tuned_minus_fixed_eaurc_improvement": delta,
        "primary_comparisons": {
            label: {"wins": w, "ties": t, "losses": l, "two_sided_p": sign_p(w, l)}
            for label, (w,t,l) in expected_primary.items()
        },
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(f"RECEIPT={args.receipt.resolve()}")


if __name__ == "__main__":
    main()
