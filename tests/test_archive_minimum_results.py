"""Smoke-test the archival helper's dry-run and byte-preserving copy path."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def test_archive_helper_stages_only_after_apply(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1] / "scripts/archive_minimum_results.py"
    spec = importlib.util.spec_from_file_location("archive_minimum_results_test", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    root = tmp_path / "fresh_repo"
    dest = root / "paper_reproducibility" / "results"
    source = tmp_path / "old_results"
    source.mkdir()
    a = b"original JSON bytes\n"
    b = b"{\"run\":1}\n"
    (source / "a.json").write_bytes(a)
    (source / "b.jsonl").write_bytes(b)

    monkeypatch.setattr(mod, "ROOT", root)
    monkeypatch.setattr(mod, "DEST", dest)
    monkeypatch.setattr(mod, "PINNED", {"a.json": hashlib.sha256(a).hexdigest()})
    monkeypatch.setattr(mod, "OTHER_REQUIRED", {"b.jsonl": len(b)})
    monkeypatch.setattr(mod, "FILES", ("a.json", "b.jsonl"))

    monkeypatch.setattr(sys, "argv", [str(script), "--source-results-dir", str(source)])
    mod.main()  # no --apply
    assert not dest.exists(), "Dry run must not write to destination"

    monkeypatch.setattr(sys, "argv", [str(script), "--source-results-dir", str(source), "--apply"])
    mod.main()
    assert (dest / "a.json").read_bytes() == a
    assert (dest / "b.jsonl").read_bytes() == b
    manifest = json.loads((dest / "archived_source_manifest.json").read_text(encoding="utf-8"))
    assert [row["path"] for row in manifest["files"]] == [
        "paper_reproducibility/results/a.json",
        "paper_reproducibility/results/b.jsonl",
    ]

    # Idempotent second invocation must also succeed without mutating files.
    mod.main()
    assert (dest / "a.json").read_bytes() == a
