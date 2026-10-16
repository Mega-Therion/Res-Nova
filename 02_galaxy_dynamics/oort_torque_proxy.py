#!/usr/bin/env python3
"""Oort-cloud torque proxy for the tidal screen. Pre-registered in PREREG_OORT_TORQUE_2026-10-16.md.

Vokrouhlicky, Nesvorny & Tremaine 2024 (arXiv:2403.09555, "VNT") find that MOND fails the long-period-comet data
because torques at r >~ r_M make new comets with a ~ 1e3-1e4 au, which buries the Oort peak. That holds even for the
sharp mu10 with g_e = 3.35e-10 (their S3). They leave open "theories in which non-Newtonian effects are screened on
small spatial scales". This script computes, for a lone 1 Msun Sun in the Galactic external field:

1. The heliocentric anomalous field dg(r, theta) = g_ph(x) - g_ph(Sun) (theta from g_e), from the same kernels as
   tidal_screening_two_body.py. For the action form the source is F + V, V = div W, through the D2 kernel and its
   local term. Both points use their own centred shells, so the uniform part cancels exactly.
2. The first-order change of angular momentum over one orbit, dL = Int x * g dt, for q = 10 au Kepler orbits with
   isotropic orientations. It is computed from the Galactic tide (VNT eq. 31, McMillan 2017 values), from dg, and
   from their sum. ΔL_crit = L(15 au) - L(5 au), the jump across the Jupiter-Saturn barrier. Reported per a:
   the medians and the fraction of orbits with |dL| >= ΔL_crit, plus a_J, the smallest a where the median |dL| reaches ΔL_crit.
3. The binding offset of near-parabolic comets measured with a Newtonian orbit at perihelion:
   Δ(1/a) = 2 Phi_anom(0) / GM, with Phi_anom(0) = -Int_0^inf <dg_r> dr (orientation average).

Usage: oort_torque_proxy.py gates | run     Output: OORT_TORQUE_PROXY.json (OORT_TORQUE_GATES.json)
"""
import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
AU, KAU = T.AU, T.AU * 1e3
GM = T.GM_SUN
A0_LIVE, A0_VNT = T.A0, 1.2e-10
XS_A = json.load(open(HERE / "TIDAL_ACTION_CASSINI.json"))["x_star_action"]
KPC, MSUN, PC = 3.0857e19, T.MSUN, T.PC
# Galactic tide, VNT eq. 31 with McMillan 2017: A = -B = 14.2 km/s/kpc, rho0 = 0.11 Msun/pc^3
OMEGA0 = 2 * 14.2e3 / KPC
DELTA = 0.0
QTIDE = np.pi * T.G * 0.11 * MSUN / PC**3 / OMEGA0**2
DL_CRIT = np.sqrt(2 * GM * AU) * (np.sqrt(15) - np.sqrt(5))
R_MAP_KAU = np.array([0.05, 0.08, 0.12, 0.2, 0.3, 0.5, 0.7, 1, 1.4, 2, 2.8, 3.6, 4.5, 5.5, 6.5, 7.5, 8.7, 10, 11.5, 13, 15, 17.5, 20,
                      24, 28, 34, 40, 50, 65, 85, 110, 150, 200, 300])
MU_MAP, _ = np.polynomial.legendre.leggauss(12)
A_GRID_KAU = np.geomspace(0.5, 120, 34)


def make_nu_n(n):
    """nu for mu_n(x) = x / (1 + x^n)^(1/n): solve x mu_n(x) = y on a table, interpolate in log."""
    x = np.geomspace(1e-8, 1e8, 40001)
    y = x**2 / (1 + x**n) ** (1 / n)
    lnx, lny = np.log(x), np.log(y)
    return lambda yy: np.exp(np.interp(np.log(np.maximum(yy, 1e-100)), lny, lnx)) / np.maximum(yy, 1e-100)


NU_STD = T.nu
CONFIGS = {
    # name: (nu, a0, g_e, form, x*)
    "unscreened|live|1.9": (NU_STD, A0_LIVE, 1.9e-10, "unscreened", None),
    "unscreened|live|2.32": (NU_STD, A0_LIVE, 2.32e-10, "unscreened", None),
    "unscreened|VNT_S1|2.32": (NU_STD, A0_VNT, 2.32e-10, "unscreened", None),
    "mu10|VNT_S3|3.35": (make_nu_n(10), A0_VNT, 3.35e-10, "unscreened", None),
    "action|live|1.9": (NU_STD, A0_LIVE, 1.9e-10, "action", XS_A),
    "action|live|2.32": (NU_STD, A0_LIVE, 2.32e-10, "action", XS_A),
}


