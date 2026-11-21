#!/usr/bin/env python3
"""Gate 2 audit: Close D10 by measured X-COP ICM outer gas profiles to R200 (no screen, no Cosh, no second metric).

Strictly adheres to the single-metric unscreened live AeST seat:
  - Screen S(r) == 1 identically everywhere (NO x_H screen, NO tidal/Cassini screen).
  - Quadratic AeST dust source -mu0^2 r^2 Phi (NO Cosh concentration).
  - Single metric (Psi == Phi), universal mu0 = 1/(0.9895 Mpc), cosmic dust ratio 5.36, canonical mu_std.

Compares 5 baryon models across all 12 X-COP clusters (and the 11 direct-R200 clusters excluding A3266)
under 3 unscreened live AeST solvers:
  (S1) static_rv: uncapped Dirichlet Phi(r_v) = 0 at universal mu0.
  (S2) capped_mu_rv: cosmic supply-capped via mu_eff <= mu0 so M_dust(r_v) <= 5.36 M_b(r_v).
  (S3) free_boundary_polytrope_fixed_mu: fixed universal mu0, chemical potential Phi_0 (free edge R_edge <= r_v)
       capping M_dust(R_edge) <= 5.36 M_b(r_v).

Gas profiles:
  - M0_beta_control: 2-pt beta model of xcop_test.py (reproduces XCOP_RESULT.json).
  - M1_stacked_measured: Ghirardini+19 (arXiv:1805.00042, Table 5) 49-pt stacked n_e(x) to 1.9 R500
    (med, low, high 68% envelopes), normalized to each cluster's measured M_gas(R500) (plus 9% stars).
  - M2_vikhlinin_CCNCC: Ghirardini+19 Table 3 universal CC/NCC Vikhlinin density profile (gamma=3),
    normalized to measured M_gas(R500) (plus 9% stars).
  - M3_per_cluster_exact_vikhlinin: CC/NCC inner shape fixed from Table 3 + per-cluster outer steepening
    eps_i solved so BOTH M_gas(R500) AND M_gas(R200) match Eckert+19 Table 2 exactly (plus 9% stars).
  - M4_outer_baryon_floor: conservative outer-baryon bounds on M3 (M4a concentrated stars f_star=0.015,
    M4b pure measured ICM gas with zero stars, M4c hard truncation rho_b(r > R200) = 0).

Pre-registered criteria (exploration/d10_xcop/PREREG.md):
  - All 12: 0.80 <= median(R) <= 1.25 AND >= 9/12 in [0.7, 1.4] at BOTH R500 and R200.
  - Direct-R200 11: 0.80 <= median(R) <= 1.25 AND >= 8/11 in [0.7, 1.4] at BOTH R500 and R200.
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
D_CL = os.path.abspath(os.path.join(HERE, "../../02_galaxy_dynamics/clusters"))
_cwd = os.getcwd()
os.chdir(D_CL)
_spec = importlib.util.spec_from_file_location("cm", "cluster_mond_test.py")
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)
os.chdir(_cwd)

MPC = cm.MPC_M
G = cm.G_SI
MS = cm.MSUN
MU0 = 1.0 / (0.9895 * MPC)
COSMIC_RATIO = 5.36
law = lambda u: cm.g_mond(max(u, 0.0))

# Ghirardini et al. 2019 (A&A 621, A41, arXiv:1805.00042) Table 1 cool-core classification (K0 < 30 keV cm^2)
CC_CLUSTERS = {"A1644", "A1795", "A2029", "A85"}

# Ghirardini et al. 2019 Table 3 (Eq. 4 Vikhlinin density, gamma=3): (ln_n0, ln_rc, ln_rs, alpha, beta, eps)
# Verified against Table 5 to 2-6% that log() in Table 3 is natural log.
VIKH_PARAMS = {
    "ALL": (-4.4, -3.0, -0.29, 0.89, 0.43, 2.86),
    "CC":  (-3.9, -3.2, +0.17, 0.80, 0.49, 4.67),
    "NCC": (-4.9, -2.7, -0.51, 0.70, 0.39, 2.60),
}

# Ghirardini et al. 2019 Table 5 (tab:stack) verbatim 49 radial density bins:
# (x = R/R500, ne_med, ne_low, ne_high, N_X) in units of E(z)^{-2} cm^{-3}
GHIRARDINI_TAB5_STACK = [
    (1.058e-02, 8.814e-03, 6.543e-03, 1.503e-02, 12),
    (1.179e-02, 8.751e-03, 6.224e-03, 1.416e-02, 12),
    (1.313e-02, 8.684e-03, 6.018e-03, 1.457e-02, 12),
    (1.463e-02, 8.712e-03, 5.929e-03, 1.421e-02, 12),
    (1.630e-02, 8.409e-03, 5.839e-03, 1.324e-02, 12),
    (1.816e-02, 8.110e-03, 5.666e-03, 1.269e-02, 12),
    (2.024e-02, 8.007e-03, 5.560e-03, 1.314e-02, 12),
    (2.255e-02, 7.720e-03, 5.432e-03, 1.100e-02, 12),
    (2.513e-02, 7.627e-03, 5.440e-03, 1.167e-02, 12),
    (2.799e-02, 7.593e-03, 5.445e-03, 1.165e-02, 12),
    (3.119e-02, 7.513e-03, 5.503e-03, 1.133e-02, 12),
    (3.475e-02, 7.334e-03, 5.534e-03, 1.089e-02, 12),
    (3.872e-02, 7.086e-03, 5.271e-03, 1.058e-02, 12),
    (4.314e-02, 6.889e-03, 5.086e-03, 1.000e-02, 12),
    (4.807e-02, 6.675e-03, 4.839e-03, 9.519e-03, 12),
    (5.356e-02, 6.408e-03, 4.531e-03, 8.860e-03, 12),
    (5.967e-02, 6.161e-03, 4.246e-03, 8.219e-03, 12),
    (6.649e-02, 5.628e-03, 3.817e-03, 7.509e-03, 12),
    (7.408e-02, 5.255e-03, 3.550e-03, 6.841e-03, 12),
    (8.254e-02, 4.875e-03, 3.359e-03, 6.049e-03, 12),
    (9.197e-02, 4.473e-03, 3.196e-03, 5.461e-03, 12),
    (1.025e-01, 4.141e-03, 2.992e-03, 4.983e-03, 12),
    (1.142e-01, 3.813e-03, 2.728e-03, 4.495e-03, 12),
    (1.272e-01, 3.429e-03, 2.527e-03, 4.023e-03, 12),
    (1.417e-01, 3.011e-03, 2.327e-03, 3.565e-03, 12),
    (1.579e-01, 2.678e-03, 2.123e-03, 3.089e-03, 12),
    (1.759e-01, 2.385e-03, 1.854e-03, 2.676e-03, 12),
    (1.960e-01, 2.142e-03, 1.650e-03, 2.296e-03, 12),
    (2.184e-01, 1.892e-03, 1.478e-03, 1.992e-03, 12),
    (2.434e-01, 1.675e-03, 1.328e-03, 1.723e-03, 12),
    (2.712e-01, 1.444e-03, 1.159e-03, 1.475e-03, 12),
    (3.021e-01, 1.193e-03, 1.038e-03, 1.238e-03, 12),
    (3.366e-01, 1.013e-03, 9.677e-04, 1.039e-03, 12),
    (3.751e-01, 8.583e-04, 8.375e-04, 8.741e-04, 12),
    (4.179e-01, 7.145e-04, 6.885e-04, 7.349e-04, 12),
    (4.656e-01, 5.997e-04, 5.689e-04, 6.211e-04, 12),
    (5.188e-01, 4.926e-04, 4.631e-04, 5.208e-04, 12),
    (5.780e-01, 4.043e-04, 3.744e-04, 4.390e-04, 12),
    (6.440e-01, 3.391e-04, 3.190e-04, 3.530e-04, 12),
    (7.176e-01, 2.742e-04, 2.657e-04, 2.832e-04, 12),
    (7.995e-01, 2.199e-04, 2.106e-04, 2.277e-04, 12),
    (8.908e-01, 1.783e-04, 1.691e-04, 1.843e-04, 12),
    (9.925e-01, 1.423e-04, 1.312e-04, 1.493e-04, 12),
    (1.106e+00, 1.142e-04, 1.051e-04, 1.213e-04, 11),
    (1.232e+00, 8.635e-05, 7.469e-05, 9.571e-05, 11),
    (1.373e+00, 6.274e-05, 5.512e-05, 6.934e-05, 11),
    (1.530e+00, 4.767e-05, 4.269e-05, 5.336e-05, 10),
    (1.704e+00, 3.720e-05, 3.132e-05, 4.402e-05, 5),
    (1.899e+00, 2.769e-05, 2.355e-05, 3.228e-05, 2),
]

_STACK_X = np.array([row[0] for row in GHIRARDINI_TAB5_STACK])
_STACK_LOGX = np.log(_STACK_X)
_STACK_COLS = {
    "med": np.log(np.array([row[1] for row in GHIRARDINI_TAB5_STACK])),
    "low": np.log(np.array([row[2] for row in GHIRARDINI_TAB5_STACK])),
    "high": np.log(np.array([row[3] for row in GHIRARDINI_TAB5_STACK])),
}
_STACK_SPLINES = {b: CubicSpline(_STACK_LOGX, ly, bc_type="natural") for b, ly in _STACK_COLS.items()}


def eval_stacked_shape(x: np.ndarray | float, branch: str = "med") -> np.ndarray | float:
    """Smooth C^2 log-log spline of Table 5 with exact natural-tangent continuation outside [0.01058, 1.899]."""
    if np.isscalar(x):
        lx = math.log(max(float(x), 1e-12))
        sp_b = _STACK_SPLINES[branch]
        if lx < _STACK_LOGX[0]:
            slope = float(sp_b(_STACK_LOGX[0], 1))
            y = float(_STACK_COLS[branch][0]) + slope * (lx - float(_STACK_LOGX[0]))
        elif lx > _STACK_LOGX[-1]:
            ly = _STACK_COLS[branch]
            slope = float((ly[-1] - ly[-2]) / (_STACK_LOGX[-1] - _STACK_LOGX[-2]))
            y = float(ly[-1]) + slope * (lx - float(_STACK_LOGX[-1]))
        else:
            y = float(sp_b(lx))
        return math.exp(y)
    xa = np.maximum(np.asarray(x, dtype=float), 1e-12)
    return np.array([eval_stacked_shape(float(xi), branch) for xi in xa])


def eval_vikh_shape(x: np.ndarray | float, ln_rc: float, ln_rs: float, alpha: float, beta: float, eps: float) -> np.ndarray | float:
    """Ghirardini+19 Eq. 4 Vikhlinin n_e(x) shape (up to constant n0) for x = r / R500."""
    if np.isscalar(x):
        xv = max(float(x), 1e-8)
        rc = math.exp(ln_rc)
        rs = math.exp(ln_rs)
        return ((xv / rc) ** (-0.5 * alpha)) * ((1.0 + (xv / rc) ** 2) ** (-0.5 * (3.0 * beta - 0.5 * alpha))) * ((1.0 + (xv / rs) ** 3) ** (-eps / 6.0))
    xa = np.maximum(np.asarray(x, dtype=float), 1e-8)
    rc = math.exp(ln_rc)
    rs = math.exp(ln_rs)
    return ((xa / rc) ** (-0.5 * alpha)) * ((1.0 + (xa / rc) ** 2) ** (-0.5 * (3.0 * beta - 0.5 * alpha))) * ((1.0 + (xa / rs) ** 3) ** (-eps / 6.0))


def build_smooth_baryons(R5: float, rv: float, dMdr_fn, truncate_at_r: float | None = None):
    """Return precomputed cumulative Mb(r) evaluator and direct smooth analytic dM(r)."""
    rg = np.concatenate([
        [0.0],
        np.geomspace(1e-6 * R5, 0.05 * R5, 1000, endpoint=False),
        np.linspace(0.05 * R5, rv, 2000),
    ])
    dM_g = np.array([0.0 if (truncate_at_r is not None and float(r) > truncate_at_r) else (0.0 if float(r) == 0.0 else float(dMdr_fn(float(r)))) for r in rg])
    Mb_g = np.concatenate([[0.0], np.cumsum(0.5 * (dM_g[1:] + dM_g[:-1]) * np.diff(rg))])
    Mb = lambda r: float(np.interp(r, rg, Mb_g))
    dM = lambda r: (0.0 if (truncate_at_r is not None and r > truncate_at_r) else float(dMdr_fn(r)))
    return Mb, dM


def make_profile_for_cluster(row: list[str], model: str):
    """Construct (Mb, dMdr, meta) for one X-COP cluster under baryon model tag."""
    nm, z, R5_s, R2_s, MH5_s, MH2_s, f5_s, f2_s, Mt5_s, Mt2_s = row
    z = float(z)
    R5 = float(R5_s) * MPC
    R2 = float(R2_s) * MPC
    MH5 = float(MH5_s) * 1e14 * MS
    MH2 = float(MH2_s) * 1e14 * MS
    Mg5 = float(f5_s) * MH5
    Mg2 = float(f2_s) * MH2
    Mt5 = float(Mt5_s) * 1e14 * MS
    Mt2 = float(Mt2_s) * 1e14 * MS
    rv = R2 * (200.0 / 177.8) ** (1.0 / 3.0)
    cc_tag = "CC" if nm in CC_CLUSTERS else "NCC"

    if model == "M0_beta_control":
        # Exact reproduction of xcop_test.py
        xc = 0.1
        rc = xc * R5
        x2 = R2 / R5
        sm = lambda x, b: quad(lambda t: t**2 * (1.0 + (t / xc) ** 2) ** (-1.5 * b), 0.0, x, limit=200)[0]
        beta = brentq(lambda b: sm(x2, b) / sm(1.0, b) - Mg2 / Mg5, 0.3, 3.0)
        A = 1.09 * Mg5 / (4.0 * math.pi * (R5**3) * sm(1.0, beta))
        rho = lambda r: A * (1.0 + (r / rc) ** 2) ** (-1.5 * beta)
        rg = np.linspace(0.0, rv, 4001)
        Mb_g = np.concatenate([[0.0], np.cumsum(0.5 * (4.0 * math.pi * rg[1:] ** 2 * rho(rg[1:]) + 4.0 * math.pi * rg[:-1] ** 2 * rho(rg[:-1])) * np.diff(rg))])
        Mb = lambda r: float(np.interp(r, rg, Mb_g))
        dM = lambda r: float(4.0 * math.pi * r * r * rho(r))
        return Mb, dM, {"nm": nm, "cc": cc_tag, "R5": R5, "R2": R2, "rv": rv, "Mt5": Mt5, "Mt2": Mt2, "Mg5": Mg5, "Mg2": Mg2, "outer_slope_R200": -3.0 * beta, "M5_gas_ratio": 1.0, "M2_gas_ratio": Mg2 / Mg2}

    if model.startswith("M1_stacked"):
        branch = model.split("_")[-1] if model != "M1_stacked_measured" else "med"
        I5 = quad(lambda x: x * x * eval_stacked_shape(x, branch), 0.0, 1.0, limit=300, points=[0.01058, 0.1, 0.5])[0]
        norm = Mg5 / ((R5**3) * I5)
        dMdr_gas = lambda r: norm * (R5**2) * ((r / R5) ** 2) * eval_stacked_shape(r / R5, branch)
        dMdr_tot = lambda r: 1.09 * dMdr_gas(r)
        Mb, dM = build_smooth_baryons(R5, rv, dMdr_tot)
        # Slope between outermost table bin crossing R2/R5
        x2 = R2 / R5
        eps_s = 1e-3
        slope_200 = math.log(eval_stacked_shape(x2 * (1 + eps_s), branch) / eval_stacked_shape(x2 * (1 - eps_s), branch)) / math.log((1 + eps_s) / (1 - eps_s))
        Mg_mod_2 = Mb(R2) / 1.09
        return Mb, dM, {"nm": nm, "cc": cc_tag, "R5": R5, "R2": R2, "rv": rv, "Mt5": Mt5, "Mt2": Mt2, "Mg5": Mg5, "Mg2": Mg2, "outer_slope_R200": slope_200, "M2_gas_ratio": Mg_mod_2 / Mg2, "trunc": None}

    if model == "M2_vikhlinin_CCNCC":
        _, ln_rc, ln_rs, al, be, ep = VIKH_PARAMS[cc_tag]
        shape_fn = lambda x: eval_vikh_shape(x, ln_rc, ln_rs, al, be, ep)
        I5 = quad(lambda x: x * x * shape_fn(x), 0.0, 1.0, limit=300, epsrel=1e-9)[0]
        norm = 1.09 * Mg5 / ((R5**3) * I5)
        dMdr_tot = lambda r: norm * (R5**2) * ((r / R5) ** 2) * shape_fn(r / R5)
        Mb, dM = build_smooth_baryons(R5, rv, dMdr_tot)
        x2 = R2 / R5
        eps_s = 1e-3
        slope_200 = math.log(shape_fn(x2 * (1 + eps_s)) / shape_fn(x2 * (1 - eps_s))) / math.log((1 + eps_s) / (1 - eps_s))
        return Mb, dM, {"nm": nm, "cc": cc_tag, "R5": R5, "R2": R2, "rv": rv, "Mt5": Mt5, "Mt2": Mt2, "Mg5": Mg5, "Mg2": Mg2, "outer_slope_R200": slope_200, "M2_gas_ratio": (Mb(R2) / 1.09) / Mg2, "trunc": None}

    # M3 & M4 share per-cluster exact Vikhlinin matching BOTH Mg(R500) and Mg(R200)
    _, ln_rc, ln_rs, al, be, _ = VIKH_PARAMS[cc_tag]
    x2 = R2 / R5
    # Vectorized radial integral on log-uniform grid up to x2 to solve for eps_i robustly and fast
    xg = np.concatenate([[0.0], np.geomspace(1e-6, x2, 3000)])
    base_xg = np.array([0.0 if xv == 0.0 else eval_vikh_shape(xv, ln_rc, ln_rs, al, be, 0.0) for xv in xg])
    rs_v = math.exp(ln_rs)
    rs3 = (xg / rs_v) ** 3

    def gas_ratio_for_eps(ep_val: float) -> float:
        prf = (xg**2) * base_xg * ((1.0 + rs3) ** (-ep_val / 6.0))
        I_all = np.concatenate([[0.0], np.cumsum(0.5 * (prf[1:] + prf[:-1]) * np.diff(xg))])
        I5 = float(np.interp(1.0, xg, I_all))
        I2 = float(I_all[-1])
        return (I2 / I5) - (Mg2 / Mg5)

    eps_i = brentq(gas_ratio_for_eps, -4.0, 25.0, xtol=1e-8)
    shape_fn = lambda x: eval_vikh_shape(x, ln_rc, ln_rs, al, be, eps_i)
    I5 = quad(lambda x: x * x * shape_fn(x), 0.0, 1.0, limit=300, epsrel=1e-10)[0]
    norm_gas = Mg5 / ((R5**3) * I5)
    dMdr_gas = lambda r: norm_gas * (R5**2) * ((r / R5) ** 2) * shape_fn(r / R5)
    eps_s = 1e-3
    slope_200 = math.log(shape_fn(x2 * (1 + eps_s)) / shape_fn(x2 * (1 - eps_s))) / math.log((1 + eps_s) / (1 - eps_s))

    trunc = None
    if model == "M3_per_cluster_exact_vikhlinin":
        dMdr_tot = lambda r: 1.09 * dMdr_gas(r)
    elif model == "M4a_eckert_fstar_concentrated":
        # Eckert+19 constant f_star = 0.015 concentrated within c=5 NFW/Hernquist stars so M*(r500) = 0.015*MH5
        Mstar_500 = 0.015 * MH5
        rs_star = 0.2 * R5
        norm_st = Mstar_500 / (math.log(1.0 + 5.0) - 5.0 / 6.0)
        dMdr_star = lambda r: norm_st * r / ((r + rs_star) ** 2) if r > 0 else 0.0
        dMdr_tot = lambda r: dMdr_gas(r) + dMdr_star(r)
    elif model == "M4b_gas_only_no_stars":
        dMdr_tot = dMdr_gas
    elif model == "M4c_hard_trunc_at_R200":
        dMdr_tot = lambda r: 1.09 * dMdr_gas(r)
        trunc = R2
    else:
        raise ValueError(model)

    Mb, dM = build_smooth_baryons(R5, rv, dMdr_tot, truncate_at_r=trunc)
    return Mb, dM, {
        "nm": nm, "cc": cc_tag, "R5": R5, "R2": R2, "rv": rv,
        "Mt5": Mt5, "Mt2": Mt2, "Mg5": Mg5, "Mg2": Mg2,
        "eps_fit": float(eps_i), "outer_slope_R200": float(slope_200),
        "M5_gas_check": float(quad(dMdr_gas, 0.0, R5, limit=200, epsrel=1e-7)[0] / Mg5),
        "M2_gas_check": float(quad(dMdr_gas, 0.0, R2, limit=200, epsrel=1e-7)[0] / Mg2),
        "trunc": trunc,
    }


def _solve_segmented(rhs_on, rhs_off, y_init, rmin: float, rout: float, r_trunc: float | None, event_fn=None, full: bool = False):
    """Integrate (rmin, rout) with exact piecewise split at r_trunc so DOP853 sees zero discontinuities."""
    if r_trunc is None or r_trunc >= rout * (1.0 - 1e-12):
        kw = {"method": "DOP853", "rtol": 1e-8, "atol": [1e21, 1.0], "dense_output": full}
        if event_fn is not None:
            kw["events"] = event_fn
        s = solve_ivp(rhs_on, (rmin, rout), y_init, **kw)
        return s, (s.sol if full else None), s.y[:, -1], (list(s.t_events[0]) if event_fn else [])
    s1 = solve_ivp(rhs_on, (rmin, r_trunc), y_init, method="DOP853", rtol=1e-8, atol=[1e21, 1.0], dense_output=full, events=event_fn)
    kw2 = {"method": "DOP853", "rtol": 1e-8, "atol": [1e21, 1.0], "dense_output": full}
    if event_fn is not None:
        kw2["events"] = event_fn
    s2 = solve_ivp(rhs_off, (r_trunc, rout), s1.y[:, -1], **kw2)
    evs = []
    if event_fn:
        evs = list(s1.t_events[0]) + list(s2.t_events[0])
    sol_fn = (lambda r: s1.sol(r) if r <= r_trunc else s2.sol(r)) if full else None
    return s2, sol_fn, s2.y[:, -1], evs


def solve_dirichlet_bvp(Mb, dM, R5: float, R2: float, rout: float, Mt5: float, Mt2: float, mu: float, r_trunc: float | None = None):
    """Unscreened AeST BVP with Phi(rout) = 0."""
    rmin = 1e-4 * R5
    bad = {"u_nonpos": False}

    def rhs_on(r, y):
        W, Phi = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        return [G * dM(r) - mu * mu * r * r * Phi, law(u)]

    def rhs_off(r, y):
        W, Phi = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        return [-mu * mu * r * r * Phi, law(u)]

    def shoot(P0, full=False):
        bad["u_nonpos"] = False
        _, sol_fn, y_end, _ = _solve_segmented(rhs_on, rhs_off, [G * Mb(rmin), P0], rmin, rout, r_trunc, full=full)
        return sol_fn if full else float(y_end[1])

    g0 = -law(G * Mb(R5) / (R5**2)) * rout * 3.0
    grid = np.linspace(-6.0 * abs(g0), 2.0 * abs(g0), 17)
    F = [shoot(p) for p in grid]
    idx = next((j for j in range(len(grid) - 1) if F[j] * F[j + 1] <= 0), None)
    if idx is None:
        grid = np.linspace(-6.0 * abs(g0), 2.0 * abs(g0), 41)
        F = [shoot(p) for p in grid]
        idx = next(j for j in range(len(grid) - 1) if F[j] * F[j + 1] <= 0)
    P0 = brentq(shoot, grid[idx], grid[idx + 1], xtol=1e-6 * abs(g0))
    sol_fn = shoot(P0, True)
    assert not bad["u_nonpos"]
    Md = lambda r: law(float(sol_fn(r)[0]) / (r * r)) * (r * r) / G
    Md_out = float(sol_fn(rout)[0]) / G - Mb(rout)
    dust_ratio = Md_out / (COSMIC_RATIO * Mb(rout))
    return float(Mt5 / Md(R5)), float(Mt2 / Md(R2)), float(dust_ratio), float(P0)


def integrate_free_boundary(Psi_c: float, rmin: float, rv: float, Mb, dM, mu: float, r_trunc: float | None = None):
    """Integrate free-boundary n=1 polytrope Psi_rel(rmin)=Psi_c <= 0 with dust active only for Psi_rel < 0."""
    bad = {"u_nonpos": False}

    def rhs_on(r, y):
        W, Psi_rel = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        dust_src = (-mu * mu * r * r * Psi_rel) if Psi_rel < 0.0 else 0.0
        return [G * dM(r) + dust_src, law(u)]

    def rhs_off(r, y):
        W, Psi_rel = y
        u = W / (r * r)
        if u <= 0.0:
            bad["u_nonpos"] = True
        dust_src = (-mu * mu * r * r * Psi_rel) if Psi_rel < 0.0 else 0.0
        return [dust_src, law(u)]

    def edge_event(r, y):
        return y[1]

    edge_event.terminal = False
    edge_event.direction = 1
    _, sol_fn, y_end, evs = _solve_segmented(rhs_on, rhs_off, [G * Mb(rmin), Psi_c], rmin, rv, r_trunc, event_fn=edge_event, full=True)
    return sol_fn, evs, bad["u_nonpos"]


def solve_all_unscreened(Mb, dM, meta: dict) -> dict:
    """Run all three unscreened live AeST solvers (+ diagnostic R_out=R200) on one cluster profile."""
    R5, R2, rv, Mt5, Mt2 = meta["R5"], meta["R2"], meta["rv"], meta["Mt5"], meta["Mt2"]
    r_trunc = meta.get("trunc")
    rmin = 1e-4 * R5

    Rm5 = float(Mt5 / (law(G * Mb(R5) / (R5**2)) * (R5**2) / G))
    Rm2 = float(Mt2 / (law(G * Mb(R2) / (R2**2)) * (R2**2) / G))

    # (S1) static_rv
    S5, S2, dust_rv, P0_unc = solve_dirichlet_bvp(Mb, dM, R5, R2, rv, Mt5, Mt2, MU0, r_trunc=r_trunc)

    # (S2) capped_mu_rv
    if dust_rv > 1.0:
        sc = brentq(lambda s: solve_dirichlet_bvp(Mb, dM, R5, R2, rv, Mt5, Mt2, MU0 * s, r_trunc=r_trunc)[2] - 1.0, 1e-3, 1.0, xtol=1e-4)
        C5, C2, dust_cap, _ = solve_dirichlet_bvp(Mb, dM, R5, R2, rv, Mt5, Mt2, MU0 * sc, r_trunc=r_trunc)
    else:
        sc, C5, C2, dust_cap = 1.0, S5, S2, dust_rv

    # (S3) free_boundary_polytrope_fixed_mu
    M_budget = COSMIC_RATIO * Mb(rv)
    if dust_rv <= 1.0:
        F5, F2, R_edge_ov_rv, capped_poly = S5, S2, 1.0, False
    else:
        def excess_dust(Psi_c: float) -> float:
            sol_fb, _, _ = integrate_free_boundary(Psi_c, rmin, rv, Mb, dM, MU0, r_trunc=r_trunc)
            return ((float(sol_fb(rv)[0]) / G) - Mb(rv)) - M_budget

        f_lo = excess_dust(P0_unc)
        f_hi = excess_dust(0.0)
        assert f_lo > 0.0 and f_hi < 0.0
        Psi_c_star = brentq(excess_dust, P0_unc, 0.0, xtol=1e-6 * abs(P0_unc))
        sol_fb, evs, ubad = integrate_free_boundary(Psi_c_star, rmin, rv, Mb, dM, MU0, r_trunc=r_trunc)
        assert not ubad
        Md_fb = lambda r: law(float(sol_fb(r)[0]) / (r * r)) * (r * r) / G
        F5 = float(Mt5 / Md_fb(R5))
        F2 = float(Mt2 / Md_fb(R2))
        R_edge = float(evs[0]) if len(evs) > 0 else float(rv)
        R_edge_ov_rv = float(R_edge / rv)
        capped_poly = True

    return {
        "name": meta["nm"],
        "cc": meta["cc"],
        "direct_R200": bool(meta["nm"] != "A3266"),
        "outer_slope_R200": round(meta["outer_slope_R200"], 3),
        "Mb_rv_over_Mb_R500": round(float(Mb(rv) / Mb(R5)), 4),
        "R500_pureMOND": Rm5,
        "R200_pureMOND": Rm2,
        "static_rv": {"R500": S5, "R200": S2, "dust_ratio": dust_rv},
        "capped_mu_rv": {"R500": C5, "R200": C2, "mu_scale": float(sc), "dust_ratio": dust_cap},
        "free_boundary_polytrope": {"R500": F5, "R200": F2, "capped": capped_poly, "R_edge_over_rv": R_edge_ov_rv},
    }


def summarize_subset(rows: list[dict], direct_only: bool = False) -> dict:
    sub = [r for r in rows if (r["direct_R200"] if direct_only else True)]
    n = len(sub)
    req_in = 8 if direct_only else 9
    out = {"n_clusters": n, "required_in_0.7_1.4": req_in}
    out["pureMOND"] = {
        "med_R500": round(float(np.median([r["R500_pureMOND"] for r in sub])), 4),
        "n_in_R500": int(sum(0.7 <= r["R500_pureMOND"] <= 1.4 for r in sub)),
        "med_R200": round(float(np.median([r["R200_pureMOND"] for r in sub])), 4),
        "n_in_R200": int(sum(0.7 <= r["R200_pureMOND"] <= 1.4 for r in sub)),
    }
    for solver in ("static_rv", "capped_mu_rv", "free_boundary_polytrope"):
        r5 = [r[solver]["R500"] for r in sub]
        r2 = [r[solver]["R200"] for r in sub]
        m5, n5 = float(np.median(r5)), int(sum(0.7 <= x <= 1.4 for x in r5))
        m2, n2 = float(np.median(r2)), int(sum(0.7 <= x <= 1.4 for x in r2))
        p5 = (0.8 <= m5 <= 1.25) and (n5 >= req_in)
        p2 = (0.8 <= m2 <= 1.25) and (n2 >= req_in)
        out[solver] = {
            "med_R500": round(m5, 4),
            "n_in_R500": n5,
            "pass_R500": bool(p5),
            "med_R200": round(m2, 4),
            "n_in_R200": n2,
            "pass_R200": bool(p2),
            "verdict_both": "CLOSES" if (p5 and p2) else "FAILS_R200_OVERSHOOT",
        }
    return out


def main() -> int:
    with open(os.path.join(HERE, "xcop_data.tsv"), encoding="utf-8") as f:
        rows_in = [l.strip().split("\t") for l in f if l.strip() and not l.startswith("#")]
    assert len(rows_in) == 12

    models = [
        "M0_beta_control",
        "M1_stacked_measured",
        "M1_stacked_low",
        "M1_stacked_high",
        "M2_vikhlinin_CCNCC",
        "M3_per_cluster_exact_vikhlinin",
        "M4a_eckert_fstar_concentrated",
        "M4b_gas_only_no_stars",
        "M4c_hard_trunc_at_R200",
    ]

    results = {}
    for m in models:
        m_rows = []
        for row in rows_in:
            Mb, dM, meta = make_profile_for_cluster(row, m)
            if m == "M3_per_cluster_exact_vikhlinin":
                assert abs(meta["M5_gas_check"] - 1.0) < 1e-4 and abs(meta["M2_gas_check"] - 1.0) < 1e-4
            res = solve_all_unscreened(Mb, dM, meta)
            if "eps_fit" in meta:
                res["eps_fit"] = round(meta["eps_fit"], 3)
            m_rows.append(res)

        s_all = summarize_subset(m_rows, direct_only=False)
        s_dir = summarize_subset(m_rows, direct_only=True)
        # Boundary R200 diagnostic on M3 only
        diag_bnd_r200 = None
        if m == "M3_per_cluster_exact_vikhlinin":
            bnd_vals = []
            for row in rows_in:
                Mb, dM, meta = make_profile_for_cluster(row, m)
                s5, s2, dr_b, _ = solve_dirichlet_bvp(Mb, dM, meta["R5"], meta["R2"], meta["R2"], meta["Mt5"], meta["Mt2"], MU0)
                bnd_vals.append({"name": meta["nm"], "R500": s5, "R200": s2, "dust_ratio": dr_b})
            diag_bnd_r200 = {
                "med_R500": round(float(np.median([x["R500"] for x in bnd_vals])), 4),
                "n_in_R500": int(sum(0.7 <= x["R500"] <= 1.4 for x in bnd_vals)),
                "med_R200": round(float(np.median([x["R200"] for x in bnd_vals])), 4),
                "n_in_R200": int(sum(0.7 <= x["R200"] <= 1.4 for x in bnd_vals)),
                "rows": bnd_vals,
            }
        results[m] = {
            "summary_all12": s_all,
            "summary_direct11_excl_A3266": s_dir,
            "diagnostic_dirichlet_R200": diag_bnd_r200,
            "rows": m_rows,
        }

    # Verify M0 matches XCOP_RESULT.json closely
    m0c = results["M0_beta_control"]["summary_all12"]["capped_mu_rv"]
    assert abs(m0c["med_R500"] - 0.83) < 0.02 and m0c["n_in_R500"] == 12
    assert abs(m0c["med_R200"] - 0.62) < 0.02 and m0c["n_in_R200"] <= 2

    any_closes = any(
        results[m][sub][sol]["verdict_both"] == "CLOSES"
        for m in ("M1_stacked_measured", "M2_vikhlinin_CCNCC", "M3_per_cluster_exact_vikhlinin")
        for sub in ("summary_all12", "summary_direct11_excl_A3266")
        for sol in ("static_rv", "capped_mu_rv", "free_boundary_polytrope")
    )

    out = {
        "gate2_rules": {
            "screen": "NONE (S == 1 identically everywhere)",
            "cosh": "NONE (quadratic AeST dust only)",
            "second_metric": "NONE (single metric Psi == Phi)",
            "data_sources": [
                "Ettori+19 A&A 621 A39 (arXiv:1805.00035)",
                "Eckert+19 A&A 621 A40 (arXiv:1805.00034)",
                "Ghirardini+19 A&A 621 A41 (arXiv:1805.00042) Tables 1, 3, 5",
            ],
        },
        "gate2_verdict": "REPLAN_NEEDED_MEASURED_ICM_PASSES" if any_closes else "D10_AEST_DUST_CLUSTER_ROUTE_KILLED_[X]",
        "any_measured_icm_closes_both_R500_and_R200": bool(any_closes),
        "compact_summary": {
            m: {
                "all12_static": results[m]["summary_all12"]["static_rv"],
                "all12_capped_mu": results[m]["summary_all12"]["capped_mu_rv"],
                "all12_free_boundary": results[m]["summary_all12"]["free_boundary_polytrope"],
                "direct11_capped_mu": results[m]["summary_direct11_excl_A3266"]["capped_mu_rv"],
                "direct11_free_boundary": results[m]["summary_direct11_excl_A3266"]["free_boundary_polytrope"],
            }
            for m in models
        },
        "models": results,
    }

    jpath = os.path.join(HERE, "GATE2_XCOP_MEASURED_ICM.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    print(json.dumps({
        "gate2_verdict": out["gate2_verdict"],
        "compact_summary": out["compact_summary"],
        "M3_diag_dirichlet_R200": {k: v for k, v in results["M3_per_cluster_exact_vikhlinin"]["diagnostic_dirichlet_R200"].items() if k != "rows"},
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
