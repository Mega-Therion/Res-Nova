"""Generate a compact machine-readable assurance report for Res-Nova."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assurance" / "claims.json"
OUT_JSON = ROOT / "assurance" / "ASSURANCE_REPORT.json"
OUT_MD = ROOT / "assurance" / "ASSURANCE_REPORT.md"


def command(*args: str) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def check(*args: str) -> str:
    """PASS iff the checker exits 0.

    The previous version tested whether stdout *started with* "OK" or "PASS".
    check_manuscript_inventory.py prints one line per section, so its output
    begins "OK    adjacency manifest" even on a run that goes on to fail and
    exit 1 -- this report would have printed PASS for a failing check. An exit
    code is a fact; a string prefix is a guess about formatting.
    """
    try:
        return "PASS" if subprocess.run(args, cwd=ROOT, capture_output=True).returncode == 0 else "FAIL"
    except OSError:
        return "UNAVAILABLE"


def lean_digest() -> str:
    """SHA-256 over the on-disk sources the gate actually reads.

    Not `git rev-parse HEAD:05_lean_formalization` -- that reads the committed
    tree, so an uncommitted edit to a .lean file left the record looking fresh.
    That is precisely the failure mode this session was spent reverting: an
    uncommitted working-tree change to the gate. Hash what is on disk.
    """
    directory = ROOT / "05_lean_formalization"
    names = ["lakefile.lean", "lean-toolchain", "verify_all_proofs.sh"]
    paths = sorted(directory.glob("*.lean")) + [directory / n for n in names]
    digest = hashlib.sha256()
    for path in sorted(set(paths)):
        if not path.is_file():
            continue
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def gate_record() -> dict | None:
    """Read the recorded Lean gate run. Never runs the gate (~12 min).

    A recorded PASS is only evidence for the commit it was run at, so a record
    from an older commit is reported as STALE rather than reused.
    """
    path = ROOT / "assurance" / "LEAN_GATE_RUN.json"
    if not path.is_file():
        return None
    rec = json.loads(path.read_text())
    # Staleness is keyed on the tree hash of 05_lean_formalization/, not on HEAD.
    # A commit that only touches assurance docs cannot invalidate a Lean run, and
    # keying on HEAD would mark every record stale the moment it was committed.
    # Any edit to a .lean file, the lakefile, or the gate script changes this hash.
    rec["lean_tree"] = lean_digest()
    rec["stale"] = rec.get("lean_tree_at_run") != rec["lean_tree"]
    return rec


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    claims = registry["claims"]
    report = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": command("git", "rev-parse", "HEAD"),
        "git_branch": command("git", "branch", "--show-current"),
        "lean_target_count": len(list((ROOT / "05_lean_formalization").glob("*.lean"))) - 1,
        "claim_count": len(claims),
        "claim_states": {state: sum(c["state"] == state for c in claims) for state in sorted({c["state"] for c in claims})},
        "lean_gate": gate_record(),
        "checks": {
            "claim_registry": check("python3", "scripts/validate_claim_registry.py"),
            "claim_consistency": check("python3", "scripts/check_claim_consistency.py"),
            "lean_target_inventory": check("python3", "05_lean_formalization/check_target_inventory.py"),
            "manuscript_inventory": check("python3", "05_lean_formalization/check_manuscript_inventory.py"),
        },
        "limitations": [
            "Lean verification certifies elaboration under encoded hypotheses, not physical truth.",
            "The report does not claim cold-cache CI reproducibility until that release gate is independently demonstrated.",
            "The current registry is an initial publication-critical subset and must grow before publication-grade scope is claimed.",
        ],
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")
    lines = [
        "# Res-Nova Assurance Report",
        "",
        f"Generated at (UTC): `{report['generated_at_utc']}`  ",
        f"Git commit: `{report['git_commit']}`  ",
        f"Lean targets on disk excluding `lakefile.lean`: **{report['lean_target_count']}**  ",
        f"Registry records: **{report['claim_count']}**",
        "",
        "## Checks",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for name, status in report["checks"].items():
        lines.append(f"| `{name}` | **{status}** |")
    lines += ["", "## Claim states", "", "| State | Count |", "|---|---:|"]
    for state, count in report["claim_states"].items():
        lines.append(f"| `{state}` | {count} |")
    gate = report.get("lean_gate")
    lines += ["", "## Lean gate", ""]
    if not gate:
        lines += ["No recorded run. `assurance/LEAN_GATE_RUN.json` is absent."]
    elif gate.get("stale"):
        lines += [
            f"**STALE** — `05_lean_formalization/` has changed since the last "
            f"recorded run (tree `{gate.get('lean_tree_at_run')}` then, "
            f"`{gate['lean_tree']}` now). Rerun the gate; a previous PASS is "
            "evidence only for the sources it was run against.",
        ]
    else:
        lines += [
            f"`{gate['command']}` exited **{gate['exit_code']}** at `{gate['commit']}` "
            f"({gate['run_at_utc']}), {gate['targets_passed']}/{gate['targets_declared']} targets, "
            f"Lean {gate['lean']}, Mathlib {gate['mathlib']}.",
            "",
            f"Certifies: {gate['certifies']}.",
            "",
            f"Does not certify: {gate['does_not_certify']}.",
        ]
    lines += ["", "## Limitations", ""]
    lines.extend(f"- {item}" for item in report["limitations"])
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"PASS — wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
