#!/usr/bin/env python3
"""Comet-cloud rays at the working screen. Protocol: PREREG_COMET_CLOUD_WORKING_C_2026-10-17.md.

Reuses the action|live|1.9 map in oort_torque_proxy.py. c_zero is passed into fields.
C = 0 must reproduce the stored binding offset before the working-C histogram is a verdict.
"""

import json
import multiprocessing as mp
from pathlib import Path

import numpy as np

import oort_torque_proxy as O
import tidal_screening_two_body as T

HERE = Path(__file__).resolve().parent
C_WORK = 0.579124707982253
STORED_C0 = 0.00012309721532420575
WINDOW = (1.0e4, 1.0e5)


def qfields(X, gvec, form, xs, a0, c_zero):
    F, W, V = T.fields(
        X,
        [(O.GM, np.zeros(3))],
        gvec,
        xs,
        form,
        want_V=(form == "action"),
        a0=a0,
        c_zero=c_zero,
    )
    return F, (V if form == "action" else np.zeros_like(F))


def g_point(xp, gvec, form, xs, a0, c_zero, res=1):
    r = np.linalg.norm(xp)
    R = r / 2
    gN = np.linalg.norm(gvec)
    edges = O._edges_for(r, a0, gN, xs, form)
    p = O.RESP[res]
    X, wq, rho = T.sph_grid(xp, -xp, edges, p["nr"], T.TH_EDGES, p["nth"], p["nphi"])
    F, V = qfields(X, gvec, form, xs, a0, c_zero)
    w = wq * (1 - T.bump(np.sqrt(np.einsum("ni,ni->n", X, X)) / R))
    k = T.kern(xp, X, w, F, None, V)
    X2, wq2, rho2 = T.sph_grid(
        np.zeros(3), xp, edges, p["nr"], T.TH_EDGES, p["nth"], p["nphi"]
    )
    near = rho2 < R
    F2, V2 = qfields(X2[near], gvec, form, xs, a0, c_zero)
    k2 = T.kern(xp, X2[near], wq2[near] * T.bump(rho2[near] / R), F2, None, V2)
    Fx, Vx = qfields(xp[None, :], gvec, form, xs, a0, c_zero)
    return k["F"] + k["V"] + k2["F"] + k2["V"] - (Fx[0] + Vx[0]) / 3


def g_sun(gvec, form, xs, a0, c_zero, res=1):
    gN = np.linalg.norm(gvec)
    ghat = gvec / gN if gN > 0 else np.array([0.0, 0.0, 1.0])
    edges = O._edges_for(None, a0, gN if gN > 0 else 1e-12, xs, form)
    nr, nth = {1: (14, 14), 2: (18, 18)}[res]
    X, wq, _ = T.sph_grid(np.zeros(3), ghat, edges, nr, T.TH_LONE, nth, 8)
    F, V = qfields(X, gvec, form, xs, a0, c_zero)
    k = T.kern(np.zeros(3), X, wq, F, None, V)
    return k["F"] + k["V"]


def _cell(args):
    c_zero, res, rk, mu, gs = args
    nu, a0, ge, form, xs = O.CONFIGS["action|live|1.9"]
    with O.use_nu(nu):
        gvec = np.array([0.0, 0.0, O.newtonian_ext(ge, a0)])
        st = np.sqrt(1 - mu**2)
        n = np.array([st, 0.0, mu])
        th = np.array([mu, 0.0, -st])
        dg = g_point(rk * O.KAU * n, gvec, form, xs, a0, c_zero, res) - np.array(gs)
    gref = O.GM / (rk * O.KAU) ** 2
    return rk, mu, float(dg @ n / gref), float(dg @ th / gref)


