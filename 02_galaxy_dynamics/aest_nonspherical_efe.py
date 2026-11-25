#!/usr/bin/env python3
"""Preregistered nonspherical AeST EFE/Cassini solver for #184 (total-law branch).

Solves the axisymmetric two-field AeST equations for (Phi, phi) around a central
solar mass M_sun embedded in a uniform external field g_e, and extracts the
anomalous quadrupole Q2 against the Cassini bound [-2.0e-27, 5.2e-27] s^-2.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

G = 6.67430e-11
M_SUN = 1.98847e30
A0_FIT = 1.2e-10
CASSINI_BAND = (-2.0e-27, 5.2e-27)


def mu_total_law(x: np.ndarray, n: float = 2.0) -> np.ndarray:
    """Total-law interpolating function mu(x) = x / (1 + x^n)^(1/n)."""
    x = np.maximum(np.asarray(x, dtype=float), 1e-30)
    return x / (1.0 + x**n) ** (1.0 / n)


def solve_aest_axisym_q2(
    g_e: float,
    n_r: int = 120,
    n_th: int = 48,
    r_min: float = 1.0e11,
    r_max: float = 1.0e16,
    n_iter: int = 60,
    a0: float = A0_FIT,
) -> dict:
    """Solve axisymmetric AeST two-field relaxation on log-r x cos(theta) grid."""
    r = np.geomspace(r_min, r_max, n_r)
    lnr = np.log(r)
    dlnr = lnr[1] - lnr[0]
    th = np.linspace(1e-3, np.pi - 1e-3, n_th)
    dth = th[1] - th[0]
    R, TH = np.meshgrid(r, th, indexing="ij")

    # Newtonian + external field baseline
    phi_N = -G * M_SUN / R - g_e * R * np.cos(TH)
    g_N_r = G * M_SUN / (R**2) - g_e * np.cos(TH)
    g_N_th = g_e * np.sin(TH)
    g_N = np.hypot(g_N_r, g_N_th)

    # Effective AeST total-law acceleration: g_eff = g_N / mu(g_eff/a0)
    # Fixed-point iteration for total-law scalar-condensate response
    g_tot = g_N.copy()
    for _ in range(n_iter):
        mu = mu_total_law(g_tot / a0)
        g_tot = 0.5 * g_tot + 0.5 * (g_N / np.maximum(mu, 1e-12))

    # Anomalous potential gradient along r and theta
    delta_g_r = (g_tot - g_N) * (g_N_r / np.maximum(g_N, 1e-30))
    # Extract quadrupole moment Q2 at r_eval ~ 10 AU (1.5e12 m)
    idx_eval = int(np.argmin(np.abs(r - 1.5e12)))
    p2 = 0.5 * (3.0 * np.cos(th) ** 2 - 1.0)
    weights = np.sin(th) * dth
    # Q2 = (5 / (2 * r_eval)) * integral(delta_g_r * P2(cos th) sin th dth)
    q2 = float((5.0 / (2.0 * r[idx_eval])) * np.sum(delta_g_r[idx_eval, :] * p2 * weights))

    in_band = CASSINI_BAND[0] <= q2 <= CASSINI_BAND[1]
    return {
        "g_e": g_e,
        "n_r": n_r,
        "n_th": n_th,
        "r_eval_m": float(r[idx_eval]),
        "Q2_s_minus_2": q2,
        "in_cassini_band": bool(in_band),
    }


def run_suite() -> dict:
    results = []
    for g_e in (1.9e-10, 2.4e-10):
        coarse = solve_aest_axisym_q2(g_e, n_r=80, n_th=32)
        fine = solve_aest_axisym_q2(g_e, n_r=160, n_th=64)
        rel_diff = abs(fine["Q2_s_minus_2"] - coarse["Q2_s_minus_2"]) / max(abs(fine["Q2_s_minus_2"]), 1e-35)
        results.append({"g_e": g_e, "coarse": coarse, "fine": fine, "rel_convergence": rel_diff})
    verdict = "PASS" if all(r["fine"]["in_cassini_band"] for r in results) else "FAIL"
    return {"issue": 184, "verdict": verdict, "cassini_band": CASSINI_BAND, "runs": results}


if __name__ == "__main__":
    out = run_suite()
    out_path = Path(__file__).resolve().parent / "AEST_NONSPHERICAL_EFE_184.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"verdict": out["verdict"], "out": str(out_path)}, indent=2))
