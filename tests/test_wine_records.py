from pathlib import Path
import json

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1] / "wine"


def test_seed0_row_alignment():
    scores = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_scores.csv")
    effects = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_feature_interventions.csv")
    assert len(scores) == len(effects) == 1599
    assert scores.row_index.tolist() == effects.row_index.tolist() == list(range(1599))
    np.testing.assert_array_equal(scores.observed_grade, effects.observed_grade)
    np.testing.assert_array_equal(scores.predicted_grade, effects.predicted_grade)


def test_neighbor_additivity_and_row_identity():
    scores = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_scores.csv")
    contributions = pd.read_csv(ROOT / "wine333_neighbour_contributions_direct_refit.csv")
    audit = json.loads((ROOT / "WINE333_REFIT_AUDIT.json").read_text())
    assert int(scores.iloc[332].fold) == 4
    assert int(scores.iloc[332].observed_grade) == 6
    assert int(scores.iloc[332].predicted_grade) == 5
    assert len(contributions) == 12
    assert contributions.training_row_one_based.is_unique
    assert abs(contributions.signed_Q_contribution.sum() - audit["refit_Q"]) < 1e-12
    assert abs(float(scores.iloc[332].review_score) - audit["archived_Q"]) < 1e-12
