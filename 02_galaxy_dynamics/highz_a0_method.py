#!/usr/bin/env python3
"""
High-z a0 measurement METHOD (pinned before any data analysis) — helper module + self-test.

Target data: RC100 (Nestor Shachar et al. 2023, ApJ 944, 78; arXiv:2209.12199v1), Appendix B
Table 3, transcribed in highz_data/RC100_NestorShachar2023_table3_transcribed.csv (by eye; see
its header).  Local anchor: A0_DISTANCE_CORRECTED_2026-09-16.json, treatment T3 (non-flow SPARC,
mu_std).  NOTE: CURRENT_STATE_READ_THIS_FIRST.md line 105 quotes 1.1607e-10, 95% [9.72,12.95]e-11,
which is treatment T1 (all 175), not T3.  This module reads T3 from the JSON.

Convention (identical to sparc_a0_reextract_3mu.py, the frozen z=0 harness):
    g_bar = mu(g/a0) * g,   mu_std(x) = x / sqrt(1 + x^2)
    closure  g = sqrt((g_bar^2 + sqrt(g_bar^4 + 4 g_bar^2 a0^2)) / 2)
    exact inverse  a0 = (g/g_bar) * sqrt(g^2 - g_bar^2)          (needs 0 < g_bar < g)
    fDM route (g_bar = (1-f) g):  a0 = g * sqrt(f(2-f)) / (1-f), and 1 - f = mu(g/a0).

Epistemic tag of the whole fDM route: [C]-conditional.  RC100's fDM(Re) = V_DM^2/V_circ^2 comes
from a GR + NFW forward model with a Gaussian prior on log M_bar (Chabrier SED M* + Tacconi+2020
gas).  Reading a0 off it asks "what a0 makes mu_std reproduce the baryon fraction that fit
assigned"; the NFW *shape* enters at second order (one radius), the M_bar *prior* at first order.

Estimator (recommended, implemented here): per-z-bin joint (hierarchical) likelihood, FORWARD
direction.  Latent true ln g_bar per galaxy with a Gaussian population prior N(m, s); one
lognormal intrinsic scatter sigma_int on g at fixed g_bar; free ln a0.  Observables per galaxy:
  route 'fdm'  : ln g_obs = ln(Vc^2/Re) and f_obs  (independent Gaussian errors)
  route 'mbar' : ln g_obs and ln g_bar,b = ln(k G M_bar/Re^2) (correlated through Re)
Never invert per galaxy and average: the inverse does not exist for f <= 0 and censoring would
silently drop the galaxies that carry the information.

Self-test (python3 highz_a0_method.py [--n-real N] [--jobs J]): exit 0 iff all checks pass.
Writes HIGHZ_A0_METHOD_SELFTEST_2026-09-16.json next to this file.
"""

import argparse
import csv
import json
import math
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ANCHOR_JSON = HERE / "A0_DISTANCE_CORRECTED_2026-09-16.json"
RC100_CSV = HERE / "highz_data" / "RC100_NestorShachar2023_table3_transcribed.csv"
OUT_JSON = HERE / "HIGHZ_A0_METHOD_SELFTEST_2026-09-16.json"

KPC = 3.0856775814913673e19  # m
GM_SUN = 1.32712440018e20  # m^3 s^-2 (IAU nominal)
G_KPC = 4.300917270e-6  # kpc (km/s)^2 / Msun
C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22
HUBBLE_Z1_RATIO = 1.791  # a0(z=1)/a0(0), Hubble form (HORIZON_SELECTION K7 / PR #67 L4)
BURKERT_COEF = 3.36  # RC100 eq. [8]: V_rot^2 = V_circ^2 - 3.36 sigma0^2 (r/Re)


# ----------------------------------------------------------------------------- anchor
def load_anchor():
    J = json.loads(ANCHOR_JSON.read_text())
    t3 = J["treatments"]["T3_nonflow_only"]
    t1 = J["treatments"]["T1_baseline_175"]
    return {
        "a0": t3["a0_best"],
        "ci68": t3["bootstrap_68"],
        "ci95": t3["bootstrap_95"],
        "n_galaxies": t3["n_galaxies"],
        "mu": J["mu"],
        "T1_a0": t1["a0_best"],
        "T1_ci95": t1["bootstrap_95"],
    }


# ----------------------------------------------------------------------------- mu_std algebra
def mu_std(x):
    x = np.asarray(x, float)
    return x / np.sqrt(1.0 + x * x)


def g_pred(gbar, a0):
    """Forward closure g(g_bar; a0) for mu_std."""
    gb = np.asarray(gbar, float)
    return np.sqrt(0.5 * (gb * gb + np.sqrt(gb**4 + 4.0 * gb * gb * a0 * a0)))


def nu_std(y):
    """g/g_bar as a function of y = g_bar/a0 (numerically stable for large y)."""
    y = np.asarray(y, float)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / (y * y))))


def a0_from_g_gbar(g, gbar):
    """Exact mu_std inverse; NaN where no solution (g_bar <= 0 or g_bar >= g)."""
    g = np.asarray(g, float)
    gb = np.asarray(gbar, float)
    ok = (gb > 0) & (gb < g)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = (g / gb) * np.sqrt(g * g - gb * gb)
    return np.where(ok, out, np.nan)


