#!/usr/bin/env python3
"""Exploratory: attempt 3 of the box extension (PREREG_BOX_EXTEND_2026-10-06.md). The third and last solo attempt;
if it fails, D7 box convergence goes to RY as a joint problem.

Method: projected Newton. Identical to solve_c1.ProblemC1.newton (same equilibration Sd fixed at x0, same residual
measure |Sd g|/|Sd src|, same Armijo backtracking with factor 1e-4, stop when lambda < 1e-4, same tol and maxit),
except that each Newton step y (A y = -Sd g, A = Sd H Sd) has its component in the soft band removed:
  V = eigenvectors of sym(A) with |eig| <= SOFT_FACTOR * |eig_min| among the K_SOFT smallest (eigsh, sigma = 0),
  recomputed every iteration; y_perp = y - V V^T y; dx = Sd y_perp.
Projection happens in the same equilibrated coordinates as V. The acceptance test is unchanged: the FULL residual,
soft components included, must reach tol. A residual that truly lives in the soft band cannot be faked into
convergence. Basis: SOFT_SUBSPACE_C1.json (residual share in the soft modes 1.9e-9 at attempt 2's initial guess).
Every iterate is saved; per-iteration diagnostics are logged.

VALIDATION CRITERION (fixed before the first run). Mode `validate` solves the committed 100 kpc fixed-sweep row from
the static state (box_sweep_c1.py path: 23x46, B = 1000, 100 km/s, g_e = 0) with projected Newton. It PASSES iff it
converges (residual <= 1e-10) and reproduces the committed row (BOX_SWEEP_C1_16x32_fixed.json) to relative
differences <= 1e-6 in g/flux and g/g_static and <= 1e-5 in Y/Y_static. Only after a PASS may the ladder run.

Usage:
  attempt3_projected_newton.py validate
  attempt3_projected_newton.py ladder        rungs n = 31..34 from the 1000 kpc cache (Amendment 1 path), stop rule
Outputs: ATTEMPT3_VALIDATE.json, ATTEMPT3_LADDER.json, cache_branch/attempt3_<tag>_it<k>.npy, cache_branch/attempt3_<tag>_final.npy.
"""

import json, math, os, sys, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import solve_c1 as C
from stage_c_c1 import observables

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
V_W = 100 / 299792.458
K_SOFT = 24
SOFT_FACTOR = 1000.0
DXI = math.asinh(1e4) / 30


def projected_newton(P, x0, tag, tol=1e-10, maxit=40):
    x = x0.copy()
    grad, H, _ = P.grad_hess(x)
    rown = np.asarray(abs(H).sum(axis=1)).ravel()
    Sd = sps.diags(1.0 / np.sqrt(np.maximum(rown, rown.max() * 1e-30)))
    norm0 = np.linalg.norm(Sd @ P.src)
    res = lambda gr: float(np.linalg.norm(Sd @ gr) / norm0)
    log = []
    for it in range(maxit):
        gn = res(grad)
        np.save(f"cache_branch/attempt3_{tag}_it{it}.npy", x)
        if gn < tol:
            print(f"    pnewton {it}: residual {gn:.3e}  CONVERGED", flush=True)
            return x, True, gn, log
        A = (Sd @ H @ Sd).tocsc()
        As = (0.5 * (A + A.T)).tocsc()
        ev, V = spla.eigsh(As, k=K_SOFT, sigma=0, which="LM")
        lam_min = float(np.min(np.abs(ev)))
        Vs = V[:, np.abs(ev) <= SOFT_FACTOR * lam_min]
        r = Sd @ grad
        y = P.solve_linear(A, -r)
        y_perp = y - Vs @ (Vs.T @ y)
        step = Sd @ y_perp
        entry = {
            "it": it,
            "residual": gn,
            "lam_min": lam_min,
            "n_soft": int(Vs.shape[1]),
            "soft_frac_r": float(np.linalg.norm(Vs.T @ r) / np.linalg.norm(r)),
            "soft_frac_y": float(np.linalg.norm(Vs.T @ y) / np.linalg.norm(y)),
            "dx_norm": float(np.linalg.norm(step)),
            "dx_unprojected_norm": float(np.linalg.norm(Sd @ y)),
        }
        lam = 1.0
        while True:
            gt, _, _ = P.grad_hess(x + lam * step, want_hess=False)
            if res(gt) < gn * (1 - 1e-4 * lam):
                break
            lam *= 0.5
            if lam < 1e-4:
                entry["line_search"] = "no descent (lambda < 1e-4)"
                log.append(entry)
                print(
                    f"    pnewton {it}: residual {gn:.3e}, lam_min {lam_min:.2e}, n_soft {entry['n_soft']}, "
                    f"soft_frac_r {entry['soft_frac_r']:.2e}, soft_frac_y {entry['soft_frac_y']:.2f}: NO DESCENT",
                    flush=True,
                )
                np.save(f"cache_branch/attempt3_{tag}_final.npy", x)
                return x, False, gn, log
        entry["lambda"] = lam
        log.append(entry)
        print(
            f"    pnewton {it}: residual {gn:.3e}, lam_min {lam_min:.2e}, n_soft {entry['n_soft']}, "
            f"soft_frac_r {entry['soft_frac_r']:.2e}, soft_frac_y {entry['soft_frac_y']:.2f}, lambda {lam:.3g}",
            flush=True,
        )
        x = x + lam * step
        grad, H, _ = P.grad_hess(x)
    gn = res(grad)
    np.save(f"cache_branch/attempt3_{tag}_final.npy", x)
    return x, gn < tol, gn, log