class use_nu:
    """Swap the solver's interpolating function (and P) for one configuration."""

    def __init__(self, nu):
        self.nu = nu

    def __enter__(self):
        self.old = T.nu
        T.nu = self.nu
        return self

    def __exit__(self, *a):
        T.nu = self.old


def newtonian_ext(ge, a0):
    return a0 * brentq(lambda z: z * T.nu(z) - ge / a0, 1e-10, ge / a0)


def qfields(X, gvec, form, xs, a0):
    F, W, V = T.fields(X, [(GM, np.zeros(3))], gvec, xs, form, want_V=(form == "action"), a0=a0)
    return F, (V if form == "action" else np.zeros_like(F))


def _edges_for(r, a0, gN, xs, form):
    rM = np.sqrt(GM / a0)
    re = np.sqrt(GM / gN) if gN > 0 else rM
    rs = (np.sqrt(6) * T.C**2 * GM / (a0**2 * xs)) ** (1 / 3) if form == "action" else rM
    lo = 1e-3 * min(r, rM, rs) if r else 1e-3 * min(rM, rs)
    hi = 1e4 * max(r or 0, rM, re, rs)
    ref = tuple(r * np.array([0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.125, 1.25, 1.5])) if r else \
        tuple(re * np.array([0.5, 0.75, 0.9, 1, 1.1, 1.25, 1.5]))
    return T._edges(lo, hi, refine=ref)


RESP = {1: dict(nr=8, nth=6, nphi=16), 2: dict(nr=12, nth=9, nphi=24)}


def g_point(xp, gvec, form, xs, a0, res=1):
    """Code-convention phantom acceleration at a test point xp (not at the Sun)."""
    r = np.linalg.norm(xp)
    R = r / 2
    gN = np.linalg.norm(gvec)
    edges = _edges_for(r, a0, gN, xs, form)
    p = RESP[res]
    X, wq, rho = T.sph_grid(xp, -xp, edges, p["nr"], T.TH_EDGES, p["nth"], p["nphi"])
    F, V = qfields(X, gvec, form, xs, a0)
    w = wq * (1 - T.bump(np.sqrt(np.einsum("ni,ni->n", X, X)) / R))
    k = T.kern(xp, X, w, F, None, V)
    X2, wq2, rho2 = T.sph_grid(np.zeros(3), xp, edges, p["nr"], T.TH_EDGES, p["nth"], p["nphi"])
    near = rho2 < R
    F2, V2 = qfields(X2[near], gvec, form, xs, a0)
    k2 = T.kern(xp, X2[near], wq2[near] * T.bump(rho2[near] / R), F2, None, V2)
    Fx, Vx = qfields(xp[None, :], gvec, form, xs, a0)
    return k["F"] + k["V"] + k2["F"] + k2["V"] - (Fx[0] + Vx[0]) / 3


def g_sun(gvec, form, xs, a0, res=1):
    gN = np.linalg.norm(gvec)
    ghat = gvec / gN if gN > 0 else np.array([0, 0, 1.0])
    edges = _edges_for(None, a0, gN if gN > 0 else 1e-12, xs, form)
    nr, nth = {1: (14, 14), 2: (18, 18)}[res]
    X, wq, _ = T.sph_grid(np.zeros(3), ghat, edges, nr, T.TH_LONE, nth, 8)
    F, V = qfields(X, gvec, form, xs, a0)
    k = T.kern(np.zeros(3), X, wq, F, None, V)
    return k["F"] + k["V"]


def _map_cell(args):
    name, res, rk, mu, gs = args
    nu, a0, ge, form, xs = CONFIGS[name]
    with use_nu(nu):
        gvec = np.array([0, 0, newtonian_ext(ge, a0)])
        st = np.sqrt(1 - mu**2)
        n = np.array([st, 0, mu])
        th = np.array([mu, 0, -st])                             # theta-hat, theta measured from +z = g_e
        dg = g_point(rk * KAU * n, gvec, form, xs, a0, res) - np.array(gs)
    gref = GM / (rk * KAU) ** 2
    return rk, mu, float(dg @ n / gref), float(dg @ th / gref)