def a0_from_fdm(g, f):
    """fDM route: a0 = g sqrt(f(2-f))/(1-f); NaN unless 0 < f < 1 (no M_bar enters)."""
    g = np.asarray(g, float)
    f = np.asarray(f, float)
    ok = (f > 0) & (f < 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = g * np.sqrt(f * (2.0 - f)) / (1.0 - f)
    return np.where(ok, out, np.nan)


def leverage(x):
    """Analytic sensitivities of the per-galaxy inverse at x = g/a0 (mu_std)."""
    x = np.asarray(x, float)
    return {
        "x": x,
        "gbar_over_a0": x * mu_std(x),
        "f_implied": 1.0 - mu_std(x),
        "dlna0_dlngbar_fixed_g": -(1.0 + x * x),
        "dlna0_dfdm_fixed_g": (1.0 + x * x) ** 1.5 / x,
        "dlna0_dlng_fixed_f": np.ones_like(x),
        "dlna0_dlng_fixed_gbar": 2.0 + x * x,
        # |df/dln a0| at fixed g: per-galaxy Fisher information on ln a0 is (this/sigma_f)^2 ~ x^-4
        "abs_df_dlna0_fixed_g": x / (1.0 + x * x) ** 1.5,
    }


def fdm_error_table(xs=(3.0, 10.0, 30.0), df=0.1):
    """Propagate f -> f +/- df at fixed g for x = g/a0; returns a0'/a0_true (NaN = no solution)."""
    rows = []
    for x in xs:
        g = x  # units of a0_true
        f0 = float(1.0 - mu_std(x))
        up = float(a0_from_fdm(g, f0 + df))
        dn = float(a0_from_fdm(g, f0 - df))
        rows.append(
            {
                "x": x,
                "gbar_over_a0": float(x * mu_std(x)),
                "f_implied": f0,
                "a0_ratio_f_plus": up,
                "a0_ratio_f_minus": None if math.isnan(dn) else dn,
                "f_minus_value": f0 - df,
                "linear_dlna0_df": float((1 + x * x) ** 1.5 / x),
            }
        )
    return rows


# ----------------------------------------------------------------------------- disk geometry
def sersic_b(n):
    """b_n from Gamma(2n)/2 = gamma(2n, b) (RC100 eq. [5])."""
    return float(special.gammaincinv(2.0 * n, 0.5))


def _sersic_sigma0(n, b):
    # M = 1, Re = 1
    return b ** (2 * n) / (2.0 * math.pi * n * special.gamma(2 * n))


def sersic_sigma(R, n):
    b = sersic_b(n)
    return _sersic_sigma0(n, b) * np.exp(-b * np.asarray(R, float) ** (1.0 / n))


@lru_cache(maxsize=None)
def _inner_I(m, n):
    """I(m) = int_0^inf Sigma'(m cosh t) dt  (M=1, Re=1).  rho(m) = -I(m)/(pi q)."""
    b = sersic_b(n)
    S0 = _sersic_sigma0(n, b)
    if n == 1.0:
        return float(-S0 * b * special.k0(b * m))

    def f(t):
        r = m * math.cosh(t)
        return -S0 * (b / n) * r ** (1.0 / n - 1.0) * math.exp(-b * r ** (1.0 / n))

    tmax = math.acosh(max(1.0 + 1e-12, (750.0 / b) ** n / m))
    val, _ = integrate.quad(f, 0.0, tmax, limit=400)
    return val


def inner_I_numeric(m, n):
    """Force the numeric quadrature path (used to validate the n=1 K0 closed form)."""
    b = sersic_b(n)
    S0 = _sersic_sigma0(n, b)

    def f(t):
        r = m * math.cosh(t)
        return -S0 * (b / n) * r ** (1.0 / n - 1.0) * math.exp(-b * r ** (1.0 / n))

    tmax = math.acosh(max(1.0 + 1e-12, (750.0 / b) ** n / m))
    return integrate.quad(f, 0.0, tmax, limit=400)[0]


def k_spheroid(R, n=1.0, q=0.2):
    """k = V_c^2 R / (G M) in the mid-plane at R (units of Re) for a deprojected Sersic
    oblate spheroid of intrinsic axis ratio q (Noordermeer 2008 eq. 10; B&T08 eq. 2.132).
    q=1: sphere (k = M3D(<R)/M);  q=0: razor-thin disk."""
    e2 = 1.0 - q * q

    def integrand(phi):
        s = math.sin(phi)
        m = R * s
        if m <= 0:
            return 0.0
        if q == 0.0:  # cos(phi)/sqrt(1 - sin^2 phi) == 1 exactly
            return _inner_I(m, n) * s * s
        return _inner_I(m, n) * s * s * math.cos(phi) / math.sqrt(1.0 - e2 * s * s)

    val, _ = integrate.quad(integrand, 0.0, math.pi / 2, limit=400)
    return -4.0 * R**3 * val


def k_freeman_thin(R):
    """Razor-thin exponential disk (Freeman 1970; B&T eq. 2.165), R in units of Re."""
    b1 = sersic_b(1.0)
    y = 0.5 * b1 * R
    return (
        2.0
        * b1
        * R
        * y
        * y
        * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))
    )


def reproject_sphere(R, n):
    """Sigma(R) from rho(m) = -I(m)/pi (q=1) — validates the Abel deprojection."""

    def f(u):  # r = sqrt(R^2 + u^2)
        return -_inner_I(math.sqrt(R * R + u * u), n) / math.pi

    return 2.0 * integrate.quad(f, 0.0, np.inf, limit=400)[0]


def half_mass_radius_3d(n):
    return optimize.brentq(lambda r: k_spheroid(r, n, 1.0) - 0.5, 0.3, 5.0, xtol=1e-6)


def geometry_table():
    b1 = sersic_b(1.0)
    return {
        "b1": b1,
        "burkert_2b1": 2.0 * b1,
        "cyl_enclosed_at_Re": float(special.gammainc(2.0, b1)),
        "k_sphere_half_mass (G(M/2)/Re^2)": 0.5,
        "k_thin_freeman_Re": float(k_freeman_thin(1.0)),
        "k_q0.20_Re": k_spheroid(1.0, 1.0, 0.20),
        "k_q0.25_Re": k_spheroid(1.0, 1.0, 0.25),
        "k_q1_sphere_deprojected_Re (M3D(<Re)/M)": k_spheroid(1.0, 1.0, 1.0),
        "r_half_3d_over_Re_n1": half_mass_radius_3d(1.0),
        "bulge_n4_Reb1kpc_k_at_R_kpc": {
            str(Rk): k_spheroid(float(Rk), 4.0, 1.0) for Rk in (2, 3, 5, 8)
        },
    }


# ----------------------------------------------------------------------------- data
def load_rc100(path=RC100_CSV, k_disk=None, bt=None):
    lines = [l for l in open(path) if not l.startswith("#")]
    rows = list(csv.DictReader(lines))
    d = {}
    for key in (
        "z",
        "logMstar",
        "logMbar",
        "e_logMbar",
        "Re_kpc",
        "e_Re_kpc",
        "fDM",
        "e_fDM",
        "Vc_kms",
        "e_Vc_kms",
        "sigma0_kms",
        "e_sigma0_kms",
        "logSigmaDM",
        "e_logSigmaDM",
    ):
        d[key] = np.array([float(r[key]) for r in rows])
    d["galaxy"] = [r["galaxy"] for r in rows]
    Vc, Re, f = d["Vc_kms"], d["Re_kpc"], d["fDM"]
    sV, sR = d["e_Vc_kms"] / Vc, d["e_Re_kpc"] / Re
    d["g_obs"] = (Vc * 1e3) ** 2 / (Re * KPC)
    d["lng"] = np.log(d["g_obs"])
    d["s_lng"] = np.sqrt((2 * sV) ** 2 + sR**2)
    d["s_lnV"], d["s_lnR"] = sV, sR
    d["gbar_a"] = (1.0 - f) * d["g_obs"]
    if k_disk is None:
        k_disk = k_spheroid(1.0, 1.0, 0.2)
    kk = np.full(len(f), k_disk)
    if (
        bt is not None
    ):  # optional bulge (n=4, Re_b = 1 kpc) — the M_bulge column is NOT transcribed
        kb = np.array([k_spheroid(float(r), 4.0, 1.0) for r in Re])
        kk = (1 - bt) * k_disk + bt * kb
    d["k_used"] = kk
    d["gbar_b"] = kk * GM_SUN * 10 ** d["logMbar"] / (Re * KPC) ** 2
    d["lngb"] = np.log(d["gbar_b"])
    d["s_lnM"] = math.log(10) * d["e_logMbar"]
    d["s_lngb"] = np.sqrt(d["s_lnM"] ** 2 + (2 * sR) ** 2)
    d["c_lng_lngb"] = 2 * sR**2
    d["p_pressure"] = BURKERT_COEF * d["sigma0_kms"] ** 2 / Vc**2
    d["bin"] = np.where(d["z"] < 1.2, 0, 1)
    # transcription check: log Sigma_DM(<Re) = log10(f Vc^2 Re / G / (pi Re^2))  (spherical NFW)
    sd = np.log10(f * Vc**2 / (G_KPC * math.pi * Re))
    tol = 0.02 + 0.4343 * (0.005 / np.maximum(f, 0.005) + 2 * 0.5 / Vc + 0.005 / Re)
    d["sigmaDM_recomputed"] = sd
    d["sigmaDM_ok"] = np.abs(sd - d["logSigmaDM"]) <= tol
    return d


