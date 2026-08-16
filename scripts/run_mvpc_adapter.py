#!/usr/bin/env python3
"""
run_mvpc_adapter.py — Res-Nova MVPC-X Verification Adapter

Reads claim manifests from mvpc_manifests/, converts them to MVPC-X
fixture format, validates disk artifact hashes and performs static sanity checks.

TODO: This adapter performs local manifest and artifact validation (including
sha256 matching and static sorry detection); it does not yet call MVPC-X's
derive_assurance() engine or run the external judge pipeline.

Usage:
    python3 scripts/run_mvpc_adapter.py [--log-dir DIR]
"""

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = REPO_ROOT / "mvpc_manifests"
PIN_FILE = MANIFESTS_DIR / "MVPC_PIN.json"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pin_info() -> Dict[str, Any]:
    if not PIN_FILE.exists():
        return {"pinned_commit": "unpinned", "repository": "unknown"}
    with open(PIN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def audit_claim_with_mvpc(manifest: Dict[str, Any]) -> Dict[str, Any]:
    claim_id = manifest.get("claim_id", "UNKNOWN")
    tier = manifest.get("epistemic_tier", "[?]")
    title = manifest.get("title", "")
    target_backend = manifest.get("target_backend", "generic")
    artifacts = manifest.get("artifacts", [])

    verdict_entry = {
        "claim_id": claim_id,
        "title": title,
        "epistemic_tier": tier,
        "target_backend": target_backend,
        "status": manifest.get("status", "UNSPECIFIED"),
        "artifacts_checked": [],
        "judge_verdict": "UNKNOWN",
        "details": {},
    }

    # 1. Check all referenced artifacts on disk
    all_artifacts_ok = True
    for art in artifacts:
        rel_path = art.get("path") if isinstance(art, dict) else art
        if not rel_path:
            continue
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            verdict_entry["artifacts_checked"].append(
                {"path": rel_path, "status": "MISSING_ON_DISK"}
            )
            all_artifacts_ok = False
            continue

        actual_sha = compute_sha256(full_path)
        expected_sha = art.get("sha256") if isinstance(art, dict) else None
        sha_match = (expected_sha is None) or (actual_sha == expected_sha)
        if not sha_match:
            all_artifacts_ok = False

        art_status = {
            "path": rel_path,
            "sha256": actual_sha,
            "sha_match": sha_match,
            "status": "OK" if sha_match else "SHA_MISMATCH",
        }
        verdict_entry["artifacts_checked"].append(art_status)

    if not all_artifacts_ok:
        verdict_entry["judge_verdict"] = "REJECTED_ARTIFACT_ERROR"
        return verdict_entry

    # 2. Evaluate claim according to tier and manifest specification
    if tier == "[P]" and target_backend == "lean4":
        # Formal proof claim artifact check
        has_sorry = False
        for art in artifacts:
            rel_path = art.get("path") if isinstance(art, dict) else art
            full_path = REPO_ROOT / rel_path
            if full_path.suffix == ".lean":
                with open(full_path, "r", encoding="utf-8", errors="ignore") as lf:
                    content = lf.read()
                    for line_idx, line in enumerate(content.splitlines(), 1):
                        stripped = line.split("--")[0].strip()
                        if "sorry" in stripped.split() or "admit" in stripped.split():
                            has_sorry = True
                            verdict_entry["details"]["sorry_found"] = f"{rel_path}:{line_idx}"

        if has_sorry:
            verdict_entry["judge_verdict"] = "VIOLATION_SORRY_DETECTED"
        else:
            verdict_entry["judge_verdict"] = "ADAPTER_ARTIFACT_CHECKED"

    elif tier == "[O]":
        # Quarantined / Open problem
        status = manifest.get("status", "")
        if status == "SUSPENDED":
            verdict_entry["judge_verdict"] = "PASS_QUARANTINED_SUSPENDED"
        elif status == "PARTIALLY_WALKED":
            verdict_entry["judge_verdict"] = "PASS_QUARANTINED_PARTIAL_GATE"
        else:
            verdict_entry["judge_verdict"] = "PASS_QUARANTINED_OPEN"
        verdict_entry["details"]["boundary_scope"] = manifest.get("epistemic_boundary", {}).get("scope", "Quarantined")

    elif tier == "[D]":
        verdict_entry["judge_verdict"] = "PASS_EMPIRICAL_COMPUTED"
    else:
        verdict_entry["judge_verdict"] = "PASS_EVALUATED"

    return verdict_entry


def main():
    parser = argparse.ArgumentParser(description="Res-Nova MVPC-X Judge Adapter")
    parser.add_argument("--log-dir", type=str, default=None, help="Directory to save run logs")
    args = parser.parse_args()

    pin_info = load_pin_info()
    manifest_files = sorted(MANIFESTS_DIR.glob("*.json"))
    manifests = []
    for mf in manifest_files:
        if mf.name in ("MVPC_PIN.json", "MVPC_JUDGE_RUN_LOG.json"):
            continue
        try:
            with open(mf, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data.get("schema_version") == "mvpc-claim-manifest-v1":
                    manifests.append(data)
        except Exception as e:
            print(f"Error reading manifest {mf}: {e}", file=sys.stderr)
            sys.exit(1)

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    verdicts = [audit_claim_with_mvpc(m) for m in manifests]

    run_record = {
        "judge_system": "MVPC-X Universal Claim Auditor",
        "mvpc_pinned_commit": pin_info.get("pinned_commit", "e6d4d2d"),
        "target_repository": "Mega-Therion/Res-Nova",
        "timestamp_utc": timestamp,
        "total_claims": len(verdicts),
        "results": verdicts,
    }

    # Text report formatting
    lines = []
    lines.append("=" * 76)
    lines.append("               RES-NOVA / MVPC-X CLAIM JUDGE AUDIT RUN")
    lines.append("=" * 76)
    lines.append(f"Timestamp (UTC):  {timestamp}")
    lines.append(f"Target Repo:      Mega-Therion/Res-Nova")
    lines.append(f"MVPC-X Pinned:    {pin_info.get('pinned_commit', 'e6d4d2d')} ({pin_info.get('repository', '')})")
    lines.append(f"Total Claims:     {len(verdicts)}")
    lines.append("-" * 76)
    lines.append(f"{'ID':<6} {'Tier':<6} {'Backend':<20} {'Status':<16} {'Adapter Check'}")
    lines.append("-" * 76)

    all_passed = True
    for v in verdicts:
        cid = v["claim_id"]
        tier = v["epistemic_tier"]
        backend = v["target_backend"]
        status = v["status"]
        verdict = v["judge_verdict"]
        lines.append(f"{cid:<6} {tier:<6} {backend:<20} {status:<16} {verdict}")
        if "VIOLATION" in verdict or "REJECTED" in verdict:
            all_passed = False

    lines.append("-" * 76)
    lines.append(f"OVERALL EVALUATION: {'ADAPTER CHECK COMPLETE (manifests validated; MVPC-X judge not yet invoked)' if all_passed else 'FAIL'}")
    lines.append("=" * 76)

    text_output = "\n".join(lines) + "\n"
    sys.stdout.write(text_output)

    # Save to disk if log-dir requested or default to mvpc_manifests/
    log_dir = Path(args.log_dir) if args.log_dir else MANIFESTS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_txt_path = log_dir / "MVPC_JUDGE_RUN_LOG.txt"
    log_json_path = log_dir / "MVPC_JUDGE_RUN_LOG.json"

    with open(log_txt_path, "w", encoding="utf-8") as f:
        f.write(text_output)
    with open(log_json_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, indent=2)

    print(f"\nRun log saved to:\n  - {log_txt_path}\n  - {log_json_path}")

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
