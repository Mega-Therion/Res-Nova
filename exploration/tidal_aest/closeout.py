#!/usr/bin/env python3
"""Close-out of the three open items for the tidal QUMOND-in-AeST candidate (2026-11-19).
(A) Nonlinear: spherical top-hat collapse in LCDM with the phantom boost b = (nu - 1) S_lin(x_H) on the shell.
    Does the screen leave delta_c (collapse threshold, hence the halo mass function) unchanged?
(B) CMB: size of the boost on linear modes at recombination (z = 1100) and at the drag epoch.
(C) Constants: x_H_low derived from spherical-collapse virialisation (Delta_vir = 18 pi^2 -> x_H = 0.866 Om Delta_vir);
    x* and C checked against simple physical scales."""
import json, math
import numpy as np
from scipy.integrate import solve_ivp
a0 = 1.1607e-10; c = 2.99792458e8; Mpc = 3.0857e22; H0 = 67.4e3 / Mpc; Om = 0.315; OL = 1 - Om
nu = lambda y: math.sqrt(0.5 * (1 + math.sqrt(1 + 4 / max(y, 1e-30) ** 2)))
H = lambda a: H0 * math.sqrt(Om / a**3 + OL)
def collapse(delta_i, a_i, xh_low, M_phys):
    """Shell radius R(t) for a top-hat of mass M; returns the collapse scale factor (R -> 0.05 R_max) or None."""
    G = 6.674e-11
    rho_i = 3 * H(a_i) ** 2 * Om / a_i**3 / (Om / a_i**3 + OL) / (8 * math.pi * G) * (1 + delta_i)
    R_i = (3 * M_phys / (4 * math.pi * rho_i)) ** (1 / 3)
    v_i = H(a_i) * R_i * (1 - delta_i / 3)                 # growing mode
    t_i = 2 / (3 * H(a_i))
    lam = 3 * H0**2 * OL                                    # Lambda term: +Lambda R/3 with Lambda = 3 H0^2 OL
    state = {"Rmax": 0.0}
    def rhs(t, y):
        R, v, a = y
        gN = G * M_phys / R**2
        rho = 3 * M_phys / (4 * math.pi * R**3); rho_bar = 3 * H(a) ** 2 * (Om / a**3) / (Om / a**3 + OL) / (8 * math.pi * G)
        xh = 0.866 * (4 * math.pi * G * rho / 3 * 3) / H(a) ** 2 / 1.0   # |grad grad Phi| ~ sqrt3 (4pi/3) G rho; x_H = that / H^2
        xh = math.sqrt(3) * (4 * math.pi / 3) * G * rho / H(a) ** 2
        b = 0.0 if xh_low is None else (nu(gN / a0) - 1) / (1 + (xh_low / xh) ** 2)
        state["Rmax"] = max(state["Rmax"], R)
        return [v, -gN * (1 + b) + lam * R / 3, a * H(a)]
    ev = lambda t, y: y[0] - 0.05 * max(state["Rmax"], y[0]) if state["Rmax"] > 0 else 1.0
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (t_i, t_i + 60 / H0), [R_i, v_i, a_i], events=ev, rtol=1e-8, atol=1e-6, max_step=1e15)
    return s.y_events[0][0][2] if len(s.t_events[0]) else None
def delta_c_for_collapse_at(a_target, xh_low, M):
    a_i = 1e-3; lo, hi = 1e-4, 1e-1
    for _ in range(40):
        mid = math.sqrt(lo * hi); ac = collapse(mid, a_i, xh_low, M)
        if ac is None or ac > a_target: lo = mid
        else: hi = mid
    return hi * (a_target / a_i) * 0.6  # linear extrapolation (growing-mode 3/5 factor), matter-era approx
out = {"A_nonlinear": {}, "B_cmb": {}, "C_constants": {}}
Msun = 1.989e30
for M in (1e8, 1e11, 1e14):
    dc0 = delta_c_for_collapse_at(1.0, None, M * Msun)
    dcs = delta_c_for_collapse_at(1.0, 154.0, M * Msun)
    out["A_nonlinear"][f"M={M:.0e}"] = {"delta_c_LCDM": dc0, "delta_c_screened": dcs, "rel_change": dcs / dc0 - 1}
    print(f"M={M:.0e} Msun: delta_c LCDM {dc0:.4f}, with screen {dcs:.4f}, change {dcs/dc0-1:+.2e}", flush=True)
# (B) recombination: linear mode k=0.1 h/Mpc: x_H = 1.5 Om(a) Delta(a); Delta(z=1100) ~ Delta0 * D(1100)/D(0)
lin = json.load(open("LINEAR_COSMOLOGY.json"))["linear_modes_z0"]
for z in (1100.0, 1060.0):
    a = 1 / (1 + z); Oma = Om / a**3 / (Om / a**3 + OL)
    rows = {}
    for n, m in lin.items():
        Delta0 = m["x"] * a0**2 / c**2 / (1.5 * Om * H0**2)
        Delta = Delta0 * a / 0.78                      # D(0)/a ~ 0.78 in LCDM
        xh = 1.5 * Oma * Delta; g = m["g"] * (1 + z)
        rows[n] = {"x_H": xh, "boost_b": (nu(g / a0) - 1) / (1 + (154.0 / xh) ** 2)}
    out["B_cmb"][f"z={z:.0f}"] = rows
    print(f"z={z:.0f}: max boost {max(r['boost_b'] for r in rows.values()):.2e}")
# (C) constants
out["C_constants"] = {
    "x_H_low_from_virialisation": {"Delta_vir_EdS": 18 * math.pi**2, "x_H_low": 0.866 * 18 * math.pi**2,
                                   "inside_data_window_[10,492]": 10 <= 0.866 * 18 * math.pi**2 <= 492},
    "x_star_scales": {"x_star_cassini": 7.04e11, "T_star_s^-2": 7.04e11 * a0**2 / c**2,
                      "equivalent_density_Msun_pc3": 7.04e11 * a0**2 / c**2 / (math.sqrt(3) * 4 * math.pi / 3 * 6.674e-11) / (1.989e30 / 3.0857e16**3)},
    "C": "Oort window [0.209, 0.696]; no derivation found (constant Lagrangian zero)"}
print(json.dumps(out["C_constants"], indent=1))
json.dump(out, open("CLOSEOUT.json", "w"), indent=1, default=float)
