#!/usr/bin/env python3
"""Tidal screening in wide binaries: the two-body QUMOND field, and Cassini for the action form.
Pre-registered in PREREG_TIDAL_WIDE_BINARY_2026-10-15.md before any prediction was computed.

Model (TIDAL_SCREENING_2026-10-15.md), quasistatic QUMOND:
  L = -(1/8 pi G) [2 grad Phi . grad Phi_N - a0^2 Qs(z, x)] - rho Phi,
  Qs = z + S(x) P(y),   z = y^2 = |grad Phi_N|^2 / a0^2,   P(y) = Q(z) - z = Int_0^y 2t (nu(t) - 1) dt,
  x = c^2 sqrt(|H|_F^2 + h_g^2) / a0^2,  H = grad grad Phi_N,  h_g = 4 pi G (0.1 Msun/pc^3),
  S = 1 / (1 + (x/x*)^2),  nu = nu_std (mu_std).  h_g is the Galactic tide, added in quadrature as in
  tidal_screening_sparc_cassini.py. P(0) = 0: the MOND sector carries no energy where there is no field.
Varying Phi gives del^2 Phi_N = 4 pi G rho. Varying Phi_N gives
  del^2 Phi = div[nu_eff grad Phi_N] + d_i d_j W_ij,   nu_eff = 1 + S (nu - 1),
  W_ij = -(c^2/2) S'(x) P(y) H_ij / sqrt(|H|^2 + h_g^2)          ("action form").
tidal_screening_sparc_cassini.py solved the divergence term alone ("divergence form").
Forms here: unscreened (S = 1), divergence, action, and zero (S = 0, a gate).

Phantom acceleration at x_e, with D2, D3 the 2nd and 3rd derivatives of 1/r at d = x_e - x':
  g_ph(x_e) = (1/4 pi) Int D2(d).F dV + (1/4 pi) Int D3(d):W dV,   F = S (nu - 1) grad Phi_N,
plus -F(x_e)/3 where F is continuous and nonzero at x_e (a test point). At a point mass F, W and grad W
vanish, so a star needs no local term. Integrals use spherical grids centred on each star, with a smooth
partition of unity that hands the companion's neighbourhood to the companion's own grid. The uniform part
of F integrates to zero on every shell, so g_ph is computed up to a uniform field, which cancels in the
relative acceleration.

Usage: tidal_screening_two_body.py gates | cassini | table | all
Writes TIDAL_TWO_BODY_GATES.json, TIDAL_ACTION_CASSINI.json, TIDAL_TWO_BODY_TABLE.json.
"""
import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
A0 = 1.1607e-10
A0_DERIVED = 2.998e8 * (67.4e3 / 3.0857e22) / (2 * np.pi)
C = 2.998e8
G = 6.674e-11
MSUN, PC, AU = 1.989e30, 3.0857e16, 1.496e11
GM_SUN = 1.32712e20                       # efe_quadrupole_q2.GM
H_G = 4 * np.pi * G * 0.1 * MSUN / PC**3   # Galactic tide (Frobenius norm), s^-2
GES = (1.9e-10, 2.4e-10)
Q2_WINDOW = ((1.6 - 3.6) * 1e-27, (1.6 + 3.6) * 1e-27)   # 2026 bound 1.6 +/- 1.8, 2 sigma, two-sided
XSTAR_DIV = json.load(open(HERE / "TIDAL_SCREENING_SPARC_CASSINI.json"))["x_star"]
FOUR_PI = 4 * np.pi
EYE = np.eye(3)


def nu(y):
    y = np.maximum(y, 1e-100)
    return np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y**2)))


def _p_table():
    u = np.linspace(np.log(1e-12), np.log(1e14), 60001)
    t = np.exp(u)
    f = 2 * t**2 * (nu(t) - 1)
    P = (4 / 3) * 1e-18 + np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(u))])
    return u, np.log(P)


_PU, _PL = _p_table()


def P(y):
    """P(y) = Int_0^y 2t (nu - 1) dt, so P(0) = 0."""
    lu = np.log(np.maximum(y, 1e-300))
    out = np.exp(np.interp(lu, _PU, _PL))
    out = np.where(lu < _PU[0], (4 / 3) * np.maximum(y, 0) ** 1.5, out)
    return np.where(lu > _PU[-1], np.exp(_PL[-1]) + (lu - _PU[-1]), out)


def dP(y):
    return 2 * y * (nu(y) - 1)


def screen(x, xs, form):
    """S, S'(x), S''(x)."""
    if form == "unscreened":
        o = np.ones_like(x)
        return o, 0 * o, 0 * o
    if form == "zero":
        o = np.zeros_like(x)
        return o, o, o
    u = x / xs
    d = 1 + u**2
    return 1 / d, -2 * u / (xs * d**2), (6 * u**2 - 2) / (xs**2 * d**3)