def data_view(d, idx, route):
    v = {"lng": d["lng"][idx], "s_lng": d["s_lng"][idx]}
    if route == "fdm":
        v["f"] = d["fDM"][idx]
        v["s_f"] = d["e_fDM"][idx]
    else:
        v["lngb"] = d["lngb"][idx]
        v["s_lngb"] = d["s_lngb"][idx]
        v["c"] = d["c_lng_lngb"][idx]
    return v


# ----------------------------------------------------------------------------- estimator
class JointA0Likelihood:
    """Forward, errors-in-variables, per-bin joint likelihood with intrinsic scatter."""

    def __init__(self, data, route="fdm", n_u=48, n_eps=8, u_pad=2.5):
        self.route = route
        self.d = {k: np.asarray(v, float) for k, v in data.items()}
        if route == "fdm":
            f = np.clip(self.d["f"], 0.02, 0.95)
            u_est = self.d["lng"] + np.log(1 - f)
            var_u = self.d["s_lng"] ** 2 + (self.d["s_f"] / (1 - f)) ** 2
        else:
            u_est = self.d["lngb"]
            var_u = self.d["s_lngb"] ** 2
        self.u = np.linspace(u_est.min() - u_pad, u_est.max() + u_pad, n_u)
        t, w = np.polynomial.hermite.hermgauss(n_eps)
        self.t, self.lw = t, np.log(w / math.sqrt(math.pi))
        self.m0 = float(np.mean(u_est))
        self.s0 = float(math.sqrt(max(np.var(u_est) - np.mean(var_u), 0.15**2)))

    def logA(self, lna0, sig):
        """log sum_k w_k p(obs_i | u_j, eps_k); shape (n_sig, n_gal, n_u)."""
        sig = np.atleast_1d(np.asarray(sig, float))
        u = self.u
        lngp = np.log(g_pred(np.exp(u), math.exp(lna0)))  # (n_u,)
        eps = math.sqrt(2.0) * sig[:, None] * self.t[None, :]  # (S, K)
        lngt = lngp[None, :, None] + eps[:, None, :]  # (S, U, K)
        D = self.d
        if self.route == "fdm":
            ft = 1.0 - np.exp(u[None, :, None] - lngt)  # (S, U, K)
            sf = D["s_f"][None, :, None, None]
            sl = D["s_lng"][None, :, None, None]
            r1 = (D["f"][None, :, None, None] - ft[:, None, :, :]) / sf
            r2 = (D["lng"][None, :, None, None] - lngt[:, None, :, :]) / sl
            ll = -0.5 * (r1 * r1 + r2 * r2) - np.log(sf * sl) - math.log(2 * math.pi)
        else:
            s1 = D["s_lng"][None, :, None, None]
            s2 = D["s_lngb"][None, :, None, None]
            rho = (D["c"] / (D["s_lng"] * D["s_lngb"]))[None, :, None, None]
            x1 = (D["lng"][None, :, None, None] - lngt[:, None, :, :]) / s1
            x2 = ((D["lngb"][:, None] - u[None, :])[None, :, :, None]) / s2
            q = (x1 * x1 - 2 * rho * x1 * x2 + x2 * x2) / (1 - rho * rho)
            ll = (
                -0.5 * q
                - np.log(s1 * s2 * np.sqrt(1 - rho * rho))
                - math.log(2 * math.pi)
            )
        return special.logsumexp(ll + self.lw[None, None, None, :], axis=3)

    def _lnL_ms(self, A, m, s):
        lp = -0.5 * ((self.u - m) / s) ** 2
        lp -= special.logsumexp(lp)
        return special.logsumexp(A + lp[None, None, :], axis=2).sum(axis=1)  # (n_sig,)

    def _fit_ms(self, A_single, m, s):
        def nll(p):
            return -float(self._lnL_ms(A_single[None], p[0], math.exp(p[1]))[0])

        r = optimize.minimize(
            nll,
            [m, math.log(s)],
            method="Nelder-Mead",
            options={"xatol": 1e-3, "fatol": 1e-3, "maxiter": 400},
        )
        return float(r.x[0]), float(math.exp(r.x[1])), -float(r.fun)

    def profile(self, lna0_grid, sig_grid=(0.0, 0.05, 0.1, 0.2, 0.35)):
        """Profile likelihood P(ln a0) = max over (sigma_int grid; m, s refined once)."""
        sig_grid = np.asarray(sig_grid, float)
        As = [self.logA(la, sig_grid) for la in lna0_grid]
        m, s = self.m0, self.s0
        for _ in range(2):  # refine the population prior at the current joint maximum
            L = np.array([self._lnL_ms(A, m, s) for A in As])
            ia, isg = np.unravel_index(np.argmax(L), L.shape)
            m, s, _ = self._fit_ms(As[ia][isg], m, s)
        L = np.array([self._lnL_ms(A, m, s) for A in As])
        P = L.max(axis=1)
        return P, {
            "m": m,
            "s": s,
            "sig_best": float(sig_grid[np.unravel_index(np.argmax(L), L.shape)[1]]),
        }

    @staticmethod
    def summarize(lna0_grid, P):
        g = np.asarray(lna0_grid)
        i = int(np.argmax(P))
        if 0 < i < len(g) - 1:
            c = np.polyfit(g[i - 1 : i + 2], P[i - 1 : i + 2], 2)
            best = -c[1] / (2 * c[0]) if c[0] < 0 else g[i]
            Pmax = np.polyval(c, best) if c[0] < 0 else P[i]
        else:
            best, Pmax = g[i], P[i]
        dchi = 2 * (Pmax - P)
        out = {"lna0_hat": float(best), "at_edge": bool(i in (0, len(g) - 1))}
        for lab, thr in (("68", 1.0), ("95", 3.841)):
            lo = hi = None
            # walk outwards from the max
            for j in range(i, 0, -1):
                if dchi[j - 1] > thr:
                    lo = float(np.interp(thr, [dchi[j], dchi[j - 1]], [g[j], g[j - 1]]))
                    break
            for j in range(i, len(g) - 1):
                if dchi[j + 1] > thr:
                    hi = float(np.interp(thr, [dchi[j], dchi[j + 1]], [g[j], g[j + 1]]))
                    break
            out["ci" + lab] = [lo, hi]  # None = open (grid edge reached)
        out["dchi2_fn"] = (g, dchi)
        return out

    def fit(self, lna0_grid, **kw):
        P, meta = self.profile(lna0_grid, **kw)
        s = self.summarize(lna0_grid, P)
        s.update(meta)
        return s


def dchi2_at(summary, lna0):
    g, dchi = summary["dchi2_fn"]
    return float(np.interp(lna0, g, dchi))


