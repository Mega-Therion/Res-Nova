#!/usr/bin/env python3
"""Comet orbits at the Oort C window, plus the two leftover screen questions.

1. Integrate bound radial orbits in -GM/r^2 + g_W(r; C) and read the Newtonian
   osculating 1/a at perihelion. Compare it to the energy proxy.
2. The action's derivative with respect to C, and Qs at zero field.
3. The shell width that would carry a higher-derivative relativistic completion.

Writes COMET_C_WINDOW.json. Does not retune a0 or x*.
"""

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

import screened_c_solutions as S
import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
XSTAR = json.loads((HERE / "TIDAL_ACTION_CASSINI.json").read_text())["x_star_action"]
GE = 1.9e-10
CS = (0.0, 0.208899, 0.579124707982253, 0.696200)
# Original aphelia across and outside the observed window, metres via AU.
APHELIA_AU = np.geomspace(3.0e3, 3.0e5, 13)
Q_AU = 5.0
YEAR = 365.25 * 86400.0


def force_table(c_zero):
    r = np.geomspace(20.0 * T.AU, 2.0e6 * T.AU, 6000)
    g_net, g_w, p_eff, y = S.radial_gravity(r, c_zero, XSTAR, GE)
    phi = np.concatenate([[0.0], np.cumsum(0.5 * (g_w[1:] + g_w[:-1]) * np.diff(r))])
    # phi(r) = int_0^r g_W, so phi(inf) - phi(0) is the proxy integral.
    # g_W ~ 0 at the inner edge of this grid; shift so phi(inf) = 0.
    phi = phi - phi[-1]
    g_interp = interp1d(r, g_net)
    phi_interp = interp1d(r, phi)
    r0, r1 = float(r[0]), float(r[-1])

    def g_of(rr):
        rr = float(rr)
        if rr < r0 or rr > r1:
            return -T.GM_SUN / rr**2
        return float(g_interp(rr))

    def phi_of(rr):
        rr = float(rr)
        if rr < r0:
            return float(phi[0])
        if rr > r1:
            return 0.0
        return float(phi_interp(rr))

    return {
        "g": g_of,
        "phi": phi_of,
        "phi0": float(phi[0]),
        "P_minus_C": float(p_eff),
        "y": float(y),
    }


def one_orbit(tab, r_a):
    q = Q_AU * T.AU
    a = 0.5 * (r_a + q)
    e = (r_a - q) / (r_a + q)
    L2 = T.GM_SUN * a * (1.0 - e * e)
    # Newtonian period is an upper scale; the shell can turn the comet around sooner.
    tmax = 2.0 * np.pi * np.sqrt(a**3 / T.GM_SUN)

    def f(_t, y):
        # y = (ln(r/AU), d ln r / dt). The radius stays positive.
        r = T.AU * np.exp(y[0])
        w = y[1]
        g = float(tab["g"](r))
        return [w, L2 / r**4 + g / r - w * w]

    def turn(_t, y):
        return y[1]

    turn.terminal = True
    turn.direction = 1
    sol = solve_ivp(
        f,
        (0.0, tmax),
        [np.log(r_a / T.AU), -1e-16],
        rtol=1e-8,
        atol=1e-14,
        events=turn,
    )
    if sol.t_events[0].size:
        u, w = sol.y_events[0][0]
    else:
        u, w = sol.y[0, -1], sol.y[1, -1]
    rp = float(T.AU * np.exp(u))
    vr = float(w * rp)
    vp2 = vr**2 + L2 / rp**2
    eps = 0.5 * vp2 - T.GM_SUN / rp
    inv_osc = float(-2.0 * eps / T.GM_SUN * T.AU)
    # Acceleration is -GM/r^2 + dphi/dr, so the potential is -GM/r - phi.
    e_true = -T.GM_SUN / r_a - float(tab["phi"](r_a))
    eps_energy = e_true + float(tab["phi"](rp))
    inv_from_energy = float(-2.0 * eps_energy / T.GM_SUN * T.AU)
    inv_proxy = float(
        2.0 / (r_a / T.AU + Q_AU)
        + (2.0 * (float(tab["phi"](r_a)) - float(tab["phi"](rp))) / T.GM_SUN * T.AU)
    )
    return {
        "a_start_au": float(r_a / T.AU),
        "reached": bool(sol.success and rp < 0.5 * r_a),
        "q_au": float(rp / T.AU),
        "inv_a_osculating_au": inv_osc,
        "inv_a_from_energy_au": inv_from_energy,
        "inv_a_proxy_au": inv_proxy,
    }


