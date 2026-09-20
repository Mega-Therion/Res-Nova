#!/usr/bin/env python3
"""CURRENT_STATE_READ_THIS_FIRST.md must not be older than the physics.

It used to pin a specific commit SHA. That was unmaintainable: every
documentation commit moved HEAD, so the pin was stale seconds after it was
written and nobody could tell a real drift from the usual noise. A pin that is
always wrong is not a check.

The invariant that actually matters: if a PHYSICS surface changed after the
date CURRENT_STATE claims to have been verified, the file is stale and says so
with authority it has not earned. Documentation, scripts and tooling churn do
not trip this -- only the surfaces whose change would alter what the state file
asserts.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "CURRENT_STATE_READ_THIS_FIRST.md"

# Changing any of these can change what CURRENT_STATE asserts.
PHYSICS_PATHS = [
    "05_lean_formalization",
    "res_nova_manuscript.tex",
    "PEER_REVIEW_READINESS.md",
    "TARGET_D1_VARIATIONAL_DERIVATION.md",
    "TARGET_D2_PHYSICAL_ACTION_DERIVATION.md",
    "TARGET_D3_PPN_AND_SOLAR_SYSTEM.md",
    "TARGET_D5_COSMOLOGICAL_SECTOR.md",
    "TARGET_D7_COVARIANT_COMPLETION.md",
    "TARGET_D9_SKORDIS_ZLOSNIK_EMBEDDING.md",
]

DATE_RE = re.compile(r"\*\*Last verified against the physics:\*\*\s*(\d{4}-\d{2}-\d{2})")


def verified_date(text: str):
    m = DATE_RE.search(text)
    return date.fromisoformat(m.group(1)) if m else None


def newest_physics_change() -> tuple[str, str] | None:
    """(iso date, path) of the most recent commit touching a physics surface."""
    newest = None
    for p in PHYSICS_PATHS:
        r = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--", p],
            capture_output=True, text=True)
        d = r.stdout.strip()
        if d and (newest is None or d > newest[0]):
            newest = (d, p)
    return newest


def check() -> int:
    if not STATE.exists():
        print("current-state freshness: FAIL -- file missing")
        return 1
    text = STATE.read_text(encoding="utf-8")
    vd = verified_date(text)
    if vd is None:
        print("current-state freshness: FAIL -- no '**Last verified against "
              "the physics:** YYYY-MM-DD' line found")
        return 1
    if vd > date.today():
        print(f"current-state freshness: FAIL -- verified date {vd} is in the future")
        return 1
    newest = newest_physics_change()
    if newest and newest[0] > vd.isoformat():
        print(f"current-state freshness: FAIL -- physics changed {newest[0]} "
              f"({newest[1]}) but CURRENT_STATE was last verified {vd}.")
        print("  Re-read PEER_REVIEW_READINESS.md, update the state file, then "
              "set the date to today.")
        return 1
    tail = f"; newest physics change {newest[0]} ({newest[1]})" if newest else ""
    print(f"current-state freshness: PASS (verified {vd}{tail})")
    return 0


def self_test() -> int:
    """The check must fire when physics postdates the claim, and not otherwise."""
    today = date.today().isoformat()
    cases = [
        ("**Last verified against the physics:** 2026-01-01", "2030-01-01", True),
        (f"**Last verified against the physics:** {today}", "2020-01-01", False),
        ("no date line at all", None, True),
    ]
    bad = 0
    for text, newest, should_fail in cases:
        vd = verified_date(text)
        if vd is None:
            fired = True
        else:
            fired = newest is not None and newest > vd.isoformat()
        if fired != should_fail:
            print(f"  self-test MISMATCH: {text[:44]!r} newest={newest} "
                  f"fired={fired} expected={should_fail}")
            bad += 1
    print(f"current_state_freshness self-test: {'PASS' if not bad else 'FAIL'} "
          f"({len(cases)} cases)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else check())
