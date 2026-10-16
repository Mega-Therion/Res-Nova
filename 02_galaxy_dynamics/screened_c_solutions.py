#!/usr/bin/env python3
"""Radial gravity and comet binding for the screened Lagrangian zero C.

The quasistatic QUMOND action with the tidal screen S(x), x = c^2 ||grad grad Phi_N|| / a0^2,
and a constant zero C of the screened MOND Lagrangian is

  L = -(1/(8 pi G)) [2 grad Phi . grad Phi_N - a0^2 Qs] - rho Phi,
  Qs = z + S(x) (Q(z) - z - C),
  z = y^2,  y = |grad Phi_N| / a0,  P(y) = Q(z) - z = Int_0^y 2 t (nu(t) - 1) dt,
  S(x) = 1 / (1 + (x/x*)^2).

C = 0 is the pre-registered model (no MOND energy where there is no field). Varying Phi_N
gives the same nu_eff as at C = 0, because C does not depend on z. It does change the
Hessian stress, because S depends on the Newtonian tidal tensor:

  W_ij = -(c^2/2) S'(x) (P(y) - C) H_ij / sqrt(|H|^2 + h_g^2).

For a lone Sun the solar Hessian is H_ij = (GM/r^3) (delta_ij - 3 n_i n_j), |H|_F = sqrt(6) GM/r^3.
The radial piece used by the wide-binary shape note is

  g_W = (2/sqrt(6)) r^{-3} d/dr (r^3 w_tilde),
  w_tilde = -(c^2/2) S'(x) (P(y_e) - C) |H| / Hn,

with y_e the Newtonian external-field variable of a uniform Galactic field (P is then one
number, so g_W is linear in (P - C)). Outward is positive. A comet that falls from rest at
infinity, where the anomalous potential vanishes, has osculating

  1/a = 2 Phi_W(0) / GM,   Phi_W(0) = Int_0^inf g_W(r) dr.

This script does not adopt C != 0. It writes the two solutions the equation actually has
at the Cassini cap on x*: C = 0, and the C that puts 1/a at the geometric centre of the
observed Oort window 10^4–10^5 au.

Usage: screened_c_solutions.py
Writes SCREENED_C_SOLUTIONS.json next to this file.
"""

import json
import sys
from pathlib import Path

import numpy as np

import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
GM = T.GM_SUN
A0 = T.A0
SQRT6 = np.sqrt(6.0)
# Observed Oort peak, VNT section 4, as cited by OORT_TORQUE_2026-10-16.md.
OORT_A_AU = (1.0e4, 1.0e5)
GES = (1.9e-10, 2.32e-10)


def y_external(g_e, a0=A0):
    """y = g_Ne / a0 for a uniform external acceleration g_e."""
    g_ne = T.newtonian_ext(float(g_e), a0)
    return g_ne / a0, g_ne


def shell_state(r, x_star, a0=A0):
    """Solar tidal invariant and S'(x) on a radial grid. r in metres."""
    r = np.asarray(r, dtype=float)
    h_sun = SQRT6 * GM / r**3
    hn = np.sqrt(h_sun**2 + T.H_G**2)
    x = T.C**2 * hn / a0**2
    _s, s1, _s2 = T.screen(x, float(x_star), "action")
    return h_sun, hn, s1


def w_tilde(r, c_zero, x_star, g_e, a0=A0):
    """w_tilde(r) for constant external P(y_e) - C."""
    y, _g_ne = y_external(g_e, a0)
    p_eff = float(T.P(np.array(y))) - float(c_zero)
    h_sun, hn, s1 = shell_state(r, x_star, a0)
    w = -(T.C**2 / 2.0) * s1 * p_eff
    return w * h_sun / hn, p_eff, float(y)


def g_w_outward(r, c_zero, x_star, g_e, a0=A0):
    """Outward anomalous radial acceleration from W, metres and s."""
    r = np.asarray(r, dtype=float)
    wt, p_eff, y = w_tilde(r, c_zero, x_star, g_e, a0)
    u = r**3 * wt
    # d/dr on a log-spaced grid: df/dr = (df/d ln r) / r
    ln = np.log(r)
    du = np.gradient(u, ln) / r
    g = (2.0 / SQRT6) * du / r**3
    return g, p_eff, y


def radial_gravity(r, c_zero, x_star, g_e, a0=A0):
    """Outward net radial acceleration: Newtonian Sun plus g_W. Returns g_net, g_W."""
    g_w, p_eff, y = g_w_outward(r, c_zero, x_star, g_e, a0)
    g_net = -GM / np.asarray(r, dtype=float) ** 2 + g_w
    return g_net, g_w, p_eff, y


