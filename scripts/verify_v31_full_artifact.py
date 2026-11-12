#!/usr/bin/env python3
"""Verify original v3.1 OOF audit and the 12 Table 5 pooled denominators.

Usage:
    python scripts/verify_v31_full_artifact.py --raw path/to/v31_strict_oof_scaling_audit.json

No model fitting is performed. The script verifies source SHA-256 first.
"""
import argparse
import hashlib
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json"
EXPECTED_COUNTS = {
    "CGEC": {
        "top5": 6173,
        "top10": 11549
    },
    "RF_confidence": {
        "top5": 6444,
        "top10": 12147
    },
    "LR_confidence": {
        "top5": 6192,
        "top10": 11796
    },
    "LR_rival_margin": {
        "top5": 5866,
        "top10": 10938
    },
    "kNN_disagreement": {
        "top5": 5681,
        "top10": 10961
    },
    "Label_Spreading": {
        "top5": 6059,
        "top10": 11559
    }
}
METHOD_NAMES = {
    "CGEC": "cgec_oof",
    "RF_confidence": "rf_confidence_oof",
    "LR_confidence": "lr_confidence_oof",
    "LR_rival_margin": "lr_rival_margin_oof",
    "kNN_disagreement": "knn_disagreement_oof",
    "Label_Spreading": "label_spreading_oof",
}
TABLE5_DATASETS = (
    "ecoli", "mfeat_fourier", "mfeat_karhunen", "mfeat_zernike",
    "schizo", "vehicle", "wine_quality_red", "yeast",
)
KEYS = {"top5": "top_5pct_corrupt", "top10": "top_10pct_corrupt"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True,
                        help="Path to original 1,469,272-byte v3.1 audit JSON")
    args = parser.parse_args()
    source = SUMMARY.read_bytes()
    lock = json.loads(source)
    raw_bytes = args.raw.read_bytes()
    source_hash = hashlib.sha256(raw_bytes).hexdigest()
    assert len(raw_bytes) == lock["source_bytes"], "Unexpected source file size"
    assert source_hash == lock["source_sha256"], "SHA-256 mismatch against archived v3.1 summary"

    raw = json.loads(raw_bytes)
    selected = [
        row for row in raw["records"]
        if row.get("status") == "ok" and row["dataset"] in TABLE5_DATASETS
    ]
    assert len(selected) == 160, f"Expected 8 datasets x 4 conditions x 5 seeds, got {len(selected)}"
    assert set(row["dataset"] for row in selected) == set(TABLE5_DATASETS)

    print(f"SOURCE PASS: {len(raw_bytes)} bytes, SHA-256 {source_hash}")
    for name, src in METHOD_NAMES.items():
        for budget, key in KEYS.items():
            count = sum(int(row["rival_recovery"][src][key]["total"]) for row in selected)
            expected = EXPECTED_COUNTS[name][budget]
            assert count == expected, (name, budget, count, expected)
        print(f"{name:26s} n_corr,5={EXPECTED_COUNTS[name]['top5']:5d} "
              f"n_corr,10={EXPECTED_COUNTS[name]['top10']:5d} PASS")

    for method, src in METHOD_NAMES.items():
        for target, key in (
            ("all_corrupted", "all_corrupt"),
            ("top5", "top_5pct_corrupt"),
            ("top10", "top_10pct_corrupt"),
        ):
            per_dataset = []
            for dataset in TABLE5_DATASETS:
                rs = [r for r in selected if r["dataset"] == dataset]
                assert len(rs) == 20
                n = sum(r["rival_recovery"][src][key]["total"] for r in rs)
                correct = sum(r["rival_recovery"][src][key]["correct"] for r in rs)
                assert n > 0
                per_dataset.append(correct / n)
            calculated = sum(per_dataset) / len(per_dataset)
            archived = lock["table5_8_multiclass_equal_dataset_means"][method][target]
            assert abs(calculated - archived) <= 0.00005001, (method, target, calculated, archived)
    print("PASS: Table 5 denominators and equal-dataset mean recovery rates")


if __name__ == "__main__":
    main()