def newtonian_ext(ge, a0=A0):
    """Newtonian external field g_Ne with nu(g_Ne/a0) g_Ne = g_e."""
    return 0.0 if ge == 0 else a0 * brentq(lambda z: z * nu(z) - ge / a0, 1e-10, ge / a0)


def fields(X, bodies, gNe_vec, xs, form, want_V=False, a0=A0):
    """F (N,3), W (N,3,3) and optionally V = div W (N,3) at points X (N,3).
    bodies: [(GM, pos)]; gNe_vec: Newtonian external field (grad Phi_N -> -gNe_vec far away)."""
    gp = np.broadcast_to(-np.asarray(gNe_vec, float), X.shape).copy()
    H = np.zeros(X.shape + (3,))
    dH = np.zeros(X.shape + (3, 3)) if want_V else None
    for GMa, pa in bodies:
        if GMa == 0:
            continue
        d = X - pa
        r2 = np.einsum("ni,ni->n", d, d)
        r = np.sqrt(r2)
        n = d / r[:, None]
        gp += (GMa / r2)[:, None] * n
        H += (GMa / r**3)[:, None, None] * (EYE - 3 * n[:, :, None] * n[:, None, :])
        if want_V:
            nnn = n[:, :, None, None] * n[:, None, :, None] * n[:, None, None, :]
            sym = (EYE[None, :, :, None] * n[:, None, None, :] + EYE[None, :, None, :] * n[:, None, :, None]
                   + EYE[None, None, :, :] * n[:, :, None, None])
            dH += (GMa / r**4)[:, None, None, None] * (15 * nnn - 3 * sym)
    gm = np.sqrt(np.einsum("ni,ni->n", gp, gp))
    y = gm / a0
    Hn = np.sqrt(np.einsum("nij,nij->n", H, H) + H_G**2)
    x = C**2 * Hn / a0**2
    S, S1, S2d = screen(x, xs, form)
    F = (S * (nu(y) - 1))[:, None] * gp
    Py = P(y)
    w = -(C**2 / 2) * S1 * Py
    W = (w / Hn)[:, None, None] * H
    if not want_V:
        return F, W, None
    dHn = np.einsum("nij,nijl->nl", H, dH) / Hn[:, None]
    dx = (C**2 / a0**2) * dHn
    dy = np.einsum("nj,njl->nl", gp, H) / (a0 * gm[:, None])
    dw = -(C**2 / 2) * ((S2d * Py)[:, None] * dx + (S1 * dP(y))[:, None] * dy)
    V = np.einsum("nkl,nl->nk", H, dw) / Hn[:, None] - (w / Hn**2)[:, None] * np.einsum("nkl,nl->nk", H, dHn)
    return F, W, V


def kern(xe, X, wq, F, W=None, V=None):
    """Phantom acceleration at xe from sources on quadrature points X with volume weights wq."""
    d = xe - X
    r = np.sqrt(np.einsum("ni,ni->n", d, d))
    n = d / r[:, None]
    nF = np.einsum("ni,ni->n", n, F)
    out = {"F": ((wq / r**3)[:, None] * (3 * nF[:, None] * n - F)).sum(0) / FOUR_PI}
    if W is not None:
        Wn = np.einsum("nij,nj->ni", W, n)
        nWn = np.einsum("ni,ni->n", n, Wn)
        tr = np.einsum("nii->n", W)
        out["W"] = -((wq / r**4)[:, None] * (15 * nWn[:, None] * n - 6 * Wn - 3 * tr[:, None] * n)).sum(0) / FOUR_PI
    if V is not None:
        nV = np.einsum("ni,ni->n", n, V)
        out["V"] = ((wq / r**3)[:, None] * (3 * nV[:, None] * n - V)).sum(0) / FOUR_PI
    return out


def _basis(axis):
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = t - a * (t @ a)
    e1 /= np.linalg.norm(e1)
    return e1, np.cross(a, e1), a


