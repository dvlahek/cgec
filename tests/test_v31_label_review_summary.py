"""Check the v3.1 label-review summary against the 12 November manuscript.

These checks use the archived v3.1 summary, not a rerun of PMLB units.
Pooled Table 5 denominators require the separate full source JSON.
"""
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper_reproducibility/results/v31_strict_oof_scaling_audit_summary.json"

TABLE4 = {
    "CGEC": {
        "roc_auc": 0.8178,
        "pr_auc": 0.601,
        "p_at_5": 0.6918,
        "p_at_10": 0.634
    },
    "RF_confidence": {
        "roc_auc": 0.8186,
        "pr_auc": 0.6146,
        "p_at_5": 0.7032,
        "p_at_10": 0.649
    },
    "LR_confidence": {
        "roc_auc": 0.8353,
        "pr_auc": 0.622,
        "p_at_5": 0.7282,
        "p_at_10": 0.6746
    },
    "Cleanlab_OOF_LR_normalized_margin": {
        "roc_auc": 0.8292,
        "pr_auc": 0.5932,
        "p_at_5": 0.7003,
        "p_at_10": 0.6365
    },
    "kNN_disagreement": {
        "roc_auc": 0.804,
        "pr_auc": 0.5522,
        "p_at_5": 0.6191,
        "p_at_10": 0.5902
    },
    "Label_Spreading": {
        "roc_auc": 0.808,
        "pr_auc": 0.5846,
        "p_at_5": 0.6643,
        "p_at_10": 0.6183
    }
}
TABLE5 = {
    "CGEC": {
        "all_corrupted": 0.7612,
        "top5": 0.8931,
        "top10": 0.8686
    },
    "RF_confidence": {
        "all_corrupted": 0.7712,
        "top5": 0.7617,
        "top10": 0.7585
    },
    "LR_confidence": {
        "all_corrupted": 0.7544,
        "top5": 0.7428,
        "top10": 0.7455
    },
    "LR_rival_margin": {
        "all_corrupted": 0.7544,
        "top5": 0.8732,
        "top10": 0.8416
    },
    "kNN_disagreement": {
        "all_corrupted": 0.7531,
        "top5": 0.7538,
        "top10": 0.7612
    },
    "Label_Spreading": {
        "all_corrupted": 0.7421,
        "top5": 0.7308,
        "top10": 0.7354
    }
}
EXPECTED_SHA = "530f9599d945dd895cc2d155b81020e7488a58dcd7369c36c8d362fb7cbc692e"


def two_sided_sign_p(wins, losses):
    n = wins + losses
    return min(1.0, 2 * sum(comb(n, j) for j in range(min(wins, losses) + 1)) / 2**n)


def test_table4_and_table5_rounded_values():
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert result["source_sha256"] == EXPECTED_SHA
    assert result["source_bytes"] == 1469272
    a = result["table4_12_dataset_overall"]
    b = result["table5_8_multiclass_equal_dataset_means"]
    assert set(a) == set(TABLE4)
    assert set(b) == set(TABLE5)
    for method, fields in TABLE4.items():
        for metric, expected in fields.items():
            assert abs(a[method][metric] - expected) < 1e-12, (method, metric)
    for method, fields in TABLE5.items():
        for metric, expected in fields.items():
            assert abs(b[method][metric] - expected) < 1e-12, (method, metric)


def test_exact_sign_tests_and_holm():
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    for metric in ("roc_auc", "pr_auc"):
        row = result["cgec_vs_knn_dataset_sign_tests"][metric]
        assert (row["wins"], row["losses"], row["ties"]) == (10, 2, 0)
        assert abs(row["p"] - two_sided_sign_p(10, 2)) < 1e-12
    # If ROC-AUC and PR-AUC form a single family of 2 tests:
    assert abs(2 * two_sided_sign_p(10, 2) - .0771484375) < 1e-12

    tests = result["table5_primary_top_budget_sign_tests_holm"]
    assert len(tests) == 6
    for name, row in tests.items():
        if "CGEC_vs_LR_rival_margin" in name:
            assert (row["wins"], row["losses"], row["ties"]) == (6, 2, 0)
            assert abs(row["raw_p"] - .2890625) < 1e-12
            assert abs(row["holm_p"] - .578125) < 1e-12
        else:
            assert (row["wins"], row["losses"], row["ties"]) == (8, 0, 0)
            assert abs(row["raw_p"] - .0078125) < 1e-12
            assert abs(row["holm_p"] - .046875) < 1e-12
