#!/usr/bin/env python3
"""Exploratory: attempt 2 of the box extension, under Amendment 1 of PREREG_BOX_EXTEND_2026-10-06.md (committed before
this script first ran). Box continuation on exactly nested fixed-resolution grids: B_n = sinh(n * dxi) with
dxi = asinh(1e4)/30 makes the n x 2n grid contain the committed 1000 kpc 30 x 60 grid node for node (radial offset 0,
eta offset n - 30 elements per side). Each rung starts from the previous converged solution with every nodal DOF
(f, f_xi, f_eta, f_xi_eta) copied unchanged and the new outer DOFs set to 0. This tracks the stripped branch by
construction. Writes NEW files only; never touches BOX_SWEEP_C1_* or cache_branch/boxsweep_*.
Usage:
  box_ladder_c1.py check            correctness checks (identity, dxi equality, observables of the padded guess)
  box_ladder_c1.py ladder           rungs n = 31..34 in sequence from the 1000 kpc cache; stops at the first failure
  box_ladder_c1.py static <n>       static (held, stage-1) reference at rung n
  box_ladder_c1.py fromstatic <n>   wind solve at rung n from the static state (initial-guess independence check)
Outputs: BOX_LADDER_C1.json, BOX_LADDER_STATIC_n<n>.json, BOX_LADDER_FROMSTATIC_n<n>.json,
cache_branch/boxladder_n<n>_v100.npy, cache_branch/boxladder_fromstatic_n<n>_v100.npy.
"""

import json, math, os, sys, time
import numpy as np
import solve_c1 as C
from stage_c_c1 import observables

vf = 10 / 299792.458
b = 3e-4
M = 12 * math.pi * vf**4 / C.A0T
Q0 = 0.1
V = 100 / 299792.458
N_OLD = 30
DXI = math.asinh(1e4) / N_OLD
OLD_CACHE = "cache_branch/boxsweep_B10000_30x60_v100.npy"
G_OVER_FLUX_1000 = 0.9778217608849343  # committed row, BOX_SWEEP_C1_16x32_fixed.json


def grid(n):
    B = math.sinh(n * DXI)
    g = C.GridC1(n, 2 * n, 1e-4, math.asinh(B), math.asinh(B))
    assert abs(g.dxi - DXI) < 1e-12 and abs(g.deta - DXI) < 1e-12, (g.dxi, g.deta, DXI)
    return g, B


def embed(x_old, g_old, dm_old, g_new, dm_new):
    """Copy every nodal DOF of x_old onto the nested new grid; new nodes get 0."""
    assert abs(g_old.dxi - g_new.dxi) < 1e-12 and abs(g_old.deta - g_new.deta) < 1e-12
    oj = (g_new.nz - g_old.nz) // 2
    assert g_new.nR >= g_old.nR and (g_new.nz - g_old.nz) % 2 == 0
    assert (
        abs(g_new.eta[oj] - g_old.eta[0]) < 1e-9
        and abs(g_new.xi[g_old.nR] - g_old.xi[-1]) < 1e-9
    )
    a_old = dm_old.to_nodes(x_old).reshape(C.NF, g_old.nR + 1, g_old.nz + 1, 4)
    a_new = np.zeros((C.NF, g_new.nR + 1, g_new.nz + 1, 4))
    a_new[:, : g_old.nR + 1, oj : oj + g_old.nz + 1, :] = a_old
    return dm_new.from_nodes(a_new.reshape(C.NF, g_new.nnode, 4))


def obs_row(P, x):
    ob = observables(P, x)
    k = ob["0.3kpc"]
    return {
        "g": k["g"],
        "flux": k["flux"],
        "Y": k["Y"],
        "g_over_flux": k["g"] / k["flux"],
        "excess_over_GR": k["g"] / k["flux"] - 0.75,
        "max_u": ob["max_u"],
    }


def problem(g):
    return C.ProblemC1(g, V, C.plummer_fn(M, b), 0.0)


def save(path, row):
    out = (
        json.load(open(path))
        if os.path.exists(path)
        else {"prereg": "PREREG_BOX_EXTEND_2026-10-06.md Amendment 1", "rows": []}
    )
    out["rows"].append(row)
    json.dump(out, open(path, "w"), indent=1)


def old_state():
    g_old = C.GridC1(N_OLD, 2 * N_OLD, 1e-4, math.asinh(1e4), math.asinh(1e4))
    P_old = problem(g_old)
    return g_old, P_old, np.load(OLD_CACHE)


mode = sys.argv[1]