def sph_grid(center, axis, r_edges, nr, th_edges_deg, nth, nphi):
    xr, wr = np.polynomial.legendre.leggauss(nr)
    lr, wlr = [], []
    for lo, hi in zip(np.log(r_edges[:-1]), np.log(r_edges[1:])):
        lr.append(0.5 * (hi - lo) * xr + 0.5 * (hi + lo))
        wlr.append(0.5 * (hi - lo) * wr)
    rho = np.exp(np.concatenate(lr))
    wrho = rho**3 * np.concatenate(wlr)
    xt, wt = np.polynomial.legendre.leggauss(nth)
    mu, wmu = [], []
    for lo, hi in zip(np.cos(np.radians(th_edges_deg[:-1])), np.cos(np.radians(th_edges_deg[1:]))):
        mu.append(0.5 * (lo - hi) * xt + 0.5 * (lo + hi))
        wmu.append(0.5 * (lo - hi) * wt)
    mu, wmu = np.concatenate(mu), np.concatenate(wmu)
    phi = 2 * np.pi * (np.arange(nphi) + 0.5) / nphi
    e1, e2, e3 = _basis(axis)
    st = np.sqrt(1 - mu**2)
    m = (st[:, None, None] * (np.cos(phi)[None, :, None] * e1 + np.sin(phi)[None, :, None] * e2)
         + mu[:, None, None] * e3[None, None, :]).reshape(-1, 3)
    wang = (wmu[:, None] * np.full(nphi, 2 * np.pi / nphi)[None, :]).reshape(-1)
    X = center + rho[:, None, None] * m[None, :, :]
    wq = wrho[:, None] * wang[None, :]
    return X.reshape(-1, 3), wq.reshape(-1), np.repeat(rho, len(wang))


def _edges(lo, hi, refine=()):
    """Factor-2 panels from lo to hi, with extra edges (refine) replacing those nearby."""
    e = list(np.geomspace(lo, hi, int(np.ceil(np.log2(hi / lo))) + 1))
    if refine:
        a, b = min(refine) / 1.25, max(refine) * 1.25
        e = [v for v in e if v < a or v > b] + list(refine)
    return np.array(sorted(set(e)))


def bump(t):
    """C-infinity: 1 for t <= 1/2, 0 for t >= 1."""
    s = np.clip(2 * t - 1, 0, 1)
    f = lambda q: np.where(q > 0, np.exp(-1 / np.maximum(q, 1e-300)), 0.0)
    return f(1 - s) / (f(1 - s) + f(s))


RES = {1: dict(nr=8, nth=6, nphi=16), 2: dict(nr=12, nth=9, nphi=24)}
TH_EDGES = [0, 5, 10, 15, 20, 25, 30, 40, 60, 90, 120, 150, 180]


def r_screen(GM, xs):
    return (np.sqrt(6) * C**2 * GM / (A0**2 * xs)) ** (1 / 3) if xs else 0.0


TH_LONE = [0, 2, 5, 10, 20, 40, 70, 110, 140, 160, 170, 175, 178, 180]
_LONE = {}


def lone_accel(GMa, gN, form, xs, want_V=False, nr=14, nth=14):
    """Shell-integrated phantom acceleration at a lone star in a uniform Newtonian field of size gN,
    as components along that field: (F part, W part, V part). Axisymmetric, so only this component survives."""
    key = (GMa, gN, form, xs, want_V, nr, nth)
    if key in _LONE:
        return _LONE[key]
    if gN == 0 or GMa == 0:
        _LONE[key] = (0.0, 0.0, 0.0)
        return _LONE[key]
    rM, re = np.sqrt(GMa / A0), np.sqrt(GMa / gN)
    rs = r_screen(GMa, xs) if form in ("divergence", "action") else rM
    edges = _edges(1e-3 * min(rM, rs), 1e4 * max(rM, re, rs), refine=tuple(re * np.array([0.5, 0.75, 0.9, 1, 1.1, 1.25, 1.5])))
    ez = np.array([0, 0, 1.0])
    X, wq, _ = sph_grid(np.zeros(3), ez, edges, nr, TH_LONE, nth, 8)
    use_W = form == "action"
    F, W, V = fields(X, [(GMa, np.zeros(3))], gN * ez, xs, form, want_V=want_V and use_W)
    k = kern(np.zeros(3), X, wq, F, W if use_W else None, V if (use_W and want_V) else None)
    _LONE[key] = (float(k["F"][2]), float(k["W"][2]) if use_W else 0.0, float(k["V"][2]) if (use_W and want_V) else 0.0)
    return _LONE[key]


