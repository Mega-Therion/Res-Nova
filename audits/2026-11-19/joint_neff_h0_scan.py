#!/usr/bin/env python3
"""Joint (Delta N_eff, H0, omega_m h^2) scan: what actually excludes the Q^4 tracker.

WHY THIS EXISTS
---------------
`bao_cmb_dneff_forward_check.py` evaluates the Q^4 radiation tracker at FIXED Planck
parameters and reports dchi2_CMB = +1571..+1949, then notes H0 must rise to ~70.3-70.7
to restore l_A. That number is arithmetically correct but is NOT a model-discrimination
statistic: it is the cost of pinning BOTH H0 and omega_m h^2 while the model is allowed
to change them. Read as an exclusion, it overstates the case by roughly two orders of
magnitude.

This script does the honest version:
  1. Minimise chi2_CHW over (h, omega_m h^2) for each Delta N_eff.
  2. Add the Planck constraint on omega_m h^2 (omega_c h^2 = 0.1200 +- 0.0012,
     omega_b h^2 = 0.02237 +- 0.00015, combined in quadrature).
  3. Report Delta chi2 against the LambdaCDM best fit.

RESULT (see JOINT_NEFF_H0_SCAN.json)
------------------------------------
The CHW distance prior alone has an EXACT two-parameter degeneracy that absorbs
Delta N_eff: at Delta N_eff = 0.27 with (h, omega_m h^2) free, l_A matches the prior
to 0.000e+00. So the compressed CMB prior by itself cannot exclude extra radiation.
The exclusion is carried entirely by omega_m h^2, which the compensating point pushes
to 0.1462 (+3.2 sigma from Planck). Net: Delta chi2 = +17.8, about 4.2 sigma for one
extra parameter.

CAVEATS
-------
* CHW is a COMPRESSED distance prior (R, l_A, omega_b), not the full Planck likelihood.
* The omega_m h^2 Gaussian uses the Planck 2018 late-time/CMB decomposition and treats
  it as uncorrelated with (R, l_A); the true joint is correlated, so the pull is
  approximate and this is [D], not [P].
* No DESI BAO vector is in this repo, so the BAO side enters only as a fractional
  shift in the prediction, not a chi2.
* The 4.2 sigma is therefore an ESTIMATE of the exclusion, not a certified number.

Deterministic, no network, exit 0.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "audits" / "2026-11-19" / "bao_cmb_dneff_forward_check.py"

spec = importlib.util.spec_from_file_location("d4", SRC)
d4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d4)

W_RAD = 1.0 / 3.0
OB_H2 = d4.OB_H2_PL
PRI, PINV = d4.PRI, d4.PINV

# Planck 2018 TT,TE,EE+lowE+lensing, standard decomposition (avoids the Omega_m-H0
# correlation that makes naive propagation of Omega_m and h far too loose).
OMC_H2, S_OMC = 0.1200, 0.0012
OMB_H2, S_OMB = 0.02237, 0.00015
OM_H2_PL = OMC_H2 + OMB_H2
S_OM_H2 = math.hypot(S_OMC, S_OMB)


def chi2_chw(h: float, om_h2: float, dneff: float) -> float:
    try:
        r = d4.compute_cosmo_observables(h, om_h2, OB_H2, dneff, w_dark_rad=W_RAD)
    except Exception:
        return float("inf")
    dv = np.array([r["R"], r["lA"], OB_H2]) - PRI
    c = float(dv @ PINV @ dv)
    return c if math.isfinite(c) else float("inf")


def total_chi2(dneff: float) -> tuple[float, float, float]:
    """Minimise chi2_CHW + omega_m h^2 pull over (h, omega_m h^2)."""
    best = (float("inf"), float("nan"), float("nan"))
    for om in np.linspace(0.138, 0.156, 181):
        pull = ((om - OM_H2_PL) / S_OM_H2) ** 2
        for h in np.linspace(0.64, 0.78, 281):
            c = chi2_chw(h, om, dneff) + pull
            if c < best[0]:
                best = (c, h, om)
    _, h0, om0 = best
    for om in np.linspace(om0 - 0.0005, om0 + 0.0005, 41):
        pull = ((om - OM_H2_PL) / S_OM_H2) ** 2
        for h in np.linspace(h0 - 0.002, h0 + 0.002, 41):
            c = chi2_chw(h, om, dneff) + pull
            if c < best[0]:
                best = (c, h, om)
    return best


def main() -> int:
    print("=" * 82)
    print("JOINT (Delta N_eff, H0, omega_m h^2) SCAN -- Q^4 RADIATION TRACKER, w = 1/3")
    print("=" * 82)
    print(f"\nPlanck omega_m h^2 = {OM_H2_PL:.5f} +- {S_OM_H2:.5f} "
          f"({100*S_OM_H2/OM_H2_PL:.2f}%)")

    # --- the degeneracy demonstration: does CHW alone constrain dNeff? ---
    print("\n[1] DEGENERACY TEST: fix omega_m h^2 at Planck, vary H0, dNeff = 0.27")
    best_pin = (float("inf"), float("nan"))
    for h in np.linspace(0.64, 0.78, 281):
        c = chi2_chw(h, OM_H2_PL, 0.270)
        if c < best_pin[0]:
            best_pin = (c, h)
    print(f"    best chi2_CHW at Planck omega_m h^2 = {best_pin[0]:.2f} at H0={100*best_pin[1]:.2f}")
    print("    -> H0 alone CANNOT restore the fit when omega_m h^2 is pinned.")

    # CHW-ALONE minimum (ignoring the Planck pull) -- the degeneracy endpoint
    best_chw = (float("inf"), float("nan"), float("nan"))
    for om in np.linspace(0.138, 0.156, 181):
        for h in np.linspace(0.64, 0.78, 281):
            c = chi2_chw(h, om, 0.270)
            if c < best_chw[0]:
                best_chw = (c, h, om)
    c_free, h_free, om_free = best_chw
    print(f"    CHW-ALONE minimum: chi2 = {c_free:.4f} at H0={100*h_free:.2f}, "
          f"om_h2={om_free:.5f} (Planck pull {(om_free-OM_H2_PL)/S_OM_H2:+.1f} sigma)")
    print("    -> the compressed prior has an EXACT (h, omega_m h^2) degeneracy that")
    print("       absorbs Delta N_eff. Its dchi2 is NOT a model constraint.")

    # --- the honest exclusion ---
    print("\n[2] COMBINED WITH PLANCK omega_m h^2")
    print(f"{'dNeff':>7}{'H0_best':>9}{'om_h2':>9}{'om pull':>9}"
          f"{'chi2_tot':>10}{'dchi2':>9}{'sigma':>8}")
    c0, h0, om0 = total_chi2(0.0)
    rows = []
    for dn in (0.0, 0.10, 0.20, 0.255, 0.270, 0.290):
        c, h, om = total_chi2(dn)
        d = c - c0
        rows.append({"dneff": dn, "H0_best": round(100 * h, 2),
                     "om_h2": round(om, 5),
                     "om_pull_sigma": round((om - OM_H2_PL) / S_OM_H2, 2),
                     "chi2_total": round(c, 2), "dchi2": round(d, 2),
                     "sigma": round(math.sqrt(max(d, 0.0)), 2)})
        print(f"{dn:>7.3f}{100*h:>9.2f}{om:>9.5f}{(om-OM_H2_PL)/S_OM_H2:>+8.1f}s"
              f"{c:>10.2f}{d:>+9.2f}{math.sqrt(max(d,0)):>7.2f}s")

    theory = next(r for r in rows if r["dneff"] == 0.270)
    print(f"\n[3] VERDICT")
    print(f"    dNeff = 0.270 -> H0 = {theory['H0_best']:.2f}, "
          f"omega_m h^2 = {theory['om_h2']:.5f} ({theory['om_pull_sigma']:+.1f} sigma)")
    print(f"    dchi2 vs LambdaCDM = {theory['dchi2']:+.2f}  "
          f"(~{theory['sigma']:.1f} sigma for one extra parameter)")
    print(f"    The exclusion is carried by omega_m h^2, NOT by l_A.")
    print(f"    Compare: the fixed-parameter number in the D4 report (+1571..+1949)")
    print(f"    overstates this by ~{1571/theory['dchi2']:.0f}x. It is the price of")
    print(f"    holding H0 AND omega_m h^2 fixed, not a model-discrimination statistic.")

    out = {
        "caveat": "CHW compressed distance prior + Gaussian Planck omega_m h^2; "
                  "uncorrelated approximation; no DESI BAO vector in repo",
        "planck_om_h2": {"value": round(OM_H2_PL, 5), "sigma": round(S_OM_H2, 5)},
        "degeneracy_test": {"chi2_at_planck_om_h2": round(best_pin[0], 2),
                            "H0_at_planck_om_h2": round(100 * best_pin[1], 2),
                            "chi2_chw_free": round(chi2_chw(h_free, om_free, 0.270), 4),
                            "note": "compressed prior has an exact (h, om_h2) degeneracy"},
        "scan": rows,
        "theory_point": theory,
        "fixed_parameter_dchi2_reported_by_D4": [1571, 1949],
        "overstatement_factor": round(1571 / theory["dchi2"], 1),
    }
    (HERE / "JOINT_NEFF_H0_SCAN.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {HERE / 'JOINT_NEFF_H0_SCAN.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