def dg_map(c_zero, res=1):
    nu, a0, ge, form, xs = O.CONFIGS["action|live|1.9"]
    with O.use_nu(nu):
        gN = O.newtonian_ext(ge, a0)
        gs = g_sun(np.array([0.0, 0.0, gN]), form, xs, a0, c_zero, res)
    jobs = [
        (c_zero, res, float(rk), float(mu), gs.tolist())
        for rk in O.R_MAP_KAU
        for mu in O.MU_MAP
    ]
    with mp.get_context("fork").Pool(3) as pool:
        got = {(a, b): (c, d) for a, b, c, d in pool.map(_cell, jobs, chunksize=4)}
    out_r = np.array(
        [[got[(float(rk), float(mu))][0] for mu in O.MU_MAP] for rk in O.R_MAP_KAU]
    )
    out_t = np.array(
        [[got[(float(rk), float(mu))][1] for mu in O.MU_MAP] for rk in O.R_MAP_KAU]
    )
    return {
        "r_kau": list(map(float, O.R_MAP_KAU)),
        "mu": list(map(float, O.MU_MAP)),
        "dgr_over_gN": out_r.tolist(),
        "dgt_over_gN": out_t.tolist(),
        "g_sun_code": gs.tolist(),
        "gNe": gN,
        "a0": a0,
        "g_e": ge,
        "c_zero": c_zero,
    }


def ray_inv_a(m):
    """1/a along each Legendre ray, au^-1, same integral and tail as binding_offset."""
    r = np.array(m["r_kau"]) * O.KAU
    fr = np.array(m["dgr_over_gN"])
    lr = np.log(r)
    out = []
    for j in range(fr.shape[1]):
        integrand = fr[:, j] / r**2
        inner = np.trapezoid(integrand * r, lr)
        tail = fr[-1, j] / r[-1]
        out.append(2.0 * (inner + tail) * O.AU)
    return np.array(out)


def population(inv):
    mu = np.array(O.MU_MAP)
    _, w = np.polynomial.legendre.leggauss(len(mu))
    w = w / w.sum()
    order = np.argsort(inv)
    inv_s, w_s = inv[order], w[order]
    cdf = np.cumsum(w_s)
    med = float(inv_s[np.searchsorted(cdf, 0.5)])
    a = np.full(inv.shape, np.inf)
    pos = inv > 0
    a[pos] = 1.0 / inv[pos]
    inside = pos & (a >= WINDOW[0]) & (a <= WINDOW[1])
    frac = float(w[inside].sum())
    if WINDOW[0] <= (1.0 / med if med > 0 else np.inf) <= WINDOW[1] and frac >= 0.5:
        verdict = "preserved"
    elif med <= 0 or (1.0 / med) < WINDOW[0]:
        verdict = "emptied"
    else:
        verdict = "inconclusive"
    return {
        "inv_a_rays": inv.tolist(),
        "weights": w.tolist(),
        "median_inv_a": med,
        "median_a_au": None if med <= 0 else float(1.0 / med),
        "weight_in_window": frac,
        "weight_unbound": float(w[~pos].sum()),
        "verdict": verdict,
    }


def main():
    print("C=0 map", flush=True)
    m0 = dg_map(0.0)
    off0 = float(O.binding_offset(m0))
    rel = abs(off0 - STORED_C0) / STORED_C0
    print(f"C=0 offset {off0:.6e} rel {rel:.3e}", flush=True)
    if rel >= 1e-3:
        json.dump(
            {"verdict": "ABORTED", "c0_offset": off0, "rel": rel},
            open(HERE / "COMET_CLOUD_WORKING_C.json", "w"),
            indent=2,
        )
        raise SystemExit(2)
    print("working C map", flush=True)
    mw = dg_map(C_WORK)
    offw = float(O.binding_offset(mw))
    pop = population(ray_inv_a(mw))
    rows, aj = O.torque_table(O.MapField(mw))
    out = {
        "C": C_WORK,
        "x_star": O.CONFIGS["action|live|1.9"][4],
        "a0": O.CONFIGS["action|live|1.9"][1],
        "g_e": 1.9e-10,
        "c0_offset_au": off0,
        "c0_stored_au": STORED_C0,
        "c0_rel": rel,
        "working_mean_offset_au": offw,
        "population": pop,
        "a_J_kau": aj,
        "verdict": pop["verdict"],
    }
    json.dump(out, open(HERE / "COMET_CLOUD_WORKING_C.json", "w"), indent=2)
    print(
        json.dumps(
            {
                k: out[k]
                for k in ("working_mean_offset_au", "a_J_kau", "verdict", "population")
            },
            default=float,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