# ----------------------------------------------------------------------------- simulation
def _trunc_norm_mean(mu, s, lo=0.0, hi=1.0):
    a, b = (lo - mu) / s, (hi - mu) / s
    Z = special.ndtr(b) - special.ndtr(a)
    return mu + s * (np.exp(-0.5 * a * a) - np.exp(-0.5 * b * b)) / (
        math.sqrt(2 * math.pi) * np.maximum(Z, 1e-300)
    )


def simulate(gbar_true, err, a0, sig_int, rng, route="fdm", report="gauss"):
    """err: dict with s_lnV, s_lnR, s_f (fdm) / s_lnM (mbar).  Returns a data view."""
    n = len(gbar_true)
    lngt = np.log(g_pred(gbar_true, a0)) + sig_int * rng.standard_normal(n)
    eV = err["s_lnV"] * rng.standard_normal(n)
    eR = err["s_lnR"] * rng.standard_normal(n)
    lng_obs = lngt + 2 * eV - eR
    s_lng = np.sqrt((2 * err["s_lnV"]) ** 2 + err["s_lnR"] ** 2)
    if route == "fdm":
        ft = 1.0 - gbar_true / np.exp(lngt)
        f_obs = ft + err["s_f"] * rng.standard_normal(n)
        if (
            report == "bounded"
        ):  # stylized posterior-mean report under a flat [0,1] prior
            f_obs = _trunc_norm_mean(f_obs, err["s_f"])
        return {"lng": lng_obs, "s_lng": s_lng, "f": f_obs, "s_f": err["s_f"]}
    eM = err["s_lnM"] * rng.standard_normal(n)
    lngb = np.log(gbar_true) + eM - 2 * eR
    return {
        "lng": lng_obs,
        "s_lng": s_lng,
        "lngb": lngb,
        "s_lngb": np.sqrt(err["s_lnM"] ** 2 + (2 * err["s_lnR"]) ** 2),
        "c": 2 * err["s_lnR"] ** 2,
    }


def asimov(gbar_true, err, a0, route="fdm"):
    lngt = np.log(g_pred(gbar_true, a0))
    s_lng = np.sqrt((2 * err["s_lnV"]) ** 2 + err["s_lnR"] ** 2)
    if route == "fdm":
        return {
            "lng": lngt.copy(),
            "s_lng": s_lng,
            "f": 1.0 - gbar_true / np.exp(lngt),
            "s_f": err["s_f"],
        }
    return {
        "lng": lngt.copy(),
        "s_lng": s_lng,
        "lngb": np.log(gbar_true),
        "s_lngb": np.sqrt(err["s_lnM"] ** 2 + (2 * err["s_lnR"]) ** 2),
        "c": 2 * err["s_lnR"] ** 2,
    }


LNA0_GRID_REL = np.linspace(math.log(0.2), math.log(8.0), 45)


def _one_realization(args):
    gbar, err, a0_true, a0_anchor, sig_int, seed, route, report = args
    rng = np.random.default_rng(seed)
    v = simulate(gbar, err, a0_true, sig_int, rng, route, report)
    grid = math.log(a0_anchor) + LNA0_GRID_REL
    s = JointA0Likelihood(v, route).fit(grid)
    la_t = math.log(a0_true)
    la_1, la_179 = math.log(a0_anchor), math.log(a0_anchor * HUBBLE_Z1_RATIO)

    def inside(ci, x):
        lo = ci[0] if ci[0] is not None else -np.inf
        hi = ci[1] if ci[1] is not None else np.inf
        return bool(lo <= x <= hi)

    return {
        "hat": s["lna0_hat"] - la_t,
        "edge": s["at_edge"],
        "in68": inside(s["ci68"], la_t),
        "in95": inside(s["ci95"], la_t),
        "open68": s["ci68"][0] is None or s["ci68"][1] is None,
        "w68": (s["ci68"][1] - s["ci68"][0]) / 2 if None not in s["ci68"] else np.nan,
        "dchi2_at_1x": dchi2_at(s, la_1),
        "dchi2_at_179x": dchi2_at(s, la_179),
        "sig_best": s["sig_best"],
    }


def injection_recovery(
    gbar,
    err,
    a0_true,
    a0_anchor,
    n_real,
    sig_int=0.1,
    route="fdm",
    report="gauss",
    jobs=1,
    seed0=1000,
):
    args = [
        (gbar, err, a0_true, a0_anchor, sig_int, seed0 + i, route, report)
        for i in range(n_real)
    ]
    if jobs > 1:
        from multiprocessing import Pool

        with Pool(jobs) as p:
            res = p.map(_one_realization, args, chunksize=4)
    else:
        res = [_one_realization(a) for a in args]
    hat = np.array([r["hat"] for r in res])
    w68 = np.array([r["w68"] for r in res])
    other = "dchi2_at_179x" if abs(a0_true / a0_anchor - 1) < 1e-9 else "dchi2_at_1x"
    dch = np.array([r[other] for r in res])
    n = len(res)
    return {
        "n_real": n,
        "N_gal": int(len(gbar)),
        "a0_true_over_anchor": a0_true / a0_anchor,
        "route": route,
        "report": report,
        "sig_int_injected": sig_int,
        "median_bias_lna0": float(np.median(hat)),
        "mean_bias_lna0": float(np.mean(hat)),
        "ensemble_sd_lna0": float(np.std(hat)),
        "ensemble_16_84_lna0": [float(x) for x in np.percentile(hat, [16, 84])],
        "median_reported_halfwidth68_lna0": float(np.nanmedian(w68)),
        "frac_open_68": float(np.mean([r["open68"] for r in res])),
        "frac_at_grid_edge": float(np.mean([r["edge"] for r in res])),
        "coverage68": float(np.mean([r["in68"] for r in res])),
        "coverage95": float(np.mean([r["in95"] for r in res])),
        "binom_3sigma_68": 3 * math.sqrt(0.683 * 0.317 / n),
        "binom_3sigma_95": 3 * math.sqrt(0.95 * 0.05 / n),
        "alt_hypothesis": "1.791x" if other == "dchi2_at_179x" else "1x",
        "median_dchi2_alt": float(np.median(dch)),
        "frac_alt_excluded_95": float(np.mean(dch > 3.841)),
        "frac_alt_excluded_3sigma": float(np.mean(dch > 9.0)),
    }


# ----------------------------------------------------------------------------- fisher / leverage on the real x-distribution
def fisher_summary(d, a0, idx):
    x = d["g_obs"][idx] / a0
    J = x / (1 + x * x) ** 1.5
    s_eff2 = d["e_fDM"][idx] ** 2 + J**2 * d["s_lng"][idx] ** 2
    I = J**2 / s_eff2
    return {
        "N": int(len(x)),
        "x_median": float(np.median(x)),
        "x_16_84": [float(v) for v in np.percentile(x, [16, 84])],
        "f_implied_median": float(np.median(1 - mu_std(x))),
        "sigma_lna0_fisher": float(1 / math.sqrt(I.sum())),
        "N_eff": float(I.sum() ** 2 / (I * I).sum()),
        "sigma_lna0_per_galaxy_median": float(np.median(1 / np.sqrt(I))),
        "frac_per_galaxy_sigma_lna0_gt_1": float(np.mean(1 / np.sqrt(I) > 1.0)),
        "top_info_galaxies": [
            d["galaxy"][int(np.asarray(idx)[k])] for k in np.argsort(-I)[:8]
        ],
    }


