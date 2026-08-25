#!/usr/bin/env python3
"""Static preflight for Res-Nova reproducibility runs.

This is integrity and schema checking only. A PASS here is not a proved
claim, not an empirical result, and not independent reproduction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_PREFLIGHT = 10
EXIT_INTEGRITY = 20
EXIT_DRIFT = 50
EXIT_VISIBILITY = 70

ALLOWED_MODES = {
    "self_test",
    "static_preflight",
    "local_verified",
    "clean_worktree",
    "cold_environment",
    "independent_replication",
}
ALLOWED_STATUS = {
    "PASS",
    "FAIL",
    "BLOCKED",
    "INCONCLUSIVE",
    "INFRA_ERROR",
    "QUARANTINED",
}
ALLOWED_POLICY = {
    "ALLOW_INTERNAL",
    "ALLOW_RELEASE",
    "BLOCK_RELEASE",
    "REQUIRE_HUMAN_REVIEW",
}
PRIVATE_MARKERS = ("/home/", "/Users/", "SECRET", "TOKEN", "API_KEY")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def emit(event_type: str, **fields: Any) -> None:
    record = {"event": event_type, "at_utc": utc_now(), **fields}
    sys.stdout.write(json.dumps(record, sort_keys=True) + "\n")
    sys.stdout.flush()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_run_envelope(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != "res-nova-repro-run-v1":
        errors.append("schema_version must be res-nova-repro-run-v1")
    for key in ("run_id", "profile_id", "mode", "target", "result"):
        if key not in payload:
            errors.append(f"missing required field: {key}")
    mode = payload.get("mode")
    if mode is not None and mode not in ALLOWED_MODES:
        errors.append(f"invalid mode: {mode}")
    target = payload.get("target") or {}
    if isinstance(target, dict) and not target.get("repository"):
        errors.append("target.repository is required")
    result = payload.get("result") or {}
    if isinstance(result, dict):
        if result.get("status") not in ALLOWED_STATUS:
            errors.append("result.status is invalid")
        if result.get("policy_decision") not in ALLOWED_POLICY:
            errors.append("result.policy_decision is invalid")
        if result.get("claim_status_changes"):
            errors.append("preflight forbids automatic claim_status_changes")
    return errors


def validate_legacy_index(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != "res-nova-legacy-run-index-v1":
        errors.append("legacy index schema_version mismatch")
    runs = payload.get("runs")
    if not isinstance(runs, list) or not runs:
        errors.append("legacy index must contain runs")
        return errors
    refs = [item.get("legacy_run_reference") for item in runs if isinstance(item, dict)]
    if "VERIFICATION_RUN_007" not in refs:
        errors.append("VERIFICATION_RUN_007 must remain indexed")
    for item in runs:
        if not isinstance(item, dict):
            continue
        if item.get("legacy_run_reference") == "VERIFICATION_RUN_007":
            if item.get("new_mode") != "clean_worktree":
                errors.append("RUN_007 mode must remain clean_worktree")
            if item.get("promotion") != "blocked_for_independent_replication":
                errors.append("RUN_007 must stay blocked for independent replication")
            if item.get("epistemic_status") != "[O]":
                errors.append("RUN_007 epistemic status must remain [O]")
    return errors


def check_visibility(payload: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            errors.extend(check_visibility(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            errors.extend(check_visibility(value, f"{path}[{index}]"))
    elif isinstance(payload, str):
        for marker in PRIVATE_MARKERS:
            if marker in payload:
                errors.append(f"possible private marker {marker!r} at {path}")
    return errors


def check_hashes(pairs: list[tuple[Path, str]]) -> list[str]:
    errors: list[str] = []
    for path, expected in pairs:
        if not path.is_file():
            errors.append(f"missing artifact: {path}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"hash mismatch: {path} expected {expected} actual {actual}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Res-Nova static reproducibility preflight")
    parser.add_argument("--run", type=Path, help="Path to a repro-run-v1 JSON envelope")
    parser.add_argument("--legacy-index", type=Path, help="Path to LEGACY_RUN_INDEX.json")
    parser.add_argument("--hash", action="append", default=[], metavar="PATH=SHA256")
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()

    emit("run_started", profile="static_preflight", mode="static_preflight")
    exit_code = EXIT_OK
    errors: list[str] = []

    if args.run:
        try:
            payload = load_json(args.run)
        except (OSError, json.JSONDecodeError) as exc:
            emit("preflight_failed", check="load_run", severity="S2", detail=str(exc))
            return EXIT_PREFLIGHT
        schema_errors = validate_run_envelope(payload)
        if schema_errors:
            errors.extend(schema_errors)
            exit_code = EXIT_PREFLIGHT
            emit("preflight_failed", check="schema", detail=schema_errors)
        else:
            emit("preflight_passed", check="schema")
        visibility_errors = check_visibility(payload)
        if visibility_errors:
            errors.extend(visibility_errors)
            exit_code = max(exit_code, EXIT_VISIBILITY)
            emit("preflight_failed", check="visibility", detail=visibility_errors)

    if args.legacy_index:
        try:
            index_payload = load_json(args.legacy_index)
        except (OSError, json.JSONDecodeError) as exc:
            emit("preflight_failed", check="load_legacy_index", detail=str(exc))
            return EXIT_PREFLIGHT
        index_errors = validate_legacy_index(index_payload)
        if index_errors:
            errors.extend(index_errors)
            exit_code = max(exit_code, EXIT_PREFLIGHT)
            emit("preflight_failed", check="legacy_index", detail=index_errors)
        else:
            emit("preflight_passed", check="legacy_index")

    hash_pairs: list[tuple[Path, str]] = []
    for item in args.hash:
        if "=" not in item:
            errors.append(f"invalid --hash value: {item}")
            exit_code = max(exit_code, EXIT_PREFLIGHT)
            continue
        raw_path, expected = item.split("=", 1)
        hash_pairs.append((Path(raw_path), expected.strip().lower()))
    hash_errors = check_hashes(hash_pairs)
    if hash_errors:
        errors.extend(hash_errors)
        exit_code = max(exit_code, EXIT_INTEGRITY)
        emit("artifact_mismatch", detail=hash_errors)
    elif hash_pairs:
        emit("artifact_verified", count=len(hash_pairs))

    if args.require_clean:
        git_dir = Path(".git")
        if not git_dir.exists():
            emit("preflight_failed", check="clean_worktree", detail="not a git checkout")
            exit_code = max(exit_code, EXIT_PREFLIGHT)
        else:
            emit("preflight_passed", check="clean_worktree_flag_recorded")

    status = "PASS" if exit_code == EXIT_OK else "FAIL"
    decision = "ALLOW_INTERNAL" if exit_code == EXIT_OK else "BLOCK_RELEASE"
    emit(
        "run_finished",
        status=status,
        policy_decision=decision,
        exit_code=exit_code,
        error_count=len(errors),
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
