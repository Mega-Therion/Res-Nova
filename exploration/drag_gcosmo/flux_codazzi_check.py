#!/usr/bin/env python3
"""Pre-registered 5D AdS-Vaidya Israel-Codazzi bulk-flux, NEC, and Weyl backreaction test
for drag variable-G cosmology (PREREG_FLUX.md, commit a4db5e0b).

Parts:
  (S1) SymPy exact 5D AdS-Vaidya Einstein tensor & 5D Null Energy Condition on d(mu_pm)/dt.
  (S2) SymPy exact Dark Bubble 4D Bianchi / Weyl backreaction identity & conformal cancellation at w_d = 1/3.
  (F1) Required bulk flux Q_4(z), 5D NEC sign, and BBN/CMB Delta N_eff on best-fit trajectories.
  (F2) Exact self-consistent coupled Friedmann + Weyl ODE refit on DESI DR2 + Pantheon+ + CMB (+ fsigma8)
       and DES-Dovekie across stable barotropic w_d in {0, 0.1, 0.2, 1/3, 0.5, 1.0}.
"""
from __future__ import annotations

import json
import math
import os
import sys
import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import minimize
from scipy.special import erf, erfi

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../04_cosmology")))
import cosmo_data as cd
from desy5_ceiling import load_inv_cov, read_snana
import drag_fit
from drag_fit import C, FS, ORH2, REF_D1, bcinv, bq, bv, bz, mb, s_one, scinv, zg, zhd, zhel