if mode == "check":
    g_old, P_old, x_old = old_state()
    ok_all = True
    same = embed(x_old, g_old, P_old.dm, g_old, P_old.dm)
    r1 = bool(np.array_equal(same, x_old))
    ok_all &= r1
    print(f"(i) identity embed (same grid): exact = {r1}")
    g31, B31 = grid(31)
    print(
        f"(ii) dxi equality asserted: dxi = {g31.dxi!r}, deta = {g31.deta!r}, target {DXI!r}"
    )
    P31 = problem(g31)
    x31 = embed(x_old, g_old, P_old.dm, g31, P31.dm)
    r_old = obs_row(P_old, x_old)["g_over_flux"]
    r_new = obs_row(P31, x31)["g_over_flux"]
    r3 = (
        abs(r_new - G_OVER_FLUX_1000) <= 1e-12
        and abs(r_old - G_OVER_FLUX_1000) <= 1e-12
    )
    ok_all &= r3
    print(
        f"(iii) g/flux at 0.3 kpc: old grid {r_old!r}, padded on 31x62 {r_new!r}, committed {G_OVER_FLUX_1000!r} -> {r3}"
    )
    print("CHECKS", "PASS" if ok_all else "FAIL")
    sys.exit(0 if ok_all else 1)

if mode == "ladder":
    g_prev, P_prev, x_prev = old_state()
    for n in (31, 32, 33, 34):
        t = time.time()
        g, B = grid(n)
        P = problem(g)
        x0 = embed(x_prev, g_prev, P_prev.dm, g, P.dm)
        x, ok, gn = P.newton(x0, tol=1e-10, maxit=40, verbose=True)
        row = {
            "n": n,
            "B": B,
            "edge_kpc": 0.1 * B,
            "grid": [n, 2 * n],
            "converged": bool(ok),
            "residual": gn,
            "seconds": round(time.time() - t, 1),
        }
        if ok:
            row.update(obs_row(P, x))
            np.save(f"cache_branch/boxladder_n{n}_v100.npy", x)
        save("BOX_LADDER_C1.json", row)
        print(
            f"rung n={n} edge {0.1*B:.0f} kpc: converged {ok} ({gn:.1e})"
            + (
                f", e = {row['excess_over_GR']:.5f}, g/flux = {row['g_over_flux']:.5f}"
                if ok
                else ""
            )
            + f" [{row['seconds']:.0f}s]",
            flush=True,
        )
        if not ok:
            print("STOP RULE: rung did not converge; no verdict.", flush=True)
            break
        g_prev, P_prev, x_prev = g, P, x

if mode == "static":
    n = int(sys.argv[2])
    t = time.time()
    g, B = grid(n)
    P0 = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    row = {
        "n": n,
        "B": B,
        "edge_kpc": 0.1 * B,
        "static": [bool(ok1), r1, bool(ok2), r2],
        "used": "stage2" if ok2 else "stage1",
        "seconds": round(time.time() - t, 1),
    }
    row.update({"ref_" + k: v for k, v in obs_row(P0, xs).items()})
    save(f"BOX_LADDER_STATIC_n{n}.json", row)
    np.save(f"cache_branch/boxladder_static_n{n}.npy", xs)
    print(json.dumps(row, indent=1), flush=True)

if mode == "fromstatic":
    n = int(sys.argv[2])
    t = time.time()
    g, B = grid(n)
    P0 = C.ProblemC1(g, 0.0, C.plummer_fn(M, b), 0.0)
    x1, ok1, r1 = P0.newton(
        C.initial_guess_c1(g, P0.dm, M, b),
        tol=1e-11,
        maxit=25,
        verbose=False,
        freeze=P0.lambda_dofs(),
    )
    x2, ok2, r2 = P0.newton(x1, tol=1e-10, maxit=15, verbose=False)
    xs = x2 if ok2 else x1
    P = problem(g)
    x, ok, gn = P.newton(xs, tol=1e-10, maxit=40, verbose=True)
    row = {
        "n": n,
        "B": B,
        "edge_kpc": 0.1 * B,
        "kind": "fromstatic",
        "static": [bool(ok1), r1, bool(ok2), r2],
        "converged": bool(ok),
        "residual": gn,
        "seconds": round(time.time() - t, 1),
    }
    if ok:
        row.update(obs_row(P, x))
        np.save(f"cache_branch/boxladder_fromstatic_n{n}_v100.npy", x)
        lad = f"cache_branch/boxladder_n{n}_v100.npy"
        if os.path.exists(lad):
            xl = np.load(lad)
            row["rel_diff_vs_ladder"] = float(
                np.linalg.norm(x - xl) / np.linalg.norm(xl)
            )
    save(f"BOX_LADDER_FROMSTATIC_n{n}.json", row)
    print(json.dumps(row, indent=1), flush=True)
