#!/usr/bin/env python3
"""Regression & fail-closed guard tests for the 3-Layer Forward-Model Audit (2026-11-19).

Verifies:
  1. Layer 3 fail-closed quarantine: 03_observer_jwst/a0_of_z.py and a0_of_z_v2.py
     refuse default execution of the withdrawn 20-row table with exit code 2.
  2. Layer 3 forensic override: both scripts still run cleanly if --allow-withdrawn-archive
     is passed explicitly (writing only to a throwaway temp path).
  3. Layer 1b SPARC distance-scaling parity: 02_galaxy_dynamics/test_sparc_parser.py
     exits 0 (g_bar invariance across FD, T2 R & V_bar rescaling, cross-module parity).
  4. Layer 2/3 witness receipt: scripts/verify_mu_std_cassini_and_limits.py cites
     Park et al. (2026) (arXiv:2602.17884) rather than only superseded Hees (2014).

Run: python3 tests/test_forward_model_guards.py   (exit 0 on PASS)
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def test_a0_of_z_fail_closed() -> None:
    for script in ("03_observer_jwst/a0_of_z.py", "03_observer_jwst/a0_of_z_v2.py"):
        r = run_cmd([sys.executable, script])
        assert r.returncode == 2, f"{script} must fail closed with exit 2, got {r.returncode}: {r.stdout} {r.stderr}"
        assert "WITHDRAWN" in r.stderr, f"{script} stderr should explain withdrawal: {r.stderr}"


def test_a0_of_z_explicit_archive_override() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out1 = Path(tmp) / "v1.json"
        r1 = run_cmd([sys.executable, "03_observer_jwst/a0_of_z.py", "--allow-withdrawn-archive", "--out", str(out1)])
        assert r1.returncode == 0, f"v1 override failed: {r1.stderr}"
        assert out1.is_file()

        out2 = Path(tmp) / "v2.json"
        r2 = run_cmd([sys.executable, "03_observer_jwst/a0_of_z_v2.py", "--allow-withdrawn-archive", "--out", str(out2)])
        assert r2.returncode == 0, f"v2 override failed: {r2.stderr}"
        assert out2.is_file()


def test_sparc_distance_invariance_suite() -> None:
    r = run_cmd([sys.executable, "02_galaxy_dynamics/test_sparc_parser.py"])
    assert r.returncode == 0, f"test_sparc_parser failed: {r.stdout}\n{r.stderr}"
    assert "T2 g_bar invariance" in r.stdout


def test_cassini_receipt_park2026() -> None:
    receipt = json.loads((ROOT / "scripts/repro/cassini_clearance_receipt.json").read_text(encoding="utf-8"))
    scope = receipt["saturn_monopole"]["scope"]
    assert "Park et al. (2026" in scope and "2602.17884" in scope, f"Stale Cassini scope: {scope}"
    assert "superseding Hees" in scope, f"Hees 2014 must be marked superseded: {scope}"


def main() -> int:
    tests = [
        test_a0_of_z_fail_closed,
        test_a0_of_z_explicit_archive_override,
        test_sparc_distance_invariance_suite,
        test_cassini_receipt_park2026,
    ]
    for fn in tests:
        fn()
        print(f"PASS: {fn.__name__}")
    print(f"\nALL {len(tests)}/{len(tests)} FORWARD-MODEL GUARD TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
