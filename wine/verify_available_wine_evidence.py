#!/usr/bin/env python3
"""Validate the archived red-wine seed-0 evidence without downloading data."""
from pathlib import Path
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def main():
    scores = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_scores.csv")
    effects = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_feature_interventions.csv")
    neighbors = pd.read_csv(ROOT / "wine333_neighbour_contributions_direct_refit.csv")
    audit = json.loads((ROOT / "WINE333_REFIT_AUDIT.json").read_text())
    rho = json.loads((ROOT / "WINE_CHEMISTRY_CORRELATIONS_VERIFIED.json").read_text())

    assert len(scores) == len(effects) == 1599
    assert scores.row_index.to_list() == effects.row_index.to_list() == list(range(1599))
    np.testing.assert_array_equal(scores.observed_grade, effects.observed_grade)
    np.testing.assert_array_equal(scores.predicted_grade, effects.predicted_grade)
    assert scores.seed.eq(0).all()
    assert scores.observed_grade.value_counts().to_dict() == {
        3: 10, 4: 53, 5: 681, 6: 638, 7: 199, 8: 18
    }
    wine333 = scores.iloc[332]
    assert (int(wine333.fold), int(wine333.observed_grade),
            int(wine333.predicted_grade)) == (4, 6, 5)
    assert len(neighbors) == 12
    assert neighbors.training_row_one_based.is_unique
    assert neighbors.recorded_grade.value_counts().to_dict() == {5: 10, 6: 2}
    assert abs(neighbors.signed_Q_contribution.sum() - audit["refit_Q"]) < 1e-12
    assert abs(wine333.review_score - audit["archived_Q"]) < 1e-12
    assert abs(audit["refit_Q"] - audit["archived_Q"]) < 2.1e-5
    assert rho["n_total"] == 1599 and len(rho["features"]) == 6

    print("PASS: 1599 OOF rows, label alignment, wine-333 fold, "
          "12-neighbor refit contributions and recorded statistics.")
    print("This check does not reproduce the original multi-seed benchmark runs.")


if __name__ == "__main__":
    main()
