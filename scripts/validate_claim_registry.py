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
    "claim_type",
    "quotation_type",
    "source_locator",
    "falsifiability",
    "last_verified_commit",
}
ALLOWED_QUOTATION_TYPES = {"exact", "paraphrase"}
ALLOWED_FALSIFIABILITY_RESULTS = {
    "not_run",
    "supported",
    "contradicted",
    "inconclusive",
}
# A commit-contradicted result cannot coexist with a state that asserts the
# claim currently holds without qualification. This is the "no unsupported
# status upgrade" fail-closed rule from issue #50: a claim whose own
# falsifiability record says a real test contradicted it must be retracted
# or conditional, never formally-verified/derived/computed/empirically-supported.
STATES_FORBIDDEN_WHEN_CONTRADICTED = {
    "formally-verified",
    "derived",
    "computed",
    "empirically-supported",
}
# States that assert real-world support/verification must show more than an
# untested assertion: at least one artifact locating the evidence.
STATES_REQUIRING_ARTIFACT = {
    "formally-verified",
    "computed",
    "empirically-supported",
    "derived",
}


def validate(payload: object, root: Path = ROOT) -> list[str]:
    """Return a list of validation error strings; empty list means PASS."""
    errors: list[str] = []

    claims = payload.get("claims") if isinstance(payload, dict) else None
    if not isinstance(claims, list) or not claims:
        return ["claims must be a non-empty list"]

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

        state = claim.get("state")
        if state not in ALLOWED_STATES:
            errors.append(f"{prefix}.state is not allowed: {state!r}")

        for key in (
            "formal_artifacts",
            "computational_artifacts",
            "data_artifacts",
            "assumptions",
            "verification_commands",
        ):
            if not isinstance(claim.get(key), list):
                errors.append(f"{prefix}.{key} must be a list")

        for key in (
            "wording",
            "assurance_level",
            "independent_witness",
            "limitations",
            "status_owner",
            "claim_type",
            "source_locator",
        ):
            value = claim.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{key} must be non-empty")

        quotation_type = claim.get("quotation_type")
        if quotation_type not in ALLOWED_QUOTATION_TYPES:
            errors.append(f"{prefix}.quotation_type is not allowed: {quotation_type!r}")

        last_verified_commit = claim.get("last_verified_commit")
        if not isinstance(last_verified_commit, str) or len(last_verified_commit) != 40:
            errors.append(
                f"{prefix}.last_verified_commit must be a 40-character commit SHA"
            )

        falsifiability = claim.get("falsifiability")
        if not isinstance(falsifiability, dict):
            errors.append(f"{prefix}.falsifiability must be an object")
        else:
            for fkey in ("test", "scope", "result"):
                if fkey not in falsifiability:
                    errors.append(f"{prefix}.falsifiability missing {fkey}")
            result = falsifiability.get("result")
            if result not in ALLOWED_FALSIFIABILITY_RESULTS:
                errors.append(
                    f"{prefix}.falsifiability.result is not allowed: {result!r}"
                )
            if result != "not_run" and (
                falsifiability.get("test") in (None, "")
                or falsifiability.get("scope") in (None, "")
            ):
                errors.append(
                    f"{prefix}.falsifiability has a result of {result!r} but no test/scope named"
                )
            # Fail-closed: a state that asserts current support cannot survive
            # a falsifiability record that says a real test contradicted it.
            if result == "contradicted" and state in STATES_FORBIDDEN_WHEN_CONTRADICTED:
                errors.append(
                    f"{prefix}.state is {state!r} but falsifiability.result is 'contradicted' "
                    "-- must be 'retracted' or 'conditional'"
                )

        # Fail-closed: states that assert derivation, computation, formal
        # verification, or empirical support must point at the evidence, not
        # just narrate it in wording/limitations.
        if state in STATES_REQUIRING_ARTIFACT:
            artifact_count = (
                len(claim.get("formal_artifacts") or [])
                + len(claim.get("computational_artifacts") or [])
                + len(claim.get("data_artifacts") or [])
            )
            if artifact_count == 0:
                errors.append(
                    f"{prefix}.state is {state!r} but no formal/computational/data artifact is listed"
                )
        if state == "empirically-supported" and not claim.get("data_artifacts"):
            errors.append(
                f"{prefix}.state is 'empirically-supported' but data_artifacts is empty"
            )

        paths = (
            list(claim.get("formal_artifacts", []))
            + list(claim.get("computational_artifacts", []))
            + list(claim.get("data_artifacts", []))
        )
        witness = claim.get("independent_witness")
        if (
            isinstance(witness, str)
            and witness
            and not witness.startswith(("http://", "https://"))
        ):
            paths.append(witness)
        for rel in paths:
            path = root / rel
            if not path.exists():
                errors.append(f"{prefix} references missing path: {rel}")

    return errors


if __name__ == "__main__":
    if not REGISTRY.is_file():
        print("FAIL")
        print(f" - missing {REGISTRY.relative_to(ROOT)}")
        sys.exit(1)

    try:
        payload = json.loads(REGISTRY.read_text())
    except json.JSONDecodeError as exc:
        print("FAIL")
        print(f" - invalid JSON: {exc}")
        sys.exit(1)

    errors = validate(payload)
    if errors:
        print("FAIL")
        print("\n".join(f" - {error}" for error in errors))
        sys.exit(1)

    print(f"PASS — validated {len(payload['claims'])} claim records")