def solve_binary(M, r, q1, mu_e, ge, form, xs=XSTAR_DIV, res=1, want_V=False, gNe=None, subtract=True):
    """Relative phantom acceleration of a binary. M in Msun, r in m. Returns Gamma_r, Gamma_t and
    the per-star phantom accelerations (for the momentum gate). gNe overrides the Newtonian field.
    Each star's acceleration is (its lone-star value, integrated separately) + (the integral of the binary's
    sources minus that star's lone sources); the second is small and is what the binary grids integrate."""
    GM = M * GM_SUN
    m1, m2 = q1 * GM, (1 - q1) * GM
    x1, x2 = np.array([0, 0, (1 - q1) * r]), np.array([0, 0, -q1 * r])
    gN = newtonian_ext(ge) if gNe is None else gNe
    ghat = np.array([np.sqrt(max(0.0, 1 - mu_e**2)), 0.0, mu_e])
    gvec = gN * ghat
    bodies = [(m1, x1), (m2, x2)]
    mass = {1: m1, 2: m2}
    R = r / 2
    scales = [r, np.sqrt(GM / A0)] + ([np.sqrt(GM / gN)] if gN > 0 else []) + (
        [r_screen(GM, xs)] if form in ("divergence", "action") else [])
    rmin = 1e-3 * min(r, np.sqrt(min(m1, m2) / A0))
    rmax = 1e4 * max(scales)
    edges = _edges(rmin, rmax, refine=tuple(r * np.array([0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.125, 1.25, 1.5])))
    p = RES[res]
    use_W = form == "action"
    wV = want_V and use_W
    acc = {1: np.zeros(3), 2: np.zeros(3)}
    accV = {1: np.zeros(3), 2: np.zeros(3)}
    for me, other, ce, co, axis in ((1, 2, x1, x2, x2 - x1), (2, 1, x2, x1, x1 - x2)):
        X, wq, rho = sph_grid(ce, axis, edges, p["nr"], TH_EDGES, p["nth"], p["nphi"])
        Fb, Wb, Vb = fields(X, bodies, gvec, xs, form, want_V=wV)
        Fl, Wl, Vl = fields(X, [(mass[me], ce)], gvec, xs, form, want_V=wV) if subtract else (0 * Fb, 0 * Wb, None if Vb is None else 0 * Vb)
        chi_o = bump(np.sqrt(np.einsum("ni,ni->n", X - co, X - co)) / R)
        k = kern(ce, X, wq * (1 - chi_o), Fb - Fl, (Wb - Wl) if use_W else None, (Vb - Vl) if wV else None)
        acc[me] += k["F"] + (k["W"] if use_W else 0)
        if wV:
            accV[me] += k["F"] + k["V"]
        near = rho < R
        Fo, Wo, Vo = (fields(X[near], [(mass[other], co)], gvec, xs, form, want_V=wV) if subtract
                      else (0 * Fb[near], 0 * Wb[near], None if Vb is None else 0 * Vb[near]))
        k = kern(co, X[near], wq[near] * bump(rho[near] / R), Fb[near] - Fo, (Wb[near] - Wo) if use_W else None,
                 (Vb[near] - Vo) if wV else None)
        acc[other] += k["F"] + (k["W"] if use_W else 0)
        if wV:
            accV[other] += k["F"] + k["V"]
    for a in (1, 2) if subtract else ():
        lf, lw, lv = lone_accel(mass[a], gN, form, xs, want_V=wV)
        acc[a] = acc[a] + (lf + lw) * ghat
        accV[a] = accV[a] + (lf + lv) * ghat
    gref = GM / r**2
    rel = acc[1] - acc[2]
    out = {"Gamma_r": 1 - rel[2] / gref, "Gamma_t": rel[0] / gref, "acc1": acc[1], "acc2": acc[2],
           "m1": m1, "m2": m2}
    if wV:
        relV = accV[1] - accV[2]
        out["Gamma_r_V"] = 1 - relV[2] / gref
        out["Gamma_t_V"] = relV[0] / gref
    return out


def test_point(GM, r, form, xs=XSTAR_DIV, res=1, use_V=False):
    """Isolated point mass at the origin, massless test point at r on the z axis: radial Gamma."""
    xt = np.array([0, 0, r])
    bodies = [(GM, np.zeros(3))]
    R = r / 2
    rmin, rmax = 1e-3 * min(r, np.sqrt(GM / A0)), 1e4 * max(r, np.sqrt(GM / A0), r_screen(GM, xs) if xs else 0)
    edges = _edges(rmin, rmax, refine=tuple(r * np.array([0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.125, 1.25, 1.5])))
    p = RES[res]
    g = np.zeros(3)
    for ce, co, axis, sel in ((xt, np.zeros(3), -xt, "self"), (np.zeros(3), xt, xt, "cross")):
        X, wq, rho = sph_grid(ce, axis, edges, p["nr"], TH_EDGES, p["nth"], p["nphi"])
        F, W, V = fields(X, bodies, np.zeros(3), xs, form, want_V=use_V)
        if sel == "self":
            wgt = wq * (1 - bump(np.sqrt(np.einsum("ni,ni->n", X, X)) / R))
            k = kern(xt, X, wgt, F, None, V if use_V else None)
        else:
            near = rho < R
            k = kern(xt, X[near], wq[near] * bump(rho[near] / R), F[near], None, V[near] if use_V else None)
        g += k["F"] + (k["V"] if use_V else 0)
    Ft, _, Vt = fields(xt[None, :], bodies, np.zeros(3), xs, form, want_V=use_V)
    g += -Ft[0] / 3 - (Vt[0] / 3 if use_V else 0)
    return 1 - g[2] / (GM / r**2)


