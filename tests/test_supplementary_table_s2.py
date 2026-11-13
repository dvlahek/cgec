"""Check Supplementary Table S2 against the frozen real-data (digits/wine) summary."""
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper_reproducibility/results/figure_inputs.json"

EXPECTED = {
    # (printed mean E-AURC advantage, CGEC wins, ties, losses)
    "scaled_tuned_knn_confidence": (-0.000189, 7, 1, 16),
    "tuned_random_forest_confidence": (-0.002349, 1, 0, 23),
    "scaled_tuned_label_spreading_confidence": (0.000718, 7, 2, 15),
    "tuned_rbf_svm_confidence": (-0.000645, 3, 1, 20),
}


def exact_sign_p(wins, losses):
    n = wins + losses
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(wins, losses) + 1)) / 2**n)


def test_supplementary_s2_from_frozen_summary():
    summary = json.loads(SOURCE.read_text(encoding="utf-8"))
    actual = summary["predictive"]["real_primary"]
    for model, (expected_mean, wins, ties, losses) in EXPECTED.items():
        item = actual[model]["eaurc_advantage_field_over_baseline"]
        assert item["n"] == 24
        assert (item["wins"], item["ties"], item["losses"]) == (wins, ties, losses), model
        assert abs(item["mean"] - expected_mean) < 0.00000051, model
        assert abs(item["sign_test_p_two_sided"] - exact_sign_p(wins, losses)) < 1e-12, model
