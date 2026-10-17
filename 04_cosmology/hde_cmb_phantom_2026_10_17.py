#!/usr/bin/env python3
"""Tests pre-registered in PREREG_HDE_CMB_AND_PHANTOM_2026-10-17.md (14cc657).

Test 1: free-C future-event-horizon HDE versus flat LCDM on the fixed CHW CMB
block plus DESI DR2 BAO plus Pantheon+. HDE wins iff Delta chi2 < -9.
Test 2: Manus 2026-10-14 crossing history versus LCDM at the same Omega_DE0
on DESI DR2 BAO only. Excluded iff Delta chi2 > 9.
"""

import importlib.util
import json
import math
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

SPEC = importlib.util.spec_from_file_location(
    "hde_fit_chw",
    "/home/mega/Chyren/The-Hood/artifacts/2026-10-15__claude_cli__cmb-block-fixed-chw-recipe-hde-rerun-kill-stands/hde_fit_chw.py",
)
H = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(H)

PREREG = "14cc657c48ded81a182a2b3ca48d709e1d037d2d"
ODE0_MANUS = 0.6847
LN2 = math.log(2.0)
C_PRED = math.sqrt(LN2)
OUT = "/home/mega/Chyren/Res-Nova/04_cosmology/HDE_CMB_PHANTOM_2026-10-17.json"


def delta_ln_a_manus():
    """Radiation off. Integrate Omega from 0.6847 up to ln 2. Return Delta ln a."""

    def rhs(x, y):
        O = y[0]
        return [O * (1.0 - O) * (1.0 + 2.0 * math.sqrt(O) / C_PRED)]

    sol = solve_ivp(
        rhs,
        [0.0, 0.05],
        [ODE0_MANUS],
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    def f(x):
        return sol.sol(x)[0] - LN2

    x_cross = brentq(f, 0.0, 0.05)
    return float(x_cross), float(sol.sol(x_cross)[0])


def om_for_ode(h, ode0):
    target = 1.0 - ode0
    k = 2.5e4 * h * h * H.THETA**-4

    def f(om):
        return om + om / (1.0 + k * om) - target

    return brentq(f, 1e-6, min(0.95, target))


def v0():
    out = {}
    for name, (om, h, ob) in {
        "TT,TE,EE+lowE+lensing": (0.3153, 0.6736, 0.02237),
        "TT,TE,EE+lowE": (0.3166, 0.6727, 0.02236),
    }.items():
        c2, v, zs = H.cmb_chw(H.make_E("lcdm", om, h), om, h, ob)
        pulls = (v - H.PRI) / H.SIG
        out[name] = {
            "chi2_cmb": c2,
            "R": float(v[0]),
            "l_A": float(v[1]),
            "z_star": zs,
            "pulls": pulls.tolist(),
        }
        print(f"V0 {name}: chi2_CMB={c2:.4f} pulls={np.round(pulls, 3)}", flush=True)
        if not (c2 < 3 and np.all(np.abs(pulls) < 1.0)):
            raise SystemExit("V0 failed")
    return out


def bao_only(model, h, ode0, C=None):
    if not 0.5 < h < 0.9:
        return 1e9
    om = om_for_ode(h, ode0)
    try:
        E = H.make_E(model, om, h, C)
    except Exception:
        return 1e9
    return H.chi_bao(E, h, om, 0.02237), om


def main():
    t0 = time.time()
    res = {
        "prereg": PREREG,
        "cmb_block": "CHW 2019 g1=0.0738, Omega_r = Omega_m/(1+z_eq)",
    }
    dln, o_at = delta_ln_a_manus()
    z_cross = math.exp(-dln) - 1.0
    res["manus_reproduction"] = {
        "delta_ln_a": dln,
        "target": 0.01317,
        "abs_err": abs(dln - 0.01317),
        "omega_at_cross": o_at,
        "z_cross": z_cross,
        "window": [z_cross - 0.01, z_cross + 0.01],
    }
    print("MANUS", res["manus_reproduction"], flush=True)
    if abs(dln - 0.01317) > 1e-4:
        res["test2"] = {
            "verdict": "ABORTED",
            "reason": "delta ln a missed 0.01317 by more than 1e-4",
        }
        json.dump(res, open(OUT, "w"), indent=2)
        raise SystemExit(2)

    res["V0"] = v0()

    # Test 2 is the cheaper BAO-only pair. Run it before the joint fits.
    f_cross = H.fit(lambda p: bao_only("hde", p[0], ODE0_MANUS, C_PRED)[0], [0.67])
    chi_c, om_c = bao_only("hde", f_cross.x[0], ODE0_MANUS, C_PRED)
    f_l2 = H.fit(lambda p: bao_only("lcdm", p[0], ODE0_MANUS)[0], [0.67])
    chi_l2, om_l2 = bao_only("lcdm", f_l2.x[0], ODE0_MANUS)
    d2 = chi_c - chi_l2
    if d2 > 9:
        v2 = "excluded"
    elif d2 < 4:
        v2 = "allowed"
    else:
        v2 = "tension"
    w0, wa = H.w0_wa(om_c, f_cross.x[0], C_PRED)
    res["test2"] = {
        "omega_de0": ODE0_MANUS,
        "omega_b": 0.02237,
        "crossing": {
            "h": f_cross.x[0],
            "omega_m": om_c,
            "chi2_bao": chi_c,
            "w0": w0,
            "wa": wa,
        },
        "lcdm": {"h": f_l2.x[0], "omega_m": om_l2, "chi2_bao": chi_l2},
        "delta_chi2_crossing_minus_lcdm": d2,
        "verdict": v2,
    }
    print("TEST2", res["test2"], flush=True)

    f_l = H.fit(lambda p: H.total("lcdm", *p), [0.31, 0.675, 0.0224])
    parts_l = H.parts("lcdm", *f_l.x)
    f_h = H.fit(
        lambda p: H.total("hde", p[0], p[1], p[2], p[3]), [0.30, 0.68, 0.0225, 0.75]
    )
    parts_h = H.parts("hde", *f_h.x)
    d1 = f_h.fun - f_l.fun
    if d1 < -9:
        v1 = "hde_wins"
    else:
        v1 = "edge_does_not_survive"
    res["test1"] = {
        "lcdm": {
            "omega_m": f_l.x[0],
            "h": f_l.x[1],
            "omega_b": f_l.x[2],
            "chi2": f_l.fun,
            "parts": parts_l,
        },
        "hde_free": {
            "omega_m": f_h.x[0],
            "h": f_h.x[1],
            "omega_b": f_h.x[2],
            "C": f_h.x[3],
            "chi2": f_h.fun,
            "parts": parts_h,
            "w0_wa": H.w0_wa(f_h.x[0], f_h.x[1], f_h.x[3]),
        },
        "delta_chi2_hde_minus_lcdm": d1,
        "verdict": v1,
    }
    print("TEST1", res["test1"], flush=True)
    res["runtime_s"] = time.time() - t0
    json.dump(res, open(OUT, "w"), indent=2, default=float)
    print(f"wrote {OUT} in {res['runtime_s']:.0f} s", flush=True)


if __name__ == "__main__":
    main()