def dg_map(name, res=1, r_kau=R_MAP_KAU, mus=MU_MAP):
    nu, a0, ge, form, xs = CONFIGS[name]
    with use_nu(nu):
        gN = newtonian_ext(ge, a0)
        gs = g_sun(np.array([0, 0, gN]), form, xs, a0, res)
    jobs = [(name, res, float(rk), float(mu), gs.tolist()) for rk in r_kau for mu in mus]
    with mp.get_context("fork").Pool(3) as pool:
        got = {(a, b): (c, d) for a, b, c, d in pool.map(_map_cell, jobs, chunksize=4)}
    out_r = np.array([[got[(float(rk), float(mu))][0] for mu in mus] for rk in r_kau])
    out_t = np.array([[got[(float(rk), float(mu))][1] for mu in mus] for rk in r_kau])
    return {"r_kau": list(map(float, r_kau)), "mu": list(map(float, mus)), "dgr_over_gN": out_r.tolist(),
            "dgt_over_gN": out_t.tolist(), "g_sun_code": gs.tolist(), "gNe": gN, "a0": a0, "g_e": ge}


class MapField:
    """dg(x) from a map: Legendre in mu (dgr, dgt/sin theta), linear in ln r; Galactic-frame axis ex = g_e."""

    def __init__(self, m):
        self.lr = np.log(np.array(m["r_kau"]) * KAU)
        mu = np.array(m["mu"])
        L = len(mu)
        V = np.polynomial.legendre.legvander(mu, L - 1)
        st = np.sqrt(1 - mu**2)
        self.cr = np.linalg.solve(V, np.array(m["dgr_over_gN"]).T)          # (L, nr)
        self.ct = np.linalg.solve(V, (np.array(m["dgt_over_gN"]) / st).T)
        self.L = L

    def __call__(self, X):
        r = np.linalg.norm(X, axis=1)
        n = X / r[:, None]
        mu = n[:, 0]
        P = np.polynomial.legendre.legvander(mu, self.L - 1)
        lr = np.clip(np.log(r), self.lr[0], self.lr[-1])
        cr = np.stack([np.interp(lr, self.lr, self.cr[l]) for l in range(self.L)], 1)
        ct = np.stack([np.interp(lr, self.lr, self.ct[l]) for l in range(self.L)], 1)
        fr = np.sum(P * cr, 1)
        ft = np.sum(P * ct, 1) * np.sqrt(np.maximum(1 - mu**2, 0))
        ex = np.array([1.0, 0, 0])
        st = np.sqrt(np.maximum(1 - mu**2, 1e-30))
        th = (n * mu[:, None] - ex[None, :]) / st[:, None]
        gref = GM / r**2
        out = (fr * gref)[:, None] * n + (ft * gref)[:, None] * th
        out[np.log(r) < self.lr[0]] = 0.0                                     # inside 0.05 kAU (beyond the map, r^-2 scaling is kept)
        return out


def g_tide(X):
    x, y, z = X[:, 0], X[:, 1], X[:, 2]
    return OMEGA0**2 * np.stack([(1 - 2 * DELTA) * x, -y, -2 * (2 * QTIDE - DELTA) * z], 1)


def random_rotations(n, rng):
    q = rng.normal(size=(n, 4))
    q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    return np.stack([np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], -1),
                     np.stack([2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)], -1),
                     np.stack([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], -1)], 1)


def delta_L(a_kau, field, n_orient=400, q_au=10.0, nE=512, seed=7):
    """dL per orbit (n_orient, 3) for Kepler orbits a, q, isotropic orientations; field(X) -> acceleration."""
    a = a_kau * KAU
    e = 1 - q_au * AU / a
    E = (np.arange(nE) + 0.5) * 2 * np.pi / nE
    nmean = np.sqrt(GM / a**3)
    pos = np.stack([a * (np.cos(E) - e), a * np.sqrt(1 - e**2) * np.sin(E), np.zeros(nE)], 1)
    dt = (1 - e * np.cos(E)) / nmean * (2 * np.pi / nE)
    R = random_rotations(n_orient, np.random.default_rng(seed))
    X = np.einsum("oij,ej->oei", R, pos).reshape(-1, 3)
    g = field(X).reshape(n_orient, nE, 3)
    Xo = X.reshape(n_orient, nE, 3)
    return np.einsum("oe,oei->oi", np.broadcast_to(dt, (n_orient, nE)), np.cross(Xo, g))