def problem(g, v=V_W):
    return C.ProblemC1(g, v, C.plummer_fn(M, b), 0.0)


def static_state(g):
    P0 = problem(g, 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    return P0, (x2 if ok2 else x1), [bool(ok1), r1, bool(ok2), r2]


def obs03(P, x):
    k = observables(P, x)["0.3kpc"]
    return {"g": k["g"], "flux": k["flux"], "Y": k["Y"]}


def embed(x_old, g_old, dm_old, g_new, dm_new):
    assert abs(g_old.dxi - g_new.dxi) < 1e-12 and abs(g_old.deta - g_new.deta) < 1e-12
    oj = (g_new.nz - g_old.nz) // 2
    a_old = dm_old.to_nodes(x_old).reshape(C.NF, g_old.nR + 1, g_old.nz + 1, 4)
    a_new = np.zeros((C.NF, g_new.nR + 1, g_new.nz + 1, 4))
    a_new[:, : g_old.nR + 1, oj : oj + g_old.nz + 1, :] = a_old
    return dm_new.from_nodes(a_new.reshape(C.NF, g_new.nnode, 4))


mode = sys.argv[1]

if mode == "validate":
    t = time.time()
    B, nR, nz = 1000.0, 23, 46
    g = C.GridC1(nR, nz, 1e-4, math.asinh(B), math.asinh(B))
    P0, xs, st = static_state(g)
    ref = obs03(P0, xs)
    P = problem(g)
    x, ok, gn, log = projected_newton(P, xs, "validate100")
    row = {
        "edge_kpc": 0.1 * B,
        "grid": [nR, nz],
        "static": st,
        "converged": bool(ok),
        "residual": gn,
        "log": log,
        "seconds": round(time.time() - t, 1),
    }
    if ok:
        o = obs03(P, x)
        mine = {
            "g_ratio_static": o["g"] / ref["g"],
            "g_ratio_phihat_flux": o["g"] / o["flux"],
            "Y_ratio": o["Y"] / ref["Y"],
        }
        committed = [
            r
            for r in json.load(open("BOX_SWEEP_C1_16x32_fixed.json"))["rows"]
            if r["edge_kpc"] == 100.0
        ][0]
        rel = {k: abs(mine[k] - committed[k]) / abs(committed[k]) for k in mine}
        tolr = {"g_ratio_static": 1e-6, "g_ratio_phihat_flux": 1e-6, "Y_ratio": 1e-5}
        row.update(
            {
                "mine": mine,
                "committed": {k: committed[k] for k in mine},
                "rel_diff": rel,
                "PASS": all(rel[k] <= tolr[k] for k in rel),
            }
        )
    else:
        row["PASS"] = False
    json.dump(row, open("ATTEMPT3_VALIDATE.json", "w"), indent=1)
    print(
        "VALIDATION",
        "PASS" if row["PASS"] else "FAIL",
        json.dumps({k: row.get(k) for k in ("converged", "residual", "rel_diff")}),
        flush=True,
    )

if mode == "ladder":
    v = json.load(open("ATTEMPT3_VALIDATE.json"))
    assert v.get("PASS") is True, "validation has not passed; the ladder may not run"
    g_prev = C.GridC1(30, 60, 1e-4, math.asinh(1e4), math.asinh(1e4))
    P_prev = problem(g_prev)
    x_prev = np.load("cache_branch/boxsweep_B10000_30x60_v100.npy")
    out = {"prereg": "PREREG_BOX_EXTEND_2026-10-06.md Amendment 2", "rows": []}
    for n in (31, 32, 33, 34):
        t = time.time()
        Bn = math.sinh(n * DXI)
        g = C.GridC1(n, 2 * n, 1e-4, math.asinh(Bn), math.asinh(Bn))
        P = problem(g)
        x0 = embed(x_prev, g_prev, P_prev.dm, g, P.dm)
        x, ok, gn, log = projected_newton(P, x0, f"ladder_n{n}")
        row = {
            "n": n,
            "B": Bn,
            "edge_kpc": 0.1 * Bn,
            "converged": bool(ok),
            "residual": gn,
            "log": log,
            "seconds": round(time.time() - t, 1),
        }
        if ok:
            o = obs03(P, x)
            row.update(o)
            row.update(
                {
                    "g_over_flux": o["g"] / o["flux"],
                    "excess_over_GR": o["g"] / o["flux"] - 0.75,
                }
            )
            np.save(f"cache_branch/attempt3_ladder_n{n}_v100.npy", x)
        out["rows"].append(row)
        json.dump(out, open("ATTEMPT3_LADDER.json", "w"), indent=1)
        print(
            f"rung n={n} edge {0.1*Bn:.0f} kpc: converged {ok} ({gn:.1e})"
            + (f", e = {row['excess_over_GR']:.5f}" if ok else "")
            + f" [{row['seconds']:.0f}s]",
            flush=True,
        )
        if not ok:
            print("STOP RULE: rung did not converge; no verdict.", flush=True)
            break
        g_prev, P_prev, x_prev = g, P, x