def single_star_accel(M, ge, form="unscreened", xs=None):
    """Shell-integrated phantom acceleration at a lone star, along the field, in units of g_Ne.
    Free fall with the external field (g_ph = (nu_e - 1) g_Ne) gives (nu_e - 1)/3 here."""
    gN = newtonian_ext(ge)
    lf, lw, _ = lone_accel(M * GM_SUN, gN, form, xs)
    return (lf + lw) / gN


def cassini_Q2(ge, form, xs, a0=A0, res=1, parts=False):
    """Anomalous quadrupole at the Sun, Q2 = -(3/2) d_z d_z Phi_ph(0) (sign fixed by the q(eta) gate)."""
    rM = np.sqrt(GM_SUN / a0)
    gN = a0 * brentq(lambda z: z * nu(z) - ge / a0, 1e-10, ge / a0)
    re = np.sqrt(GM_SUN / gN)
    rs = (np.sqrt(6) * C**2 * GM_SUN / (a0**2 * xs)) ** (1 / 3) if form in ("divergence", "action") else rM
    edges = _edges(1e-3 * min(rM, rs), 1e4 * max(rM, re, rs), refine=tuple(re * np.array([0.5, 0.75, 0.9, 1, 1.1, 1.25, 1.5])))
    nr, nth, nphi = {1: (10, 10, 8), 2: (14, 14, 8)}[res]
    th = [0, 2, 5, 10, 20, 40, 70, 110, 140, 160, 170, 175, 178, 180]
    X, wq, rho = sph_grid(np.zeros(3), np.array([0, 0, 1.0]), edges, nr, th, nth, nphi)
    F, W, _ = fields(X, [(GM_SUN, np.zeros(3))], np.array([0, 0, gN]), xs, form, a0=a0)
    m = X / rho[:, None]
    mu = m[:, 2]
    mF = np.einsum("ni,ni->n", m, F)
    dzzF = -(wq / rho**4 * (15 * mu**2 * mF - 3 * mF - 6 * mu * F[:, 2])).sum() / FOUR_PI
    dzzW = 0.0
    if form == "action":
        Wm = np.einsum("nij,nj->ni", W, m)
        mWm = np.einsum("ni,ni->n", m, Wm)
        tr = np.einsum("nii->n", W)
        c4 = 105 * mu**2 * mWm - 15 * (mWm + 4 * mu * Wm[:, 2] + mu**2 * tr) + 3 * (tr + 2 * W[:, 2, 2])
        dzzW = -(wq / rho**5 * c4).sum() / FOUR_PI
    q2F, q2W = -1.5 * dzzF, -1.5 * dzzW
    return (q2F + q2W, q2F, q2W) if parts else q2F + q2W


def q_two_body(q1):
    q2 = 1 - q1
    return (2 / 3) * (1 - q1**1.5 - q2**1.5) / (q1 * q2)


