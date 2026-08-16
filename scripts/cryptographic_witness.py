#!/usr/bin/env python3
"""
Res-Nova Cryptographic Witness & Release Sealing Tool

Generates and verifies HMAC-SHA256 cryptographic witness attestations across
canonical Res-Nova artifacts (manuscript, measurement JSONs, and formal proofs).

Usage:
  python3 scripts/cryptographic_witness.py [--out RELEASE_WITNESS.json] [--verify FILE]
"""

import os
import sys
import json
import hmac
import hashlib
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Canonical artifacts to include in the cryptographic witness manifest
CANONICAL_ARTIFACTS = [
    "EPISTEMIC_BOUNDARY_v1.5.0.md",
    "CLAIM_EVIDENCE_LEDGER.md",
    "CORPUS_DEPENDENCY_MAP.md",
    "02_galaxy_dynamics/A0_MEASUREMENT.json",
    "02_galaxy_dynamics/PARAMETER_LEDGER.json",
    "02_galaxy_dynamics/NFW_CONSTRAINED.json",
    "02_galaxy_dynamics/HALO_CONSPIRACY.json",
    "02_galaxy_dynamics/A0_ESTIMATE.json",
    "03_observer_jwst/PREREG_A0_OF_Z.md",
    "03_observer_jwst/A0_OF_Z_REPORT.json",
    "04_cosmology/TARGET_O1_A0_HORIZON_DERIVATION.md",
    "05_lean_formalization/HorizonScale.lean",
    "final_manuscript.pdf",
]


def sha256_file(filepath: Path) -> str:
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit_sha(repo_root: Path) -> str:
    """Retrieve current Git commit SHA."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "UNKNOWN_COMMIT"


def build_manifest(repo_root: Path) -> dict:
    """Build canonical artifact hash manifest."""
    manifest = {}
    missing = []

    for rel_path in CANONICAL_ARTIFACTS:
        full_path = repo_root / rel_path
        if full_path.exists():
            manifest[rel_path] = sha256_file(full_path)
        else:
            missing.append(rel_path)

    if missing:
        print(f"Warning: {len(missing)} artifact(s) not found: {missing}", file=sys.stderr)

    return manifest


def compute_manifest_digest(manifest: dict) -> str:
    """Produce deterministic canonical representation hash of manifest."""
    sorted_items = sorted(manifest.items())
    manifest_bytes = json.dumps(sorted_items, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(manifest_bytes).hexdigest()


def compute_hmac_signature(manifest_digest: str, secret_key: str) -> str:
    """Compute HMAC-SHA256 signature using secret key."""
    key_bytes = secret_key.encode("utf-8")
    msg_bytes = manifest_digest.encode("utf-8")
    return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()


def generate_witness(repo_root: Path, secret_key: str = None) -> dict:
    """Generate complete witness package."""
    manifest = build_manifest(repo_root)
    digest = compute_manifest_digest(manifest)
    commit_sha = get_git_commit_sha(repo_root)
    timestamp = datetime.now(timezone.utc).isoformat()

    witness = {
        "format": "res-nova-cryptographic-witness-v1",
        "timestamp_utc": timestamp,
        "commit_sha": commit_sha,
        "manifest_sha256": digest,
        "artifact_count": len(manifest),
        "artifacts": manifest,
    }

    if secret_key:
        signature = compute_hmac_signature(digest, secret_key)
        witness["authenticated"] = True
        witness["hmac_sha256_signature"] = signature
        witness["seal_status"] = "SEALED_WITH_CHRYPTOS"
    else:
        witness["authenticated"] = False
        witness["hmac_sha256_signature"] = None
        witness["seal_status"] = "UNAUTHENTICATED_UNSEALED"

    return witness


def verify_witness(witness_path: Path, secret_key: str = None) -> bool:
    """Verify an existing witness file."""
    with open(witness_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    manifest = data.get("artifacts", {})
    expected_digest = data.get("manifest_sha256", "")
    actual_digest = compute_manifest_digest(manifest)

    if expected_digest != actual_digest:
        print("FAIL: Manifest digest mismatch.", file=sys.stderr)
        return False

    print(f"PASS: Manifest integrity verified ({len(manifest)} artifacts).")

    if data.get("authenticated"):
        if not secret_key:
            print("NOTE: Witness contains an HMAC seal, but no verification key was provided.")
            return True
        expected_sig = data.get("hmac_sha256_signature", "")
        actual_sig = compute_hmac_signature(actual_digest, secret_key)
        if hmac.compare_digest(expected_sig, actual_sig):
            print("PASS: HMAC-SHA256 cryptographic seal VALID (Chryptos authenticated).")
            return True
        else:
            print("FAIL: HMAC-SHA256 signature mismatch.", file=sys.stderr)
            return False
    else:
        print("PASS: Unsealed witness format valid.")
        return True


def main():
    parser = argparse.ArgumentParser(description="Res-Nova Cryptographic Witness Tool")
    parser.add_argument("--out", type=str, default="RELEASE_WITNESS.json", help="Output path for witness JSON")
    parser.add_argument("--verify", type=str, default="", help="Path to witness JSON to verify")
    parser.add_argument("--key", type=str, default="", help="Optional explicit secret key (defaults to CHRYPTOS env var)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    # Retrieve secret from environment or CLI argument
    secret_key = args.key or os.environ.get("CHRYPTOS") or os.environ.get("CHRYPTOS_KEY") or None

    if args.verify:
        verify_path = Path(args.verify)
        if not verify_path.is_absolute():
            verify_path = repo_root / verify_path
        success = verify_witness(verify_path, secret_key)
        sys.exit(0 if success else 1)

    witness = generate_witness(repo_root, secret_key)

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo_root / out_path

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(witness, f, indent=2)

    print(f"Cryptographic Witness generated: {out_path}")
    print(f"Artifacts tracked: {witness['artifact_count']}")
    print(f"Manifest Digest : {witness['manifest_sha256']}")
    print(f"Seal Status     : {witness['seal_status']}")
    if witness["authenticated"]:
        print(f"HMAC Signature  : {witness['hmac_sha256_signature'][:16]}... (Redacted)")


if __name__ == "__main__":
    main()
