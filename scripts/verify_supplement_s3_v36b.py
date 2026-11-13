#!/usr/bin/env python3
"""Read-only check of the historical v3.6b aggregate Supplementary Table S3.

Verifies each printed median using the recovered prior-chat JSON summary.
The source has 40 units aggregated, but original candidate/component checkpoint
records are not in this archive. This is not a raw-timing rerun.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper_reproducibility/results/v36b_runtime_summary_recovered.json"
EXPECTED = {
    "fixed_cgec": (None, 35.48, None),
    "tuned_cgec": (3.143, 34.45, 3),
    "baseline::scaled_tuned_knn_confidence": (0.0439, 1.14, 4),
    "baseline::tuned_random_forest_confidence": (7.821, 141.75, 3),
    "baseline::scaled_tuned_label_spreading_confidence": (0.1147, 2.39, 4),
    "baseline::tuned_rbf_svm_confidence": (0.0846, 3.19, 4),
}


def audit(path=SOURCE):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    protocol = doc["protocol"]
    assert protocol["version"] == "v3.6b"
    assert protocol["n_dataset_seed_units"] == 40
    assert protocol["seeds"] == [0, 2, 5, 8, 11]
    assert len(set(protocol["datasets"])) == len(protocol["datasets"]) == 8
    assert protocol["single_thread_policy"] is True
    assert protocol["rf_n_jobs"] == 1
    assert protocol["timing_repeats_final_model"] == 3
    assert protocol["cgec_tuning_grid"]["n_candidates"] == 36
    assert doc["environment"]["timer"] == "time.perf_counter wall-clock seconds"
    assert set(doc["dataset_metadata"]) == set(protocol["datasets"])

    runtime = doc["runtime"]["panel_all_dataset_seed_units"]
    end = runtime["end_to_end_or_fixed_final_model"]
    final = runtime["selected_final_model_fit_plus_prediction"]
    assert set(end) == set(final) == set(EXPECTED)

    for method, (display_e2e, display_final_ms, decimal_places) in EXPECTED.items():
        a, b = end[method], final[method]
        assert a["n"] == b["n"] == 40
        if display_e2e is not None:
            assert round(a["median"], decimal_places) == display_e2e, (
                method, a["median"], display_e2e
            )
        assert round(b["median"] * 1000, 2) == display_final_ms, (
            method, b["median"] * 1000, display_final_ms
        )
        print(
            f"PASS {method:51s} "
            f"end={a['median']:.7f}s "
            f"final={b['median']*1000:.5f}ms"
        )

    per_dataset = doc["runtime"]["per_dataset"]
    assert set(per_dataset) == set(protocol["datasets"])
    for dataset, result in per_dataset.items():
        for key in ("end_to_end_or_fixed_final_model",
                    "selected_final_model_fit_plus_prediction"):
            assert set(result[key]) == set(EXPECTED)
            for method in EXPECTED:
                assert result[key][method]["n"] == 5, (dataset, method, key)

    print("PASS: Table S3, 11 numerical medians, 8 datasets, 40 units, six methods")
    print("LIMITATION: original 240 component/1440 candidate timing records remain unavailable")
    return doc


if __name__ == "__main__":
    audit()
