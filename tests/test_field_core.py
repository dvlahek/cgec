"""Smoke tests for the paper-specific field-only CGEC model."""
import numpy as np
from sklearn.datasets import make_moons

from paper_reproducibility.xai.field_only_cgec import FieldOnlyCGEC


def test_prediction_margin_decomposes_over_training_neighbours():
    X, y = make_moons(n_samples=80, noise=0.12, random_state=11)
    model = FieldOnlyCGEC().fit(X[:60], y[:60])
    explanation = model.margin_contributions(X[60])
    assert len(explanation["nodes"]) == 12
    assert len(explanation["contributions"]) == 12
    np.testing.assert_allclose(
        sum(explanation["contributions"]),
        explanation["margin"],
        rtol=1e-11,
        atol=1e-12,
    )
    assert model.predict(X[60:63]).shape == (3,)


def test_feature_interventions_do_not_change_original_class_pair():
    X, y = make_moons(n_samples=80, noise=0.12, random_state=12)
    model = FieldOnlyCGEC().fit(X[:60], y[:60])
    parts = model.margin_contributions(X[60])
    interventions = model.feature_intervention_effects(X[60])
    assert interventions["winner"] == parts["winner"]
    assert interventions["runner_up"] == parts["runner_up"]
    assert len(interventions["effects"]) == X.shape[1]
    assert np.isfinite(interventions["effects"]).all()
