#!/usr/bin/env python3
"""Recompute Supplementary Fig. S5 using the archived Wine seed-0 OOF CSV.

No model fitting, downloading, or OOF evaluation. An exact conditional null
fixes, for each recorded-grade stratum g:
  N_g = number of all cases in grade g,
  K_g = count with adjacent rival-grade suggestion,
  n_g = count in the top review budget.
The selected adjacent-suggestion count is hypergeometric; the exact sum across
grades is obtained by convolving those distributions.

Usage from CGEC repository root:
  python scripts/verify_wine_s5_conditional_null.py
  python scripts/verify_wine_s5_conditional_null.py --stage

--stage saves a source-linked verification receipt for Git commit.
"""
import argparse
import csv
import hashlib
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "wine" / "source_wine_seed0" / "wine_oof_scores.csv"
EXPECTED = {
    80: {"adjacent": 69, "conditional_expected_share": 0.8394493889807555,
         "p_upper": 0.2726118077544628},
    160: {"adjacent": 133, "conditional_expected_share": 0.8283568806476624,
          "p_upper": 0.5105366444525768},
}
GRADES = {3: 10, 4: 53, 5: 681, 6: 638, 7: 199, 8: 18}


def hypergeometric_probs(population, successes, draws):
    """Exact integer combinatorics before conversion to probabilities."""
    assert 0 <= successes <= population and 0 <= draws <= population
    low = max(0, draws - (population - successes))
    high = min(draws, successes)
    denom = comb(population, draws)
    values = [0.0] * (high + 1)
    for k in range(low, high + 1):
        values[k] = (
            comb(successes, k) * comb(population - successes, draws - k) / denom
        )
    return values


def convolve(left, right):
    result = [0.0] * (len(left) + len(right) - 1)
    for i, value in enumerate(left):
        for j, other in enumerate(right):
            result[i + j] += value * other
    return result


def audit(path=SOURCE):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        records = list(csv.DictReader(file))
    assert len(records) == 1599, "Expected all 1599 original red-wine records"

    grade_counts = {int(g): 0 for g in GRADES}
    seen_rows = set()
    parsed = []
    for record in records:
        idx = int(record["row_index"])
        assert idx not in seen_rows, f"Duplicate row index: {idx}"
        seen_rows.add(idx)
        assert int(record["seed"]) == 0, f"Not seed 0 at row {idx}"
        grade = int(record["observed_grade"])
        assert grade in GRADES
        adjacent = int(record["adjacent_rival"])
        assert adjacent in (0, 1)
        # The CSV's original helper flag must agree with the grade-based definition.
        rival = int(record["rival_grade"])
        assert adjacent == int(abs(rival - grade) == 1), f"Adjacent flag differs at row {idx}"
        score = float(record["review_score"])
        grade_counts[grade] += 1
        parsed.append({"row_index": idx, "grade": grade,
                       "adjacent": adjacent, "review_score": score})
    assert seen_rows == set(range(1599))
    assert grade_counts == GRADES, f"Original recorded-grade counts differ: {grade_counts}"

    # Deterministic tie-break on original Wine row index. At the 5% boundary,
    # all equal-score rows belong to the same grade and adjacent class, so
    # this tie-break does not change S5's aggregate statistic.
    ranked = sorted(parsed, key=lambda r: (-r["review_score"], r["row_index"]))
    output = {}

    for budget, freeze in EXPECTED.items():
        selected = ranked[:budget]
        observed = sum(row["adjacent"] for row in selected)
        assert observed == freeze["adjacent"], (budget, observed, freeze["adjacent"])
        p_dist = [1.0]
        expected_count = 0.0
        strata = []
        for grade in sorted(GRADES):
            group = [row for row in parsed if row["grade"] == grade]
            chosen = [row for row in selected if row["grade"] == grade]
            N = len(group)
            K = sum(row["adjacent"] for row in group)
            n = len(chosen)
            k_obs = sum(row["adjacent"] for row in chosen)
            expected_count += n * K / N
            p_dist = convolve(p_dist, hypergeometric_probs(N, K, n))
            strata.append({"recorded_grade": grade, "N": N, "K": K,
                           "n": n, "selected_adjacent": k_obs})
        p_value = sum(p_dist[observed:])
        observed_share = observed / budget
        expected_share = expected_count / budget
        assert abs(p_value - freeze["p_upper"]) < 5e-11, (
            f"{budget} p={p_value}; expected {freeze['p_upper']}"
        )
        assert abs(expected_share - freeze["conditional_expected_share"]) < 1e-12
        assert abs(sum(p_dist) - 1) < 1e-10

        cut = selected[-1]["review_score"]
        tie_at_cutoff = [
            row for row in parsed if row["review_score"] == cut
        ]
        if len(tie_at_cutoff) > 1:
            assert len(set((r["grade"], r["adjacent"]) for r in tie_at_cutoff)) == 1, (
                "Boundary score tie affects grade or adjacent status"
            )
        output[str(budget)] = {
            "selected_cases": budget,
            "selected_adjacent": observed,
            "observed_share": observed_share,
            "conditional_expected_share": expected_share,
            "exact_one_sided_upper_tail_p": p_value,
            "strata": strata,
            "cutoff_score_tie_size": len(tie_at_cutoff),
        }
        print(
            f"PASS top {budget:>3} | adjacent={observed}/{budget}"
            f" | observed={observed_share:.5f}"
            f" | within-grade expected={expected_share:.5f}"
            f" | conditional p={p_value:.9f}"
        )

    print("PASS: Supplementary Fig. S5 exact conditional hypergeometric null from 1599 seed-0 OOF wines")
    print(f"SOURCE SHA-256={digest}")
    return {
        "artifact": "CGEC Supplementary Fig. S5 original-grade conditional adjacency null",
        "status": "PASS",
        "source": "wine/source_wine_seed0/wine_oof_scores.csv",
        "source_sha256": digest,
        "source_n": len(parsed),
        "test_definition": "Per-recorded-grade hypergeometric distributions convolved; inclusive upper tail",
        "ranking": "descending review_score, ties by ascending original row_index",
        "budgets": output,
        "run_type": "Read-only from archived OOF output; no model fitting",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, default=SOURCE)
    ap.add_argument("--stage", action="store_true", help="Stage verified JSON receipt under reproductions/")
    args = ap.parse_args()

    report = audit(args.source)
    if not args.stage:
        return

    receipt = ROOT / "reproductions/supplement_s5_wine/verification_receipt.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if receipt.exists():
        assert receipt.read_text(encoding="utf-8") == encoded, (
            f"Existing receipt differs: {receipt}"
        )
    else:
        receipt.write_text(encoded, encoding="utf-8")
    print(f"STAGED RECEIPT={receipt.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
