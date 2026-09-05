"""Generate a compact machine-readable assurance report for Res-Nova."""
from __future__ import annotations

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


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    claims = registry["claims"]
    target_checker = command("python3", "05_lean_formalization/check_target_inventory.py")
    manuscript_checker = command("python3", "05_lean_formalization/check_manuscript_inventory.py")
    claim_checker = command("python3", "scripts/check_claim_consistency.py")
    report = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": command("git", "rev-parse", "HEAD"),
        "git_branch": command("git", "branch", "--show-current"),
        "lean_target_count": len(list((ROOT / "05_lean_formalization").glob("*.lean"))) - 1,
        "claim_count": len(claims),
        "claim_states": {state: sum(c["state"] == state for c in claims) for state in sorted({c["state"] for c in claims})},
        "checks": {
            "claim_registry": "PASS" if command("python3", "scripts/validate_claim_registry.py").startswith("PASS") else "FAIL",
            "claim_consistency": "PASS" if claim_checker.startswith("PASS") else "FAIL",
            "lean_target_inventory": "PASS" if target_checker.startswith("PASS") else "FAIL",
            "manuscript_inventory": "PASS" if manuscript_checker.startswith("OK") else "FAIL",
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
    lines += ["", "## Limitations", ""]
    lines.extend(f"- {item}" for item in report["limitations"])
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"PASS — wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