def binding_inv_a(c_zero, x_star, g_e, a0=A0, n=4000):
    """Osculating 1/a in au^-1 for a comet that falls from rest at infinity."""
    r = np.geomspace(50.0 * T.AU, 2.0e6 * T.AU, n)
    g_net, g_w, p_eff, y = radial_gravity(r, c_zero, x_star, g_e, a0)
    # g_W is zero at both ends of this window (S' vanishes deep inside and far out).
    phi = np.trapezoid(g_w, r)
    inv_a = 2.0 * phi / GM * T.AU
    outward = g_net > 0
    return {
        "inv_a_au": float(inv_a),
        "P_ye": float(p_eff + c_zero),
        "P_minus_C": float(p_eff),
        "y_e": float(y),
        "sign_change": bool(outward.any()),
        "outward_r_kau": [
            float(x)
            for x in (r[outward] / (1e3 * T.AU))[:: max(outward.sum() // 8, 1)][:8]
        ],
        "g_over_gN_at_10kau": float(
            (g_w / (GM / r**2))[np.argmin(np.abs(r - 10e3 * T.AU))]
        ),
        "r_m": r,
        "g_net": g_net,
        "g_w": g_w,
    }


def c_for_inv_a(target_inv_a, x_star, g_e, a0=A0):
    """C that sets the W-only binding edge, using linearity in (P - C)."""
    base = binding_inv_a(0.0, x_star, g_e, a0)
    p = base["P_ye"]
    if base["inv_a_au"] == 0.0:
        raise RuntimeError("C = 0 produced a vanishing binding offset")
    # inv_a = inv_a(0) * (P - C) / P
    c_zero = p - p * (target_inv_a / base["inv_a_au"])
    return c_zero, base


def solve(x_star=None):
    if x_star is None:
        x_star = json.loads((HERE / "TIDAL_ACTION_CASSINI.json").read_text())[
            "x_star_action"
        ]
    target = 1.0 / np.sqrt(OORT_A_AU[0] * OORT_A_AU[1])
    rows = []
    for g_e in GES:
        c_peak, base = c_for_inv_a(target, x_star, g_e)
        at_peak = binding_inv_a(c_peak, x_star, g_e)
        at_p = binding_inv_a(base["P_ye"], x_star, g_e)
        rows.append(
            {
                "g_e_m_s2": g_e,
                "y_e": base["y_e"],
                "P_ye": base["P_ye"],
                "C_zero": {
                    "C": 0.0,
                    "inv_a_au": base["inv_a_au"],
                    "a_edge_au": (1.0 / base["inv_a_au"]) if base["inv_a_au"] else None,
                    "sign_change_outward": base["sign_change"],
                    "outward_r_kau_sample": base["outward_r_kau"],
                    "g_over_gN_at_10kau": base["g_over_gN_at_10kau"],
                },
                "C_oort_peak": {
                    "C": c_peak,
                    "target_inv_a_au": target,
                    "target_a_au": float(1.0 / target),
                    "inv_a_au": at_peak["inv_a_au"],
                    "a_edge_au": (
                        (1.0 / at_peak["inv_a_au"]) if at_peak["inv_a_au"] else None
                    ),
                    "sign_change_outward": at_peak["sign_change"],
                    "g_over_gN_at_10kau": at_peak["g_over_gN_at_10kau"],
                },
                "C_equals_P": {
                    "C": base["P_ye"],
                    "inv_a_au": at_p["inv_a_au"],
                    "sign_change_outward": at_p["sign_change"],
                },
            }
        )
    # One radial profile at the first Galactic field, both C values, decimated.
    r = np.geomspace(100.0 * T.AU, 5.0e5 * T.AU, 64)
    profiles = {}
    for label, c_zero in (("C0", 0.0), ("C_peak", rows[0]["C_oort_peak"]["C"])):
        g_net, g_w, _p, _y = radial_gravity(r, c_zero, x_star, GES[0])
        profiles[label] = {
            "r_kau": [float(v) for v in r / (1e3 * T.AU)],
            "g_net_m_s2": [float(v) for v in g_net],
            "g_W_m_s2": [float(v) for v in g_w],
        }
    return {
        "equation": "Qs = z + S(x)(Q(z) - z - C), W_ij = -(c^2/2) S'(x) (P(y)-C) H_ij / Hn",
        "x_star": x_star,
        "a0": A0,
        "oort_window_au": list(OORT_A_AU),
        "target_inv_a_au": target,
        "fields": rows,
        "profile_ge_1p9e-10": profiles,
        "tier": {
            "C_eq_0": "[X] on the Oort cloud; this is the pre-registered model",
            "C_oort_peak": "[O] a different zero, not adopted and not pre-registered",
        },
    }


def main():
    out = solve()
    # Drop nothing: profile is part of the artifact. Write compact JSON.
    path = HERE / "SCREENED_C_SOLUTIONS.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    for row in out["fields"]:
        z = row["C_zero"]
        p = row["C_oort_peak"]
        print(
            f"g_e={row['g_e_m_s2']:.3e} P={row['P_ye']:.6f} "
            f"C=0 inv_a={z['inv_a_au']:.6e} sign_change={z['sign_change_outward']} "
            f"C_peak={p['C']:.6f} inv_a={p['inv_a_au']:.6e} sign_change={p['sign_change_outward']}"
        )
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
