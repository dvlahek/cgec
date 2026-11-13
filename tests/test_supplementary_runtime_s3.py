"""Guard the 11 published runtime medians in Table S3 using recovered v3.6b data."""
import importlib.util
from pathlib import Path


def test_runtime_table_s3_recovered_summary():
    script = Path(__file__).resolve().parents[1] / "scripts/verify_supplement_s3_v36b.py"
    spec = importlib.util.spec_from_file_location("verify_runtime_s3", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.audit()["protocol"]["n_dataset_seed_units"] == 40