# ---------------------------------------------------------------------------------------------- gates
def gates():
    import tidal_screening_sparc_cassini as TS

    out, ok = {}, True

    def check(name, val, cond):
        nonlocal ok
        out[name] = val
        ok &= bool(cond)
        print(f"{'PASS' if cond else 'FAIL'}  {name}: {val}")

    # G0: the field equation, from the action, in 1D (symbolic): Phi'' = (nu_eff Phi_N')' - (c^2/2)(S'(x) P(y))''
    import sympy as sp
    u = sp.symbols("u", real=True)
    a0s, cs, Gs = sp.symbols("a0 c G", positive=True)
    Ph, PN, rho = sp.Function("Phi")(u), sp.Function("PhiN")(u), sp.Function("rho")(u)
    Sf, Pf = sp.Function("S"), sp.Function("P")
    ys, xsym = PN.diff(u) / a0s, cs**2 * PN.diff(u, 2) / a0s**2      # Phi_N' > 0, Phi_N'' > 0
    L1 = -(2 * Ph.diff(u) * PN.diff(u) - a0s**2 * (ys**2 + Sf(xsym) * Pf(ys))) / (8 * sp.pi * Gs) - rho * Ph
    eq = sp.euler_equations(L1, [Ph, PN], u)[1].lhs
    t = sp.symbols("t", positive=True)
    nu_eff = 1 + Sf(xsym) * sp.diff(Pf(t), t).subs(t, ys) / (2 * ys)
    want = Ph.diff(u, 2) - sp.diff(nu_eff * PN.diff(u), u) + (cs**2 / 2) * sp.diff(sp.diff(Sf(t), t).subs(t, xsym) * Pf(ys), u, 2)
    resid = sp.simplify(sp.expand(eq * 4 * sp.pi * Gs - want))
    check("G0_action_field_equation_1D_residual", str(resid), resid == 0)
    GM = GM_SUN
    rM = np.sqrt(GM / A0)
    # G1: isolated, unscreened, test point
    errs = [abs(test_point(GM, f * rM, "unscreened") / nu(1 / f**2) - 1) for f in (0.3, 1, 3, 10)]
    check("G1_unscreened_test_point_max_rel_err", max(errs), max(errs) < 2e-4)
    # G2: isolated, divergence and action forms, test point (x* = 2.84e12, Sun)
    rs = r_screen(GM, XSTAR_DIV)
    e2 = []
    for f in (0.5, 1, 2):
        r = f * rs
        y = GM / r**2 / A0
        x = C**2 * np.sqrt(6 * (GM / r**3) ** 2 + H_G**2) / A0**2
        e2.append(abs(test_point(GM, r, "divergence") / (1 + screen(np.array([x]), XSTAR_DIV, "d")[0][0] * (nu(y) - 1)) - 1))
    check("G2a_divergence_test_point_max_rel_err", max(e2), max(e2) < 2e-4)
    # G2b: action form, V pointwise vs the spherical identity V_r = -(2/sqrt6) r^-3 (r^3 w)', and the integral
    rr = rs * np.array([0.5, 1.0, 2.0])

    def w_of(r):
        X = np.stack([np.zeros_like(r), np.zeros_like(r), r], 1)
        _, W, _ = fields(X, [(GM, np.zeros(3))], np.zeros(3), XSTAR_DIV, "action")
        return W[:, 0, 0] * np.sqrt(6)   # W = w~ (1 - 3 n n)/sqrt6 on the z axis, w~ = w |H| / Hn
    h = 3e-3   # spans many P-table cells; 4-point stencil, error O(h^4)
    f = lambda e: w_of(rr * (1 + e)) * (rr * (1 + e)) ** 3
    dr3w = (8 * (f(h) - f(-h)) - (f(2 * h) - f(-2 * h))) / (12 * h * rr)
    X = np.stack([np.zeros(3), np.zeros(3), rr], 1)
    _, _, V = fields(X, [(GM, np.zeros(3))], np.zeros(3), XSTAR_DIV, "action", want_V=True)
    Vsph = -(2 / np.sqrt(6)) * dr3w / rr**3
    ev = float(np.max(np.abs(V[:, 2] / Vsph - 1)))
    check("G2b_V_pointwise_vs_spherical_identity", ev, ev < 1e-5)
    e2c = []
    for r, Vz in zip(rr, V[:, 2]):
        y = GM / r**2 / A0
        x = C**2 * np.sqrt(6 * (GM / r**3) ** 2 + H_G**2) / A0**2
        want = 1 + screen(np.array([x]), XSTAR_DIV, "d")[0][0] * (nu(y) - 1) + Vz / (GM / r**2)
        e2c.append(abs(test_point(GM, r, "action", use_V=True) / want - 1))
    check("G2c_action_test_point_V_integral_max_rel_err", max(e2c), max(e2c) < 2e-4)
    # G3: equal-mass binary, S = 1, external field, far separation: Banik & Zhao QUMOND eq. 36
    gN = newtonian_ext(1.9e-10)
    yN = gN / A0
    nue = nu(yN)
    Le = float(yN * (nu(yN * (1 + 1e-6)) - nu(yN * (1 - 1e-6))) / (2e-6 * yN) / nue)
    re = np.sqrt(GM / gN)
    e3 = []
    for mu in (1.0, 0.5, 0.0):
        g = solve_binary(1.0, 100 * re, 0.5, mu, 1.9e-10, "unscreened")["Gamma_r"]
        e3.append(abs(g / (nue * (1 + 0.5 * Le * (1 - mu**2))) - 1))
    check("G3_far_field_eq36_max_rel_err", max(e3), max(e3) < 1e-2)
    # G4: isolated deep MOND two-body force (virial relation), S = 1
    e4 = []
    for q1 in (0.5, 0.7):
        g = solve_binary(1.0, 300 * rM, q1, 1.0, 0.0, "unscreened", gNe=0.0)["Gamma_r"]
        e4.append(abs(g / (300 * q_two_body(q1)) - 1))
    check("G4_deep_mond_two_body_max_rel_err", max(e4), max(e4) < 1e-2)
    # G5: momentum, isolated, q1 = 0.7; action and unscreened asserted, divergence reported
    mom = {}
    for form in ("unscreened", "action", "divergence"):
        vals = []
        for r_kau in (0.5, 2.0, 8.0):
            s = solve_binary(1.0, r_kau * 1e3 * AU, 0.7, 1.0, 0.0, form, gNe=0.0)
            vals.append(float(np.linalg.norm(s["m1"] * s["acc1"] + s["m2"] * s["acc2"])
                              / (s["m1"] * np.linalg.norm(s["acc1"]) + s["m2"] * np.linalg.norm(s["acc2"]))))
        mom[form] = vals
    out["G5_divergence_form_momentum_imbalance"] = mom["divergence"]
    print(f"INFO  G5 divergence form (not asserted): {mom['divergence']}")
    check("G5_momentum_unscreened_and_action_max", max(mom["unscreened"] + mom["action"]),
          max(mom["unscreened"] + mom["action"]) < 1e-3)
    # G6: action form, W kernel vs V kernel
    e6 = []
    for r_kau in (2.0, 8.0, 30.0):
        s = solve_binary(1.0, r_kau * 1e3 * AU, 0.7, 0.6, 1.9e-10, "action", want_V=True)
        e6.append(abs(s["Gamma_r"] - s["Gamma_r_V"]))
    check("G6_action_W_vs_V_max_abs_dGamma", max(e6), max(e6) < 1e-3)
    # G7: resolution
    e7 = []
    for form in ("unscreened", "divergence", "action"):
        for r_kau in (1.0, 10.0, 100.0):
            a = solve_binary(1.0, r_kau * 1e3 * AU, 0.7, 0.6, 1.9e-10, form, res=1)["Gamma_r"]
            b = solve_binary(1.0, r_kau * 1e3 * AU, 0.7, 0.6, 1.9e-10, form, res=2)["Gamma_r"]
            e7.append(abs(a - b))
    check("G7_resolution_max_abs_dGamma", max(e7), max(e7) < 2e-4)
    # G8: S = 0
    z = solve_binary(1.0, 5e3 * AU, 0.7, 0.6, 1.9e-10, "zero")
    check("G8_zero_form_Gamma_minus_1", abs(z["Gamma_r"] - 1) + abs(z["Gamma_t"]), z["Gamma_r"] == 1 and z["Gamma_t"] == 0)
    # G9: Cassini, divergence part vs Milgrom's q(eta) (tidal_screening_sparc_cassini.Q2)
    e9 = []
    for ge in GES:
        ref1 = TS.Q2(A0_DERIVED, ge, lambda v: np.ones_like(v))
        e9.append(abs(cassini_Q2(ge, "unscreened", None, a0=A0_DERIVED) / ref1 - 1))
        ref2 = TS.Q2(A0, ge, lambda v: TS.S2(TS.x_sun(v), XSTAR_DIV))
        e9.append(abs(cassini_Q2(ge, "divergence", XSTAR_DIV) / ref2 - 1))
    check("G9_cassini_divergence_vs_q_eta_max_rel_err", max(e9), max(e9) < 5e-3)
    # G10: single star in an external field, S = 1: self-acceleration in units of g_Ne is mass-independent
    sa = [single_star_accel(M, 1.9e-10) for M in (0.5, 2.0)]
    out["G10_single_star_self_acceleration_over_gNe"] = sa
    out["G10_beyond_free_fall_over_gNe"] = [v - (nue - 1) / 3 for v in sa]
    check("G10_self_acceleration_mass_independence", abs(sa[0] - sa[1]), abs(sa[0] - sa[1]) < 1e-3)
    # G11: the lone-star split vs direct integration, unequal masses in an external field
    e11 = []
    for form in ("unscreened", "divergence", "action"):
        a = solve_binary(1.0, 10e3 * AU, 0.7, 0.6, 1.9e-10, form, res=1)["Gamma_r"]
        b = solve_binary(1.0, 10e3 * AU, 0.7, 0.6, 1.9e-10, form, res=2, subtract=False)["Gamma_r"]
        e11.append(abs(a - b))
    check("G11_lone_split_vs_direct_max_abs_dGamma", max(e11), max(e11) < 2e-4)
    out["L_e"], out["nu_e"] = Le, float(nue)
    json.dump(out, open(HERE / "TIDAL_TWO_BODY_GATES.json", "w"), indent=1, default=float)
    print("ALL GATES PASS" if ok else "GATES FAILED")
    return ok


