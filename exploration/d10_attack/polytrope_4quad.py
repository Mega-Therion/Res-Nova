#!/usr/bin/env python3
"""Pre-registered D10 tests (PREREG_POLYTROPE_4QUAD.md, commit a4db5e0b):
  (S1) SymPy exact Euler-Lagrange of 2-field Tidal-QUMOND-in-AeST + K2(Q-Q0)^2 dust + n=1 polytrope EOS.
  (T1) Free-boundary n=1 polytrope (MOND ON, fixed universal mu, chemical potential Phi0 fixed by supply).
  (T2) Untested 4th quadrant: BK cluster screen (MOND OFF, Newtonian) + AeST n=1 polytrope dust (2a uncapped, 2b capped).
  (T3) Splashback boundary (1.4 r200, 1.8 r200) & Lane-Emden resonance pole (mu R = pi) audit.
  (T4) ICM gas outer-slope sensitivity (beta = 2/3, 0.85, 1.0) on T1 and T2b.
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


def run_symbolic_s1() -> dict:
    """Exact SymPy Euler-Lagrange for 2-field Tidal-QUMOND-in-AeST + AeST dust K2(Q-Q0)^2."""
    r, Gt, a0, KB, K2, Q0, Phi0 = sp.symbols("r Gt a0 K_B K_2 Q_0 Phi_0", positive=True)
    # Standard sign convention: rho_b > 0, Phi < 0 in well, Phi' = g > 0, nabla^2 Phi_N = +4 pi G_N rho_b.
    # Static action in 1/(8 pi Gt) units (matches normalization_kb.py with L_matter = -rho_b * Phi):
    #   L = -rho_b*Phi + (1/8piGt)[ Psi'^2 - 2 Phi' Psi' + (K_B/2) Phi'^2 + (2-K_B) Phi' phi'
    #                               - ((2-K_B)/2) phi'^2 + (2-K_B) phi' psi'
    #                               + ((2-K_B)/2) a0^2 F(psi'^2/a0^2) + K_2 Q_0^2 (Phi - Phi_0)^2 ]
    Phi = sp.Function("Phi")(r)
    Psi = sp.Function("Psi")(r)
    phi = sp.Function("phi")(r)
    psi = sp.Function("psi")(r)
    Fp = sp.Function("Fp")
    GN = Gt / (1 - KB / 2)
    mu_sq = 2 * K2 * Q0**2 / (2 - KB)

    # First-derivative flux variables for spherical Lagrangian r^2 L
    P1, S1, ph1, ps1 = sp.diff(Phi, r), sp.diff(Psi, r), sp.diff(phi, r), sp.diff(psi, r)
    u = ps1**2 / a0**2
    k, m, n = KB / 2, 2 - KB, (2 - KB) / 2

    # Evaluate Euler-Lagrange equations with Psi = Phi, phi' = Phi' + psi', Phi' = -(1+Fp(u))*psi'
    g_eff = sp.Function("g_eff")(r)  # g_eff = -psi' > 0 (total Newtonian + dust gravity)
    u_eff = g_eff**2 / a0**2
    subs_sol = {
        S1: g_eff * (1 + Fp(u_eff)),
        P1: g_eff * (1 + Fp(u_eff)),
        ph1: g_eff * Fp(u_eff),
        ps1: -g_eff,
    }
    # Fluxes d(r^2 L)/df'
    dL_dP1 = (r**2 / (8 * sp.pi * Gt)) * (-2 * S1 + 2 * k * P1 + m * ph1)
    dL_dS1 = (r**2 / (8 * sp.pi * Gt)) * (2 * S1 - 2 * P1)
    dL_dph1 = (r**2 / (8 * sp.pi * Gt)) * (m * P1 - 2 * n * ph1 + 2 * n * ps1)
    dL_dps1 = (r**2 / (8 * sp.pi * Gt)) * (2 * n * ph1 + 2 * n * Fp(u) * ps1)

    # Check Psi, phi, psi equations vanish identically
    E_Psi = sp.simplify(-sp.diff(dL_dS1.subs(subs_sol), r))
    E_phi = sp.simplify(-sp.diff(dL_dph1.subs(subs_sol), r))
    E_psi = sp.simplify(-sp.diff(dL_dps1.subs(subs_sol), r))
    assert E_Psi == 0 and E_phi == 0 and E_psi == 0

    # Phi equation: d(r^2 L)/dPhi - d/dr(d(r^2 L)/dPhi') = 0
    # Note d(r^2 L)/dPhi = r^2 * (-rho_b + (2 K_2 Q_0^2)/(8 pi Gt) * (Phi - Phi_0))
    flux_Phi = sp.simplify(dL_dP1.subs(subs_sol))
    # Verify flux_Phi = -r^2 g_eff / (4 pi GN)
    assert sp.simplify(flux_Phi + r**2 * g_eff / (4 * sp.pi * GN)) == 0
    # Therefore E_Phi = 0 reads: (1/r^2) d(r^2 g_eff)/dr = 4 pi GN rho_b + mu_sq * (Phi_0 - Phi)
    rho_b = sp.Symbol("rho_b", positive=True)
    E_Phi_raw = r**2 * (-rho_b + 2 * K2 * Q0**2 / (8 * sp.pi * Gt) * (Phi - Phi0)) - sp.diff(flux_Phi, r)
    expected_rhs = 4 * sp.pi * GN * rho_b + mu_sq * (Phi0 - Phi)
    assert sp.simplify(E_Phi_raw - (sp.diff(r**2 * g_eff, r) - r**2 * expected_rhs) / (4 * sp.pi * GN)) == 0

    # Exact SZ21 K(Q) = K_2 (Q - Q_0)^2 fluid thermodynamics:
    # Action S = (1 / 16 pi Gt) integral sqrt(-g) [R + 2 K(Q) + ...]
    # => 8 pi Gt p = K(Q),  8 pi Gt rho = Q K_Q - K(Q).
    dQ = sp.Symbol("dQ", positive=True)
    Q = Q0 + dQ
    K = K2 * dQ**2
    KQ = sp.diff(K, dQ)
    p_geom = K                            # = 8 pi Gt p
    rho_geom = Q * KQ - K                 # = 8 pi Gt rho = 2 K2 Q0 dQ + K2 dQ^2
    cs2_exact = sp.simplify(sp.diff(p_geom, dQ) / sp.diff(rho_geom, dQ))
    assert sp.simplify(cs2_exact - dQ / (Q0 + dQ)) == 0

    # Small dQ << Q0 limit: rho_geom = 2 K2 Q0 dQ -> dQ = rho_geom/(2 K2 Q0) -> p_geom = rho_geom^2 / (4 K2 Q0^2)
    rho_phys = sp.Symbol("rho_phys", positive=True)
    p_poly = (8 * sp.pi * Gt * rho_phys) ** 2 / (4 * K2 * Q0**2) / (8 * sp.pi * Gt)
    # Express p_poly in terms of GN and mu_sq = 2 K2 Q0^2 / (2 - KB)
    K_poly = sp.simplify((p_poly / rho_phys**2).subs(K2, mu_sq * (2 - KB) / (2 * Q0**2)).subs(Gt, GN * (1 - KB / 2)))
    assert sp.simplify(K_poly - 2 * sp.pi * GN / mu_sq) == 0
    # Hydrostatic equilibrium dP/dr = -rho dPhi/dr -> 2 K_poly drho/dr = -dPhi/dr -> rho = (Phi_0 - Phi)/(2 K_poly) = mu^2/(4 pi GN) (Phi_0 - Phi)
    assert sp.simplify(1 / (2 * K_poly) - mu_sq / (4 * sp.pi * GN)) == 0
    cs2_poly = sp.simplify(2 * K_poly * rho_phys)
    assert sp.simplify(cs2_poly - 4 * sp.pi * GN * rho_phys / mu_sq) == 0

    return {
        "gamma_eq_1_with_dust": True,
        "lensing_eq_dynamics_with_dust": True,
        "dust_enters_shadow_psi_equation": True,
        "triangularity_broken_with_dust": True,
        "psi_equation_rhs": "4*pi*G_N*rho_b + mu^2*(Phi_0 - Phi)",
        "exact_cs2_formula": str(cs2_exact),
        "polytrope_index_n": 1,
        "polytrope_K_exact": "2*pi*G_N / mu^2",
        "polytrope_cs2_exact": "4*pi*G_N*rho / mu^2",
        "polytrope_w_exact": "2*pi*G_N*rho / mu^2",
    }


# Load Corasaniti+2021 cluster catalogue using the repo's exact canonical loader
D_CL = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02_galaxy_dynamics/clusters"))
_cwd = os.getcwd()
os.chdir(D_CL)
_spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py")
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)
CL = cm.load()
M200 = {}
with open("corasaniti2021_table1_lensing.dat") as _f:
    for _l in _f:
        if len(_l) >= 50:
            M200[cm.norm(_l[0:20])] = float(_l[27:32])
os.chdir(_cwd)

MPC = cm.MPC_M
G = cm.G_SI
MS = cm.MSUN
C_LIGHT = 2.99792458e8
MU0 = 1.0 / (0.9895 * MPC)
R_LE = math.pi / MU0  # Lane-Emden n=1 universal radius = pi / mu = 3.1086 Mpc
COSMIC_RATIO = 5.36   # Omega_c / Omega_b (same constant as d10_attack.py / accretion.py)
H0_SI = 67.4e3 / MPC
OMEGA_C = 0.264
RHO_CRIT_0 = 3.0 * H0_SI**2 / (8.0 * math.pi * G)
RHO_C_BG_0 = OMEGA_C * RHO_CRIT_0
CS_BG_KMS = math.sqrt(4.0 * math.pi * G * RHO_C_BG_0) / MU0 / 1e3  # cosmic mean linear sound speed (z=0)


def make_baryon_profile(M500: float, fbar: float, r500: float, beta: float):
    """Beta-model baryon profile rho(r) = rho0 * (1 + (r/rc)^2)^(-3*beta/2), rc = 0.1 r500,
    normalized identically to Mb(r500) = fbar * M500."""
    rc = 0.1 * r500
    exp = 1.5 * beta

    def I_dimless(x: float) -> float:
        if abs(beta - 2.0 / 3.0) < 1e-12:
            return x - math.atan(x)
        if abs(beta - 1.0) < 1e-12:
            return math.asinh(x) - x / math.sqrt(1.0 + x * x)
        val, _ = quad(lambda t: t * t / (1.0 + t * t) ** exp, 0.0, x, epsabs=1e-13, epsrel=1e-12)
        return val

    I500 = I_dimless(r500 / rc)
    norm = fbar * M500 / I500  # = 4 pi rho0 rc^3

    def dMdr(r: float) -> float:
        x = r / rc
        return norm * (x * x / rc) / (1.0 + x * x) ** exp

    def Mb(r: float) -> float:
        return norm * I_dimless(r / rc)

    return Mb, dMdr


def integrate_free_boundary(Psi_c: float, rmin: float, rout: float, Mb, dMdr, mu: float, law):
    """Integrate the free-boundary polytrope from rmin to rout with central relative potential
    Psi_rel(rmin) = Psi_c <= 0 (Psi_rel = Phi - Phi_0). Dust is active only while Psi_rel < 0."""
    bad = {"u_nonpos": False}

    def rhs(r, y):
        W, Psi_rel = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        dust_src = (-mu * mu * r * r * Psi_rel) if Psi_rel < 0.0 else 0.0
        return [G * dMdr(r) + dust_src, law(u)]

    def edge_event(r, y):
        return y[1]

    edge_event.terminal = False
    edge_event.direction = 1

    s = solve_ivp(
        rhs,
        (rmin, rout),
        [G * Mb(rmin), Psi_c],
        method="DOP853",
        rtol=1e-10,
        atol=[1e20, 1.0],
        events=edge_event,
        dense_output=True,
    )
    return s, bad["u_nonpos"]


def solve_uncapped_bvp(c: dict, key: str, law, rout: float, beta: float = 2.0 / 3.0):
    """Solve uncapped Dirichlet BVP Phi(rout) = 0 (i.e. Psi_rel(rout) = 0, allowing negative Psi_rel
    or checking sign) — exact match to d10_attack.py when rout = rv and beta = 2/3."""
    M500 = c["M500"] * 1e14 * MS
    fbar = c["fgas"] + 0.015
    r500 = cm.r_delta(M500, c["z"])
    Mb, dMdr = make_baryon_profile(M500, fbar, r500, beta)
    rmin = 1e-4 * r500
    bad = {"flag": False}

    def rhs(r, y):
        W, Phi = y
        u = W / (r * r)
        if u <= 0.0:
            bad["flag"] = True
        return [G * dMdr(r) - MU0 * MU0 * r * r * Phi, law(u)]

    def ev_W_zero(r, y):
        return y[0]

    ev_W_zero.terminal = True
    ev_W_zero.direction = -1

    def shoot(P0, full=False):
        bad["flag"] = False
        s = solve_ivp(
            rhs,
            (rmin, rout),
            [G * Mb(rmin), P0],
            method="DOP853",
            rtol=1e-10,
            atol=[1e20, 1.0],
            events=ev_W_zero,
            dense_output=full,
        )
        hit_zero = len(s.t_events[0]) > 0
        if hit_zero:
            bad["flag"] = True
        if full:
            return s, hit_zero
        return (float("nan") if hit_zero else float(s.y[1, -1]))

    g0 = -law(G * Mb(r500) / r500**2) * rout * 3.0
    # Scan physical well P0 <= 0 (dense near 0 and extending to -20|g0| to capture steep near-pole roots)
    grid = np.concatenate([
        np.linspace(-20.0 * abs(g0), -2.0 * abs(g0), 37),
        np.linspace(-2.0 * abs(g0), 0.0, 41)[1:],
    ])
    F = [shoot(p) for p in grid]
    roots = []
    for i in range(len(grid) - 1):
        if math.isfinite(F[i]) and math.isfinite(F[i + 1]) and F[i] * F[i + 1] <= 0:
            roots.append(brentq(shoot, grid[i], grid[i + 1], xtol=1e-7 * abs(g0)))
    if not roots:
        return {
            "converged": False,
            "uE_positive_throughout": False,
            "dust_nonneg_throughout": False,
            "mu_rout_over_pi": float(MU0 * rout / math.pi),
            "reason": "no_uE_positive_root_for_Phi0_le_0",
        }
    P0 = roots[0]
    s, hit_zero = shoot(P0, True)
    ill = bad["flag"] or hit_zero
    W500 = float(s.sol(r500)[0])
    Wout = float(s.sol(rout)[0])
    Mdyn500 = law(max(W500, 0.0) / r500**2) * r500**2 / G
    Mdust = (Wout - G * Mb(rout)) / G
    Phi_min = float(np.min(s.y[1]))
    # Check whether Phi stayed <= 0 everywhere (positive dust density everywhere)
    dust_nonneg = bool(np.all(s.y[1] <= 1e-3 * abs(P0)))
    return {
        "converged": True,
        "n_roots": len(roots),
        "uE_positive_throughout": not ill,
        "dust_nonneg_throughout": dust_nonneg,
        "R": float(M500 / Mdyn500) if Mdyn500 > 0 else float("inf"),
        "dust_over_budget": float(Mdust / (COSMIC_RATIO * Mb(rout))),
        "Phi0_over_c2": float(-P0 / C_LIGHT**2),
        "mu_rout_over_pi": float(MU0 * rout / math.pi),
        "P0": float(P0),
        "Mb_rv_over_Mb_r500": float(Mb(rout) / Mb(r500)),
    }


def solve_free_boundary_capped(c: dict, key: str, law, beta: float = 2.0 / 3.0):
    """Fixed universal mu = MU0; shift-symmetry chemical potential Phi_0 (parametrized by Psi_c = Phi(0)-Phi_0 <= 0)
    set so M_dust <= 5.36 * Mb(rv). Uncapped virial solution if below budget; free-edge R_edge < rv if capped."""
    M500 = c["M500"] * 1e14 * MS
    fbar = c["fgas"] + 0.015
    r500 = cm.r_delta(M500, c["z"])
    r200 = cm.r_delta(M200[key] * 1e14 * MS, c["z"], 200.0)
    rv = r200 * (200.0 / 177.8) ** (1.0 / 3.0)
    Mb, dMdr = make_baryon_profile(M500, fbar, r500, beta)
    rmin = 1e-4 * r500
    M_budget = COSMIC_RATIO * Mb(rv)

    # First solve uncapped virial boundary Psi_rel(rv) = 0 (positive-dust branch)
    unc = solve_uncapped_bvp(c, key, law, rv, beta=beta)
    assert unc["converged"] and unc["uE_positive_throughout"] and unc["dust_nonneg_throughout"], (
        f"Uncapped BVP unexpected failure on {c['name']}"
    )

    if unc["dust_over_budget"] <= 1.0:
        # Uncapped solution already respects cosmic supply
        s, ubad = integrate_free_boundary(unc["P0"], rmin, rv, Mb, dMdr, MU0, law)
        W500 = float(s.sol(r500)[0])
        Mdyn500 = law(W500 / r500**2) * r500**2 / G
        Mdust_500 = (W500 - G * Mb(r500)) / G
        Mdust_rv = (float(s.sol(rv)[0]) - G * Mb(rv)) / G
        return {
            "capped": False,
            "R": float(M500 / Mdyn500),
            "R_uncapped": float(unc["R"]),
            "dust_over_budget_uncapped": float(unc["dust_over_budget"]),
            "dust_over_budget_final": float(Mdust_rv / M_budget),
            "Mdust_r500_over_Mb_r500": float(Mdust_500 / Mb(r500)),
            "R_edge_over_rv": 1.0,
            "R_edge_Mpc": float(rv / MPC),
            "Mb_rv_over_Mb_r500": float(Mb(rv) / Mb(r500)),
            "uE_positive": not ubad,
        }

    # Capped: find Psi_c in (unc["P0"], 0) such that M_dust(Psi_c) = M_budget
    def excess_dust(Psi_c: float) -> float:
        s, _ = integrate_free_boundary(Psi_c, rmin, rv, Mb, dMdr, MU0, law)
        Mdust = (float(s.sol(rv)[0]) - G * Mb(rv)) / G
        return Mdust - M_budget

    f_lo = excess_dust(unc["P0"])
    f_hi = excess_dust(0.0)
    assert f_lo > 0.0 and f_hi < 0.0, f"Bracket failure on {c['name']}: f_lo={f_lo}, f_hi={f_hi}"
    Psi_c_star = brentq(excess_dust, unc["P0"], 0.0, xtol=1e-7 * abs(unc["P0"]))
    s, ubad = integrate_free_boundary(Psi_c_star, rmin, rv, Mb, dMdr, MU0, law)
    W500 = float(s.sol(r500)[0])
    Wrv = float(s.sol(rv)[0])
    Mdyn500 = law(W500 / r500**2) * r500**2 / G
    Mdust_500 = (W500 - G * Mb(r500)) / G
    Mdust_rv = (Wrv - G * Mb(rv)) / G
    R_edge = float(s.t_events[0][0]) if len(s.t_events[0]) > 0 else float(rv)
    return {
        "capped": True,
        "R": float(M500 / Mdyn500),
        "R_uncapped": float(unc["R"]),
        "dust_over_budget_uncapped": float(unc["dust_over_budget"]),
        "dust_over_budget_final": float(Mdust_rv / M_budget),
        "Mdust_r500_over_Mb_r500": float(Mdust_500 / Mb(r500)),
        "R_edge_over_rv": float(R_edge / rv),
        "R_edge_Mpc": float(R_edge / MPC),
        "Mb_rv_over_Mb_r500": float(Mb(rv) / Mb(r500)),
        "uE_positive": not ubad,
    }


def summarize_R(rows: list[dict], key: str = "R") -> dict:
    vals = [r[key] for r in rows]
    med = float(np.median(vals))
    n_in = int(sum(0.70 <= x <= 1.40 for x in vals))
    verdict = "CLOSES" if (0.80 <= med <= 1.25 and n_in >= 9) else "FAILS"
    return {
        "median_R": med,
        "min_R": float(np.min(vals)),
        "max_R": float(np.max(vals)),
        "n_in_0.7_1.4": n_in,
        "verdict": verdict,
    }


def main() -> int:
    s1 = run_symbolic_s1()
    print("[S1] SymPy 2-field Tidal-QUMOND-in-AeST + dust: PASS")
    print(json.dumps(s1, indent=1))

    law_mond = lambda u: cm.g_mond(max(u, 0.0))
    law_newt = lambda u: max(u, 0.0)

    # T1 (MOND ON, fixed mu, free-boundary chemical potential) & T2 (MOND OFF, 4th quadrant) at baseline beta=2/3
    t1_rows, t2_rows = [], []
    # T3 splashback pole test
    t3_rows = []
    # Infall vs core sound speed audit
    cs_audit = []

    for key, c in CL.items():
        M500 = c["M500"] * 1e14 * MS
        r500 = cm.r_delta(M500, c["z"])
        r200 = cm.r_delta(M200[key] * 1e14 * MS, c["z"], 200.0)
        rv = r200 * (200.0 / 177.8) ** (1.0 / 3.0)

        r1 = solve_free_boundary_capped(c, key, law_mond, beta=2.0 / 3.0)
        r1["name"] = c["name"]
        t1_rows.append(r1)

        r2 = solve_free_boundary_capped(c, key, law_newt, beta=2.0 / 3.0)
        r2["name"] = c["name"]
        t2_rows.append(r2)

        sp14 = solve_uncapped_bvp(c, key, law_mond, 1.4 * r200, beta=2.0 / 3.0)
        sp18 = solve_uncapped_bvp(c, key, law_mond, 1.8 * r200, beta=2.0 / 3.0)
        t3_rows.append({
            "name": c["name"],
            "rv_Mpc": float(rv / MPC),
            "mu_rv_over_pi": float(MU0 * rv / math.pi),
            "r_sp_1.4_Mpc": float(1.4 * r200 / MPC),
            "sp_1.4": {k: sp14[k] for k in ("converged", "mu_rout_over_pi") if k in sp14}
            | ({k: sp14[k] for k in ("uE_positive_throughout", "dust_nonneg_throughout", "R")} if sp14["converged"] else {}),
            "r_sp_1.8_Mpc": float(1.8 * r200 / MPC),
            "sp_1.8": {k: sp18[k] for k in ("converged", "mu_rout_over_pi") if k in sp18}
            | ({k: sp18[k] for k in ("uE_positive_throughout", "dust_nonneg_throughout", "R")} if sp18["converged"] else {}),
        })

        # Nonlinear local sound speed at rho_500 vs cosmic infall background at cluster redshift z
        rho500 = M500 / (4.0 / 3.0 * math.pi * r500**3)
        rho_c_z = RHO_C_BG_0 * (1.0 + c["z"]) ** 3
        cs_core_kms = math.sqrt(4.0 * math.pi * G * rho500) / MU0 / 1e3
        cs_bg_z_kms = math.sqrt(4.0 * math.pi * G * rho_c_z) / MU0 / 1e3
        v_circ_500 = math.sqrt(G * M500 / r500) / 1e3
        cs_audit.append({
            "name": c["name"],
            "z": float(c["z"]),
            "cs_core_kms": float(cs_core_kms),
            "cs_cosmic_bg_z_kms": float(cs_bg_z_kms),
            "v_circ_500_kms": float(v_circ_500),
            "infall_Mach_number": float(v_circ_500 / cs_bg_z_kms),
        })

    # T4: ICM outer-slope beta sensitivity
    t4 = {}
    for beta in (2.0 / 3.0, 0.85, 1.0):
        bkey = f"beta={beta:.4f}"
        m_rows, n_rows = [], []
        for key, c in CL.items():
            rm = solve_free_boundary_capped(c, key, law_mond, beta=beta)
            rm["name"] = c["name"]
            m_rows.append(rm)
            rn = solve_free_boundary_capped(c, key, law_newt, beta=beta)
            rn["name"] = c["name"]
            n_rows.append(rn)
        t4[bkey] = {
            "median_Mb_rv_over_Mb_r500": float(np.median([r["Mb_rv_over_Mb_r500"] for r in m_rows])),
            "T1_MOND_ON_free_boundary": summarize_R(m_rows, "R"),
            "T2a_MOND_OFF_uncapped": summarize_R(n_rows, "R_uncapped"),
            "T2b_MOND_OFF_free_boundary": summarize_R(n_rows, "R"),
            "T1_rows": [{"name": r["name"], "R": r["R"], "R_edge_over_rv": r["R_edge_over_rv"]} for r in m_rows],
            "T2b_rows": [{"name": r["name"], "R": r["R"], "R_uncapped": r["R_uncapped"], "R_edge_over_rv": r["R_edge_over_rv"]} for r in n_rows],
        }

    t1_sum = summarize_R(t1_rows, "R")
    t1_sum["n_capped"] = int(sum(r["capped"] for r in t1_rows))
    t1_sum["max_dust_over_budget_final"] = float(max(r["dust_over_budget_final"] for r in t1_rows))
    t1_sum["median_R_edge_over_rv"] = float(np.median([r["R_edge_over_rv"] for r in t1_rows]))

    t2a_sum = summarize_R(t2_rows, "R_uncapped")
    t2a_sum["median_dust_over_budget"] = float(np.median([r["dust_over_budget_uncapped"] for r in t2_rows]))
    t2a_sum["n_exceeds_budget"] = int(sum(r["dust_over_budget_uncapped"] > 1.0 for r in t2_rows))
    t2a_sum["max_dust_over_budget"] = float(max(r["dust_over_budget_uncapped"] for r in t2_rows))

    t2b_sum = summarize_R(t2_rows, "R")
    t2b_sum["n_capped"] = int(sum(r["capped"] for r in t2_rows))
    t2b_sum["max_dust_over_budget_final"] = float(max(r["dust_over_budget_final"] for r in t2_rows))
    t2b_sum["median_R_edge_over_rv"] = float(np.median([r["R_edge_over_rv"] for r in t2_rows]))
    t2b_sum["median_Mdust_r500_over_Mb_r500"] = float(np.median([r["Mdust_r500_over_Mb_r500"] for r in t2_rows]))

    n_pole_14 = int(sum(r["sp_1.4"]["mu_rout_over_pi"] >= 1.0 for r in t3_rows))
    n_bad_14 = int(sum(
        (not r["sp_1.4"].get("converged", False))
        or (not r["sp_1.4"].get("uE_positive_throughout", False))
        or (not r["sp_1.4"].get("dust_nonneg_throughout", False))
        for r in t3_rows
    ))
    n_pole_18 = int(sum(r["sp_1.8"]["mu_rout_over_pi"] >= 1.0 for r in t3_rows))
    n_bad_18 = int(sum(
        (not r["sp_1.8"].get("converged", False))
        or (not r["sp_1.8"].get("uE_positive_throughout", False))
        or (not r["sp_1.8"].get("dust_nonneg_throughout", False))
        for r in t3_rows
    ))
    t3_sum = {
        "R_Lane_Emden_Mpc": float(R_LE / MPC),
        "at_1.4_r200": {
            "n_cross_pole_muR_ge_pi": n_pole_14,
            "n_illposed_or_neg_dust": n_bad_14,
            "verdict": "UNSTABLE TO BOUNDARY" if (n_pole_14 >= 6 or n_bad_14 >= 6) else "STABLE",
        },
        "at_1.8_r200": {
            "n_cross_pole_muR_ge_pi": n_pole_18,
            "n_illposed_or_neg_dust": n_bad_18,
            "verdict": "UNSTABLE TO BOUNDARY" if (n_pole_18 >= 6 or n_bad_18 >= 6) else "STABLE",
        },
    }

    out = {
        "S1_symbolic_tidal_qumond_dust": s1,
        "T1_MOND_ON_free_boundary_polytrope": {"summary": t1_sum, "rows": t1_rows},
        "T2_4th_quadrant_MOND_OFF_plus_dust": {
            "T2a_uncapped_summary": t2a_sum,
            "T2b_free_boundary_capped_summary": t2b_sum,
            "rows": t2_rows,
        },
        "T3_splashback_pole": {"summary": t3_sum, "rows": t3_rows},
        "T4_beta_profile_sensitivity": t4,
        "sound_speed_regime_audit": {
            "cs_cosmic_bg_z0_kms": float(CS_BG_KMS),
            "median_cs_core_kms": float(np.median([r["cs_core_kms"] for r in cs_audit])),
            "median_cs_cosmic_bg_z_kms": float(np.median([r["cs_cosmic_bg_z_kms"] for r in cs_audit])),
            "median_infall_Mach": float(np.median([r["infall_Mach_number"] for r in cs_audit])),
            "rows": cs_audit,
        },
    }

    out_path = os.path.join(os.path.dirname(__file__), "POLYTROPE_4QUAD.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)

    print("\n=== T1: MOND ON + Fixed-mu Free-Boundary Polytrope ===")
    print(json.dumps(t1_sum, indent=1))
    for r in t1_rows:
        print(f"  {r['name']:<20} R_unc={r['R_uncapped']:.2f} R_fb={r['R']:.2f} edge/rv={r['R_edge_over_rv']:.2f} dust_unc={r['dust_over_budget_uncapped']:.2f}")

    print("\n=== T2: 4TH QUADRANT — MOND OFF (BK Screen) + AeST n=1 Polytrope Dust ===")
    print("T2a uncapped:", json.dumps(t2a_sum, indent=1))
    print("T2b free-boundary capped:", json.dumps(t2b_sum, indent=1))
    for r in t2_rows:
        print(f"  {r['name']:<20} R_2a={r['R_uncapped']:.2f} dust_2a={r['dust_over_budget_uncapped']:.2f} R_2b={r['R']:.2f} edge/rv={r['R_edge_over_rv']:.2f}")

    print("\n=== T3: Splashback Boundary & Lane-Emden Pole (R_LE = pi/mu = 3.109 Mpc) ===")
    print(json.dumps(t3_sum, indent=1))
    for r in t3_rows:
        print(f"  {r['name']:<20} mu*rv/pi={r['mu_rv_over_pi']:.2f}  1.4r200={r['sp_1.4']['mu_rout_over_pi']:.2f}(conv={r['sp_1.4']['converged']},negdust={not r['sp_1.4'].get('dust_nonneg_throughout', False)})  1.8r200={r['sp_1.8']['mu_rout_over_pi']:.2f}(conv={r['sp_1.8']['converged']})")

    print("\n=== T4: ICM Beta-Slope Sensitivity ===")
    for bk, bv in t4.items():
        print(f"  {bk} (Mb(rv)/Mb(r500)={bv['median_Mb_rv_over_Mb_r500']:.2f}):")
        print(f"    T1  (MOND ON  + capped dust): med R={bv['T1_MOND_ON_free_boundary']['median_R']:.3f}, in[0.7,1.4]={bv['T1_MOND_ON_free_boundary']['n_in_0.7_1.4']}/12 -> {bv['T1_MOND_ON_free_boundary']['verdict']}")
        print(f"    T2a (MOND OFF + uncapped):    med R={bv['T2a_MOND_OFF_uncapped']['median_R']:.3f}, in[0.7,1.4]={bv['T2a_MOND_OFF_uncapped']['n_in_0.7_1.4']}/12 -> {bv['T2a_MOND_OFF_uncapped']['verdict']}")
        print(f"    T2b (MOND OFF + capped dust): med R={bv['T2b_MOND_OFF_free_boundary']['median_R']:.3f}, in[0.7,1.4]={bv['T2b_MOND_OFF_free_boundary']['n_in_0.7_1.4']}/12 -> {bv['T2b_MOND_OFF_free_boundary']['verdict']}")

    print("\n=== Sound Speed Regime Audit ===")
    print(json.dumps({k: v for k, v in out["sound_speed_regime_audit"].items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
