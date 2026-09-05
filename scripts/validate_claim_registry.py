"""Validate the Res-Nova machine-readable assurance claim registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assurance" / "claims.json"
ALLOWED_STATES = {
    "proposed",
    "axiomatic",
    "derived",
    "computed",
    "formally-verified",
    "empirically-supported",
    "conditional",
    "retracted",
}
REQUIRED = {
    "id",
    "wording",
    "state",
    "assurance_level",
    "formal_artifacts",
    "computational_artifacts",
    "data_artifacts",
    "assumptions",
    "verification_commands",
    "independent_witness",
    "limitations",
    "status_owner",
}
errors: list[str] = []

if not REGISTRY.is_file():
    errors.append(f"missing {REGISTRY.relative_to(ROOT)}")
else:
    try:
        payload = json.loads(REGISTRY.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {exc}")
        payload = {}

    claims = payload.get("claims") if isinstance(payload, dict) else None
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []

    ids: set[str] = set()
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = REQUIRED - claim.keys()
        errors.extend(f"{prefix} missing {key}" for key in sorted(missing))
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{prefix}.id must be non-empty")
        elif claim_id in ids:
            errors.append(f"duplicate claim id {claim_id}")
        else:
            ids.add(claim_id)
        if claim.get("state") not in ALLOWED_STATES:
            errors.append(f"{prefix}.state is not allowed: {claim.get('state')!r}")
        for key in ("formal_artifacts", "computational_artifacts", "data_artifacts", "assumptions", "verification_commands"):
            if not isinstance(claim.get(key), list):
                errors.append(f"{prefix}.{key} must be a list")
        for key in ("wording", "assurance_level", "independent_witness", "limitations", "status_owner"):
            if not isinstance(claim.get(key), str) or not claim.get(key).strip():
                errors.append(f"{prefix}.{key} must be non-empty")
        paths = list(claim.get("formal_artifacts", [])) + list(claim.get("computational_artifacts", [])) + list(claim.get("data_artifacts", []))
        witness = claim.get("independent_witness")
        if isinstance(witness, str) and witness and not witness.startswith(("http://", "https://")):
            paths.append(witness)
        for rel in paths:
            path = ROOT / rel
            if not path.exists():
                errors.append(f"{prefix} references missing path: {rel}")

if errors:
    print("FAIL")
    print("\n".join(f" - {error}" for error in errors))
    sys.exit(1)

print(f"PASS — validated {len(claims)} claim records")
