#!/usr/bin/env python3
"""
Cassini Q2 Layer 1b Milky Way External-Field (g_e) & a0-Convention Uncertainty Band (2026-11-19).

Uses the repo's independent axisymmetric QUMOND PDE solver (02_galaxy_dynamics/qumond_axisym_efe.py)
to propagate realistic astrophysical uncertainty in the Solar System's local Milky Way
external field g_e in [1.5, 2.3]e-10 m/s^2 (+/-21%, covering V_0 in [210, 250] km/s,
R_0 in [7.9, 8.5] kpc) across all three live a0 conventions:
  - Derived horizon anchor: c*H0/(2*pi) = 1.0422e-10 m/s^2 (H0=67.4)
  - SPARC S2 distance-corrected (real e_D/D): 1.1205e-10 m/s^2
  - SPARC legacy T1 (2026-09-16): 1.1607e-10 m/s^2

Compares every (a0, g_e) cell against Park et al. (2026), arXiv:2602.17884, Phys. Rev. D:
  Q2_Park = (1.6 +/- 1.8)e-27 s^-2   (DE440 + full Cassini tracking through Aug 2017).

Run: python3 audits/2026-11-19/cassini_ge_uncertainty_band.py   (exit 0, deterministic)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "02_galaxy_dynamics"))
import qumond_axisym_efe as qe  # noqa: E402

OUT = Path(__file__).resolve().parent / "CASSINI_GE_UNCERTAINTY_BAND.json"

Q2_PARK_MEAN = 1.6e-27
Q2_PARK_SIG = 1.8e-27
Q2_HEES_MEAN = 3.0e-27
Q2_HEES_SIG = 3.0e-27

A0_BASES = [
    ("derived_cH0_2pi", qe.A0_DERIVED),
    ("sparc_S2_real_eD", 1.1205e-10),
    ("sparc_T1_legacy", qe.A0_FIT),
]
GE_GRID = [1.5e-10, 1.7e-10, 1.9e-10, 2.1e-10, 2.3e-10]


def main() -> int:
    nu = qe.nu_n(2)  # exact inverse of live mu_std(x) = x / sqrt(1 + x^2)
    rows = []

    print("=" * 94)
    print("CASSINI Q2 LAYER 1b SENSITIVITY BAND: g_e in [1.5, 2.3]e-10 x 3 a0 CONVENTIONS (mu_std)")
    print("Benchmark: Park et al. (2026) arXiv:2602.17884 Q2 = (1.6 +/- 1.8)e-27 s^-2")
    print("=" * 94)
    print(f"{'a0 basis':<18} {'a0':>10} {'g_e':>10} {'eta=ge/a0':>10} {'Q2 [1e-27]':>12} {'err [1e-27]':>12} {'Park sigma':>11} {'Hees sigma':>11}")
    print("-" * 94)

    min_park_sig = 1e9
    max_park_sig = -1e9
    for label, a0 in A0_BASES:
        for ge in GE_GRID:
            q_ext, q_fine, q_err = qe.Q2_richardson(nu, a0, ge, n_r=1000, n_th=200)
            sig_park = (q_ext - Q2_PARK_MEAN) / Q2_PARK_SIG
            sig_hees = (q_ext - Q2_HEES_MEAN) / Q2_HEES_SIG
            min_park_sig = min(min_park_sig, sig_park)
            max_park_sig = max(max_park_sig, sig_park)
            print(f"{label:<18} {a0:10.4e} {ge:10.2e} {ge/a0:10.3f} {q_ext*1e27:12.3f} {q_err*1e27:12.4f} {sig_park:+11.2f} {sig_hees:+11.2f}")
            rows.append({
                "a0_label": label,
                "a0_mps2": a0,
                "ge_mps2": ge,
                "eta": round(ge / a0, 4),
                "Q2_extrap_s2": q_ext,
                "Q2_fine_s2": q_fine,
                "Q2_richardson_err_s2": q_err,
                "Q2_1e27": round(q_ext * 1e27, 4),
                "sigma_Park2026": round(sig_park, 3),
                "sigma_Hees2014_superseded": round(sig_hees, 3),
            })

    print("-" * 94)
    print(f"Park et al. (2026) exclusion across ENTIRE (+/-21% g_e x all 3 a0 bases) box: "
          f"+{min_park_sig:.2f} sigma to +{max_park_sig:.2f} sigma")

    # Even the most favorable corner (lowest a0, highest/lowest g_e) must still strongly exclude bare mu_std
    assert min_park_sig > 5.0, f"Unexpected low exclusion: {min_park_sig}"

    report = {
        "generated": "2026-11-19",
        "epistemic_tag": "[D] / [E]",
        "solver": "02_galaxy_dynamics/qumond_axisym_efe.py (axisymmetric QUMOND PDE, Richardson extrapolated)",
        "benchmark_Park2026": {
            "citation": "Park, Hees, Famaey, Desmond, Durakovic 2026, arXiv:2602.17884, Phys. Rev. D",
            "Q2_mean_s2": Q2_PARK_MEAN,
            "Q2_sigma_s2": Q2_PARK_SIG,
        },
        "grid": rows,
        "summary": {
            "min_exclusion_sigma_Park2026": round(min_park_sig, 3),
            "max_exclusion_sigma_Park2026": round(max_park_sig, 3),
            "verdict": (
                f"Bare unscreened mu_std QUMOND is excluded by Park et al. (2026) at "
                f"+{min_park_sig:.2f} to +{max_park_sig:.2f} sigma across the entire +/-21% "
                "Milky Way external-field uncertainty band and all three a0 conventions. "
                "Forward-model / astrophysical environment uncertainty cannot rescue bare mu_std."
            ),
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
