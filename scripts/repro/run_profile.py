#!/usr/bin/env python3
"""Run a declared reproducibility profile and emit a public-safe envelope.

Does not change claim status. O6 remains [O] even on PASS.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {"steps": [], "verifiers": [], "required_outputs": [], "claim_ids": []}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current:
            item = raw[4:].strip()
            if ": " in item:
                key, value = item.split(": ", 1)
                if current == "steps" and key == "id":
                    data["steps"].append({"id": value.strip()})
                elif current == "steps" and data["steps"]:
                    data["steps"][-1][key] = _scalar(value)
                elif current == "verifiers" and key == "kind":
                    data["verifiers"].append({"kind": value.strip()})
                elif current == "verifiers" and data["verifiers"]:
                    data["verifiers"][-1][key] = _scalar(value)
            elif current == "required_outputs":
                data["required_outputs"].append(item.strip())
            elif current == "claim_ids":
                data["claim_ids"].append(item.strip().strip(","))
            continue
        if raw.startswith("  ") and current == "steps" and data["steps"] and ": " in raw:
            key, value = raw.strip().split(": ", 1)
            data["steps"][-1][key] = _scalar(value)
            continue
        if ":" in raw and not raw.startswith(" "):
            key, value = raw.split(":", 1)
            current = key.strip() if value.strip() in {"", "|"} or value.strip().startswith("[") else None
            if value.strip().startswith("[") and value.strip().endswith("]"):
                inner = value.strip()[1:-1]
                data[key.strip()] = [part.strip() for part in inner.split(",") if part.strip()]
                current = None
            elif value.strip():
                data[key.strip()] = _scalar(value)
                current = None
            else:
                current = key.strip()
    return data


def _scalar(value: str) -> Any:
    text = value.strip().strip('"')
    if text in {"true", "false"}:
        return text == "true"
    if text.isdigit():
        return int(text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a Res-Nova reproducibility profile")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    profile = parse_simple_yaml(args.profile)
    run_id = f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    steps_out: list[dict[str, Any]] = []
    status = "PASS"
    exit_code = 0

    for required in profile.get("required_outputs") or []:
        path = ROOT / required
        if not path.is_file():
            status = "FAIL"
            exit_code = 20
            steps_out.append({"step_id": f"required:{required}", "status": "FAIL", "failure_class": "ARTIFACT_INTEGRITY"})

    if not args.dry_run:
        for step in profile.get("steps") or []:
            command = step.get("command")
            if not command:
                continue
            proc = subprocess.run(command, shell=True, cwd=ROOT, check=False, capture_output=True, text=True)
            step_status = "PASS" if proc.returncode == 0 else "FAIL"
            if step_status == "FAIL":
                status = "FAIL"
                exit_code = proc.returncode or 30
            steps_out.append(
                {
                    "step_id": step.get("id"),
                    "kind": "command",
                    "exit_code": proc.returncode,
                    "status": step_status,
                    "stdout_sha256": hashlib.sha256((proc.stdout or "").encode()).hexdigest(),
                    "stderr_sha256": hashlib.sha256((proc.stderr or "").encode()).hexdigest(),
                }
            )

    envelope = {
        "schema_version": "res-nova-repro-run-v1",
        "run_id": run_id,
        "requested_at_utc": utc_now(),
        "started_at_utc": utc_now(),
        "finished_at_utc": utc_now(),
        "profile_id": profile.get("profile_id", args.profile.stem),
        "mode": profile.get("mode", "static_preflight"),
        "target": {
            "repository": "Mega-Therion/Res-Nova",
            "claim_ids": profile.get("claim_ids") or ["O6"],
            "working_tree_clean": None,
        },
        "result": {
            "status": status,
            "policy_decision": "BLOCK_RELEASE",
            "claim_status_changes": [],
            "summary": "O6 remains [O]; promotion blocked for independent replication.",
        },
        "steps": steps_out,
        "environment": {"isolation": profile.get("mode", "clean_worktree"), "network_policy": profile.get("network_policy", "recorded")},
    }
    encoded = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode()
    envelope["integrity"] = {"receipt_sha256": hashlib.sha256(encoded).hexdigest()}
    text = json.dumps(envelope, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return exit_code if not args.dry_run else 0


if __name__ == "__main__":
    raise SystemExit(main())
