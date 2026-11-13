#!/usr/bin/env python3
"""Verify Supplementary Table S1 against the original v2.9 sensitivity JSON.

This is a read-only source-data audit by default: it never imports or fits ML
models. Optional --stage copies the verified source into the new CGEC repo
byte-for-byte and writes a verification receipt for the next Git commit.

PowerShell:
  .\\.venv\\Scripts\\python.exe scripts\\verify_supplement_s1_v29.py --raw "C:\\Articles\\Clanci\\MCGC-new-repo\\results\\v29_field_core_parameter_sensitivity.json"
  .\\.venv\\Scripts\\python.exe scripts\\verify_supplement_s1_v29.py --raw "C:\\Articles\\Clanci\\MCGC-new-repo\\results\\v29_field_core_parameter_sensitivity.json" --stage
"""
import argparse
import hashlib
import json
import shutil
from math import comb
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
NAME = "v29_field_core_parameter_sensitivity.json"
EXPECTED_BYTES = 231765
NOMINAL = "nominal_K12_a085_nD40"
# Values printed to four decimals in Table S1 of the 2026-11-12 Supplementary PDF.
EXPECTED = {
    "nominal_K12_a085_nD40": (0.8077, 0.0761),
    "K8": (0.8091, 0.0759),
    "K16": (0.8111, 0.0797),
    "alpha075": (0.8110, 0.0755),
    "alpha095": (0.8065, 0.0837),
    "nD20": (0.8077, 0.0761),
    "nD80": (0.8077, 0.0761),
}
TOL_PRINTED = 0.00005001
# Reported rounded two-sided exact sign-test p-values.
REPORTED_P = {
    ("K8", "accuracy"): 0.860,
    ("K8", "eaurc"): 0.618,
    ("alpha075", "accuracy"): 1.000,
    ("alpha075", "eaurc"): 0.065,
    ("K16", "eaurc"): 6.96e-5,
    ("alpha095", "eaurc"): 1.29e-5,
}


def sign_test(wins, losses):
    n = wins + losses
    if n == 0:
        return None
    k = min(wins, losses)
    return min(1.0, 2.0 * sum(comb(n, i) for i in range(k + 1)) / (2**n))


def compare(actual, expected, label, tol=1e-12):
    assert abs(float(actual) - float(expected)) <= tol, (
        f"{label}: calculated={actual!r}, archived={expected!r}"
    )