def shell_width():
    r = np.geomspace(100.0 * T.AU, 5.0e5 * T.AU, 4000)
    _h, _hn, s1 = S.shell_state(r, XSTAR)
    w = np.abs(s1)
    peak = int(np.argmax(w))
    half = w >= 0.5 * w[peak]
    inside = np.where(half)[0]
    return {
        "r_peak_au": float(r[peak] / T.AU),
        "r_half_lo_au": float(r[inside[0]] / T.AU),
        "r_half_hi_au": float(r[inside[-1]] / T.AU),
        "fractional_width": float((r[inside[-1]] - r[inside[0]]) / r[peak]),
    }


def c_principle():
    """dL/dC is the integral of (S-1). Qs(z=0) = -S*C."""
    r = np.geomspace(50.0 * T.AU, 2.0e6 * T.AU, 4000)
    h_sun, hn, s1 = S.shell_state(r, XSTAR)
    x = T.C**2 * hn / T.A0**2
    s, _s1, _s2 = T.screen(x, XSTAR, "action")
    # Spherical volume element. The constant piece of the action density.
    integrand = (s - 1.0) * 4.0 * np.pi * r**2
    integral = float(np.trapezoid(integrand, r))
    return {
        "volume_integral_S_minus_1_m3": integral,
        "action_fixes_C": bool(abs(integral) < 1.0),
        "Qs_at_zero_field": "-S(x)*C",
        "zero_field_condition_forces": "C=0",
    }


def main():
    rows = []
    for c_zero in CS:
        tab = force_table(c_zero)
        orbits = [one_orbit(tab, a * T.AU) for a in APHELIA_AU]
        osc = np.array([o["inv_a_osculating_au"] for o in orbits])
        energy = np.array([o["inv_a_from_energy_au"] for o in orbits])
        proxy = np.array([o["inv_a_proxy_au"] for o in orbits])
        reached = np.array([o["reached"] for o in orbits])
        rows.append(
            {
                "C": c_zero,
                "P_minus_C": tab["P_minus_C"],
                "phi0_term_au": float(2.0 * tab["phi0"] / T.GM_SUN * T.AU),
                "n": len(orbits),
                "n_reached_perihelion": int(reached.sum()),
                "max_abs_osc_minus_energy": float(np.max(np.abs(osc - energy))),
                "max_abs_osc_minus_proxy_reached": float(
                    np.max(np.abs(osc[reached] - proxy[reached]))
                    if reached.any()
                    else None
                ),
                "orbits": orbits,
            }
        )
        print(
            f"C={c_zero:.6f} reached={int(reached.sum())}/{len(orbits)} "
            f"max|osc-energy|={rows[-1]['max_abs_osc_minus_energy']:.3e} "
            f"max|osc-proxy|={rows[-1]['max_abs_osc_minus_proxy_reached']}",
            flush=True,
        )
    out = {
        "x_star": XSTAR,
        "g_e": GE,
        "q_target_au": Q_AU,
        "window_au": [1.0e4, 1.0e5],
        "fields": rows,
        "shell": shell_width(),
        "C_from_action": c_principle(),
        "tier": "[D] orbit integral and the action derivative. Not a VNT population run.",
    }
    path = HERE / "COMET_C_WINDOW.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path)
    print("shell", out["shell"])
    print("C", out["C_from_action"])


if __name__ == "__main__":
    main()
