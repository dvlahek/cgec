#!/usr/bin/env python3
"""Recompute Spearman associations between Wine chemistry and signed interventions."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
FEATURES = [
    "alcohol", "sulphates", "volatile acidity",
    "total sulfur dioxide", "chlorides", "pH"
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uci-csv", type=Path, required=True)
    args = parser.parse_args()

    wine = pd.read_csv(args.uci_csv, sep=";")
    effects = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_feature_interventions.csv")
    assert wine.shape == (1599, 12)
    assert effects.row_index.to_list() == list(range(1599))
    np.testing.assert_array_equal(wine.quality, effects.observed_grade)
    pair56 = (
        np.minimum(effects.predicted_grade, effects.runner_up_grade).eq(5)
        & np.maximum(effects.predicted_grade, effects.runner_up_grade).eq(6)
    ).to_numpy()
    assert pair56.sum() == 1304
    signs = np.sign(effects.predicted_grade - effects.runner_up_grade)
    for feature in FEATURES:
        x = wine[feature].to_numpy()
        J = (effects[feature] * signs).to_numpy()
        print(f"{feature:24s} all={spearmanr(x, J).statistic:+.6f}  "
              f"pair5-6={spearmanr(x[pair56], J[pair56]).statistic:+.6f}")


if __name__ == "__main__":
    main()