# ---------------------------------------------------------------------------------------------- Cassini
def cassini():
    """Pre-registered: x*_A = largest x* with Q2 in the two-sided 2-sigma window at both g_e."""
    passes = lambda lx: all(Q2_WINDOW[0] <= cassini_Q2(ge, "action", 10**lx) <= Q2_WINDOW[1] for ge in GES)
    grid = np.round(np.arange(6.0, 16.0001, 0.05), 2)
    scan = []
    for lx in grid:
        row = {"log10_xstar": float(lx)}
        for ge in GES:
            tot, qf, qw = cassini_Q2(ge, "action", 10**lx, parts=True)
            row[f"{ge:.1e}"] = {"Q2": tot, "divergence_part": qf, "W_part": qw}
        row["pass"] = all(Q2_WINDOW[0] <= row[f"{ge:.1e}"]["Q2"] <= Q2_WINDOW[1] for ge in GES)
        scan.append(row)
    ok = [r["log10_xstar"] for r in scan if r["pass"]]
    out = {"window": Q2_WINDOW, "scan": scan, "x_star_divergence_form": XSTAR_DIV}
    if not ok:
        out["x_star_action"] = None
        out["verdict"] = "FAIL: no x* passes Cassini in the action form"
        print(out["verdict"])
    else:
        lo = max(ok)
        hi = lo + 0.05
        if hi <= grid[-1]:
            assert passes(lo) and not passes(hi)
            for _ in range(30):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if passes(mid) else (lo, mid)
        out["x_star_action"] = 10**lo
        out["passing_log10_xstar_on_grid"] = ok
        out["at_x_star_action"] = {f"{ge:.1e}": dict(zip(("Q2", "divergence_part", "W_part"),
                                                         cassini_Q2(ge, "action", 10**lo, parts=True))) for ge in GES}
        out["resolution_check"] = {f"{ge:.1e}": cassini_Q2(ge, "action", 10**lo, res=2) for ge in GES}
        out["verdict"] = "PASS"
        print(f"x*_A = {10**lo:.4e}; Q2 = " + ", ".join(f"{k}: {v['Q2'] * 1e27:.3f}e-27 (div {v['divergence_part'] * 1e27:.3f}, W {v['W_part'] * 1e27:.3f})"
                                              for k, v in out["at_x_star_action"].items()))
    json.dump(out, open(HERE / "TIDAL_ACTION_CASSINI.json", "w"), indent=1, default=float)
    return out