def binding_offset(m):
    """Delta(1/a) in au^-1 from the orientation-averaged radial anomaly: 2 Phi_anom(0)/GM."""
    r = np.array(m["r_kau"]) * KAU
    mu = np.array(m["mu"])
    _, w = np.polynomial.legendre.leggauss(len(mu))
    fr0 = 0.5 * np.array(m["dgr_over_gN"]) @ w                               # <dg_r> / (GM/r^2)
    integrand = fr0 / r**2                                                    # <dg_r>/GM
    lr = np.log(r)
    inner = np.trapezoid(integrand * r, lr)                                   # Int dg_r/GM dr over the map
    tail = fr0[-1] / r[-1]                                                    # beyond: fr0 constant
    phi0_over_GM = inner + tail                                               # Phi_anom(0)/GM = Int_0^inf dg_r dr / GM (< 0 when dg_r points inward)
    return 2 * phi0_over_GM * AU


def torque_table(field):
    rows = []
    for ak in A_GRID_KAU:
        Lt = delta_L(ak, g_tide)
        Lm = delta_L(ak, field) if field is not None else np.zeros_like(Lt)
        tot = Lt + Lm
        rows.append({"a_kau": float(ak), "median_dL_tide": float(np.median(np.linalg.norm(Lt, axis=1))),
                     "median_dL_mond": float(np.median(np.linalg.norm(Lm, axis=1))),
                     "median_dL_total": float(np.median(np.linalg.norm(tot, axis=1))),
                     "frac_jump": float(np.mean(np.linalg.norm(tot, axis=1) >= DL_CRIT))})
    aj = next((r["a_kau"] for r in rows if r["median_dL_total"] >= DL_CRIT), None)
    return rows, aj


def gates():
    out, ok = {}, True

    def check(name, val, cond):
        nonlocal ok
        out[name] = val
        ok &= bool(cond)
        print(f"{'PASS' if cond else 'FAIL'}  {name}: {val}")

    # O1: isolated, unscreened and action: matches the validated test_point
    e1 = []
    for form, xs in (("unscreened", None), ("action", T.XSTAR_DIV)):
        for rk in (3.0, 10.0):
            x = np.array([0.0, 0.0, rk * KAU])
            g = g_point(x, np.zeros(3), form, xs, A0_LIVE) - g_sun(np.zeros(3), form, xs, A0_LIVE)
            want = 1 - T.test_point(GM, rk * KAU, form, xs=xs, use_V=(form == "action"))   # = g_z / gref there
            e1.append(abs(g[2] / (GM / (rk * KAU) ** 2) - want))
    check("O1_isolated_vs_test_point_max_abs", max(e1), max(e1) < 1e-6)
    # O2: external field, r = 0.5 kAU: the quadrupole from cassini_Q2 (independent integral)
    e2 = []
    for form, xs in (("unscreened", None), ("action", XS_A)):
        gN = newtonian_ext(1.9e-10, A0_LIVE)
        gvec = np.array([0, 0, gN])
        gs = g_sun(gvec, form, xs, A0_LIVE)
        r = 0.5 * KAU
        par = (g_point(np.array([0, 0, r]), gvec, form, xs, A0_LIVE)[2] - g_point(np.array([0, 0, -r]), gvec, form, xs, A0_LIVE)[2]) / 2
        per = (g_point(np.array([r, 0, 0]), gvec, form, xs, A0_LIVE)[0] - g_point(np.array([-r, 0, 0]), gvec, form, xs, A0_LIVE)[0]) / 2
        q2 = T.cassini_Q2(1.9e-10, form, xs if xs else 1e30)
        e2.append(max(abs(abs(par) / ((2 / 3) * abs(q2) * r) - 1), abs(per / par + 0.5)))
        out[f"O2_{form}_par_per_q2"] = [float(par), float(per), float(q2)]
    check("O2_quadrupole_vs_cassini_Q2_max_rel", max(e2), max(e2) < 0.03)
    # O3: far field, unscreened, r = 100 r_e: Banik & Zhao QUMOND eq. 36
    gN = newtonian_ext(1.9e-10, A0_LIVE)
    gvec = np.array([0, 0, gN])
    yN = gN / A0_LIVE
    nue = T.nu(yN)
    Le = float(yN * (T.nu(yN * (1 + 1e-6)) - T.nu(yN * (1 - 1e-6))) / (2e-6 * yN) / nue)
    re = np.sqrt(GM / gN)
    gs = g_sun(gvec, "unscreened", None, A0_LIVE)
    e3 = []
    for mu in (1.0, 0.0, 0.6):
        st = np.sqrt(1 - mu**2)
        n, th = np.array([st, 0, mu]), np.array([mu, 0, -st])
        x = 100 * re * n
        dg = g_point(x, gvec, "unscreened", None, A0_LIVE) - gs
        gref = GM / (100 * re) ** 2
        want_r = -(nue * (1 + 0.5 * Le * st**2) - 1)
        want_t = nue * Le * st * mu
        e3.append(max(abs(dg @ n / gref - want_r), abs(dg @ th / gref - want_t)))
    check("O3_far_field_eq36_max_abs", max(e3), max(e3) < 2e-3)
    # O4: resolution
    e4 = []
    for form, xs in (("unscreened", None), ("action", XS_A)):
        for rk, mu in ((3.0, 0.3), (12.0, 0.8), (40.0, -0.5)):
            st = np.sqrt(1 - mu**2)
            x = rk * KAU * np.array([st, 0, mu])
            d1 = g_point(x, gvec, form, xs, A0_LIVE, 1) - g_sun(gvec, form, xs, A0_LIVE, 1)
            d2 = g_point(x, gvec, form, xs, A0_LIVE, 2) - g_sun(gvec, form, xs, A0_LIVE, 2)
            e4.append(float(np.linalg.norm(d1 - d2) / (GM / (rk * KAU) ** 2)))
    check("O4_resolution_max_rel_to_gN", max(e4), max(e4) < 2e-4)
    json.dump(out, open(HERE / "OORT_TORQUE_GATES.json", "w"), indent=1, default=float)
    print("ALL GATES PASS" if ok else "GATES FAILED")
    return ok