def audit(path):
    raw = path.read_bytes()
    assert len(raw) == EXPECTED_BYTES, (
        f"Unexpected v29 JSON file size: got {len(raw)}, expected {EXPECTED_BYTES}"
    )
    digest = hashlib.sha256(raw).hexdigest()
    result = json.loads(raw)
    protocol = result["protocol"]
    assert protocol["version"] == "v2.9"
    assert protocol["nominal_configuration"] == NOMINAL
    assert protocol["selection_from_sensitivity_results"] is False
    assert set(protocol["configurations"]) == set(EXPECTED)
    dataset_names = protocol["primary_datasets"]
    seeds = {int(x) for x in protocol["seeds"]}
    assert len(dataset_names) == 3 and len(set(dataset_names)) == 3
    assert seeds == set(range(12))
    assert set(result["datasets"]) == set(dataset_names)
    assert set(result["pooled_primary"]) == set(EXPECTED)

    units = []
    for ds in dataset_names:
        bundle = result["datasets"][ds]
        runs = bundle["runs"]
        assert len(runs) == 12
        assert {int(x["seed"]) for x in runs} == seeds
        for run in runs:
            current = run["configurations"]
            assert set(current) == set(EXPECTED)
            baseline = current[NOMINAL]
            for configuration in EXPECTED:
                item = current[configuration]
                paired = item["paired_vs_nominal"]
                compare(
                    item["accuracy"] - baseline["accuracy"],
                    paired["accuracy_delta_config_minus_nominal"],
                    f"{ds}/{run['seed']}/{configuration}/accuracy_delta",
                )
                compare(
                    item["eaurc"] - baseline["eaurc"],
                    paired["eaurc_delta_config_minus_nominal"],
                    f"{ds}/{run['seed']}/{configuration}/eaurc_delta",
                )
        units.extend(runs)

    assert len(units) == 36
    checks = {}
    for cfg, (expected_accuracy, expected_eaurc) in EXPECTED.items():
        acc = mean(float(u["configurations"][cfg]["accuracy"]) for u in units)
        eaurc = mean(float(u["configurations"][cfg]["eaurc"]) for u in units)
        assert abs(acc - expected_accuracy) <= TOL_PRINTED, (
            f"Table S1 {cfg} accuracy: calculated={acc:.8f}, PDF={expected_accuracy:.4f}"
        )
        assert abs(eaurc - expected_eaurc) <= TOL_PRINTED, (
            f"Table S1 {cfg} E-AURC: calculated={eaurc:.8f}, PDF={expected_eaurc:.4f}"
        )
        compare(acc, result["pooled_primary"][cfg]["mean_accuracy"], f"{cfg}/mean_accuracy")
        compare(eaurc, result["pooled_primary"][cfg]["mean_eaurc"], f"{cfg}/mean_eaurc")
        checks[cfg] = {"accuracy": acc, "eaurc": eaurc}
        print(f"PASS {cfg:25s} Acc={acc:.4f} E-AURC={eaurc:.4f}")

    p_checks = {}
    for (cfg, metric), reported in REPORTED_P.items():
        key = f"{metric}_delta_config_minus_nominal"
        diffs = [
            float(u["configurations"][cfg]["paired_vs_nominal"][key])
            for u in units
        ]
        wins = sum(v > 1e-12 for v in diffs)
        losses = sum(v < -1e-12 for v in diffs)
        ties = len(diffs) - wins - losses
        pvalue = sign_test(wins, losses)
        assert pvalue is not None
        saved = result["pooled_primary"][cfg]["paired_vs_nominal"][key]
        assert (saved["wins"], saved["ties"], saved["losses"]) == (wins, ties, losses)
        compare(pvalue, saved["sign_test_p_two_sided"], f"{cfg}/{metric}/exact_p")
        tol = 0.000051 if reported < 0.001 else 0.00051
        assert abs(pvalue - reported) <= tol, (
            f"{cfg}/{metric} p mismatch: {pvalue}, PDF {reported}"
        )
        if (cfg, metric) == ("K16", "eaurc"):
            assert wins == 30, f"Expected 30/36 units worsen with K=16, got {wins}"
        if (cfg, metric) == ("alpha095", "eaurc"):
            assert wins == 31, f"Expected 31/36 units worsen with alpha=0.95, got {wins}"
        p_checks[f"{cfg}_{metric}"] = {
            "wins": wins, "ties": ties, "losses": losses, "p_two_sided": pvalue,
        }
        print(f"PASS {cfg:15s} {metric:8s} W/T/L={wins}/{ties}/{losses} p={pvalue:.9g}")

    change20 = sum(
        u["configurations"]["nD20"]["paired_vs_nominal"]["prediction_disagreement_rate"] > 0
        for u in units
    )
    change80 = sum(
        u["configurations"]["nD80"]["paired_vs_nominal"]["prediction_disagreement_rate"] > 0
        for u in units
    )
    assert change20 == 2, f"nD20: expected changed predictions in two units, got {change20}"
    assert change80 == 0, f"nD80: expected zero changed prediction sets, got {change80}"

    print("PASS: Supplementary Table S1, 14 printed means, 36 source units, 6 reported sign-test checks")
    print(f"SHA256={digest}")
    return {
        "artifact": "CGEC Supplementary Table S1 original v2.9 sensitivity audit",
        "status": "PASS",
        "source_file": NAME,
        "source_sha256": digest,
        "source_bytes": len(raw),
        "source_units": len(units),
        "printed_means_checked": 14,
        "sign_test_checks": p_checks,
        "calculated_means": checks,
        "changed_prediction_units": {"nD20": change20, "nD80": change80},
        "method": "Read-only JSON arithmetic; no model training",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--stage", action="store_true",
                        help="After passing, copy the original JSON and its receipt into Git-tracked folders")
    parser.add_argument("--receipt", type=Path, default=ROOT / "validation/supplement_s1_v29_verification.json")
    args = parser.parse_args()
    assert args.raw.is_file(), f"Missing source JSON: {args.raw}"
    receipt = audit(args.raw)

    if args.stage:
        target = ROOT / "paper_reproducibility/results" / NAME
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert hashlib.sha256(target.read_bytes()).hexdigest() == receipt["source_sha256"], (
                f"Different target file exists; refusing to overwrite: {target}"
            )
        else:
            shutil.copyfile(args.raw, target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == receipt["source_sha256"]
        receipt_path = ROOT / "reproductions/supplement_s1_v29/verification_receipt.json"
        print(f"STAGED SOURCE={target.relative_to(ROOT).as_posix()}")
    else:
        receipt_path = args.receipt
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    serial = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if receipt_path.exists():
        assert receipt_path.read_text(encoding="utf-8") == serial, (
            f"Different receipt exists; refusing to overwrite: {receipt_path}"
        )
    else:
        receipt_path.write_text(serial, encoding="utf-8")
    print(f"RECEIPT={receipt_path}")
    if args.stage:
        print("Use git status, review exact two new files, then commit and push.")


if __name__ == "__main__":
    main()
