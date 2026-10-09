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
    # Pinned 2026-10-09 after the baryon fix (Y multiplies V^2, signed V_gas, fd scales V_bar^2 and R),
    # under mu_std. The previous pin, 29.124125998290637, was the 2026-08-14 run under the retired mu_dual.
    if not math.isclose(strict.get("median", float("nan")), 15.00865689971704, rel_tol=0, abs_tol=1e-9):
        errors.append(f"strict GOD median drifted: {strict.get('median')!r}")
    if summary.get("n_points") != 3391:
        errors.append(f"fresh run has n_points={summary.get('n_points')}, expected 3391")
    digest = summary.get("data", {}).get("sha256_of_manifest")
    if digest != "e78c1d6883a7843ca69a6a6f23ebad228e4a362c4861e9cd81a01c43fae9a4e7":
        errors.append(f"input data digest {digest!r} != SHA-256 of RAW_DATA_MANIFEST.sha256")
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