def run():
    if not gates():
        sys.exit(1)
    res = {"dL_crit": DL_CRIT, "tide": {"Omega0": OMEGA0, "delta": DELTA, "Q": QTIDE}, "configs": {}}
    rows_n, aj_n = torque_table(None)
    res["newton"] = {"rows": rows_n, "a_J_kau": aj_n}
    print(f"Newton (tide only): a_J = {aj_n} kAU", flush=True)
    assert aj_n is not None and 15 <= aj_n <= 40, f"Newtonian a_J {aj_n} outside 15-40 kAU: proxy machinery fails validation"
    for name in CONFIGS:
        m = dg_map(name)
        rows, aj = torque_table(MapField(m))
        res["configs"][name] = {"map": m, "rows": rows, "a_J_kau": aj, "binding_offset_au": binding_offset(m)}
        print(f"{name}: a_J = {aj} kAU; binding offset {res['configs'][name]['binding_offset_au']:.3e} /au", flush=True)
        json.dump(res, open(HERE / "OORT_TORQUE_PROXY.json", "w"), indent=1, default=float)
    v = res["configs"]["unscreened|VNT_S1|2.32"]["a_J_kau"]
    res["validation_unscreened_VNT_S1_aJ_lt_5kau"] = bool(v is not None and v < 5)
    s3 = res["configs"]["mu10|VNT_S3|3.35"]["a_J_kau"]
    verdicts = {}
    for ge in ("1.9", "2.32"):
        c = res["configs"][f"action|live|{ge}"]
        aj = c["a_J_kau"]
        if not res["validation_unscreened_VNT_S1_aJ_lt_5kau"]:
            verdicts[ge] = "proxy uninformative: it does not reproduce VNT's unscreened failure"
        elif aj is not None and s3 is not None and aj <= s3:
            verdicts[ge] = "fails like VNT: torques at least as strong as mu10 at g_e = 3.35e-10 (VNT S3, excluded)"
        elif aj is not None and aj >= 0.8 * aj_n and abs(c["binding_offset_au"]) <= 1e-5:
            verdicts[ge] = "Newton-like in this proxy; a full simulation is needed"
        else:
            verdicts[ge] = "intermediate: weaker than VNT S3, not Newton-like; inconclusive in this proxy"
    res["verdicts"] = verdicts
    print("verdicts", verdicts, flush=True)
    json.dump(res, open(HERE / "OORT_TORQUE_PROXY.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    {"gates": gates, "run": run}[sys.argv[1] if len(sys.argv) > 1 else "run"]()
