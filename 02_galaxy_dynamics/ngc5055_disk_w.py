#!/usr/bin/env python3
"""Midplane tide of W on NGC 5055. Does not retune a0, mu_std, x*, or C.

The spherical estimate in SCREENING_FIVE_CHECKS_2026-10-16.md section 3
left the disk evaluation unrun. This script differentiates the baryonic
g_N(R) from the SPARC table. It is not a 2D Poisson solve.
"""

import json
import os
from pathlib import Path

import numpy as np

import sparc_reproduce as sr

A0 = 1.1607e-10
XS = 7.035884281332817e11
C_LIGHT = 299792458.0
KPC = 3.085677581e19
YD, FD = 0.55, 0.9


def p_of_y(y):
    """P(y) = integral_0^y 2 t (nu(t)-1) dt, nu the mu_std inverse."""
    t = np.geomspace(1e-8, max(float(y), 1e-6), 2000)
    nu = np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / t**2)))
    integrand = 2.0 * t * (nu - 1.0)
    return float(np.trapezoid(integrand, t))


def main():
    data = os.environ.get(
        "SPARC_DATA_DIR",
        "/home/mega/Chyren/Research_and_Data/07_Domain_Tiers_and_Data/Datasets/data/sparc_data",
    )
    g = sr.load_rotmod(Path(data) / "NGC5055_rotmod.dat")
    vb = sr.v_baryon(g["v_gas"], g["v_disk"], g["v_bulge"], YD, 0.0)
    R = g["r"] * FD
    r_m = R * KPC
    gN = FD * (vb * 1e3) ** 2 / np.maximum(r_m, 1.0)
    # In-plane eigenvalues of the baryonic tide. Vertical closes the trace
    # off the disk mass, lambda_z = -(lambda_R + lambda_phi).
    h_r = np.gradient(gN, r_m)
    h_phi = gN / r_m
    h_z = -(h_r + h_phi)
    hf = np.sqrt(h_r**2 + h_phi**2 + h_z**2)
    x = C_LIGHT**2 * hf / A0**2
    s = 1.0 / (1.0 + (x / XS) ** 2)
    sp = -2.0 * (x / XS**2) / (1.0 + (x / XS) ** 2) ** 2
    outer = g["r"] >= 10.0
    p = np.array([p_of_y(float(gn) / A0) for gn in gN])
    # W is a potential. Its radial derivative is the acceleration.
    w = 0.5 * C_LIGHT**2 * sp * p
    g_w = np.abs(np.gradient(w, r_m))
    rows = []
    for i in np.where(outer)[0]:
        rows.append(
            {
                "R_kpc": float(g["r"][i]),
                "gN": float(gN[i]),
                "x_over_xs": float(x[i] / XS),
                "S": float(s[i]),
                "abs_gW_over_gN": float(g_w[i] / gN[i]),
            }
        )
    ratios = np.array([row["abs_gW_over_gN"] for row in rows])
    out = {
        "a0": A0,
        "xstar": XS,
        "C": 0.0,
        "upsilon_disk": YD,
        "fd": FD,
        "n_outer": len(rows),
        "x_over_xs_max": max(row["x_over_xs"] for row in rows),
        "S_min": min(row["S"] for row in rows),
        "abs_gW_over_gN_max": float(ratios.max()),
        "rows": rows,
    }
    dest = Path(__file__).with_name("NGC5055_DISK_W.json")
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in out if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
