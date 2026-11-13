"""Regression-check the exact Supplementary Fig. S5 conditional null."""
import importlib.util
from pathlib import Path


def test_supplementary_s5_exact_wine_conditional_null():
    script = Path(__file__).resolve().parents[1] / "scripts/verify_wine_s5_conditional_null.py"
    spec = importlib.util.spec_from_file_location("verify_wine_s5", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = mod.audit()
    assert result["status"] == "PASS"
    assert result["source_n"] == 1599

    low = result["budgets"]["80"]
    high = result["budgets"]["160"]
    assert low["selected_adjacent"] == 69
    assert high["selected_adjacent"] == 133
    assert abs(low["observed_share"] - 0.8625) < 1e-12
    assert abs(high["observed_share"] - 0.83125) < 1e-12
    assert abs(low["conditional_expected_share"] - 0.8394493889807555) < 1e-12
    assert abs(high["conditional_expected_share"] - 0.8283568806476624) < 1e-12
    assert abs(low["exact_one_sided_upper_tail_p"] - 0.2726118077544628) < 5e-11
    assert abs(high["exact_one_sided_upper_tail_p"] - 0.5105366444525768) < 5e-11
    assert low["cutoff_score_tie_size"] == 3
    assert high["cutoff_score_tie_size"] == 1
    assert len(low["strata"]) == len(high["strata"]) == 6
