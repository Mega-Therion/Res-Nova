#!/usr/bin/env python3
"""
Hill-sphere barycentric matching BVP for the single-metric AeST/QUMOND Cassini quadrupole Q_2 (2026-11-21).

PRE-REGISTRATION (frozen before solving):
  1. Metric & Field Equations (single-metric AeST weak-field limit, Psi == Phi):
       ds^2 = -(1 + 2 Phi) dt^2 + (1 - 2 Psi) dx^2,   Psi = Phi,   G_N = G_tilde / (1 - K_B / 2).
       Phi = Phi_N + phi,   lap(Phi_N) = 4 pi G_N rho,   lap(phi) = -div[(nu(|g_N| / a_0) - 1) g_N],
       with nu = nu_2 (exact inverse of live mu_std(x) = x / sqrt(1 + x^2)), and NO fitted parameter.
  2. Barycentric Frame & Fermi-Coordinate Distinction:
       Solar-system barycentric coordinates x centered on the Sun with +z toward the Galactic Center
       at R_GC = R_sun z_hat (g_N = -G M_sun x / r^3 + g_e z_hat + g_tide,MW(x)).
       A free-falling Fermi frame removes a constant external acceleration g_e from a LINEAR Poisson
       equation (lap(Phi_N + g_e z) = lap(Phi_N)), leaving only the Milky Way tide O(v_circ^2 / R_sun^2),
       but it does NOT remove g_e from the nonlinear interpolating function nu(|grad Phi_N| / a_0).
  3. Domain & Computed Hill Radius:
       Radial domain r in [0.2 AU, R_Hill], with R_Hill computed directly in code from R_sun, v_circ,
       and G M_sun via:
           M_MW = v_circ^2 R_sun / G,   M_sun = GM_sun / G,   R_Hill = R_sun * (M_sun / (3 M_MW))^(1/3).
       Outer boundary at R_Hill: Milky Way tidal potential plus constant g_e in barycentric coordinates.
  4. Exact Q_2 Definition & Empirical Cap:
       Same definition as 02_galaxy_dynamics/qumond_axisym_efe.py and audits/2026-11-19/cassini_ge_uncertainty_band.py
       (Hees et al. 2014 Eq. 6):
           Phi_tot(x) = -GM_sun / r - g_e z - (Q_2 / 2) x^i x^j (e_i e_j - delta_ij / 3) + ...
                      = -GM_sun / r - g_e z - (Q_2 / 3) r^2 P_2(cos theta) + ...
           Q_2(r_Sat) = -3 c_2(r_Sat) a_0 / r_M  evaluated at r_Sat = 9.5 AU, r_M = sqrt(GM_sun / a_0).
       Scored against the 5.2e-27 s^-2 cap (+2 sigma bound of Park et al. 2026, arXiv:2602.17884,
       Q_2 = (1.6 +/- 1.8)e-27 s^-2).
       Control & scoring rule: a linear (nu == 1) control rerun must recover the Newtonian Milky Way
       tide Omega_0^2 = v_circ^2 / R_sun^2 (~ 7.560e-31 s^-2; Q_2,tide = 3 Omega_0^2 ~ 2.268e-30 s^-2),
       which is NOT a Cassini pass. The nonlinear single-metric scalar rerun is the one scored.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import solve_banded
from scipy.special import eval_legendre
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "02_galaxy_dynamics"))
import qumond_axisym_efe as qe  # noqa: E402

AU_M = 1.495978707e11
KPC_M = 3.085677581491367e19
PC_M = KPC_M / 1000.0
GM_SUN = float(qe.GM)
G_SI = 6.67430e-11

R_MIN_AU = 0.2
R_SAT_AU = 9.5
R_SUN_KPC = 8.2
R_SUN_M = R_SUN_KPC * KPC_M
V_CIRC_NOMINAL = 220.0e3  # m/s

Q2_PARK_MEAN = 1.6e-27
Q2_PARK_SIG = 1.8e-27
Q2_CAP_2SIG = Q2_PARK_MEAN + 2.0 * Q2_PARK_SIG  # 5.2e-27 s^-2

A0_BASES = [
    ("derived_cH0_2pi", float(qe.A0_DERIVED)),
    ("sparc_S2_real_eD", 1.1205e-10),
    ("sparc_T1_legacy", float(qe.A0_FIT)),
]
GE_GRID = [1.5e-10, 1.7e-10, 1.9e-10, 2.1e-10, 2.3e-10]


def make_linear_nu():
    """Control interpolating function nu(y) == 1 identically (Newtonian linear Poisson)."""
    def nu(y):
        arr = np.asarray(y, dtype=float)
        return 1.0 if arr.ndim == 0 else np.ones_like(arr)

    def minus_1(y):
        arr = np.asarray(y, dtype=float)
        return 0.0 if arr.ndim == 0 else np.zeros_like(arr)

    nu.minus_1 = minus_1
    return nu


def run_sympy_checks() -> dict:
    """Verify single-metric AeST flux reduction and non-removal of g_e in Fermi coordinates."""
    # 1. Exact Euler-Lagrange single-metric static check (normalization_kb.py)
    r, Gt, a0, KB = sp.symbols("r Gt a0 K_B", positive=True)
    gN = sp.Function("gN")(r)
    Fp = sp.Function("Fp")
    u = gN**2 / a0**2
    GN = Gt / (1 - KB / 2)
    P1 = gN * (1 + Fp(u))
    S1 = P1
    ph1 = P1 - gN
    ps1 = -gN
    rho = -sp.diff(r**2 * gN, r) / (4 * sp.pi * GN * r**2)
    k, m, n = KB / 2, 2 - KB, (2 - KB) / 2
    dL_dPhi1 = r**2 * (-2 * S1 + 2 * k * P1 + m * ph1) / (8 * sp.pi * Gt)
    dL_dPsi1 = r**2 * (2 * S1 - 2 * P1) / (8 * sp.pi * Gt)
    dL_dph1 = r**2 * (m * P1 - 2 * n * ph1 + 2 * n * ps1) / (8 * sp.pi * Gt)
    dL_dps1 = r**2 * (2 * n * ph1 + 2 * n * Fp(u) * ps1) / (8 * sp.pi * Gt)
    el_resids = {
        "Phi": sp.simplify(r**2 * rho - sp.diff(dL_dPhi1, r)),
        "Psi": sp.simplify(-sp.diff(dL_dPsi1, r)),
        "phi": sp.simplify(-sp.diff(dL_dph1, r)),
        "psi": sp.simplify(-sp.diff(dL_dps1, r)),
    }
    for name, expr in el_resids.items():
        assert expr == 0, f"Euler-Lagrange residual {name} nonzero: {expr}"

    # 2. Fermi-frame test: constant g_e drops out of linear Laplacian, NOT out of |grad Phi|
    x, y, z, gm_s, g_e_sym, a0_sym = sp.symbols("x y z GM g_e a_0", positive=True)
    Phi_fermi = -gm_s / sp.sqrt(x**2 + y**2 + z**2)
    Phi_bary = Phi_fermi - g_e_sym * z
    lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
    grad_sq = lambda f: sp.diff(f, x) ** 2 + sp.diff(f, y) ** 2 + sp.diff(f, z) ** 2

    lin_lap_diff = sp.simplify(lap(Phi_bary) - lap(Phi_fermi))
    assert lin_lap_diff == 0

    grad_sq_diff = sp.simplify(grad_sq(Phi_bary) - grad_sq(Phi_fermi))
    assert grad_sq_diff != 0
    # Check at equatorial/polar test point (x=0, y=0, z=r) where g_e enters nu(|grad Phi|/a0) directly
    z_pos = sp.Symbol("r", positive=True)
    nu_bary_on_z = sp.sqrt(1 + 4 * a0_sym**2 / (grad_sq(Phi_bary).subs({x: 0, y: 0, z: z_pos})))
    nu_fermi_on_z = sp.sqrt(1 + 4 * a0_sym**2 / (grad_sq(Phi_fermi).subs({x: 0, y: 0, z: z_pos})))
    assert sp.simplify(nu_bary_on_z - nu_fermi_on_z) != 0

    return {
        "euler_lagrange_residuals": {k: int(v) for k, v in el_resids.items()},
        "Psi_equals_Phi": True,
        "G_N_formula": str(sp.simplify(GN)),
        "fermi_linear_laplacian_difference": str(lin_lap_diff),
        "fermi_nonlinear_grad_sq_difference": str(grad_sq_diff),
        "fermi_removes_ge_from_linear_poisson": True,
        "fermi_removes_ge_from_nonlinear_nu": False,
    }


def compute_hill_geometry(g_e: float, R_sun_m: float = R_SUN_M) -> dict:
    """Compute M_MW, R_Hill = R_sun * (M_sun / (3 M_MW))^(1/3), and tidal Omega0^2 from fundamentals."""
    v_circ = math.sqrt(g_e * R_sun_m)
    M_mw = (v_circ**2 * R_sun_m) / G_SI
    M_sun = GM_SUN / G_SI
    R_hill_m = R_sun_m * (M_sun / (3.0 * M_mw)) ** (1.0 / 3.0)
    Omega0_sq = (v_circ**2) / (R_sun_m**2)
    return {
        "g_e_mps2": g_e,
        "R_sun_m": R_sun_m,
        "R_sun_kpc": R_sun_m / KPC_M,
        "v_circ_mps": v_circ,
        "v_circ_kms": v_circ / 1e3,
        "M_sun_kg": M_sun,
        "M_MW_enclosed_kg": M_mw,
        "R_Hill_m": R_hill_m,
        "R_Hill_au": R_hill_m / AU_M,
        "R_Hill_pc": R_hill_m / PC_M,
        "Omega0_sq_s2": Omega0_sq,
        "Q2_tide_newtonian_s2": 3.0 * Omega0_sq,
    }


def _flux_AB_hill(nu_fn, nue: float, ye: float, tau_N: float, r: np.ndarray, th: np.ndarray, w: np.ndarray, l: int, include_tide_in_gN: bool):
    """Legendre projections A_l(r), B_l(r) of V on the Hill-sphere barycentric Newtonian field."""
    st, ct = np.sin(th), np.cos(th)
    mu = ct
    R = r[:, None]

    gx = -st / (R**2)
    gz = -ct / (R**2) + ye
    if include_tide_in_gN:
        gx = gx - tau_N * R * st
        gz = gz + 2.0 * tau_N * R * ct

    y = np.hypot(gx, gz)
    f = nu_fn.minus_1(y)

    P2 = 0.5 * (3.0 * ct**2 - 1.0)
    tide_r = (2.0 * tau_N * R * P2) if include_tide_in_gN else 0.0
    tide_t = (-3.0 * tau_N * R * st * ct) if include_tide_in_gN else 0.0

    # V = (nu - 1) g_N + (1 - nu_e) g_MW; (-x/r^3)*(1 - nu_e) is pure l=0 and divergence-free off origin.
    k_coef = 1.0 - nue
    Vr = f * (gx * st + gz * ct) + k_coef * (ye * ct + tide_r)
    Vt = f * (gx * ct - gz * st) + k_coef * (-ye * st + tide_t)

    Pl = eval_legendre(l, mu)
    dPl = qe._legendre_deriv(l, mu)
    wt = w * st
    A = (2 * l + 1) / 2.0 * (Vr * Pl) @ wt
    B = (2 * l + 1) / 2.0 * (Vt * st * dPl) @ wt
    return A, B


def solve_hill_l2_bvp(
    nu_fn,
    a0: float,
    g_e: float,
    R_sun_m: float = R_SUN_M,
    r_min_au: float = R_MIN_AU,
    n_r: int = 1500,
    n_th: int = 300,
    bc: str = "dirichlet",
    include_tide_in_gN: bool = True,
    is_linear: bool = False,
) -> dict:
    """Solve the axisymmetric l=2 BVP on r in [r_min_au, R_Hill] in solar barycentric coordinates."""
    geom = compute_hill_geometry(g_e, R_sun_m=R_sun_m)
    R_hill_m = geom["R_Hill_m"]
    r_M = math.sqrt(GM_SUN / a0)
    eta = g_e / a0

    if is_linear:
        ye = eta
        nue = 1.0
    else:
        ye = float(qe.y_external(nu_fn, eta))
        nue = float(nu_fn(ye))

    tau_N = ye * r_M / R_sun_m
    tau_tot = nue * tau_N

    r_min_dim = (r_min_au * AU_M) / r_M
    r_max_dim = R_hill_m / r_M
    r_sat_dim = (R_SAT_AU * AU_M) / r_M

    s = np.linspace(math.log(r_min_dim), math.log(r_max_dim), n_r)
    h = float(s[1] - s[0])
    x, wx = np.polynomial.legendre.leggauss(n_th)
    th = 0.5 * np.pi * (x + 1.0)
    w = 0.5 * np.pi * wx

    sh = np.concatenate([[s[0] - 0.5 * h], 0.5 * (s[1:] + s[:-1]), [s[-1] + 0.5 * h]])
    Ah = np.empty_like(sh)
    for i in range(0, len(sh), 512):
        Ah[i:i + 512], _ = _flux_AB_hill(
            nu_fn, nue, ye, tau_N, np.exp(sh[i:i + 512]), th, w, 2, include_tide_in_gN
        )
    Bn = np.empty_like(s)
    for i in range(0, len(s), 512):
        _, Bn[i:i + 512] = _flux_AB_hill(
            nu_fn, nue, ye, tau_N, np.exp(s[i:i + 512]), th, w, 2, include_tide_in_gN
        )

    Fh = np.exp(2.0 * sh) * Ah
    rhs = -np.exp(-s) * (Fh[1:] - Fh[:-1]) / h - np.exp(s) * Bn

    L = 6.0  # l * (l + 1) for l = 2
    lo = 1.0 / (h**2) - 1.0 / (2.0 * h)
    di = -2.0 / (h**2) - L
    up = 1.0 / (h**2) + 1.0 / (2.0 * h)

    ab = np.zeros((3, n_r))
    ab[0, 1:] = up
    ab[1, :] = di
    ab[2, :-1] = lo

    # Inner regularity BC at r_min = 0.2 AU: u_2 ~ r^2 => u'_s = 2 u => u_{-1} = u_1 - 4 h u_0
    ab[1, 0] = di - lo * 4.0 * h
    ab[0, 1] = up + lo

    # Outer Milky Way tidal potential at r = R_Hill: u_{2,MW}(R_Hill) = -tau_tot * r_max^2
    u2_mw_hill = -tau_tot * (r_max_dim**2)
    if bc == "dirichlet":
        ab[2, -2] = 0.0
        ab[1, -1] = 1.0
        rhs[-1] = u2_mw_hill
    elif bc == "robin":
        # Incoming u_2(r) = u_{2,MW}(r) + C r^-3 => r (u - u_MW)' + 3 (u - u_MW) = 0
        # Since r d/dr(r^2) = 2 r^2: u_s' + 3 u = 5 u_MW => u_N = u_{N-2} - 6 h u_{N-1} + 10 h u_MW
        ab[2, -2] = lo + up
        ab[1, -1] = di - 6.0 * h * up
        rhs[-1] = rhs[-1] - 10.0 * h * up * u2_mw_hill
    else:
        raise ValueError(f"Unknown bc: {bc}")

    u2 = solve_banded((1, 1), ab, rhs)
    c2_grid = u2 * np.exp(-2.0 * s)

    s_sat = math.log(r_sat_dim)
    assert s[0] < s_sat < s[-1], "r_Sat outside radial grid"
    c2_sat = float(np.interp(s_sat, s, c2_grid))
    Q2_sat = -3.0 * c2_sat * a0 / r_M

    diag_radii_au = [5.2, 9.5, 30.0, 70.0]
    diag_q2 = {}
    for r_au in diag_radii_au:
        c2_r = float(np.interp(math.log((r_au * AU_M) / r_M), s, c2_grid))
        diag_q2[str(r_au)] = -3.0 * c2_r * a0 / r_M

    return {
        "geom": geom,
        "r_M_m": r_M,
        "r_M_au": r_M / AU_M,
        "r_min_au": r_min_au,
        "r_Hill_over_rM": r_max_dim,
        "ye": ye,
        "nue": nue,
        "tau_N": tau_N,
        "tau_tot": tau_tot,
        "c2_sat": c2_sat,
        "Q2_sat_s2": Q2_sat,
        "neg_c2_phys_s2": -c2_sat * a0 / r_M,
        "diag_Q2_s2": diag_q2,
    }


def Q2_hill_richardson(
    nu_fn,
    a0: float,
    g_e: float,
    n_r: int = 1500,
    n_th: int = 300,
    bc: str = "dirichlet",
    include_tide_in_gN: bool = True,
    is_linear: bool = False,
) -> dict:
    """Two-resolution (h, h/2) second-order Richardson extrapolation on the Hill domain."""
    c_res = solve_hill_l2_bvp(
        nu_fn, a0, g_e, n_r=n_r, n_th=n_th, bc=bc, include_tide_in_gN=include_tide_in_gN, is_linear=is_linear
    )
    f_res = solve_hill_l2_bvp(
        nu_fn, a0, g_e, n_r=2 * n_r - 1, n_th=2 * n_th, bc=bc, include_tide_in_gN=include_tide_in_gN, is_linear=is_linear
    )
    q1 = c_res["Q2_sat_s2"]
    q2 = f_res["Q2_sat_s2"]
    q_ext = q2 + (q2 - q1) / 3.0
    c2_ext = f_res["c2_sat"] + (f_res["c2_sat"] - c_res["c2_sat"]) / 3.0
    return {
        "geom": f_res["geom"],
        "r_M_au": f_res["r_M_au"],
        "r_Hill_over_rM": f_res["r_Hill_over_rM"],
        "ye": f_res["ye"],
        "nue": f_res["nue"],
        "Q2_coarse_s2": q1,
        "Q2_fine_s2": q2,
        "Q2_extrap_s2": q_ext,
        "Q2_richardson_err_s2": abs(q2 - q_ext),
        "neg_c2_phys_extrap_s2": -c2_ext * a0 / math.sqrt(GM_SUN / a0),
        "fine_diag_Q2_s2": f_res["diag_Q2_s2"],
    }


def run_audit() -> dict:
    sympy_check = run_sympy_checks()
    nu_lin = make_linear_nu()
    nu_mon = qe.nu_n(2)

    g_e_nom = (V_CIRC_NOMINAL**2) / R_SUN_M
    a0_nom = float(qe.A0_DERIVED)

    # 1. Linear control (nu == 1): MUST recover Newtonian Milky Way tide and is NOT a Cassini pass
    lin_dir = Q2_hill_richardson(nu_lin, a0_nom, g_e_nom, n_r=1500, n_th=300, bc="dirichlet", include_tide_in_gN=True, is_linear=True)
    lin_rob = Q2_hill_richardson(nu_lin, a0_nom, g_e_nom, n_r=1500, n_th=300, bc="robin", include_tide_in_gN=True, is_linear=True)
    omega0_sq = lin_dir["geom"]["Omega0_sq_s2"]
    tide_q2 = lin_dir["geom"]["Q2_tide_newtonian_s2"]

    assert abs(omega0_sq - 7.560e-31) / 7.560e-31 < 1e-3, f"Unexpected Omega0^2: {omega0_sq}"
    assert abs(lin_dir["neg_c2_phys_extrap_s2"] - omega0_sq) / omega0_sq < 1e-6
    assert abs(lin_dir["Q2_extrap_s2"] - tide_q2) / tide_q2 < 1e-6
    assert abs(lin_rob["Q2_extrap_s2"] - tide_q2) / tide_q2 < 1e-6

    # 2. Nonlinear single-metric benchmark across all 3 a0 bases at nominal MW (220 km/s, 8.2 kpc)
    nominal_benchmarks = []
    for label, a0 in A0_BASES:
        nl_dir = Q2_hill_richardson(nu_mon, a0, g_e_nom, n_r=1500, n_th=300, bc="dirichlet", include_tide_in_gN=True, is_linear=False)
        nl_rob = Q2_hill_richardson(nu_mon, a0, g_e_nom, n_r=1500, n_th=300, bc="robin", include_tide_in_gN=True, is_linear=False)
        nl_notide = Q2_hill_richardson(nu_mon, a0, g_e_nom, n_r=1500, n_th=300, bc="dirichlet", include_tide_in_gN=False, is_linear=False)
        unb_q, unb_fine, unb_err = qe.Q2_richardson(nu_mon, a0, g_e_nom, n_r=1000, n_th=200)

        rel_dir_vs_rob = abs(nl_dir["Q2_extrap_s2"] - nl_rob["Q2_extrap_s2"]) / abs(nl_dir["Q2_extrap_s2"])
        rel_dir_vs_unb = abs(nl_dir["Q2_extrap_s2"] - unb_q) / abs(unb_q)
        rel_tide_effect = abs(nl_dir["Q2_extrap_s2"] - nl_notide["Q2_extrap_s2"]) / abs(nl_dir["Q2_extrap_s2"])

        assert rel_dir_vs_rob < 0.01, f"Dirichlet vs Robin mismatch: {rel_dir_vs_rob}"
        assert rel_dir_vs_unb < 0.01, f"Hill vs unbounded mismatch: {rel_dir_vs_unb}"
        # Planetary zone radial constancy
        q_diag = list(nl_dir["fine_diag_Q2_s2"].values())
        max_radial_spread = (max(q_diag) - min(q_diag)) / abs(nl_dir["Q2_fine_s2"])
        assert max_radial_spread < 0.01, f"Q2 radial drift across 5.2-70 AU: {max_radial_spread}"

        sig_park = (nl_dir["Q2_extrap_s2"] - Q2_PARK_MEAN) / Q2_PARK_SIG
        nominal_benchmarks.append({
            "a0_label": label,
            "a0_mps2": a0,
            "r_M_au": round(nl_dir["r_M_au"], 2),
            "R_Hill_au": round(nl_dir["geom"]["R_Hill_au"], 1),
            "R_Hill_pc": round(nl_dir["geom"]["R_Hill_pc"], 4),
            "R_Hill_over_rM": round(nl_dir["r_Hill_over_rM"], 3),
            "Q2_hill_dirichlet_s2": nl_dir["Q2_extrap_s2"],
            "Q2_hill_dirichlet_1e27": round(nl_dir["Q2_extrap_s2"] * 1e27, 4),
            "Q2_hill_dirichlet_err_1e27": round(nl_dir["Q2_richardson_err_s2"] * 1e27, 4),
            "Q2_hill_robin_1e27": round(nl_rob["Q2_extrap_s2"] * 1e27, 4),
            "Q2_hill_no_mw_tide_1e27": round(nl_notide["Q2_extrap_s2"] * 1e27, 4),
            "Q2_unbounded_1e27": round(unb_q * 1e27, 4),
            "rel_diff_dirichlet_vs_robin": rel_dir_vs_rob,
            "rel_diff_hill_vs_unbounded": rel_dir_vs_unb,
            "rel_mw_tidal_correction": rel_tide_effect,
            "planetary_radial_spread_5_70AU": max_radial_spread,
            "sigma_Park2026": round(sig_park, 3),
            "passes_5p2e27_cap": bool(nl_dir["Q2_extrap_s2"] <= Q2_CAP_2SIG),
        })

    # 3. Full 15-cell uncertainty grid matching cassini_ge_uncertainty_band.py
    grid_rows = []
    for label, a0 in A0_BASES:
        for ge_val in GE_GRID:
            res = Q2_hill_richardson(nu_mon, a0, ge_val, n_r=1000, n_th=200, bc="dirichlet", include_tide_in_gN=True, is_linear=False)
            unb_q, _, _ = qe.Q2_richardson(nu_mon, a0, ge_val, n_r=1000, n_th=200)
            q_ext = res["Q2_extrap_s2"]
            sig_park = (q_ext - Q2_PARK_MEAN) / Q2_PARK_SIG
            grid_rows.append({
                "a0_label": label,
                "a0_mps2": a0,
                "g_e_mps2": ge_val,
                "v_circ_kms": round(res["geom"]["v_circ_kms"], 2),
                "R_Hill_au": round(res["geom"]["R_Hill_au"], 1),
                "R_Hill_pc": round(res["geom"]["R_Hill_pc"], 4),
                "R_Hill_over_rM": round(res["r_Hill_over_rM"], 3),
                "eta": round(ge_val / a0, 4),
                "Q2_sat_hill_s2": q_ext,
                "Q2_sat_hill_1e27": round(q_ext * 1e27, 4),
                "Q2_richardson_err_1e27": round(res["Q2_richardson_err_s2"] * 1e27, 4),
                "Q2_unbounded_1e27": round(unb_q * 1e27, 4),
                "rel_diff_hill_vs_unbounded": abs(q_ext - unb_q) / abs(unb_q),
                "Omega0_sq_s2": res["geom"]["Omega0_sq_s2"],
                "Q2_tide_newtonian_s2": res["geom"]["Q2_tide_newtonian_s2"],
                "cap_5p2e27_s2": Q2_CAP_2SIG,
                "ratio_to_cap": round(q_ext / Q2_CAP_2SIG, 3),
                "sigma_Park2026": round(sig_park, 3),
                "passes_5p2e27_cap": bool(q_ext <= Q2_CAP_2SIG),
            })

    n_pass = sum(1 for r in grid_rows if r["passes_5p2e27_cap"])
    q2_min = min(r["Q2_sat_hill_1e27"] for r in grid_rows)
    q2_max = max(r["Q2_sat_hill_1e27"] for r in grid_rows)
    sig_min = min(r["sigma_Park2026"] for r in grid_rows)
    sig_max = max(r["sigma_Park2026"] for r in grid_rows)
    assert n_pass == 0, f"Unexpected Hill pass cells: {n_pass}"

    return {
        "meta": {
            "date": "2026-11-21",
            "script": "audits/2026-11-21/hill_sphere_efe_bvp.py",
            "epistemic_tag": "[D] / [X]",
            "preregistration": {
                "domain": "r in [0.2 AU, R_Hill], barycentric Sun-centered coordinates with +z toward Galactic Center",
                "R_Hill_formula": "R_Hill = R_sun * (M_sun / (3 * M_MW))^(1/3), M_MW = v_circ^2 * R_sun / G, M_sun = GM_sun / G",
                "equation": "Single-metric AeST/QUMOND flux-form PDE lap Phi = -div(nu_2(|g_N|/a_0) g_N), no fitted parameter",
                "Q2_definition": "Same as 02_galaxy_dynamics/qumond_axisym_efe.py and cassini_ge_uncertainty_band.py: Q2(9.5 AU) = -3 c2(9.5 AU) a0 / r_M",
                "cap_s2": Q2_CAP_2SIG,
                "fermi_statement": "A Fermi normal frame removes a constant g_e from a LINEAR Poisson equation (leaving only the Newtonian tide), and does NOT remove g_e from the nonlinear interpolating function nu(|grad Phi|).",
            },
        },
        "sympy_checks": sympy_check,
        "linear_control_nu_eq_1": {
            "description": "Linear Newtonian Poisson control (nu == 1) on [0.2 AU, R_Hill] for v_circ = 220 km/s, R_sun = 8.2 kpc",
            "R_Hill_au": round(lin_dir["geom"]["R_Hill_au"], 1),
            "R_Hill_pc": round(lin_dir["geom"]["R_Hill_pc"], 4),
            "Omega0_sq_newtonian_tide_s2": omega0_sq,
            "Q2_tide_expected_3_Omega0_sq_s2": tide_q2,
            "dirichlet_neg_c2_phys_s2": lin_dir["neg_c2_phys_s2"] if "neg_c2_phys_s2" in lin_dir else lin_dir["neg_c2_phys_extrap_s2"],
            "dirichlet_Q2_sat_s2": lin_dir["Q2_extrap_s2"],
            "robin_Q2_sat_s2": lin_rob["Q2_extrap_s2"],
            "recovers_newtonian_tide": True,
            "cassini_verdict": "LINEAR_CONTROL_ONLY_NOT_A_CASSINI_PASS",
            "note": "Recovering Omega0^2 = v_circ^2/R_sun^2 = 7.560e-31 s^-2 (or Q2_tide = 2.268e-30 s^-2) verifies linear boundary matching only and is NOT a Cassini pass for nonlinear nu(|grad Phi|).",
        },
        "nonlinear_nominal_benchmarks": nominal_benchmarks,
        "nonlinear_15cell_band": grid_rows,
        "summary": {
            "nominal_v_circ_kms": V_CIRC_NOMINAL / 1e3,
            "nominal_R_sun_kpc": R_SUN_KPC,
            "nominal_g_e_mps2": g_e_nom,
            "nominal_R_Hill_au": round(nominal_benchmarks[0]["R_Hill_au"], 1),
            "nominal_R_Hill_pc": nominal_benchmarks[0]["R_Hill_pc"],
            "nonlinear_Q2_sat_range_1e27": [q2_min, q2_max],
            "cap_1e27": round(Q2_CAP_2SIG * 1e27, 2),
            "Park2026_exclusion_sigma_range": [sig_min, sig_max],
            "cells_passing_5p2e27_cap": f"{n_pass}/{len(grid_rows)}",
            "verdict": (
                f"FAILS_CASSINI_CAP_[X]: On [0.2 AU, R_Hill] (~{nominal_benchmarks[0]['R_Hill_au']:.0f} AU = "
                f"{nominal_benchmarks[0]['R_Hill_over_rM']:.1f} r_M >> r_M), the nonlinear single-metric nu_2 "
                f"barycentric Hill-sphere BVP yields Saturn Q2(9.5 AU) = {q2_min:.2f}-{q2_max:.2f} x 10^-27 s^-2 "
                f"(+{sig_min:.2f} to +{sig_max:.2f} sigma above Park et al. 2026; 0/15 cells below 5.2e-27 s^-2), "
                f"matching the unbounded qumond_axisym_efe.py solver to <{max(r['rel_diff_hill_vs_unbounded'] for r in grid_rows)*100:.2f}%. "
                f"Only the linear (nu=1) control recovers the Milky Way tide 7.560e-31 s^-2 (Q2_tide = 2.268e-30 s^-2), which is not a Cassini pass."
            ),
        },
    }


def write_markdown(res: dict, out_md: Path) -> None:
    lin = res["linear_control_nu_eq_1"]
    summ = res["summary"]
    sym = res["sympy_checks"]
    nom = res["nonlinear_nominal_benchmarks"]
    grid = res["nonlinear_15cell_band"]

    lines = [
        "# Hill-Sphere Barycentric Matching BVP for Cassini ($Q_2$ at $9.5\\,\\mathrm{AU}$)",
        "",
        f"- **Date:** {res['meta']['date']}",
        f"- **Epistemic Tag:** `{res['meta']['epistemic_tag']}`",
        "- **Script:** `audits/2026-11-21/hill_sphere_efe_bvp.py`",
        "- **Receipt:** `audits/2026-11-21/HILL_SPHERE_EFE_BVP.json`",
        "",
        "## 1. Pre-Registered Problem & Fermi-Frame Distinction",
        "",
        "- **Single-metric equation (no fitted parameter):** $\\nabla^2\\Phi = -\\nabla\\cdot(\\nu_2(|\\mathbf{g}_N|/a_0)\\,\\mathbf{g}_N)$ with $\\Psi = \\Phi$ (`normalization_kb.py` Euler–Lagrange residuals: `0` for `Phi`, `Psi`, `phi`, `psi`; $G_N = \\tilde{G}/(1 - K_B/2)$).",
        "- **Why a Fermi frame does not remove $\\mathbf{g}_e$:** As verified symbolically (`fermi_linear_laplacian_difference = 0`, `fermi_nonlinear_grad_sq_difference != 0`), shifting $\\Phi_N \\to \\Phi_N + \\mathbf{g}_e\\cdot\\mathbf{x}$ removes constant $\\mathbf{g}_e$ from a **linear** Poisson equation, leaving only the tidal quadrupole; it does **not** remove $\\mathbf{g}_e$ from the nonlinear interpolating function $\\nu(|\\nabla\\Phi_N|/a_0)$.",
        f"- **Computed Hill radius (from $R_\\odot = {R_SUN_KPC}\\,\\mathrm{{kpc}}$, $M_\\odot$, $M_{{\\mathrm{{MW}}}} = v_{{\\mathrm{{circ}}}}^2 R_\\odot / G$):** At nominal $v_{{\\mathrm{{circ}}}} = 220\\,\\mathrm{{km/s}}$ ($g_e = {summ['nominal_g_e_mps2']:.4e}\\,\\mathrm{{m/s^2}}$), $R_{{\\mathrm{{Hill}}}} = {summ['nominal_R_Hill_au']:.1f}\\,\\mathrm{{AU}} = {summ['nominal_R_Hill_pc']:.4f}\\,\\mathrm{{pc}}$, which sits at ${nom[0]['R_Hill_over_rM']:.1f}\\,r_M \\gg r_M = {nom[0]['r_M_au']:.1f}\\,\\mathrm{{AU}}$.",
        "- **Empirical benchmark:** Saturn $Q_2(9.5\\,\\mathrm{AU}) = -3 c_2(9.5\\,\\mathrm{AU}) a_0 / r_M$ scored against Park et al. (2026, `arXiv:2602.17884`) $Q_2 = (1.6 \\pm 1.8)\\times 10^{-27}\\,\\mathrm{s}^{-2}$ (`+2 sigma` cap $5.2\\times 10^{-27}\\,\\mathrm{s}^{-2}$). Note `fermi_removes_ge_from_linear_poisson = " + str(sym["fermi_removes_ge_from_linear_poisson"]) + "`, `fermi_removes_ge_from_nonlinear_nu = " + str(sym["fermi_removes_ge_from_nonlinear_nu"]) + "`.",
        "",
        "## 2. Linear Control ($\\nu \\equiv 1$) vs. Nonlinear Single-Metric BVP ($\\nu = \\nu_2$)",
        "",
        f"- **Linear Newtonian control ($\\nu \\equiv 1$, NOT a Cassini pass):** On $r \\in [0.2\\,\\mathrm{{AU}}, {lin['R_Hill_au']:.1f}\\,\\mathrm{{AU}}]$, Dirichlet and Robin BCs recover $-c_{{2,\\mathrm{{phys}}}} = \\Omega_0^2 = v_{{\\mathrm{{circ}}}}^2/R_\\odot^2 = {lin['Omega0_sq_newtonian_tide_s2']:.3e}\\,\\mathrm{{s}}^{{-2}}$ (`dirichlet_neg_c2_phys_s2 = {lin['dirichlet_neg_c2_phys_s2']:.3e} s^-2`) and $Q_{{2,\\mathrm{{tide}}}} = 3\\Omega_0^2 = {lin['Q2_tide_expected_3_Omega0_sq_s2']:.3e}\\,\\mathrm{{s}}^{{-2}}$ (`dirichlet = {lin['dirichlet_Q2_sat_s2']:.3e}`, `robin = {lin['robin_Q2_sat_s2']:.3e} s^-2`). A result equal to the Milky Way tide is not a Cassini pass.",
        "",
        "### Nominal Milky Way Benchmarks ($v_{\\mathrm{circ}} = 220\\,\\mathrm{km/s}$, $R_\\odot = 8.2\\,\\mathrm{kpc}$, $g_e = 1.9128\\times 10^{-10}\\,\\mathrm{m/s^2}$)",
        "",
        "| $a_0$ Basis | $a_0\\,[10^{-10}]$ | $r_M\\,[\\mathrm{AU}]$ | $R_{\\mathrm{Hill}}/r_M$ | $Q_2$ Hill Dirichlet $[10^{-27}\\,\\mathrm{s}^{-2}]$ | $Q_2$ Hill Robin $[10^{-27}]$ | $Q_2$ Unbounded $[10^{-27}]$ | Rel Diff vs Unbounded | Park+2026 $\\sigma$ | Cap $\\le 5.2$ |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for r in nom:
        lines.append(
            f"| `{r['a0_label']}` | `{r['a0_mps2']*1e10:.4f}` | `{r['r_M_au']:.1f}` | `{r['R_Hill_over_rM']:.2f}` | "
            f"**`{r['Q2_hill_dirichlet_1e27']:.4f}`** | `{r['Q2_hill_robin_1e27']:.4f}` | `{r['Q2_unbounded_1e27']:.4f}` | "
            f"`{r['rel_diff_hill_vs_unbounded']*100:.4f}%` | `+{r['sigma_Park2026']:.2f} sigma` | **`{r['passes_5p2e27_cap']}`** |"
        )

    lines.extend([
        "",
        "## 3. Full 15-Cell $(a_0, g_e)$ Band (`0/15` Pass the $5.2\\times 10^{-27}\\,\\mathrm{s}^{-2}$ Cap)",
        "",
        "| $a_0$ Basis | $g_e\\,[10^{-10}]$ | $v_{\\mathrm{circ}}\\,\\mathrm{[km/s]}$ | $R_{\\mathrm{Hill}}\\,\\mathrm{[AU]}$ | $Q_2(9.5\\,\\mathrm{AU})$ Hill $[10^{-27}\\,\\mathrm{s}^{-2}]$ | Unbounded $[10^{-27}]$ | $Q_2 / 5.2$ | Park+2026 $\\sigma$ | Pass Cap |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])
    for r in grid:
        lines.append(
            f"| `{r['a0_label']}` | `{r['g_e_mps2']*1e10:.2f}` | `{r['v_circ_kms']:.1f}` | `{r['R_Hill_au']:.0f}` | "
            f"`{r['Q2_sat_hill_1e27']:.3f}` | `{r['Q2_unbounded_1e27']:.3f}` | `{r['ratio_to_cap']:.2f}x` | "
            f"`+{r['sigma_Park2026']:.2f}` | `{r['passes_5p2e27_cap']}` |"
        )

    lines.extend([
        "",
        "## 4. Verdict",
        "",
        f"> **{summ['verdict']}**",
        "",
        f"Because $R_{{\\mathrm{{Hill}}}} \\approx {summ['nominal_R_Hill_au']:.0f}\\,\\mathrm{{AU}}$ lies ~`36x` outside the solar MOND transition radius $r_M \\approx 7100\\,\\mathrm{{AU}}$, matching the barycentric field at the Hill surface reproduces the full nonlinear QUMOND $Q_2(9.5\\,\\mathrm{{AU}}) = {summ['nonlinear_Q2_sat_range_1e27'][0]:.2f}\\text{{--}}{summ['nonlinear_Q2_sat_range_1e27'][1]:.2f}\\times 10^{{-27}}\\,\\mathrm{{s}}^{{-2}}$ (exceeding the $5.2\\times 10^{{-27}}\\,\\mathrm{{s}}^{{-2}}$ cap in every cell, `0/15` pass).",
        "",
    ])
    out_md.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    result = run_audit()
    out_json = HERE / "HILL_SPHERE_EFE_BVP.json"
    out_md = HERE / "HILL_SPHERE_EFE_BVP.md"
    out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_markdown(result, out_md)
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    print("Linear control Omega0^2 =", result["linear_control_nu_eq_1"]["Omega0_sq_newtonian_tide_s2"])
    print("Linear control Q2_tide  =", result["linear_control_nu_eq_1"]["dirichlet_Q2_sat_s2"])
    for r in result["nonlinear_nominal_benchmarks"]:
        print(
            f"  Nominal {r['a0_label']}: R_Hill={r['R_Hill_au']} AU ({r['R_Hill_over_rM']} r_M), "
            f"Q2_dir={r['Q2_hill_dirichlet_1e27']}e-27 (unbounded={r['Q2_unbounded_1e27']}e-27), "
            f"Park={r['sigma_Park2026']:+}sigma, pass={r['passes_5p2e27_cap']}"
        )
    print("Summary:", result["summary"]["verdict"])