# ---------------------------------------------------------------------------------------------- table
TAB_M = [0.25, 0.45, 0.8, 1.4, 2.5]
TAB_R_KAU = list(np.round(np.geomspace(0.2, 400, 18), 5))
TAB_Q1 = [0.5, 0.65, 0.8]
TAB_MU, TAB_MU_W = np.polynomial.legendre.leggauss(4)


def _cell(args):
    form, xs, ge, M, rk, q1, mu = args
    s = solve_binary(M, rk * 1e3 * AU, q1, mu, ge, form, xs=xs)
    return args, s["Gamma_r"], s["Gamma_t"]


def table():
    cas = json.load(open(HERE / "TIDAL_ACTION_CASSINI.json"))
    forms = [("unscreened", None), ("divergence", XSTAR_DIV)]
    if cas.get("x_star_action"):
        forms.append(("action", cas["x_star_action"]))
    jobs = [(f, xs, ge, M, rk, q1, float(mu)) for f, xs in forms for ge in GES for M in TAB_M
            for rk in TAB_R_KAU for q1 in TAB_Q1 for mu in TAB_MU]
    res = {}
    with mp.get_context("fork").Pool(4) as pool:
        for i, (a, gr, gt) in enumerate(pool.imap_unordered(_cell, jobs, chunksize=8)):
            res[a] = (gr, gt)
            if i % 500 == 0:
                print(f"{i}/{len(jobs)}", flush=True)
    out = {"M_sun": TAB_M, "r_kau": TAB_R_KAU, "q1": TAB_Q1, "mu_e": list(TAB_MU), "mu_e_weights": list(TAB_MU_W),
           "a0": A0, "x_star": {f: xs for f, xs in forms}, "forms": {}}
    for f, xs in forms:
        out["forms"][f] = {}
        for ge in GES:
            Gr = np.array([[[[res[(f, xs, ge, M, rk, q1, float(mu))][0] for mu in TAB_MU] for q1 in TAB_Q1]
                            for rk in TAB_R_KAU] for M in TAB_M])
            Gt = np.array([[[[res[(f, xs, ge, M, rk, q1, float(mu))][1] for mu in TAB_MU] for q1 in TAB_Q1]
                            for rk in TAB_R_KAU] for M in TAB_M])
            out["forms"][f][f"{ge:.1e}"] = {"Gamma_r": np.round(Gr, 7).tolist(), "Gamma_t": np.round(Gt, 7).tolist(),
                                            "Gamma_r_orientation_avg": np.round(0.5 * Gr @ TAB_MU_W, 7).tolist()}
    json.dump(out, open(HERE / "TIDAL_TWO_BODY_TABLE.json", "w"))
    return out


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("gates", "all"):
        if not gates():
            sys.exit(1)
    if stage in ("cassini", "all"):
        cassini()
    if stage in ("table", "all"):
        table()
