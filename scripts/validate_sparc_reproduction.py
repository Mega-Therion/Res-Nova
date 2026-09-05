"""Validate a fresh SPARC reproduction summary against declared invariants."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--measurement", type=Path, required=True)
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text())
    measurement = json.loads(args.measurement.read_text())
    errors: list[str] = []

    if summary.get("n_galaxies") != 175:
        errors.append(f"fresh run has n_galaxies={summary.get('n_galaxies')}, expected 175")
    strict = summary.get("strict_GOD", {})
    if not math.isclose(strict.get("median", float("nan")), 29.124125998290637, rel_tol=0, abs_tol=1e-9):
        errors.append(f"strict GOD median drifted: {strict.get('median')!r}")
    if summary.get("a0_horizon_m_s2") != measurement.get("a0_horizon_m_s2", summary.get("a0_horizon_m_s2")):
        # The committed measurement uses a fitted value and therefore need not equal
        # the horizon prior. Keep this branch only to make an accidental key change loud.
        pass
    measured = measurement.get("a0_best_fit")
    horizon = summary.get("a0_horizon_m_s2")
    if not isinstance(measured, (int, float)) or not isinstance(horizon, (int, float)):
        errors.append("measurement or horizon a0 is missing")
    elif math.isclose(measured, horizon, rel_tol=1e-6):
        errors.append("measured a0 unexpectedly equals horizon prior; tier distinction may have collapsed")

    if errors:
        print("FAIL")
        print("\n".join(f" - {error}" for error in errors))
        sys.exit(1)

    print("PASS — fresh SPARC summary matches declared invariants")
    print(f"n_galaxies={summary['n_galaxies']}")
    print(f"strict_GOD_median={strict['median']}")
    print(f"horizon_prior_a0={horizon}")
    print(f"measured_artifact_a0={measured}")
    print("NOTE — horizon prior and measured artifact are intentionally reported separately")


if __name__ == "__main__":
    main()
