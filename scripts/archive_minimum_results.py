#!/usr/bin/env python3
"""Stage existing, verified CGEC experimental source files without retraining.

PowerShell from cgec repository root:

  .\\.venv\\Scripts\\python.exe scripts\\archive_minimum_results.py --source-results-dir "C:\\Articles\\Clanci\\MCGC-new-repo\\paper_reproducibility\\results"
  .\\.venv\\Scripts\\python.exe scripts\\archive_minimum_results.py --source-results-dir "C:\\Articles\\Clanci\\MCGC-new-repo\\paper_reproducibility\\results" --apply

Default is dry-run; --apply copies files byte-for-byte into the repository's
paper_reproducibility/results/ folder. Existing files are never overwritten
if their content differs. No models are fitted and no Git actions are performed.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "paper_reproducibility/results"
# These SHA-256 values have already been checked by successful local audits.
PINNED = {
    "v31_strict_oof_scaling_audit.json": "530f9599d945dd895cc2d155b81020e7488a58dcd7369c36c8d362fb7cbc692e",
    "v32c_real_data_confirmation_runs.jsonl": "7f26f3d4028a119a8b83d71faad05fbc031ae37d9002695be56c6a5fe0a67a76",
    "v33_tuned_cgec_runs.jsonl": "cc367789512d3b1bc2c3c77a8e5fee35309de8bfd0afdedd583893f27c08a91f",
    "v33_tuned_cgec_summary.json": "a99547042f7845a90811894b801f32d16a671c98610aa1a1bcdc00e8e650f96b",
}
# Preserve the frozen experiment's complete source context too.
OTHER_REQUIRED = {
    "v32c_real_data_confirmation.json": 2979336,
    "v33_tuned_cgec_candidates.jsonl": 1294741,
}
FILES = tuple(PINNED) + tuple(OTHER_REQUIRED)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-results-dir", required=True, type=Path)
    ap.add_argument("--apply", action="store_true", help="Actually copy after validation")
    args = ap.parse_args()

    source = args.source_results_dir.resolve()
    destination = DEST.resolve()
    assert source.is_dir(), f"Source results folder not found: {source}"
    assert source != destination, "Source and destination are the same; no copy necessary"

    verified = []
    for name in FILES:
        orig = source / name
        assert orig.is_file(), f"Missing archived experiment file: {orig}"
        original_size = orig.stat().st_size
        digest = sha256(orig)
        if name in PINNED:
            assert digest == PINNED[name], f"SHA-256 mismatch for {name}: {digest}"
        else:
            assert original_size == OTHER_REQUIRED[name], (
                f"Unexpected file size for {name}: {original_size}"
            )
        target = destination / name
        if target.exists():
            assert sha256(target) == digest, f"Conflicting destination! Will not overwrite {target}"
        verified.append((orig, target, digest, original_size))
        print(f"SOURCE PASS: {name:45s} {original_size:>9d} bytes {digest}")

    if not args.apply:
        print("DRY RUN PASS. Files verified, nothing copied. Add --apply to stage them.")
        return

    destination.mkdir(parents=True, exist_ok=True)
    entries = []
    for orig, target, digest, size in verified:
        if not target.exists():
            shutil.copyfile(orig, target)
        assert sha256(target) == digest, f"Copy integrity failed: {target}"
        entries.append({"path": str(target.relative_to(ROOT)), "sha256": digest, "bytes": size})
    manifest = destination / "archived_source_manifest.json"
    metadata = {
        "description": "Preserved original multi-seed experiment outputs; no model retraining",
        "files": entries,
        "note": "This manifest inventories files copied byte-for-byte from an existing local experiment archive. It is not an independent environment lock.",
    }
    if manifest.exists():
        existing = json.loads(manifest.read_text(encoding="utf-8"))
        assert existing == metadata, "Existing manifest differs; refusing to overwrite"
    else:
        manifest.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"ARCHIVE PASS: copied/verified {len(entries)} original files")
    print("Inspect 'git status', then add and commit ONLY the reviewed original files and manifest.")
    print("git add paper_reproducibility/results")
    print("git commit -m \"data: archive original verified CGEC reproducibility outputs\"")
    print("git push")


if __name__ == "__main__":
    main()
