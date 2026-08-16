#!/usr/bin/env python3
"""
render_mvpc_fixtures.py — Res-Nova to MVPC-X Fixture Generator

Reads MVPC claim manifests from mvpc_manifests/ and emits a consolidated
MVPC-X claim fixture bundle in JSON format.

Usage:
    python3 scripts/render_mvpc_fixtures.py [--out PATH] [--check]
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = REPO_ROOT / "mvpc_manifests"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifests():
    if not MANIFESTS_DIR.exists():
        print(f"Error: manifests directory not found: {MANIFESTS_DIR}", file=sys.stderr)
        sys.exit(1)

    manifest_files = sorted(MANIFESTS_DIR.glob("*.json"))
    manifests = []
    for mf in manifest_files:
        if mf.name in ("MVPC_PIN.json", "MVPC_JUDGE_RUN_LOG.json", "MVPC_JUDGE_VERDICTS.json"):
            continue
        try:
            with open(mf, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data.get("schema_version") == "mvpc-claim-manifest-v1":
                    manifests.append((mf.name, data))
        except Exception as e:
            print(f"Error reading manifest {mf}: {e}", file=sys.stderr)
            sys.exit(1)
    return manifests


def validate_artifacts(manifests):
    errors = 0
    for name, m in manifests:
        claim_id = m.get("claim_id", name)
        artifacts = m.get("artifacts", [])
        for art in artifacts:
            rel_path = art.get("path") if isinstance(art, dict) else art
            if not rel_path:
                continue
            full_path = REPO_ROOT / rel_path
            if not full_path.exists():
                print(f"[{claim_id}] Missing artifact on disk: {rel_path}", file=sys.stderr)
                errors += 1
            else:
                expected_sha = art.get("sha256") if isinstance(art, dict) else None
                if expected_sha:
                    actual_sha = compute_sha256(full_path)
                    if actual_sha != expected_sha:
                        print(
                            f"[{claim_id}] SHA mismatch for {rel_path}:\n  expected: {expected_sha}\n  actual:   {actual_sha}",
                            file=sys.stderr,
                        )
                        errors += 1
    return errors == 0


def render_bundle(manifests):
    bundle = {
        "$schema": "https://raw.githubusercontent.com/Mega-Therion/MVPC-X/main/schemas/fixture_bundle_v1.json",
        "fixture_format_version": "1.0.0",
        "source_repository": "Mega-Therion/Res-Nova",
        "claims_count": len(manifests),
        "claims": [m for _, m in manifests],
    }
    return bundle


def main():
    parser = argparse.ArgumentParser(description="Render Res-Nova claims into MVPC fixture JSON format")
    parser.add_argument("--out", "-o", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--check", action="store_true", help="Validate all referenced artifacts and exit")
    args = parser.parse_args()

    manifests = load_manifests()
    valid = validate_artifacts(manifests)

    if args.check:
        if valid:
            print(f"PASS: {len(manifests)} manifest(s) validated cleanly against disk artifacts.")
            sys.exit(0)
        else:
            print("FAIL: Artifact validation errors detected.", file=sys.stderr)
            sys.exit(1)

    bundle = render_bundle(manifests)
    json_str = json.dumps(bundle, indent=2, ensure_ascii=False) + "\n"

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"Wrote {len(manifests)} claims fixture to {args.out}")
    else:
        sys.stdout.write(json_str)


if __name__ == "__main__":
    main()
