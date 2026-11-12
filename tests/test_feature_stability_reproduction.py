"""Validate the uploaded feature-stability reproduction against the numerical lock."""
import json
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]

def test_feature_stability_reproduction():
    result = json.loads((ROOT / "reproductions/feature_stability_v30/feature_stability_v30.json").read_text())
    lock = json.loads((ROOT / "paper_reproducibility/results/final_manuscript_results.json").read_text())["feature_intervention_stability"]
    assert result["protocol"]["dataset"] == "breast_cancer"
    assert result["protocol"]["seeds"] == [0,1,2,3,4]
    assert [x["seed"] for x in result["runs"]] == [0,1,2,3,4]
    assert all(x["n_test"] == 171 for x in result["runs"])
    pairs = result["rank_stability_mean_reference"]["pairs"]
    assert len(pairs) == len({(x["seed_a"],x["seed_b"]) for x in pairs}) == 10
    checks = {
        "mean_pairwise_spearman": mean(x["spearman"] for x in pairs),
        "median_pairwise_spearman": median(x["spearman"] for x in pairs),
        "mean_top5_jaccard": mean(x["top5_jaccard"] for x in pairs),
        "aggregate_mean_vs_median_spearman": result["reference_sensitivity"]["aggregate"]["spearman"],
        "aggregate_top5_jaccard": result["reference_sensitivity"]["aggregate"]["top5_jaccard"],
        "aggregate_top10_jaccard": result["reference_sensitivity"]["aggregate"]["top10_jaccard"],
    }
    for key,value in checks.items():
        assert abs(value-lock[key]) < 1e-6, key
    for key,part in (("spearman","per_seed_spearman"),("top5_jaccard","per_seed_top5_jaccard")):
        assert abs(mean(x["mean_vs_median"][key] for x in result["runs"])-result["reference_sensitivity"][part]["mean"]) < 1e-12