# ----------------------------------------------------------------------------- distance
class FlatLCDM:
    def __init__(self, H0=70.0, Om=0.3):
        self.H0, self.Om = H0, Om

    def chi(self, z):
        return (
            C_LIGHT
            / (self.H0 * 1e3 / MPC)
            * integrate.quad(
                lambda zz: 1 / math.sqrt(self.Om * (1 + zz) ** 3 + 1 - self.Om), 0, z
            )[0]
        )

    def D_A(self, z):
        return self.chi(z) / (1 + z)

    def D_L(self, z):
        return self.chi(z) * (1 + z)


def observe_infer(z, true, assumed, w, x_true=3.0, a0=1.0):
    """Observed (V, theta, flux, fDM) of a galaxy under cosmology `true`, re-inferred with
    `assumed`.  w = weight of the photometric M_bar prior in the dynamical fit (0: data-only).
    """
    DA_t, DA_a = true.D_A(z), assumed.D_A(z)
    DL_t, DL_a = true.D_L(z), assumed.D_L(z)
    s = DA_a / DA_t  # == DL_a/DL_t (Etherington, flat both)
    g_true = x_true * a0
    gb_true = g_true * mu_std(x_true)
    g_inf = g_true / s  # V^2 / (theta D_A,assumed)
    gb_phot = gb_true * (DL_a / DL_t) ** 2 / s**2  # G M(D_L^2) / Re(D_A)^2
    r_true = gb_true / g_true
    r_inf = (
        r_true * s**w
    )  # V_bar^2 at fixed angle: data-only invariant; prior ∝ M/Re ∝ D
    a0_fdm = float(a0_from_fdm(g_inf, 1 - r_inf))
    return {"s": s, "g_inf": g_inf, "gbar_phot": gb_phot, "a0_fdm": a0_fdm}


def distance_record(anchor_a0):
    rc = FlatLCDM(70.0, 0.3)
    pl = FlatLCDM(67.36, 0.3153)
    h73 = FlatLCDM(73.0, 0.3)
    out = {"slopes": {}, "zp": {}}
    eps = 1e-6
    for w in (0.0, 1.0):
        for x in (3.0, 10.0):
            base = observe_infer(1.0, rc, rc, w, x)
            pert = observe_infer(1.0, rc, FlatLCDM(70.0 / (1 + eps), 0.3), w, x)
            dl = math.log(pert["s"])
            out["slopes"][f"w={w:g},x={x:g}"] = {
                "dln_gobs": math.log(pert["g_inf"] / base["g_inf"]) / dl,
                "dln_gbar_phot": math.log(pert["gbar_phot"] / base["gbar_phot"]) / dl,
                "dln_a0_fdm": math.log(pert["a0_fdm"] / base["a0_fdm"]) / dl,
                "predicted_a0_fdm": -1 - w * (1 + x * x),
            }
    for z in (0.9, 1.5, 2.2):
        out["zp"][f"z={z}"] = {
            "D_A(70,0.3)/D_A(Planck)": rc.D_A(z) / pl.D_A(z),
            "D_A(70,0.3)/D_A(73,0.3)": rc.D_A(z) / h73.D_A(z),
            "D_A(70,0.3)/D_A(70,0.3153)": rc.D_A(z) / FlatLCDM(70, 0.3153).D_A(z),
        }
    return out


# ----------------------------------------------------------------------------- systematics (Asimov)
def perturb(v_fdm, d, idx, kind, amp, w=1.0, limit="vbar_fixed"):
    """Apply a systematic to a noise-free fdm-route data view.  Returns a new view."""
    v = {k: np.array(val, float) for k, val in v_fdm.items()}
    f = v["f"]
    r = 1 - f
    g = np.exp(v["lng"])
    if kind == "df":  # fDM zero-point shift
        v["f"] = f + amp
        return v
    if kind in ("imf", "gas"):  # dex shift on one M_bar component, prior-weight w
        frac = amp[1]  # stellar (imf) or gas (gas) fraction of M_bar
        dlnM = math.log(frac * 10 ** amp[0] + (1 - frac))
        v["f"] = 1 - r * math.exp(w * dlnM)
        return v
    if kind in ("pressure", "vc"):
        if kind == "pressure":
            fac = 1 + (amp - 1) * d["p_pressure"][idx]  # Vc'^2/Vc^2
        else:
            fac = math.exp(2 * amp)
        v["lng"] = v["lng"] + np.log(fac)
        if limit == "vbar_fixed":
            v["f"] = 1 - r / fac
        return v
    if kind == "distance":  # amp = D_assumed/D_true ; data-dominated w=0 default
        v["lng"] = v["lng"] - math.log(amp)
        v["f"] = 1 - r * amp ** (-w) if w else f
        return v
    raise ValueError(kind)


def systematics_table(d, idx, gbar, err, a0_true, anchor):
    grid = math.log(anchor) + LNA0_GRID_REL
    base_v = asimov(gbar, err, a0_true)
    base = JointA0Likelihood(base_v).fit(grid)["lna0_hat"]
    rows = []

    def run(name, v, note=""):
        h = JointA0Likelihood(v).fit(grid)
        rows.append(
            {
                "systematic": name,
                "dlna0": h["lna0_hat"] - base,
                "at_edge": h["at_edge"],
                "note": note,
            }
        )

    for amp, src in (
        (+0.05, "AC on vs off / G20 A.4"),
        (-0.05, "halo c 4->2 at z~2.3 / G20 A.4"),
        (+0.11, "MCMC minus chi2 fDM offset / G20 A.4"),
        (-0.11, "same, reversed"),
    ):
        run(f"fDM zero-point {amp:+.2f}", perturb(base_v, d, idx, "df", amp), src)
    for fst in (0.5, 0.67):
        for dex in (+0.23, +0.3, -0.2):
            run(
                f"IMF dlogM*={dex:+.2f}, f*={fst}, w=1",
                perturb(base_v, d, idx, "imf", (dex, fst), 1.0),
                "w=0 (data-dominated fit) gives exactly 0; +0.23 = Salpeter vs Chabrier (G20)",
            )
    for fg in (1 / 3, 0.5):
        for dex in (+0.25, -0.25):
            run(
                f"gas dlogMgas={dex:+.2f}, fgas={fg:.2f}, w=1",
                perturb(base_v, d, idx, "gas", (dex, fg), 1.0),
                "T20: +/-0.25 dex CO/dust mass systematics; G20: Mgas/M* ~0.5-1 at z~1-2.5",
            )
    for alpha, src in (
        (0.5, "test amplitude"),
        (1.5, "test amplitude"),
        (2 * sersic_b(0.5) / 0.5 / BURKERT_COEF, "Sersic n=0.5 dlnSigma/dlnr at Re"),
        (2 * sersic_b(2.0) / 2.0 / BURKERT_COEF, "Sersic n=2 dlnSigma/dlnr at Re"),
    ):
        for lim in ("vbar_fixed", "f_fixed"):
            run(
                f"pressure alpha={alpha:.3f} ({lim})",
                perturb(base_v, d, idx, "pressure", alpha, limit=lim),
                src,
            )
    for dv in (+0.05, -0.05, +0.10, -0.10):
        for lim in ("vbar_fixed", "f_fixed"):
            run(
                f"beam/Vc dlnVc={dv:+.2f} ({lim})",
                perturb(base_v, d, idx, "vc", dv, limit=lim),
                "test amplitude; RC100 methods A/B/C agree within combined errors",
            )
    zmed = float(np.median(d["z"][idx]))
    rc, pl, h73 = FlatLCDM(70, 0.3), FlatLCDM(67.36, 0.3153), FlatLCDM(73.0, 0.3)
    for name, cos in (("Planck 67.36/0.3153", pl), ("H0=73", h73)):
        s = rc.D_A(zmed) / cos.D_A(zmed)
        run(
            f"distance RC100 -> {name} (w=0)",
            perturb(base_v, d, idx, "distance", s, w=0.0),
            f"z_med={zmed:.2f}, D_ass/D_true={s:.4f}",
        )
        run(
            f"distance RC100 -> {name} (w=1)",
            perturb(base_v, d, idx, "distance", s, w=1.0),
            "prior-dominated limit",
        )
    return {"base_lna0_minus_true": base - math.log(a0_true), "rows": rows}


