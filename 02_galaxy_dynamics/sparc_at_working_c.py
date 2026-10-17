#!/usr/bin/env python3
"""SPARC at the working C. Protocol: PREREG_SPARC_WORKING_C_2026-10-16.md.

g_W is the spherical identity in tidal_screening_action_sparc.py, with P(y) - C.
Centripetal acceleration is nu_eff*g_N - g_W, the inward sign of radial_gravity.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import environment_screening as E
import tidal_screening_sparc_cassini as TS
import tidal_screening_two_body as T
from parameter_ledger import (
    FD_STD,
    KM_TO_M,
    KPC_TO_M,
    YB_MEAN,
    YB_STD,
    YD_MEAN,
    YD_STD,
    chi2,
    load,
    v_bary_sq,
)
from sparc_paths import resolve_sparc_dir

HERE = Path(__file__).resolve().parent
XS = 703588428133.2817
C_WORK = 0.579124707982253
HZ = 0.1


def g_parts(g, sb, yd, yb, fd, screen):
    vb2 = v_bary_sq(g, yd, yb, fd)
    r = g["r"] * fd * KPC_TO_M
    gN = vb2 * KM_TO_M**2 / r
    if not screen:
        return gN, np.zeros_like(gN)
    y = np.maximum(gN / TS.A0, 1e-12)
    x = TS.tidal_x(g, sb, yd, yb, fd, HZ)
    s, s1, _ = T.screen(x, XS, "action")
    wt = -(T.C**2 / 2) * s1 * (T.P(y) - C_WORK)
    gW = (2 / np.sqrt(6)) * np.gradient(r**3 * wt, r) / r**3
    return (1 + s * (T.nu(y) - 1)) * gN, gW


def v_of(g, sb, yd, yb, fd, screen):
    r = g["r"] * fd * KPC_TO_M
    g_in, gW = g_parts(g, sb, yd, yb, fd, screen)
    g_c = g_in - gW if screen else g_in
    return np.sqrt(np.maximum(g_c, 0.0) * r) / KM_TO_M


def fit(g, sb, screen):
    nb = 1 + (1 if g["has_bulge"] else 0)

    def f(t):
        yd, fd = t[0], t[-1]
        yb = t[1] if g["has_bulge"] else 0.0
        pr = (
            ((yd - YD_MEAN) / YD_STD) ** 2
            + ((fd - 1) / FD_STD) ** 2
            + (((yb - YB_MEAN) / YB_STD) ** 2 if g["has_bulge"] else 0)
        )
        return chi2(g, v_of(g, sb, yd, yb, fd, screen), pr)

    r = minimize(
        f,
        [YD_MEAN] + ([YB_MEAN] if g["has_bulge"] else []) + [1.0],
        bounds=[(0.01, 5)] * nb + [(0.5, 2.0)],
        method="L-BFGS-B",
    )
    return float(r.fun)


def main():
    gals = load(resolve_sparc_dir(None))
    path = HERE / "SPARC_AT_WORKING_C.json"
    if len(gals) != 171:
        out = {"n": len(gals), "verdict": "sample mismatch", "excluded": False}
        path.write_text(json.dumps(out, indent=1) + "\n")
        print(out["verdict"], out["n"], flush=True)
        return
    sb = TS.sb_columns(resolve_sparc_dir(None), gals)
    rows = []
    for i, g in enumerate(gals):
        sbg = sb[g["name"]]
        cn = fit(g, sbg, screen=False)
        cu = E.fit1(g, TS.A0, 0.0)[0]
        cs = fit(g, sbg, screen=True)
        rows.append(
            {
                "name": g["name"],
                "chi2_newton": cn,
                "chi2_unscreened": cu,
                "chi2_screen": cs,
            }
        )
        if i % 20 == 0:
            print(i, g["name"], round(cs, 2), flush=True)
    ntot = sum(r["chi2_newton"] for r in rows)
    stot = sum(r["chi2_screen"] for r in rows)
    utot = sum(r["chi2_unscreened"] for r in rows)
    outliers = [
        r["name"]
        for r in rows
        if r["chi2_screen"] > r["chi2_newton"] + 1
        and r["chi2_screen"] > r["chi2_unscreened"] + 1
    ]
    excluded = bool(stot > ntot + 1)
    out = {
        "prereg": "PREREG_SPARC_WORKING_C_2026-10-16.md",
        "n": 171,
        "C": C_WORK,
        "x_star": XS,
        "a0": TS.A0,
        "h_z_kpc": HZ,
        "chi2_newton": ntot,
        "chi2_screen": stot,
        "chi2_unscreened": utot,
        "delta_screen_minus_newton": stot - ntot,
        "excluded": excluded,
        "verdict": "excluded" if excluded else "not excluded",
        "outliers": outliers,
        "galaxies": rows,
    }
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(
        "newton",
        ntot,
        "screen",
        stot,
        "unscreened",
        utot,
        "excluded",
        excluded,
        flush=True,
    )
    print("outliers", outliers, flush=True)


if __name__ == "__main__":
    main()
