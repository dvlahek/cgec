#!/usr/bin/env python3
"""Recompute low/high measurement strata from frozen seed-0 interventions."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
FEATURES = ["alcohol", "sulphates", "volatile acidity", "total sulfur dioxide"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uci-csv", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    wine = pd.read_csv(args.uci_csv, sep=";")
    effects = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_feature_interventions.csv")
    assert wine.shape == (1599, 12)
    assert list(effects.row_index) == list(range(1599))
    np.testing.assert_array_equal(wine.quality.to_numpy(), effects.observed_grade.to_numpy())
    oriented = effects[FEATURES].multiply(
        np.sign(effects.predicted_grade - effects.runner_up_grade), axis=0
    )

    rows = []
    for lower, higher in [(5, 6), (6, 7)]:
        mask = (
            np.minimum(effects.predicted_grade, effects.runner_up_grade).eq(lower)
            & np.maximum(effects.predicted_grade, effects.runner_up_grade).eq(higher)
        )
        ix = np.flatnonzero(mask.to_numpy())
        for feature in FEATURES:
            x = wine.loc[ix, feature]
            low, high = np.quantile(x.to_numpy(), [0.2, 0.8])
            lo_ix = ix[x.to_numpy() <= low]
            hi_ix = ix[x.to_numpy() >= high]
            rows.append({
                "pair": f"{lower}-{higher}", "feature": feature, "n_pair": len(ix),
                "q20": low, "q80": high, "n_low": len(lo_ix), "n_high": len(hi_ix),
                "mean_J_low": oriented.loc[lo_ix, feature].mean(),
                "mean_J_high": oriented.loc[hi_ix, feature].mean(),
                "pred_upper_low": (effects.loc[lo_ix, "predicted_grade"] == higher).mean(),
                "pred_upper_high": (effects.loc[hi_ix, "predicted_grade"] == higher).mean()
            })
    result = pd.DataFrame(rows)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(args.out, index=False)
    print(result.to_string(index=False, float_format=lambda x: f"{x:.6f}"))


if __name__ == "__main__":
    main()