def mbar_geometry_shifts(d, idx, gbar, err, a0_true, anchor, geo):
    """Route (b): g_bar_b scales with the assumed k; shift of a0 under k choices (Asimov)."""
    grid = math.log(anchor) + LNA0_GRID_REL
    v0 = asimov(gbar, {**err}, a0_true, route="mbar")
    base = JointA0Likelihood(v0, "mbar").fit(grid)["lna0_hat"]
    k0 = geo["k_q0.20_Re"]
    out = {"base_lna0_minus_true": base - math.log(a0_true)}
    for lab, k in (
        ("sphere M/2", 0.5),
        ("thin Freeman", geo["k_thin_freeman_Re"]),
        ("q=0.25", geo["k_q0.25_Re"]),
        ("deprojected sphere", geo["k_q1_sphere_deprojected_Re (M3D(<Re)/M)"]),
    ):
        v = dict(v0)
        v["lngb"] = v0["lngb"] + math.log(k / k0)
        out[f"k: q0.20 -> {lab}"] = (
            JointA0Likelihood(v, "mbar").fit(grid)["lna0_hat"] - base
        )
    for dex in (+0.1, -0.1):
        v = dict(v0)
        v["lngb"] = v0["lngb"] + dex * math.log(10)
        out[f"M_bar {dex:+.1f} dex"] = (
            JointA0Likelihood(v, "mbar").fit(grid)["lna0_hat"] - base
        )
    return out


