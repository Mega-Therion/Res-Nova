#!/usr/bin/env python3
"""O6 clean-worktree runner.

Seals a public receipt, then optionally notifies a local AEON observer.
A PASS is clean-worktree evidence only. promotion_allowed stays false.
Observer failure does not change the Res-Nova verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = ROOT / "reproducibility" / "profiles" / "o6-lean-clean-worktree.json"
SORRY = ROOT / "scripts" / "repro" / "check_sorry.py"

EXIT_OK = 0
EXIT_PREFLIGHT = 10
EXIT_INTEGRITY = 20
EXIT_PROOF = 30
EXIT_DRIFT = 50
EXIT_INFRA = 60
CASE_STATUSES = {"FAIL", "BLOCKED", "INFRA_ERROR", "QUARANTINED", "INCONCLUSIVE"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def seal(receipt: dict[str, Any]) -> dict[str, Any]:
    body = {key: value for key, value in receipt.items() if key != "integrity"}
    digest = hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()
    body["integrity"] = {"receipt_sha256": digest, "canonicalization": "sha256-json-sort-keys-separators"}
    return body


def emit(events: list[dict[str, Any]], event: str, **fields: Any) -> None:
    events.append({"event": event, "at_utc": utc_now(), **fields})


def git_dirty(worktree: Path) -> bool:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
    )
    return bool(proc.stdout.strip()) or proc.returncode != 0


def write_incident(run_dir: Path, run_id: str, failure_class: str, summary: str) -> None:
    incident = {
        "schema_version": "res-nova-incident-v1",
        "incident_id": f"INC-{run_id}",
        "run_id": run_id,
        "severity": "S1",
        "failure_class": failure_class,
        "promotion_blocked": True,
        "summary": summary,
    }
    path = ROOT / "reproducibility" / "incidents" / f"INC-{run_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(incident, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "incident.json").write_text(json.dumps(incident, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def notify_observer(receipt_path: Path, events: list[dict[str, Any]]) -> None:
    observer = os.environ.get("AEON_RES_NOVA_OBSERVER")
    if not observer:
        emit(events, "observer_skipped", reason="AEON_RES_NOVA_OBSERVER unset")
        return
    try:
        proc = subprocess.run(
            [observer, "--receipt", str(receipt_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        emit(
            events,
            "observer_finished",
            exit_code=proc.returncode,
            status="notified" if proc.returncode == 0 else "observer_unavailable",
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        emit(events, "observer_unavailable", detail=str(exc))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the sealed O6 clean-worktree profile")
    parser.add_argument("--worktree-dir", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--skip-lake", action="store_true")
    args = parser.parse_args()
    worktree = args.worktree_dir.resolve()
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    run_id = f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:10]}"
    run_dir = ROOT / "reproducibility" / "runs" / datetime.now(timezone.utc).strftime("%Y") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    events: list[dict[str, Any]] = []
    emit(events, "run_started", run_id=run_id, profile=profile["profile_id"], mode=profile["mode"])

    status = "PASS"
    exit_code = EXIT_OK
    failure_class = None
    steps: list[dict[str, Any]] = []
    input_lock = {"files": []}

    if profile.get("repository_clean_required") and not args.allow_dirty and git_dirty(worktree):
        status, exit_code, failure_class = "BLOCKED", EXIT_PREFLIGHT, "POLICY_CONFLICT"
        emit(events, "preflight_failed", check="clean_worktree")
    else:
        emit(events, "preflight_passed", check="clean_worktree_or_allowed")

    for rel in profile.get("checked_inputs") or []:
        path = worktree / rel
        if not path.is_file():
            status, exit_code, failure_class = "FAIL", EXIT_INTEGRITY, "ARTIFACT_INTEGRITY"
            emit(events, "artifact_mismatch", path=rel, detail="missing")
            steps.append({"step_id": f"input:{rel}", "status": "FAIL", "failure_class": "ARTIFACT_INTEGRITY"})
            continue
        digest = sha256_file(path)
        input_lock["files"].append({"path": rel, "sha256": digest})
        emit(events, "artifact_verified", path=rel, sha256=digest)

    toolchain = worktree / "05_lean_formalization" / "lean-toolchain"
    if not toolchain.is_file() and status == "PASS" and not args.dry_run:
        status, exit_code, failure_class = "FAIL", EXIT_DRIFT, "DEPENDENCY_DRIFT"
        emit(events, "preflight_failed", check="toolchain")

    if status == "PASS":
        sorry = subprocess.run(
            [sys.executable, str(SORRY), "--root", str(worktree / "05_lean_formalization")],
            check=False,
            capture_output=True,
            text=True,
        )
        steps.append({"step_id": "verify-proof-hygiene", "exit_code": sorry.returncode, "status": "PASS" if sorry.returncode == 0 else "FAIL"})
        if sorry.returncode != 0:
            status, exit_code, failure_class = "FAIL", EXIT_PROOF, "PROOF_PLACEHOLDER"
            emit(events, "verdict_emitted", verifier="lean_hygiene", verdict="FAIL")
        else:
            emit(events, "verdict_emitted", verifier="lean_hygiene", verdict="PASS")

    if status == "PASS" and not args.dry_run and not args.skip_lake:
        lake = shutil.which("lake")
        if not lake:
            status, exit_code, failure_class = "FAIL", EXIT_DRIFT, "DEPENDENCY_DRIFT"
            emit(events, "preflight_failed", check="lake_missing")
        else:
            built = subprocess.run(
                [lake, "build"],
                cwd=worktree / "05_lean_formalization",
                check=False,
                capture_output=True,
                text=True,
            )
            steps.append({"step_id": "lake-build", "exit_code": built.returncode, "status": "PASS" if built.returncode == 0 else "FAIL"})
            if built.returncode != 0:
                status, exit_code, failure_class = "FAIL", EXIT_PROOF, "PROOF_FAILURE"

    if args.dry_run and status == "PASS":
        emit(events, "dry_run_complete")

    receipt = {
        "schema_version": "res-nova-repro-run-v1",
        "run_id": run_id,
        "requested_at_utc": utc_now(),
        "started_at_utc": utc_now(),
        "finished_at_utc": utc_now(),
        "profile_id": profile["profile_id"],
        "mode": profile["mode"],
        "target": {
            "repository": "Mega-Therion/Res-Nova",
            "working_tree_clean": not git_dirty(worktree),
            "claim_ids": profile.get("claim_ids") or ["O6"],
        },
        "inputs": input_lock,
        "steps": steps,
        "result": {
            "status": status,
            "policy_decision": "BLOCK_RELEASE",
            "claim_status_changes": [],
            "summary": "O6 remains [O]; promotion blocked for independent replication.",
        },
        "promotion_allowed": False,
        "environment": {"isolation": "clean-worktree", "network_policy": profile.get("network_policy", "recorded")},
    }
    sealed = seal(receipt)
    receipt_path = run_dir / "public_receipt.json"
    receipt_path.write_text(json.dumps(sealed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "inputs.lock.json").write_text(json.dumps(input_lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "result.json").write_text(json.dumps(sealed["result"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "report.md").write_text(
        f"# {run_id}\n\nstatus: {status}\nmode: clean_worktree\npromotion_allowed: false\npolicy: BLOCK_RELEASE\n",
        encoding="utf-8",
    )
    if status in CASE_STATUSES and failure_class:
        write_incident(run_dir, run_id, failure_class, sealed["result"]["summary"])
        emit(events, "incident_created", incident_id=f"INC-{run_id}", severity="S1")
    emit(events, "run_finished", status=status, decision="BLOCK_RELEASE", receipt_digest=sealed["integrity"]["receipt_sha256"])
    (run_dir / "events.ndjson").write_text("\n".join(json.dumps(item, sort_keys=True) for item in events) + "\n", encoding="utf-8")
    notify_observer(receipt_path, events)
    (run_dir / "events.ndjson").write_text("\n".join(json.dumps(item, sort_keys=True) for item in events) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": run_id, "status": status, "receipt": str(receipt_path), "exit_code": exit_code}, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
