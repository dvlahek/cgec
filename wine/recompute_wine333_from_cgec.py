#!/usr/bin/env python3
"""Independently reconstruct wine 333's fold-4 CGEC evidence and 12 contributions."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.sparse import coo_matrix, diags

ROOT = Path(__file__).resolve().parent
FEATURES = [
    "fixed acidity", "volatile acidity", "citric acid", "residual sugar",
    "chlorides", "free sulfur dioxide", "total sulfur dioxide",
    "density", "pH", "sulphates", "alcohol"
]
EXPECTED_NEIGHBORS = {191, 256, 196, 621, 415, 792, 622, 208, 694, 790, 1197, 1200}


def run(wine_file, out_dir):
    wine_file = Path(wine_file)
    source_hash = hashlib.sha256(wine_file.read_bytes()).hexdigest()
    df = pd.read_csv(wine_file, sep=";")
    oof = pd.read_csv(ROOT / "source_wine_seed0/wine_oof_scores.csv")
    assert df.shape == (1599, 12)
    assert FEATURES == list(df.columns[:11])
    assert len(oof) == 1599
    np.testing.assert_array_equal(df.quality.to_numpy(), oof.observed_grade.to_numpy())
    np.testing.assert_array_equal(oof.row_index.to_numpy(), np.arange(1599))

    # Identical measured vectors were assigned to the same OOF fold.
    groups = df[FEATURES].astype(str).agg("|".join, axis=1)
    assert (oof.groupby(groups).fold.nunique() == 1).all()

    target = 332     # One-based UCI record 333
    fold = int(oof.loc[target, "fold"])
    assert fold == 4
    training_rows = oof.index[oof.fold != fold].to_numpy()
    assert len(training_rows) == 1279

    raw = df.loc[:, FEATURES].to_numpy(dtype=float)
    mean = raw[training_rows].mean(axis=0)
    std = raw[training_rows].std(axis=0, ddof=0)
    std[std < 1e-12] = 1.0
    z = (raw[training_rows] - mean) / std
    q = (raw[target] - mean) / std
    labels = df.quality.to_numpy()[training_rows]
    classes = np.unique(labels)
    np.testing.assert_array_equal(classes, np.arange(3, 9))

    K, alpha, steps = 12, 0.85, 40

    # Directed locally scaled 12-neighbor graph, excluding each training node itself.
    distances_sq = cdist(z, z, metric="sqeuclidean")
    np.fill_diagonal(distances_sq, np.inf)
    nearest = np.argsort(distances_sq, axis=1, kind="stable")[:, :K]
    nearest_sq = np.take_along_axis(distances_sq, nearest, axis=1)
    scale = np.maximum(np.sqrt(nearest_sq[:, -1]), 1e-12)

    source = np.repeat(np.arange(len(training_rows)), K)
    destination = nearest.ravel()
    weight = np.exp(
        -distances_sq[source, destination]
        / np.maximum(scale[source] * scale[destination], 1e-12)
    )
    W = coo_matrix(
        (weight, (source, destination)), shape=(len(training_rows), len(training_rows))
    ).tocsr()
    W = W.maximum(W.T).tocsr()
    row_sums = np.asarray(W.sum(axis=1)).ravel()
    P = diags(1.0 / np.maximum(row_sums, 1e-12)) @ W

    B = (labels[:, None] == classes[None, :]).astype(float)
    field = B.copy()
    for _ in range(steps):
        field = (1.0 - alpha) * B + alpha * (P @ field)

    competitor = np.empty_like(field)
    for c in range(len(classes)):
        competitor[:, c] = np.max(np.delete(field, c, axis=1), axis=1)
    contrast = field - competitor

    query_sq = np.sum((z - q[None, :]) ** 2, axis=1)
    indices = np.argsort(query_sq, kind="stable")[:K]
    query_scale_sq = max(float(query_sq[indices[-1]]), 1e-24)
    affinities = np.exp(-query_sq[indices] / query_scale_sq)
    affinities /= affinities.sum()

    i5 = int(np.flatnonzero(classes == 5)[0])
    i6 = int(np.flatnonzero(classes == 6)[0])
    terms = affinities * (contrast[indices, i5] - contrast[indices, i6])
    refit_margin = float(
        affinities @ contrast[indices, i5] - affinities @ contrast[indices, i6]
    )
    archive_margin = float(oof.loc[target, "review_score"])

    assert abs(float(terms.sum()) - refit_margin) < 1e-12
    uci_rows = training_rows[indices] + 1
    assert set(uci_rows) == EXPECTED_NEIGHBORS
    assert (labels[indices] == 5).sum() == 10
    assert (labels[indices] == 6).sum() == 2

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = pd.DataFrame({
        "training_row_one_based": uci_rows,
        "recorded_grade": labels[indices],
        "affinity": affinities,
        "signed_Q_contribution": terms,
        "standardized_distance": np.sqrt(query_sq[indices]),
    }).sort_values("signed_Q_contribution", ascending=False)
    output.to_csv(
        out_dir / "wine333_neighbour_contributions_model_export.csv",
        index=False, float_format="%.17g"
    )

    audit = {
        "source_sha256": source_hash,
        "n_wines": 1599, "n_train": len(training_rows),
        "target_uci_record": 333, "fold": fold, "K": K,
        "diffusion_alpha": alpha, "diffusion_steps": steps,
        "Q_refit": refit_margin,
        "Q_archived": archive_margin,
        "refit_minus_archive": refit_margin - archive_margin,
        "sum_neighbor_contributions": float(terms.sum()),
        "neighbor_set_matches_archived_evidence": True,
    }
    (out_dir / "wine333_neighbour_model_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wine", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    run(args.wine, args.out_dir)


if __name__ == "__main__":
    main()