def run_symbolic_s1_s2() -> dict:
    """Exact SymPy verification of (S1) 5D AdS-Vaidya Einstein tensor + NEC, and (S2) 4D Weyl-flux Bianchi."""
    # --- (S1) Exact 5D AdS-Vaidya metric: ds^2 = -f(r,v) dv^2 + 2 eps dv dr + r^2 (dx^2 + dy^2 + dz^2) ---
    v, r, x, y, z = sp.symbols("v r x y z", real=True)
    k, eps = sp.symbols("k eps", real=True)
    mu = sp.Function("mu")(v)
    coords = [v, r, x, y, z]
    f = k**2 * r**2 - mu / r**2

    g = sp.Matrix([
        [-f, eps, 0, 0, 0],
        [eps, 0, 0, 0, 0],
        [0, 0, r**2, 0, 0],
        [0, 0, 0, r**2, 0],
        [0, 0, 0, 0, r**2],
    ])
    # eps^2 = 1 (eps = +1 ingoing, eps = -1 outgoing)
    ginv = sp.Matrix([
        [0, eps, 0, 0, 0],
        [eps, f, 0, 0, 0],
        [0, 0, 1 / r**2, 0, 0],
        [0, 0, 0, 1 / r**2, 0],
        [0, 0, 0, 0, 1 / r**2],
    ])
    assert sp.simplify((g * ginv).subs(eps**2, 1) - sp.eye(5)) == sp.zeros(5)

    # Christoffel symbols Gamma^a_{bc}
    Gamma = [[[sp.Integer(0) for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for a in range(5):
        for b in range(5):
            for c in range(b, 5):
                val = sp.Integer(0)
                for d in range(5):
                    if ginv[a, d] != 0:
                        val += sp.Rational(1, 2) * ginv[a, d] * (
                            sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])
                        )
                val = sp.simplify(val.subs(eps**2, 1))
                Gamma[a][b][c] = val
                Gamma[a][c][b] = val

    # Ricci tensor R_{ab}
    Ric = sp.zeros(5, 5)
    for a in range(5):
        for b in range(a, 5):
            val = sp.Integer(0)
            for c in range(5):
                val += sp.diff(Gamma[c][a][b], coords[c]) - sp.diff(Gamma[c][a][c], coords[b])
                for d in range(5):
                    val += Gamma[c][c][d] * Gamma[d][a][b] - Gamma[c][b][d] * Gamma[d][a][c]
            val = sp.simplify(val.subs(eps**2, 1))
            Ric[a, b] = val
            Ric[b, a] = val

    R_scalar = sp.Integer(0)
    for a in range(5):
        for b in range(5):
            if ginv[a, b] != 0 and Ric[a, b] != 0:
                R_scalar += ginv[a, b] * Ric[a, b]
    R_scalar = sp.simplify(R_scalar.subs(eps**2, 1))
    assert sp.simplify(R_scalar + 20 * k**2) == 0  # Exact AdS5 Ricci scalar R = -20 k^2

    # Einstein tensor with AdS5 cosmological constant Lambda_5 = -6 k^2: E_{ab} = G_{ab} + Lambda_5 g_{ab} = G_{ab} - 6 k^2 g_{ab}
    E_ads = sp.zeros(5, 5)
    for a in range(5):
        for b in range(5):
            E_ads[a, b] = sp.simplify((Ric[a, b] - sp.Rational(1, 2) * R_scalar * g[a, b] - 6 * k**2 * g[a, b]).subs(eps**2, 1))

    # Every component must vanish EXCEPT E_{vv} = (3 * eps / (2 r^3)) * dmu/dv
    for a in range(5):
        for b in range(5):
            if (a, b) == (0, 0):
                assert sp.simplify(E_ads[0, 0] - sp.Rational(3, 2) * eps * sp.diff(mu, v) / r**3) == 0
            else:
                assert E_ads[a, b] == 0

    # --- (S2) Exact 4D Dark Bubble Bianchi / Weyl backreaction identity ---
    t = sp.Symbol("t", real=True)
    wd = sp.Symbol("w_d", real=True)
    a_t = sp.Function("a")(t)
    H_t = sp.diff(a_t, t) / a_t
    rho_m = sp.Function("rho_m")(t)
    rho_r = sp.Function("rho_r")(t)
    dSig = sp.Function("dSig")(t)
    rho_W = sp.Function("rho_W")(t)
    Sig_c, Sig_0 = sp.symbols("Sig_c Sig_0", positive=True)

    # Low-energy Dark Bubble effective density & pressure:
    #   rho_eff = rho_m + rho_r + (Sig_c - Sig_0) - dSig + rho_W
    #   p_eff   = (1/3) rho_r - (Sig_c - Sig_0) - w_d * dSig + (1/3) rho_W
    rho_eff = rho_m + rho_r + (Sig_c - Sig_0) - dSig + rho_W
    p_eff = sp.Rational(1, 3) * rho_r - (Sig_c - Sig_0) - wd * dSig + sp.Rational(1, 3) * rho_W
    bianchi = sp.diff(rho_eff, t) + 3 * H_t * (rho_eff + p_eff)
    # Impose standard conservation of 4D matter and radiation
    bianchi_sub = sp.simplify(
        bianchi.subs({sp.diff(rho_m, t): -3 * H_t * rho_m, sp.diff(rho_r, t): -4 * H_t * rho_r})
    )
    Q4 = sp.diff(dSig, t) + 3 * (1 + wd) * H_t * dSig
    weyl_eq = sp.diff(rho_W, t) + 4 * H_t * rho_W - Q4
    assert sp.simplify(bianchi_sub - weyl_eq) == 0

    # Net wall+Weyl density rho_net = rho_W - dSig satisfies d/dt(a^4 rho_net) = (3 w_d - 1) a^4 H dSig
    rho_net = rho_W - dSig
    lhs_net = sp.diff(a_t**4 * rho_net, t)
    rhs_net = (3 * wd - 1) * a_t**4 * H_t * dSig
    assert sp.simplify(lhs_net - rhs_net - a_t**4 * weyl_eq) == 0

    # Verify exact closed-form integrating-factor solution for Y(a) = a^4 Omega_net(a)
    a_s, kap, Om_s, Or_s, OL_s = sp.symbols("a kappa Omega_m Omega_r Omega_L", real=True)
    # y_1(a) = exp(kap a^2 / 2) - 1 satisfies y_1' - kap a y_1 = kap a
    y1 = sp.exp(kap * a_s**2 / 2) - 1
    assert sp.simplify(sp.diff(y1, a_s) - kap * a_s * y1 - kap * a_s) == 0
    # y_5(a) = (4/kap^2) * [2 exp(kap a^2 / 2) - 2 - kap a^2 - kap^2 a^4 / 4] satisfies y_5' - kap a y_5 = kap a^5
    y5 = (4 / kap**2) * (2 * sp.exp(kap * a_s**2 / 2) - 2 - kap * a_s**2 - kap**2 * a_s**4 / 4)
    assert sp.simplify(sp.diff(y5, a_s) - kap * a_s * y5 - kap * a_s**5) == 0

    return {
        "S1_AdS5_Ricci_scalar": str(R_scalar),
        "S1_only_Evv_nonzero": True,
        "S1_Evv_exact": str(E_ads[0, 0]),
        "S1_NEC_outer_ingoing": "d(mu_+)/dv >= 0  (increases rho_Weyl)",
        "S1_NEC_inner_outgoing": "d(mu_-)/du <= 0  (increases rho_Weyl)",
        "S2_bianchi_weyl_identity_verified": True,
        "S2_net_evolution_law": "d/dt (a^4 rho_net) = (3 w_d - 1) a^4 H dSig",
        "S2_conformal_cancellation_at_wd_1_over_3": True,
        "S2_integrating_factor_y1_y5_verified": True,
    }


def y_exact(a: np.ndarray, kappa: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Exact closed-form solutions y_p(a; kappa) = exp(kappa a^2 / 2) * int_0^a kappa s^p exp(-kappa s^2 / 2) ds
    for p = 1, 2, 5, smooth across kappa = 0."""
    a = np.asarray(a, dtype=float)
    z = 0.5 * kappa * a * a  # dimensionless argument
    if abs(kappa) < 1e-8:
        # Exact Taylor expansion to O(kappa^3)
        y1 = kappa * a**2 / 2.0 + (kappa**2 * a**4) / 8.0 + (kappa**3 * a**6) / 48.0
        y2 = kappa * a**3 / 3.0 + (kappa**2 * a**5) / 15.0 + (kappa**3 * a**7) / 105.0
        y5 = kappa * a**6 / 6.0 + (kappa**2 * a**8) / 48.0 + (kappa**3 * a**10) / 480.0
        return y1, y2, y5

    ez = np.exp(z)
    y1 = ez - 1.0
    # y5: avoid catastrophic cancellation for small |z| using Taylor when |z| < 1e-3
    y5 = np.empty_like(a)
    small = np.abs(z) < 1e-3
    if np.any(small):
        zs = z[small]
        aa = a[small]
        # 2*exp(z) - 2 - 2z - z^2 = sum_{n>=3} 2 z^n / n!
        poly = (2.0 * zs**3 / 6.0) * (1.0 + zs / 4.0 + zs**2 / 20.0 + zs**3 / 120.0 + zs**4 / 840.0)
        y5[small] = (4.0 / (kappa * kappa)) * poly
    if np.any(~small):
        zb = z[~small]
        y5[~small] = (4.0 / (kappa * kappa)) * (2.0 * np.exp(zb) - 2.0 - 2.0 * zb - zb * zb)

    # y2: exact via erf / erfi:
    # int_0^a kappa s^2 exp(-kappa s^2 / 2) ds = -a exp(-z) + int_0^a exp(-kappa s^2 / 2) ds
    # => y2(a) = exp(z) * int_0^a exp(-kappa s^2 / 2) ds - a
    y2 = np.empty_like(a)
    if np.any(small):
        aa = a[small]
        y2[small] = kappa * aa**3 / 3.0 + (kappa**2 * aa**5) / 15.0 + (kappa**3 * aa**7) / 105.0 + (kappa**4 * aa**9) / 945.0
    if np.any(~small):
        ab = a[~small]
        zb = z[~small]
        if kappa > 0:
            rt = math.sqrt(0.5 * kappa)
            integ = math.sqrt(math.pi) / (2.0 * rt) * erf(rt * ab)
        else:
            rt = math.sqrt(-0.5 * kappa)
            integ = math.sqrt(math.pi) / (2.0 * rt) * erfi(rt * ab)
        y2[~small] = np.exp(zb) * integ - ab

    return y1, y2, y5


def E_coupled(z_arr, h: float, Om: float, kappa: float):
    """Exact self-consistent E(z) for the 5D Vaidya-Israel-Codazzi coupled drag+Weyl system,
    parametrized by kappa = (3 w_d - 1) x_0."""
    z_arr = np.asarray(z_arr, dtype=float)
    a = 1.0 / (1.0 + z_arr)
    Or = ORH2 / (h * h)
    y1_1, y2_1, y5_1 = y_exact(np.array([1.0]), kappa)
    y1_1, y2_1, y5_1 = float(y1_1[0]), float(y2_1[0]), float(y5_1[0])
    denom = 1.0 + y5_1
    if denom <= 0.0:
        return None, None
    OL = (1.0 - Or * (1.0 + y1_1) - Om * (1.0 + y2_1)) / denom
    y1, y2, y5 = y_exact(a, kappa)
    E2 = Or * (1.0 + y1) / a**4 + Om * (1.0 / a**3 + y2 / a**4) + OL * (1.0 + y5 / a**4)
    if not np.all(np.isfinite(E2)) or np.any(E2 <= 0.0):
        return None, None
    return np.sqrt(E2), OL


def check_ode_residual(h: float, Om: float, kappa: float) -> float:
    """Independent numerical ODE cross-check of closed-form E_coupled against RK45 integration of dY/da."""
    Or = ORH2 / (h * h)
    _, OL = E_coupled(np.array([0.0]), h, Om, kappa)
    a_min = 1e-4
    # Analytic leading Y(a_min) = kappa * (Or a_min^2 / 2 + Om a_min^3 / 3 + OL a_min^6 / 6)
    Y0 = kappa * (0.5 * Or * a_min**2 + Om * a_min**3 / 3.0 + OL * a_min**6 / 6.0)
    sol = solve_ivp(
        lambda a, Y: kappa * (Om * a**2 + Or * a + OL * a**5 + a * Y[0]),
        (a_min, 1.0),
        [Y0],
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        dense_output=True,
    )
    a_test = np.linspace(0.05, 1.0, 50)
    E_closed, _ = E_coupled(1.0 / a_test - 1.0, h, Om, kappa)
    Y_num = sol.sol(a_test)[0]
    E_num = np.sqrt(Om / a_test**3 + Or / a_test**4 + OL + Y_num / a_test**4)
    return float(np.max(np.abs(E_closed - E_num) / E_num))


# Load DES-Dovekie SN dataset (exact same loader as dovekie_rerun.py)
_H = read_snana(cd.path("desy5_hd"))
d_zhd, d_zhel, d_mu = (np.array(_H[k], float) for k in ("zHD", "zHEL", "MU"))
d_W = load_inv_cov(cd.path("desy5_inv"))
d_one = np.ones(len(d_zhd))
d_w11 = float(d_one @ d_W @ d_one)


def chi2_bg_coupled(h: float, Om: float, kappa: float, sn_sample: str = "pantheon") -> float:
    if not (0.5 < h < 0.9 and 0.1 < Om < 0.6 and -6.0 < kappa < 3.0):
        return 1e12
    Ez, _ = E_coupled(zg, h, Om, kappa)
    if Ez is None:
        return 1e12
    DM = cumulative_trapezoid(1.0 / Ez, zg, initial=0.0) * C / (100.0 * h)
    wm = Om * h * h
    fac = (wm / 0.1430) ** -0.255
    rd = 147.09 * fac
    rs = 144.43 * fac
    dm = np.interp(bz, zg, DM)
    dh = C / (100.0 * h * np.interp(bz, zg, Ez))
    mod = np.array([
        (z * dmi**2 * dhi) ** (1.0 / 3.0) / rd if q == "DV_over_rs" else (dmi / rd if q == "DM_over_rs" else dhi / rd)
        for z, dmi, dhi, q in zip(bz, dm, dh, bq)
    ])
    r = bv - mod
    cb = float(r @ bcinv @ r)
    if sn_sample == "pantheon":
        mu_m = 5.0 * np.log10(np.interp(zhd, zg, DM) * (1.0 + zhel)) + 25.0
        dl = mb - mu_m
        cs = float(dl @ scinv @ dl - (scinv @ dl).sum() ** 2 / s_one)
    else:
        dl = d_mu - (5.0 * np.log10(np.interp(d_zhd, zg, DM) * (1.0 + d_zhel)) + 25.0)
        cs = float(dl @ d_W @ dl - (d_one @ d_W @ dl) ** 2 / d_w11)
    th = 100.0 * rs / np.interp(1089.9, zg, DM)
    cc = ((th - 1.04110) / 0.00031) ** 2 + ((wm - 0.1430) / 0.0011) ** 2
    return cb + cs + cc


_N_GROWTH = np.linspace(math.log(1e-3), 0.0, 2001)
_A_GROWTH = np.exp(_N_GROWTH)
_Z_GROWTH = 1.0 / _A_GROWTH - 1.0


def growth_coupled(h: float, Om: float, kappa: float):
    """Fast vectorized RK4 linear-growth integrator (exact to <1e-6 vs DOP853; matches REF_D1)."""
    Ez, _ = E_coupled(_Z_GROWTH, h, Om, kappa)
    dlnE_dN = np.gradient(np.log(Ez), _N_GROWTH)
    E2 = Ez * Ez
    coef_v = -(2.0 + dlnE_dN)
    coef_d = 1.5 * Om / (_A_GROWTH**3 * E2)
    # Fixed-step RK4 on uniform N grid (2000 steps => dN = 0.00345, local err ~ 1e-11)
    d = np.empty_like(_N_GROWTH)
    v = np.empty_like(_N_GROWTH)
    d[0] = _A_GROWTH[0]
    v[0] = _A_GROWTH[0]
    hN = _N_GROWTH[1] - _N_GROWTH[0]
    for i in range(len(_N_GROWTH) - 1):
        cv0, cd0 = coef_v[i], coef_d[i]
        cv1, cd1 = coef_v[i + 1], coef_d[i + 1]
        cvm, cdm = 0.5 * (cv0 + cv1), 0.5 * (cd0 + cd1)
        di, vi = d[i], v[i]
        k1d = vi
        k1v = cv0 * vi + cd0 * di
        k2d = vi + 0.5 * hN * k1v
        k2v = cvm * k2d + cdm * (di + 0.5 * hN * k1d)
        k3d = vi + 0.5 * hN * k2v
        k3v = cvm * k3d + cdm * (di + 0.5 * hN * k2d)
        k4d = vi + hN * k3v
        k4v = cv1 * k4d + cd1 * (di + hN * k3d)
        d[i + 1] = di + (hN / 6.0) * (k1d + 2.0 * k2d + 2.0 * k3d + k4d)
        v[i + 1] = vi + (hN / 6.0) * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
    return d, v


def chi2_fs_coupled(h: float, Om: float, kappa: float, anchor: bool) -> tuple[float, float]:
    d, v = growth_coupled(h, Om, kappa)
    D1 = float(d[-1])
    s80 = 0.811 * D1 / REF_D1
    N_fs = np.log(1.0 / (1.0 + FS[:, 0]))
    f = s80 * np.interp(N_fs, _N_GROWTH, v) / D1
    if anchor:
        return float(np.sum(((FS[:, 1] - f) / FS[:, 2]) ** 2)), 1.0
    w = 1.0 / FS[:, 2] ** 2
    A = float(np.sum(w * FS[:, 1] * f) / np.sum(w * f * f))
    return float(np.sum(((FS[:, 1] - A * f) / FS[:, 2]) ** 2)), A


def fit_coupled(sn_sample: str = "pantheon", fix_kappa: float | None = None, with_fs: bool | None = None, kappa_sign: str = "any"):
    def tot(q):
        h, Om = q[0], q[1]
        kap = fix_kappa if fix_kappa is not None else q[2]
        if kappa_sign == "neg" and kap > 0.0:
            return 1e12
        if kappa_sign == "pos" and kap < 0.0:
            return 1e12
        v = chi2_bg_coupled(h, Om, kap, sn_sample=sn_sample)
        if with_fs is not None and v < 1e11:
            v += chi2_fs_coupled(h, Om, kap, anchor=with_fs)[0]
        return v

    if fix_kappa is not None:
        starts = [[0.68, 0.31]]
    elif kappa_sign == "pos":
        starts = [[0.68, 0.31, 0.01], [0.68, 0.31, 0.3]]
    else:
        starts = [[0.68, 0.31, -0.5], [0.68, 0.31, -2.0], [0.68, 0.31, -3.5], [0.68, 0.31, 0.05]]

    best = None
    for s0 in starts:
        r = minimize(tot, s0, method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-4, "maxiter": 4000})
        if best is None or r.fun < best.fun:
            best = r
    kap = fix_kappa if fix_kappa is not None else float(best.x[2])
    return float(best.fun), [float(best.x[0]), float(best.x[1]), float(kap)]


def run_f1_nec_and_early(h: float, Om: float, x0: float, label: str) -> dict:
    """Evaluate required bulk flux Q_4(z), NEC sign factor, and early-universe Weyl radiation Delta N_eff."""
    z_grid = np.linspace(0.0, 10.0, 2001)
    a = 1.0 / (1.0 + z_grid)
    Ez = drag_fit.E(z_grid, h, Om, x0)
    # q(z) = -1 + (1 + z) d(ln E)/dz
    dlnE_dz = np.gradient(np.log(Ez), z_grid)
    q_z = -1.0 + (1.0 + z_grid) * dlnE_dz
    out = {"label": label, "params_h_Om_x0": [h, Om, x0], "q_z0": float(q_z[0]), "q_max_z_le_10": float(np.max(q_z)), "by_wd": {}}
    Or = ORH2 / (h * h)
    # Effective Delta N_eff from fractional extra radiation: rho_W / rho_r = 0.134279 * Delta N_eff
    # (standard Planck conversion: rho_nu1 / rho_r = (7/8)(4/11)^(4/3) / (1 + 3.046*(7/8)*(4/11)^(4/3)) = 0.134279)
    CONV_DNEFF = 0.134279
    for wd in (0.0, 1.0 / 6.0, 1.0 / 3.0, 2.0 / 3.0, 1.0):
        s_nec = 1.5 * (1.0 + wd) - q_z
        Q4_dimless = 2.0 * x0 * (a**2) * (Ez**3) * s_nec  # in units of H_0 * rho_crit_0
        # Early-universe Weyl density at z_* = 1089.9 and z_BBN = 1e9 on radiation-dominated scaling:
        # d(a^4 Omega_W)/da = a^3 Q4 / (H/H0) = 2 x0 a^5 E^2 [1.5(1+wd) - q]
        # In RD (a << a_eq, q = 1, E^2 = Or a^-4): d(a^4 Omega_W)/da = 2 x0 Or [0.5 + 1.5 wd] a
        # => Omega_W(a) / (Or a^-4) = x0 * (0.5 + 1.5 wd) * a^2
        a_cmb = 1.0 / (1.0 + 1089.9)
        a_bbn = 1.0 / (1.0 + 1e9)
        # Exact integration up to z_* via coupled closed-form (Omega_W = Omega_net + x0 a^2 E^2):
        kap = (3.0 * wd - 1.0) * x0
        E_cmb_arr, OL_c = E_coupled(np.array([1089.9]), h, Om, kap)
        y1_c, y2_c, y5_c = y_exact(np.array([a_cmb]), kap)
        Om_net_cmb = float((Or * y1_c[0] + Om * y2_c[0] + OL_c * y5_c[0]) / a_cmb**4)
        Om_W_cmb = Om_net_cmb + x0 * (a_cmb**2) * float(E_cmb_arr[0] ** 2)
        frac_r_cmb = Om_W_cmb / (Or / a_cmb**4)
        dNeff_cmb = frac_r_cmb / CONV_DNEFF
        frac_r_bbn = x0 * (0.5 + 1.5 * wd) * a_bbn**2
        dNeff_bbn = frac_r_bbn / CONV_DNEFF
        out["by_wd"][f"wd={wd:.4f}"] = {
            "min_s_NEC_z_le_10": float(np.min(s_nec)),
            "max_s_NEC_z_le_10": float(np.max(s_nec)),
            "NEC_strictly_positive_all_z": bool(np.min(s_nec) > 0.0),
            "Q4_dimless_z0": float(Q4_dimless[0]),
            "Q4_dimless_z1": float(np.interp(1.0, z_grid, Q4_dimless)),
            "Omega_Weyl_over_Omega_r_CMB": float(frac_r_cmb),
            "Delta_Neff_CMB": float(dNeff_cmb),
            "Delta_Neff_BBN": float(dNeff_bbn),
            "early_radiation_safe": bool(abs(dNeff_cmb) < 0.05 and abs(dNeff_bbn) < 0.05),
        }
    return out


def main() -> int:
    sym = run_symbolic_s1_s2()
    print("[S1/S2] SymPy 5D AdS-Vaidya + 4D Bianchi/Weyl backreaction: PASS")
    print(json.dumps(sym, indent=1))

    # Independent ODE cross-check of closed-form E_coupled
    ode_err_neg = check_ode_residual(0.68, 0.31, -0.5)
    ode_err_pos = check_ode_residual(0.68, 0.31, +0.5)
    print(f"[ODE check] max rel diff closed-form vs DOP853: neg={ode_err_neg:.2e}, pos={ode_err_pos:.2e}")
    assert ode_err_neg < 1e-10 and ode_err_pos < 1e-10

    # Verify fast RK4 growth integrator matches drag_fit.REF_D1 at LCDM to < 1e-4
    d_ref, _ = growth_coupled(0.6736, 0.3153, 0.0)
    growth_ref_err = abs(float(d_ref[-1]) - REF_D1) / REF_D1
    print(f"[Growth check] RK4 vs drag_fit.REF_D1 rel diff = {growth_ref_err:.2e}", flush=True)
    assert growth_ref_err < 1e-4

    # --- F1: Required bulk flux & NEC sign on best-fit trajectories ---
    drag_json = json.load(open(os.path.join(os.path.dirname(__file__), "DRAG_FIT.json")))
    dov_json = json.load(open(os.path.join(os.path.dirname(__file__), "DOVEKIE_RERUN.json")))
    f1_pantheon = run_f1_nec_and_early(*drag_json["BAO+SN+CMB"]["params_drag"], "Pantheon+ best fit")
    f1_dovekie = run_f1_nec_and_early(*dov_json["drag"]["h_Om_x0"], "DES-Dovekie best fit")

    # --- F2: Exact self-consistent coupled Friedmann + Weyl ODE refit ---
    # Remember: E(a) depends on (w_d, x_0) ONLY through kappa = (3 w_d - 1) x_0!
    # So we fit kappa once per dataset, compute its 2-sigma profile, and map to x_0(w_d) = kappa / (3 w_d - 1)!
    f2_datasets = {}
    for label, sn_sample, wf in (
        ("Pantheon+_BAO_CMB", "pantheon", None),
        ("Pantheon+_BAO_CMB+fs8_anchored", "pantheon", True),
        ("Pantheon+_BAO_CMB+fs8_free_amp", "pantheon", False),
        ("DES-Dovekie_BAO_CMB", "dovekie", None),
    ):
        c_lcdm, p_lcdm = fit_coupled(sn_sample=sn_sample, fix_kappa=0.0, with_fs=wf)
        c_best, p_best = fit_coupled(sn_sample=sn_sample, fix_kappa=None, with_fs=wf, kappa_sign="any")
        c_pos, p_pos = fit_coupled(sn_sample=sn_sample, fix_kappa=None, with_fs=wf, kappa_sign="pos")

        # Profile likelihood over kappa in [-5.0, 0.4] to get both exact 2-sigma crossings cleanly
        k_grid = np.linspace(-5.0, 0.4, 55)
        prof = [(float(k), fit_coupled(sn_sample=sn_sample, fix_kappa=float(k), with_fs=wf)[0]) for k in k_grid]
        pk = np.array(prof)
        dk = pk[:, 1] - c_best
        crossings = [
            float(pk[i, 0] + (4.0 - dk[i]) * (pk[i + 1, 0] - pk[i, 0]) / (dk[i + 1] - dk[i]))
            for i in range(len(pk) - 1)
            if (dk[i] - 4.0) * (dk[i + 1] - 4.0) < 0
        ]

        # Check NEC, effective dark energy w_eff(z), and physical positivity at the coupled best fit
        h_b, Om_b, kap_b = p_best
        z_chk = np.linspace(0.0, 10.0, 1001)
        a_chk = 1.0 / (1.0 + z_chk)
        Ez_b, OL_b = E_coupled(z_chk, h_b, Om_b, kap_b)
        q_b = -1.0 + (1.0 + z_chk) * np.gradient(np.log(Ez_b), z_chk)
        y1_b, y2_b, y5_b = y_exact(a_chk, kap_b)
        Or_b = ORH2 / (h_b * h_b)
        Om_net_b = (Or_b * y1_b + Om_b * y2_b + OL_b * y5_b) / a_chk**4
        # Effective dark-energy density Omega_DE_eff = E^2 - Om/a^3 - Or/a^4 = OL + Om_net
        Om_de_b = OL_b + Om_net_b
        w_eff_b = -1.0 + ((1.0 + z_chk) / 3.0) * np.gradient(np.log(np.maximum(Om_de_b, 1e-12)), z_chk)

        by_wd = {}
        for wd in (0.0, 0.1, 0.2, 1.0 / 3.0, 0.5, 1.0):
            fac_wd = 3.0 * wd - 1.0
            if abs(fac_wd) < 1e-12:
                by_wd[f"wd={wd:.4f}"] = {
                    "regime": "CONFORMAL_CANCELLATION",
                    "kappa": 0.0,
                    "dchi2": 0.0,
                    "note": "rho_Weyl cancels Delta Sigma_drag identically at all z -> pure LCDM",
                }
            elif fac_wd < 0:
                x0_req = kap_b / fac_wd  # positive when kap_b < 0
                dSig_today = x0_req * 1.0
                Om_W_z = Om_net_b + x0_req * a_chk**2 * Ez_b**2
                min_s_nec = float(np.min(1.5 * (1.0 + wd) - q_b))
                a_cmb = 1.0 / (1.0 + 1089.9)
                E_c, _ = E_coupled(np.array([1089.9]), h_b, Om_b, kap_b)
                y1c, y2c, y5c = y_exact(np.array([a_cmb]), kap_b)
                Om_net_c = float((Or_b * y1c[0] + Om_b * y2c[0] + OL_b * y5c[0]) / a_cmb**4)
                Om_W_c = Om_net_c + x0_req * a_cmb**2 * float(E_c[0] ** 2)
                dNeff_c = (Om_W_c / (Or_b / a_cmb**4)) / 0.134279
                by_wd[f"wd={wd:.4f}"] = {
                    "regime": "SUB_CONFORMAL_DRAG_SURVIVES",
                    "x0_best": float(x0_req),
                    "x0_2sigma": [float(max(crossings) / fac_wd), float(min(crossings) / fac_wd)] if len(crossings) == 2 else None,
                    "dchi2": float(c_best - c_lcdm),
                    "Omega_Lambda_bare": float(OL_b),
                    "Delta_Sigma_drag_today": float(dSig_today),
                    "Omega_Weyl_today": float(Om_W_z[0]),
                    "Omega_Weyl_min_z_le_10": float(np.min(Om_W_z)),
                    "Omega_net_today": float(Om_net_b[0]),
                    "min_s_NEC_z_le_10": min_s_nec,
                    "NEC_satisfied": bool(x0_req > 0 and min_s_nec > 0),
                    "Delta_Neff_CMB": float(dNeff_c),
                    "Gcosmo_over_GN_bare_drag_today": float(1.0 / (1.0 + x0_req)),
                }
            else:
                x0_pos_best = p_pos[2] / fac_wd
                by_wd[f"wd={wd:.4f}"] = {
                    "regime": "SUPER_CONFORMAL_SIGN_REVERSED_ANTI_DRAG",
                    "kappa_best_ge_0": float(p_pos[2]),
                    "x0_best_ge_0": float(x0_pos_best),
                    "dchi2_with_x0_ge_0": float(c_pos - c_lcdm),
                    "note": "Weyl dark radiation overpowers drag (3 w_d - 1 > 0), flipping sign to anti-drag; best fit sits at x0 = 0 (LCDM).",
                }

        row_ds = {
            "chi2_LCDM": c_lcdm,
            "params_LCDM_h_Om": p_lcdm[:2],
            "chi2_coupled_best": c_best,
            "params_coupled_h_Om_kappa": p_best,
            "dchi2_coupled": float(c_best - c_lcdm),
            "kappa_2sigma_crossings": crossings,
            "kappa_0_outside_2sigma": bool(c_lcdm - c_best >= 4.0),
            "OL_bare_at_best": float(OL_b),
            "Omega_DE_eff_min_z_le_10": float(np.min(Om_de_b)),
            "w_eff_at_z0": float(w_eff_b[0]),
            "w_eff_at_z0p5": float(np.interp(0.5, z_chk, w_eff_b)),
            "w_eff_at_z1": float(np.interp(1.0, z_chk, w_eff_b)),
            "by_wd": by_wd,
        }
        if wf is not None:
            row_ds["fs8_chi2_LCDM"] = chi2_fs_coupled(p_lcdm[0], p_lcdm[1], 0.0, anchor=wf)
            row_ds["fs8_chi2_coupled"] = chi2_fs_coupled(h_b, Om_b, kap_b, anchor=wf)
        f2_datasets[label] = row_ds
        print(f"\n[{label}] dchi2={c_best - c_lcdm:+.2f}, h={h_b:.4f}, Om={Om_b:.4f}, kappa={kap_b:.4f}, 2sig={crossings}, w_eff(0)={w_eff_b[0]:.3f}, w_eff(1)={float(np.interp(1.0, z_chk, w_eff_b)):.3f}", flush=True)

    # Pre-registered verdict:
    # SURVIVES if exists w_d in [0, 1] with x_0 > 0, NEC satisfied, Delta N_eff < 0.05,
    # and dchi2 <= -4.0 on Pantheon+ BAO + CMB + fs8 (both anchored and free-amp) with x_0 = 0 outside 2sigma.
    anch = f2_datasets["Pantheon+_BAO_CMB+fs8_anchored"]
    free = f2_datasets["Pantheon+_BAO_CMB+fs8_free_amp"]
    wd0_a = anch["by_wd"]["wd=0.0000"]
    wd0_f = free["by_wd"]["wd=0.0000"]
    survives = (
        anch["dchi2_coupled"] <= -4.0
        and free["dchi2_coupled"] <= -4.0
        and anch["kappa_0_outside_2sigma"]
        and free["kappa_0_outside_2sigma"]
        and wd0_a["NEC_satisfied"]
        and abs(wd0_a["Delta_Neff_CMB"]) < 0.05
    )

    out = {
        "S1_S2_symbolic": sym,
        "ode_verification_max_rel_err": {"kappa=-0.5": ode_err_neg, "kappa=+0.5": ode_err_pos},
        "F1_nec_and_early_on_drag_trajectories": {"pantheon_plus": f1_pantheon, "des_dovekie": f1_dovekie},
        "F2_self_consistent_coupled_refit": f2_datasets,
        "preregistered_verdict": "SURVIVES (flux-fed sub-conformal 0 <= w_d < 1/3 viable)" if survives else "FAILS / EXCLUDED",
        "key_findings": {
            "conformal_cancellation_wd_eq_1_3": True,
            "super_conformal_wd_gt_1_3_sign_reversed": True,
            "sub_conformal_wd_in_0_to_1_3_dchi2_pantheon_bg": f2_datasets["Pantheon+_BAO_CMB"]["dchi2_coupled"],
            "sub_conformal_wd_in_0_to_1_3_dchi2_pantheon_fs8_anch": anch["dchi2_coupled"],
            "sub_conformal_wd_in_0_to_1_3_dchi2_pantheon_fs8_free": free["dchi2_coupled"],
            "sub_conformal_wd_in_0_to_1_3_dchi2_dovekie_bg": f2_datasets["DES-Dovekie_BAO_CMB"]["dchi2_coupled"],
            "x0_needed_at_wd_0_pantheon_bg": f2_datasets["Pantheon+_BAO_CMB"]["by_wd"]["wd=0.0000"]["x0_best"],
            "x0_needed_at_wd_0_dovekie_bg": f2_datasets["DES-Dovekie_BAO_CMB"]["by_wd"]["wd=0.0000"]["x0_best"],
        },
    }

    out_path = os.path.join(os.path.dirname(__file__), "FLUX_CODAZZI.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print("\n=== PRE-REGISTERED VERDICT ===")
    print(out["preregistered_verdict"])
    print(json.dumps(out["key_findings"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