# ----------------------------------------------------------------------------- self-test
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}", flush=True)


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items() if k != "dchi2_fn"}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (np.floating, float)):
        return None if (isinstance(o, float) and math.isnan(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-real", type=int, default=200)
    ap.add_argument("--n-real-aux", type=int, default=100)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    rec = {
        "generated": "2026-09-16",
        "module": "02_galaxy_dynamics/highz_a0_method.py",
        "status": "METHOD ONLY — estimator not run on RC100 observables (blind)",
    }

    anc = load_anchor()
    A0 = anc["a0"]
    rec["anchor"] = anc
    print(
        f"anchor T3: a0={A0:.5e} 95%={anc['ci95']}  (CURRENT_STATE headline is T1 {anc['T1_a0']:.4e})"
    )

    # S1 algebra
    gb = np.logspace(-2, 2, 400) * A0
    g = g_pred(gb, A0)
    cl = np.max(np.abs(g * mu_std(g / A0) / gb - 1))
    inv = np.max(np.abs(a0_from_g_gbar(g, gb) / A0 - 1))
    fr = np.max(np.abs(a0_from_fdm(g, 1 - gb / g) / A0 - 1))
    nu = np.max(np.abs(nu_std(gb / A0) - g / gb))
    check(
        "S1 closure g*mu(g/a0)=gbar; exact inverse and fDM inverse round-trip",
        cl < 1e-12 and inv < 1e-6 and fr < 1e-6 and nu < 1e-12,
        f"closure {cl:.1e} inv {inv:.1e} fdm-inv {fr:.1e} nu {nu:.1e}",
    )
    no_sol = np.isnan(a0_from_fdm(1.0, -0.01)) and np.isnan(a0_from_g_gbar(1.0, 1.01))
    check("S1b inverse undefined for f<=0 / gbar>=g (censoring is real)", no_sol)

    # S2 leverage
    worst = 0.0
    for x in (3.0, 10.0, 30.0):
        L = leverage(x)
        gg, gbb = x, x * mu_std(x)
        h = 1e-7
        n1 = (
            math.log(a0_from_g_gbar(gg, gbb * math.exp(h)))
            - math.log(a0_from_g_gbar(gg, gbb * math.exp(-h)))
        ) / (2 * h)
        n4 = (
            math.log(a0_from_g_gbar(gg * math.exp(h), gbb))
            - math.log(a0_from_g_gbar(gg * math.exp(-h), gbb))
        ) / (2 * h)
        f0 = 1 - mu_std(x)
        n2 = (
            math.log(a0_from_fdm(gg, f0 + h * f0))
            - math.log(a0_from_fdm(gg, f0 - h * f0))
        ) / (2 * h * f0)
        n3 = (
            math.log(a0_from_fdm(gg * math.exp(h), f0))
            - math.log(a0_from_fdm(gg * math.exp(-h), f0))
        ) / (2 * h)
        for num, ana in (
            (n1, L["dlna0_dlngbar_fixed_g"]),
            (n2, L["dlna0_dfdm_fixed_g"]),
            (n3, L["dlna0_dlng_fixed_f"]),
            (n4, L["dlna0_dlng_fixed_gbar"]),
        ):
            worst = max(worst, abs(num / float(ana) - 1))
        worst = max(
            worst,
            abs(float(L["dlna0_dlngbar_fixed_g"] + L["dlna0_dlng_fixed_gbar"]) - 1),
        )
    check(
        "S2 leverage derivatives == finite differences; d/dln gbar + d/dln g = 1",
        worst < 1e-4,
        f"worst rel {worst:.1e}",
    )
    lev = {
        f"x={x:g}": {k: float(v) for k, v in leverage(x).items()}
        for x in (1.0, 3.0, 10.0, 30.0)
    }
    rec["leverage"] = lev
    rec["fdm_pm0.1_table"] = fdm_error_table()
    for r in rec["fdm_pm0.1_table"]:
        print(
            f"  x={r['x']:>4g} gbar/a0={r['gbar_over_a0']:.3f} f_impl={r['f_implied']:.5f} "
            f"a0'(f+0.1)/a0={r['a0_ratio_f_plus']:.3f} a0'(f-0.1)={r['a0_ratio_f_minus']} "
            f"lin dlna0/df={r['linear_dlna0_df']:.1f}"
        )

    # S3 geometry
    geo = geometry_table()
    rec["geometry"] = geo
    k0a = max(
        abs(_inner_I(m, 1.0) / inner_I_numeric(m, 1.0) - 1)
        for m in (0.05, 0.3, 1.0, 2.5)
    )
    rp = max(
        abs(reproject_sphere(R, n) / float(sersic_sigma(R, n)) - 1)
        for n in (1.0, 4.0)
        for R in (0.5, 1.0, 2.0)
    )
    thin = max(
        abs(k_spheroid(R, 1.0, 0.0) / float(k_freeman_thin(R)) - 1)
        for R in (0.5, 1.0, 2.0)
    )
    thin_q = abs(k_spheroid(1.0, 1.0, 1e-3) / float(k_freeman_thin(1.0)) - 1)
    far = max(
        abs(k_spheroid(40.0, n, q) - 1)
        for n, q in ((1.0, 1.0), (1.0, 0.25), (4.0, 1.0))
    )
    check(
        "S3a n=1 deprojection: numeric inner integral == K0 closed form",
        k0a < 1e-6,
        f"{k0a:.1e}",
    )
    check(
        "S3b Abel deprojection re-projects to the Sersic Sigma (n=1,4)",
        rp < 1e-4,
        f"{rp:.1e}",
    )
    check(
        "S3c q->0 spheroid == Freeman thin disk (B&T 2.165)",
        thin < 1e-4 and thin_q < 5e-3,
        f"q=0 {thin:.1e}, q=1e-3 {thin_q:.1e}",
    )
    check("S3d k -> 1 far outside (total mass)", far < 5e-3, f"{far:.1e}")
    check(
        "S3e Burkert 3.36 == 2 b_1; projected enclosed fraction at Re == 1/2",
        abs(geo["burkert_2b1"] - 3.36) < 0.005
        and abs(geo["cyl_enclosed_at_Re"] - 0.5) < 1e-12,
        f"2b1={geo['burkert_2b1']:.4f}",
    )
    vr = math.sqrt(geo["k_q0.25_Re"] / geo["k_thin_freeman_Re"])
    check(
        "S3f G20 A: thick disk (q~0.25) V(Re) ~10% below Freeman",
        0.85 < vr < 0.95,
        f"V ratio {vr:.3f}",
    )
    print(
        "  geometry:",
        {k: (round(v, 4) if isinstance(v, float) else v) for k, v in geo.items()},
    )

    # S4 data
    d = load_rc100(k_disk=geo["k_q0.20_Re"])
    nok = int(d["sigmaDM_ok"].sum())
    bad = [d["galaxy"][i] for i in np.where(~d["sigmaDM_ok"])[0]]
    check(
        "S4 RC100 transcription: Sigma_DM(<Re) recomputed from (fDM,Vc,Re) matches column",
        nok >= 95 and len(d["z"]) == 100,
        f"{nok}/100 within rounding; off: {bad}",
    )
    evc = d["e_Vc_kms"] / d["Vc_kms"]
    ratio_ab = d["gbar_a"] / d["gbar_b"]
    keff = (
        (1 - d["fDM"]) * (d["Vc_kms"] ** 2) * d["Re_kpc"] / (G_KPC * 10 ** d["logMbar"])
    )
    datarec = {
        "N": 100,
        "bins": {
            "z<1.2": int((d["bin"] == 0).sum()),
            "z>=1.2": int((d["bin"] == 1).sum()),
        },
        "sigmaDM_check_pass": nok,
        "sigmaDM_check_off": bad,
        "e_Vc_over_Vc": {
            "min": float(evc.min()),
            "median": float(np.median(evc)),
            "max": float(evc.max()),
        },
        "s_lng_median": float(np.median(d["s_lng"])),
        "e_fDM_median": float(np.median(d["e_fDM"])),
        "s_lngb_median": float(np.median(d["s_lngb"])),
        "k_eff=(1-f)Vc^2Re/(G Mbar)": {
            "median": float(np.median(keff)),
            "16_84": [float(v) for v in np.percentile(keff, [16, 84])],
            "min": float(keff.min()),
            "max": float(keff.max()),
        },
        "gbar_a_over_gbar_b(q0.2,BT=0)": {
            "median": float(np.median(ratio_ab)),
            "16_84": [float(v) for v in np.percentile(ratio_ab, [16, 84])],
        },
        "log10_gbar_a_over_anchor": {
            "median": float(np.median(np.log10(d["gbar_a"] / A0))),
            "16_84": [
                float(v) for v in np.percentile(np.log10(d["gbar_a"] / A0), [16, 84])
            ],
        },
        "log10_gobs_over_anchor": {
            "median": float(np.median(np.log10(d["g_obs"] / A0))),
            "min": float(np.log10(d["g_obs"] / A0).min()),
            "max": float(np.log10(d["g_obs"] / A0).max()),
        },
        "pressure_p=3.36sig0^2/Vc^2": {
            "median": float(np.median(d["p_pressure"])),
            "max": float(d["p_pressure"].max()),
            "n_p_ge_1": int((d["p_pressure"] >= 1).sum()),
            "p_ge_1": [d["galaxy"][i] for i in np.where(d["p_pressure"] >= 1)[0]],
        },
        "n_f_minus_1sigma_le_0": int(((d["fDM"] - d["e_fDM"]) <= 0).sum()),
        "fisher_at_anchor": {
            "all": fisher_summary(d, A0, np.arange(100)),
            "z<1.2": fisher_summary(d, A0, np.where(d["bin"] == 0)[0]),
            "z>=1.2": fisher_summary(d, A0, np.where(d["bin"] == 1)[0]),
        },
        "fisher_at_1.791x": {
            "all": fisher_summary(d, A0 * HUBBLE_Z1_RATIO, np.arange(100))
        },
    }
    rec["rc100_inputs"] = datarec
    print(
        "  k_eff:",
        datarec["k_eff=(1-f)Vc^2Re/(G Mbar)"],
        " gbar_a/gbar_b:",
        datarec["gbar_a_over_gbar_b(q0.2,BT=0)"],
    )
    print(
        "  fisher:",
        {
            k: (v["sigma_lna0_fisher"], v["N_eff"], v["x_median"])
            for k, v in datarec["fisher_at_anchor"].items()
        },
    )

    # S5 distance
    dist = distance_record(A0)
    rec["distance"] = dist
    sl_ok = all(
        abs(v["dln_gobs"] + 1) < 1e-4
        and abs(v["dln_gbar_phot"]) < 1e-4
        and abs(v["dln_a0_fdm"] / v["predicted_a0_fdm"] - 1) < 1e-3
        for v in dist["slopes"].values()
    )
    check(
        "S5 distance log-slopes: g_obs -1 (PR #67 rotation-curve exponent), photometric gbar 0, "
        "fDM-route a0 -1-w(1+x^2)",
        sl_ok,
        json.dumps({k: round(v["dln_a0_fdm"], 3) for k, v in dist["slopes"].items()}),
    )

    # errors & truths for injections
    def err_for(idx):
        return {
            "s_lnV": d["s_lnV"][idx],
            "s_lnR": d["s_lnR"][idx],
            "s_f": d["e_fDM"][idx],
            "s_lnM": d["s_lnM"][idx],
        }

    ALL = np.arange(100)
    gbar_all = d["gbar_a"]
    grid = math.log(A0) + LNA0_GRID_REL

    # S6 engine sanity with tiny errors
    # (errors /10; the latent ln g_bar grid is refined to n_u=320 so it resolves the narrower
    #  per-galaxy likelihood — at RC100 error sizes n_u=48 is converged to <1e-3 in ln a0)
    tiny = {k: v / 10 for k, v in err_for(ALL).items()}
    rng = np.random.default_rng(3)
    ok6 = []
    for mult in (1.0, HUBBLE_Z1_RATIO):
        for route in ("fdm", "mbar"):
            v = simulate(gbar_all, tiny, A0 * mult, 0.0, rng, route)
            h = JointA0Likelihood(v, route, n_u=320).fit(grid)["lna0_hat"]
            ok6.append(abs(h - math.log(A0 * mult)))
    check(
        "S6 estimator recovers a0 with errors /10 (both routes, both truths)",
        max(ok6) < 0.02,
        f"max |dln a0| {max(ok6):.4f}",
    )

    # S7 Asimov bias at real error sizes
    asi = {}
    for mult in (1.0, HUBBLE_Z1_RATIO):
        for route in ("fdm", "mbar"):
            v = asimov(gbar_all, err_for(ALL), A0 * mult, route)
            asi[f"{route},{mult:g}x"] = JointA0Likelihood(v, route).fit(grid)[
                "lna0_hat"
            ] - math.log(A0 * mult)
    rec["asimov_bias_lna0"] = asi
    check(
        "S7 Asimov (noise-free) bias at RC100 error sizes < 0.05 in ln a0",
        max(abs(x) for x in asi.values()) < 0.05,
        json.dumps({k: round(v, 4) for k, v in asi.items()}),
    )

    # S8 injection-recovery with coverage (primary: fdm route, full sample)
    inj = {}
    for mult in (1.0, HUBBLE_Z1_RATIO):
        key = f"fdm,all,{mult:g}x"
        t1 = time.time()
        inj[key] = injection_recovery(
            gbar_all, err_for(ALL), A0 * mult, A0, a.n_real, jobs=a.jobs
        )
        print(
            f"  {key}: {json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in inj[key].items()})} "
            f"[{time.time() - t1:.0f}s]",
            flush=True,
        )
    for b, lab in ((0, "z<1.2"), (1, "z>=1.2")):
        idx = np.where(d["bin"] == b)[0]
        for mult in (1.0, HUBBLE_Z1_RATIO):
            key = f"fdm,{lab},{mult:g}x"
            inj[key] = injection_recovery(
                d["gbar_a"][idx],
                err_for(idx),
                A0 * mult,
                A0,
                a.n_real_aux,
                jobs=a.jobs,
                seed0=5000 + b,
            )
            print(
                f"  {key}: bias {inj[key]['median_bias_lna0']:+.3f} sd {inj[key]['ensemble_sd_lna0']:.3f} "
                f"cov68 {inj[key]['coverage68']:.2f} cov95 {inj[key]['coverage95']:.2f} "
                f"alt-excl95 {inj[key]['frac_alt_excluded_95']:.2f}",
                flush=True,
            )
    for mult in (1.0, HUBBLE_Z1_RATIO):
        key = f"fdm,all,{mult:g}x,bounded-report"
        inj[key] = injection_recovery(
            gbar_all,
            err_for(ALL),
            A0 * mult,
            A0,
            a.n_real_aux,
            report="bounded",
            jobs=a.jobs,
            seed0=7000,
        )
        print(
            f"  {key}: bias {inj[key]['median_bias_lna0']:+.3f} cov68 {inj[key]['coverage68']:.2f}",
            flush=True,
        )
        key = f"mbar,all,{mult:g}x"
        inj[key] = injection_recovery(
            d["gbar_b"],
            err_for(ALL),
            A0 * mult,
            A0,
            a.n_real_aux,
            route="mbar",
            jobs=a.jobs,
            seed0=9000,
        )
        print(
            f"  {key}: bias {inj[key]['median_bias_lna0']:+.3f} sd {inj[key]['ensemble_sd_lna0']:.3f} "
            f"cov68 {inj[key]['coverage68']:.2f} alt-excl95 {inj[key]['frac_alt_excluded_95']:.2f}",
            flush=True,
        )
    rec["injection"] = inj
    for mult in (1.0, HUBBLE_Z1_RATIO):
        r = inj[f"fdm,all,{mult:g}x"]
        check(
            f"S8 fdm route N=100 truth {mult:g}x: |median bias| < ensemble sd/3",
            abs(r["median_bias_lna0"]) < r["ensemble_sd_lna0"] / 3,
            f"bias {r['median_bias_lna0']:+.4f} sd {r['ensemble_sd_lna0']:.4f}",
        )
        check(
            f"S9 fdm route N=100 truth {mult:g}x: 68%/95% profile intervals calibrated (3-sigma binomial)",
            abs(r["coverage68"] - 0.683) < r["binom_3sigma_68"]
            and abs(r["coverage95"] - 0.95) < r["binom_3sigma_95"] + 0.005,
            f"cov68 {r['coverage68']:.3f} cov95 {r['coverage95']:.3f}",
        )
    rec["discrimination_1x_vs_1.791x"] = {
        k: {
            "alt": v["alt_hypothesis"],
            "median_dchi2_alt": v["median_dchi2_alt"],
            "frac_excl_95": v["frac_alt_excluded_95"],
            "frac_excl_3sigma": v["frac_alt_excluded_3sigma"],
        }
        for k, v in inj.items()
    }

    # S10 systematics (Asimov)
    syst = {}
    for mult in (1.0, HUBBLE_Z1_RATIO):
        syst[f"{mult:g}x"] = systematics_table(
            d, ALL, gbar_all, err_for(ALL), A0 * mult, A0
        )
        print(f"  systematics @ {mult:g}x:")
        for r in syst[f"{mult:g}x"]["rows"]:
            print(
                f"    {r['systematic']:<48s} dln a0 = {r['dlna0']:+.3f}{'  [EDGE]' if r['at_edge'] else ''}"
            )
    syst["mbar_geometry"] = {
        f"{m:g}x": mbar_geometry_shifts(
            d, ALL, d["gbar_b"], err_for(ALL), A0 * m, A0, geo
        )
        for m in (1.0, HUBBLE_Z1_RATIO)
    }
    print("  mbar geometry:", json.dumps(_clean(syst["mbar_geometry"]), indent=None))
    rec["systematics_asimov"] = syst
    zero_w0 = abs(
        JointA0Likelihood(
            perturb(asimov(gbar_all, err_for(ALL), A0), d, ALL, "imf", (0.23, 0.6), 0.0)
        ).fit(grid)["lna0_hat"]
        - JointA0Likelihood(asimov(gbar_all, err_for(ALL), A0)).fit(grid)["lna0_hat"]
    )
    check(
        "S10 IMF shift has zero effect in the data-dominated (w=0) limit",
        zero_w0 < 1e-9,
        f"{zero_w0:.1e}",
    )

    rec["checks"] = [{"name": n, "pass": p} for n, p in RESULTS]
    rec["runtime_s"] = time.time() - t0
    if not a.no_write:
        OUT_JSON.write_text(json.dumps(_clean(rec), indent=1))
        print("written:", OUT_JSON.relative_to(HERE.parent))
    npass = sum(p for _, p in RESULTS)
    print(f"\n{npass}/{len(RESULTS)} checks passed  ({time.time() - t0:.0f}s)")
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
